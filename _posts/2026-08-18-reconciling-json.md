---
layout: post
title: "Reconciling JSON in DuckDB, One Patch at a Time"
author: "Mustafa Khan"
thumb: "/images/blog/thumbs/json-patch.svg"
image: "/images/blog/thumbs/json-patch.jpg"
excerpt: "DuckDB v2.0 will ship JSON functions that alolw you to easily patch apply JSON patches."
tags: ["extension"]
---

> Guest blog post by [Mustafa Khan](https://www.linkedin.com/in/mustafahasankhan/) ([Atlan](https://atlan.com/)).

DuckDB's JSON extension already covers reading JSON, extracting paths, applying RFC 7396 merge patches, and the usual scalar accessors. The [upcoming v2.0]({% post_url 2026-08-17-duckdb-20-highlights %}) release will extend it with four new scalar functions: `json_merge_patch_diff` computes the inverse of an RFC 7396 merge patch, `json_deep_merge` applies patches with skip-on-null semantics, `json_normalize` canonicalizes key order, and `json_strip_nulls` recursively removes null-valued keys. You can try these primitives today by installing the preview version of DuckDB v2.0-dev.

These primitives address a handful of recurring problems in data pipelines that reconcile state between systems. The examples in this post come from [Atlan](https://atlan.com/). Atlan is a _context layer_ for AI: a platform that gathers metadata, lineage, and semantics from a company's data systems so that data teams and AI agents can find and understand the data. Keeping that layer up to date means constantly reconciling entity documents from many upstream sources. Two upstream services may describe the same entity with different key orderings. Partial updates may carry `null` in a field to indicate either deletion or absence of data. Most events change only one or two fields out of dozens. Handling these cases in SQL previously required leaving the database. The four new functions allow you to perform the work in a single query.

In the rest of this post, we walk through each function, then chain them into an end-to-end reconciliation example. Finally, we present the results of a simple benchmark against equivalent Python implementations on 500,000 synthetic change data capture (CDC) events.

## `json_merge_patch_diff`: The Inverse of `json_merge_patch`

`json_merge_patch_diff(orig, modified)` returns the minimal RFC 7396 patch such that `json_merge_patch(orig, patch) = modified`.
json_merge_patch already exists in DuckDB. It applies an RFC 7396 patch to a document: a null value in the patch deletes the key, nested objects are merged recursively, and any other value overwrites the original.
Deleted keys appear as `null` in the patch, changed and added keys appear with their new values, and unchanged keys are omitted entirely.

```sql
SELECT json_merge_patch_diff('{"a":1,"b":2,"c":3}', '{"a":1,"b":99,"d":4}');
```

```text
{"c":null,"b":99,"d":4}
```

`a` is unchanged, so it is omitted. `b` changed. `c` was removed, so it becomes `null`. `d` is new.

The function recurses into nested objects, producing patches that only touch the changed paths:

```sql
SELECT json_merge_patch_diff(
    '{"user":{"name":"Alice","age":30}}',
    '{"user":{"name":"Alice","age":31}}'
);
```

```text
{"user":{"age":31}}
```

The round trip with `json_merge_patch` holds by construction:

```sql
SELECT json_merge_patch(
    '{"a":1,"b":2,"c":3}',
    json_merge_patch_diff('{"a":1,"b":2,"c":3}', '{"a":1,"b":99,"d":4}')
) = '{"a":1,"b":99,"d":4}' AS round_trips;
```

```text
true
```

Equality between subtrees is computed with `yyjson_equals`, which compares two `yyjson` values structurally without serializing either side. Subtrees that compare equal contribute nothing to the output and short-circuit the recursion:

```sql
SELECT json_merge_patch_diff(
    '{"a":{"b":{"c":{"d":1}}}}',
    '{"a":{"b":{"c":{"d":1}}}}'
);
```

```text
{}
```

This function is particularly useful for CDC pipelines, where most events on a metadata catalog touch one or two fields out of dozens. Shipping the output of `json_merge_patch_diff(prev_state, new_state)` downstream, instead of the full new state, cuts the change payload to a small fraction of its previous size. The diff is the change itself, so there is nothing extra to filter on the consumer side, and a `json_merge_patch` on the other end reconstructs the new state from `prev_state` and the patch.

## `json_deep_merge`: Recursive Merge where `null` Means "Skip"

The patches from the previous section are applied with `json_merge_patch`, which strictly follows RFC 7396: null in the patch deletes the key. That is the right rule for the round trip with `json_merge_patch_diff`, but it is the wrong rule when you are reconciling fragments from multiple upstreams that emit null to mean “I do not have a value for this field on this message.”
`json_deep_merge` covers that case. 

`json_deep_merge` follows the same recursive merge structure as `json_merge_patch`, with one difference: a `null` value in the patch means “keep the original value” instead of “delete the key”. Everything else, including handling of non-null values, nested objects, and the variadic argument shape, matches `json_merge_patch`. In the following example, we apply a patch with the key `b` set to null with `json_merge_patch` and `json_deep_merge`, respectively, resulting in two different results:

```sql
SELECT json_merge_patch('{"a":1,"b":2}', '{"b":null}') AS rfc_7396;
```

```text
{"a":1}
```

```sql
SELECT json_deep_merge('{"a":1,"b":2}', '{"b":null}') AS deep_merge;
```

```text
{"a":1,"b":2}
```

Both functions replace the original value with the patch value when the patch contains a non-null value, and both recurse into nested objects when the original and patch are both objects. The handling of `null` is the only divergence:

```sql
SELECT json_deep_merge(
    '{"a":{"x":1,"y":2}}',
    '{"a":{"y":null,"z":3}}'
);
```

```text
{"a":{"x":1,"y":2,"z":3}}
```

The nested `y` is preserved because the patch contained `null`. `z` is added because the patch had a real value. The same patch through `json_merge_patch` deletes `y` instead:
```sql
SELECT json_merge_patch(
    '{"a":{"x":1,"y":2}}',
    '{"a":{"y":null,"z":3}}'
);
```

```text
{"a":{"x":1,"z":3}}
```
The function is variadic: pass any number of patches and they apply left to right.

```sql
SELECT json_deep_merge(
    '{"a":1}',
    '{"a":null}',
    '{"a":2}'
);
```

```text
{"a":2}
```

The first patch skips (keeps `a=1`), the second overwrites (`a` becomes `2`).

The use case that motivates the skip-on-null rule is reconciling fragments from multiple sources. One source knows the column name (`columnName`) but not its parent table (`parentColumn`). Another knows the parent but not the column name. Each emits a fragment with the unknown fields as `null`:

```sql
SELECT json_deep_merge(
    '{"columnName":"user_id","parentColumn":null}',
    '{"columnName":null,"parentColumn":"accounts.id"}'
);
```

```text
{"columnName":"user_id","parentColumn":"accounts.id"}
```

Note that passing SQL `NULL` as an argument and using JSON `null` values result in different behaviors. A SQL NULL patch makes the result NULL, and a SQL NULL original is ignored, matching the behavior of `json_merge_patch`. JSON `null` inside a patch means "keep the original value for this key".

## `json_normalize`: Canonical Form for Hashing

The third primitive answers the first of the questions this post opened with: when two services emit the same JSON object with different key orders, are they the same document? Lexically they are not, which means comparing the content hashes of the raw strings will conclude they differ. `json_normalize` fixes that by recursively sorting the keys of every object, including objects nested inside arrays. Array elements keep their order, since element order is meaningful in JSON and key order is not. Scalar values are returned unchanged.

```sql
SELECT json_normalize('{"z":1,"a":2,"m":3}');
```

```text
{"a":2,"m":3,"z":1}
```

Recursion descends into nested objects, and into objects nested inside arrays:

```sql
SELECT json_normalize('{"c":{"b":{"z":1,"a":2},"a":3},"a":4}');
```

```text
{"a":4,"c":{"a":3,"b":{"a":2,"z":1}}}
```

```sql
SELECT json_normalize('[{"z":1,"a":2},{"y":3,"b":4}]');
```

```text
[{"a":2,"z":1},{"b":4,"y":3}]
```

Once two semantically-equal documents normalize to the same bytes, hashing them collapses duplicates trivially:

```sql
SELECT
    md5(json_normalize('{"z":1,"a":2}')) =
    md5(json_normalize('{"a":2,"z":1}')) AS same_hash;
```

```text
true
```

A `GROUP BY md5(json_normalize(payload))` collapses duplicate emissions to a single row, deduplicating entities that differ only in key ordering. This is useful for a metadata catalog where the same entity may be described by two different upstream sources with slightly different key orderings.

Internally, the function walks the mutable doc, sorts each object's key-value pairs with `std::sort`, and rebuilds the object in order.

## `json_strip_nulls`: Recursively Drop Null-Valued Keys

`json_strip_nulls` is a cleanup helper. It removes every key whose value is JSON `null`, recursively. Array elements are not modified (since `null` is a valid array element), and scalar values are returned unchanged.

```sql
SELECT json_strip_nulls('{"a":1,"b":null,"c":null,"d":2}');
```

```text
{"a":1,"d":2}
```

It descends into nested objects:

```sql
SELECT json_strip_nulls('{"a":{"x":1,"y":null},"b":2}');
```

```text
{"a":{"x":1},"b":2}
```

And into objects inside arrays, while leaving the array structure intact:

```sql
SELECT json_strip_nulls('{"a":[{"x":1,"y":null},{"z":null}]}');
```

```text
{"a":[{"x":1},{}]}
```

The motivating case is cleaning patches before storing them. After computing a `json_merge_patch_diff`, the patch contains `null` entries for deleted keys, which is correct under RFC 7396. If you only want to ship the additions and updates, `json_strip_nulls(json_merge_patch_diff(orig, modified))` removes those null entries from the patch. The resulting patch can add and update fields but never delete them. The same idea applies to trimming verbose API responses before hashing or storing them.

Under the hood, this uses `yyjson_mut_obj_iter_remove`, which deletes keys during iteration without invalidating the iterator. Calling `json_strip_nulls` on an already-clean document reduces to a parse, one pass, and a serialize.

## Composing Them: An End-to-End Reconciliation

The four functions compose into a small reconciliation workflow. Suppose an upstream system emits partial JSON documents on each change. Some fields are present with new values, some are absent because the upstream did not include them, and some are explicitly `null` because the upstream has no data for them on this event. The goal is to clean the event, compute the minimal patch against the previous state, ship that patch, and store a canonical hash of the resulting document so identical entities collapse on deduplication.

Let's see this workflow through a concrete example:

```sql
CREATE TABLE catalog (id INTEGER, state JSON);
INSERT INTO catalog VALUES (
    1,
    '{"typeName":"Column","name":"user_id","description":"primary key","dataType":"BIGINT","ownerEmail":"alice@example.com"}'
);

CREATE TABLE incoming_events (id INTEGER, event JSON);
INSERT INTO incoming_events VALUES (
    1,
    '{"name":"user_id","description":"primary key for the users table","dataType":"BIGINT","ownerEmail":null,"team":null}'
);
```

Step 1: strip the `null` placeholders out of the incoming event so they do not get treated as deletes:

```sql
SELECT json_strip_nulls(event) AS clean_event
FROM incoming_events
WHERE id = 1;
```

```text
{"name":"user_id","description":"primary key for the users table","dataType":"BIGINT"}
```

Step 2: produce a minimal patch against the current state. Deep-merge the cleaned event onto the original (so missing fields keep their previous value), then diff back against the original:

```sql
SELECT json_merge_patch_diff(
    c.state,
    json_deep_merge(c.state, json_strip_nulls(e.event))
) AS patch
FROM catalog c
JOIN incoming_events e USING (id);
```

```text
{"description":"primary key for the users table"}
```

Only the changed field appears. `dataType` was unchanged, `ownerEmail` and `team` were `null` and got stripped, so neither are returned. The patch is what you would ship downstream.

Step 3: apply the patch back and hash the normalized result:

```sql
SELECT
    md5(json_normalize(
        json_merge_patch(
            c.state,
            '{"description":"primary key for the users table"}'
        )
    )) AS content_hash
FROM catalog c
WHERE id = 1;
```

```text
21ceaced24d8958d71d537f6fcebe8a2
```

Each function performs a single transformation, and the whole chain runs in a single query.

## Benchmarks: DuckDB vs. Python on 500,000 CDC Events

The benchmark below compares each function and the full composed chain against equivalent Python implementations on 500,000 synthetic catalog-event pairs (roughly 600 bytes per document). The Python implementations parse with `json.loads`, apply the equivalent transformation in pure Python (the Python output matches DuckDB's exactly on 100 sample documents), and serialize back with `json.dumps`. That is the closest apples-to-apples comparison to what DuckDB does end-to-end on a JSON column.

| Function              | Python (s) | DuckDB (s) | Speedup |
|-----------------------|-----------:|-----------:|--------:|
| `json_normalize`        |       7.02 |       0.15 |   46.8x |
| `json_deep_merge`       |       8.45 |       0.47 |   18.0x |
| `json_merge_patch_diff` |       6.66 |       0.19 |   35.1x |
| `json_strip_nulls`      |       6.17 |       0.05 |  123.4x |
| Full chain (composed)   |      11.11 |       1.03 |   10.8x |

The benchmark methodology is as follows. Each measurement is the median of five iterations. Python timings include parse, transform, and serialize per row, with data pre-loaded into memory so disk I/O is excluded. For DuckDB, we timed the whole run from the command line and subtracted a no-op SELECT json run, so only the transformation is measured. Hardware is an Apple M3 Pro (arm64) with 18 GB RAM, Python 3.11. DuckDB runs multi-threaded by default, while the Python script is single-threaded. The benchmark code and synthetic data generator are available [on GitHub](https://github.com/mustafahasankhan/duckdb-json-bench).

The speedup comes from two sources: DuckDB operates on `yyjson` trees in place, while the Python equivalent spends most of its cycles in `json.loads` and `json.dumps`. The result is a speedup of about 1-2 orders of magnitude, depending on how much transformation work the function does. `json_strip_nulls` is the extreme case, since the work after parsing reduces to a single iterator pass with an in-place delete. On the composed chain, the per-function gap narrows because the absolute work goes up on both sides, but DuckDB still finishes the full reconciliation of 500,000 event pairs in roughly one second.

## Performance Notes

There are a few characteristics worth pointing out:

* All four functions operate on `yyjson` mutable values directly. 
* `json_merge_patch_diff` uses `yyjson_equals` for deep equality, and subtrees that compare equal stop the recursion.
* `json_normalize`'s sort is per-object, not global. The cost scales with the size of each object, not the document.
* All four are plain scalar functions that process one vector of rows at a time, so they fit DuckDB's vectorized execution model.

## Trying the Functions

The four functions will ship in DuckDB v2.0. To try them today, install [a v2.0-dev preview build](https://duckdb.org/preview), then load the JSON extension:

```sql
LOAD json;

SELECT json_normalize('{"z":1,"a":2}');
```

## Wrapping Up

These four functions extend the DuckDB JSON extension with primitives for diffing, merging, normalizing, and stripping null values. They compose into reconciliation pipelines that previously required transformations outside SQL.

That's not all. The functions `json_set(json, path, value)`, `json_remove`, `json_insert`, and `json_replace` are also available in DuckDB v2.0 preview ([#23786](https://github.com/duckdb/duckdb/pull/23786)), completing the set of edit primitives defined in the SQL/JSON specification. For the implementations, see the JSON extension source in [`extension/json`](https://github.com/duckdb/duckdb/tree/main/extension/json).

Feedback and bug reports are welcome on [Discord](https://discord.duckdb.org) or [GitHub](https://github.com/duckdb/duckdb).
