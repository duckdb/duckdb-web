---
layout: post
title: "From JSON Strings to Typed Columns"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/json.svg"
image: "/images/blog/thumbs/json.png"
excerpt: "JSON often arrives as a text column inside a table, not as a file. In this post, we infer a schema from such a column, adjust it, and turn the column into typed columns, without first writing the data to a file."
tag: using-duckdb
---

DuckDB's [`read_json`]({% link docs/current/data/json/loading_json.md %}) turns JSON files into tables. It reads through part of the data to work out a schema, then gives you typed columns. However, a lot of JSON does not come as files. It comes as a text column: event payloads in a Postgres table, API responses stored by an ingestion job, a `metadata` column in a CSV export.

People regularly [ask](https://github.com/duckdb/duckdb/discussions/9558) how to get the `read_json` treatment for such a column, and one workaround that comes up is to [`COPY`]({% link docs/current/sql/statements/copy.md %}) the column to a file and read the file back.

You do not need the round trip. In this post, we get the same result directly in SQL.

## The Data

Here is a small table of events, with the payload stored as `VARCHAR`:

```sql
CREATE TABLE events (id INTEGER, payload VARCHAR);
INSERT INTO events VALUES
    (1, '{"user": {"id": 17, "country": "NL"}, "action": "click", "ts": "2026-10-01 10:00:00"}'),
    (2, '{"user": {"id": 23, "country": "BE"}, "action": "view", "ts": "2026-10-01 10:00:05", "duration_ms": 1200}'),
    (3, '{"user": {"id": 17}, "action": "purchase", "ts": "2026-10-01 10:02:11", "items": [{"sku": "A-1", "qty": 2}, {"sku": "B-7", "qty": 1}]}');
```

Like most real payloads, the objects do not all have the same keys. Only the second event has a `duration_ms`, only the third has `items`, and the third has no `country`.

## Picking out a Few Fields

If you only need a handful of fields, the [JSON extraction operators]({% link docs/current/data/json/json_functions.md %}) are enough. `->` returns `JSON` and `->>` returns `VARCHAR`. Both accept a key name or a JSON path:

```sql
SELECT
    id,
    payload ->> '$.user.country' AS country,
    payload ->> 'action' AS action,
    (payload ->> 'duration_ms')::INTEGER AS duration_ms
FROM events;
```

```text
┌───────┬─────────┬──────────┬─────────────┐
│  id   │ country │  action  │ duration_ms │
│ int32 │ varchar │ varchar  │    int32    │
├───────┼─────────┼──────────┼─────────────┤
│     1 │ NL      │ click    │        NULL │
│     2 │ BE      │ view     │        1200 │
│     3 │ NULL    │ purchase │        NULL │
└───────┴─────────┴──────────┴─────────────┘
```

Missing keys come back as `NULL`, which is what you want for optional fields. However, this approach parses the JSON again for every extracted field, and it becomes verbose once you want more than a few columns.

## Inferring a Structure from the Column

[`json_structure`]({% link docs/current/data/json/json_functions.md %}) returns the structure of a single JSON value. Its aggregate variation, [`json_group_structure`]({% link docs/current/data/json/json_functions.md %}), merges the structures of all values in a column into one. It needs `JSON` input, so cast the `VARCHAR` column first:

```sql
SELECT json_group_structure(payload::JSON) AS structure
FROM events;
```

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                      structure                                                                      │
│                                                                        json                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"user":{"id":"UBIGINT","country":"VARCHAR"},"action":"VARCHAR","ts":"VARCHAR","duration_ms":"UBIGINT","items":[{"sku":"VARCHAR","qty":"UBIGINT"}]} │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Every key that appears in any row is in there, including `duration_ms` and the array of `items`.

For a large table, you do not have to scan every row for this. Running it over a [sample]({% link docs/current/sql/query_syntax/sample.md %}), for example `FROM events USING SAMPLE 10_000 ROWS`, is much cheaper, at the risk of missing keys that are very rare.

## Adjusting the Types

The inferred structure needs a few fixes. `ts` came out as `VARCHAR` because JSON has no timestamp type, and the integers came out as `UBIGINT`, which is wider than needed.

Since the structure is itself a JSON document, you can override parts of it with [`json_merge_patch`]({% link docs/current/data/json/json_functions.md %}). Store the result in a [variable]({% link docs/current/sql/statements/set_variable.md %}) so you can use it in the next query:

```sql
SET VARIABLE payload_structure = (
    SELECT json_merge_patch(
        json_group_structure(payload::JSON),
        '{
            "user": {"id": "INTEGER"},
            "ts": "TIMESTAMP",
            "duration_ms": "INTEGER",
            "items": [{"sku": "VARCHAR", "qty": "INTEGER"}]
        }'
    )
    FROM events
);
```

The patch only lists what you want to change. Keys you leave out, such as `user.country` and `action`, keep their inferred types.

## Building the Table

[`json_transform`]({% link docs/current/data/json/json_functions.md %}) (also available as [`from_json`]({% link docs/current/data/json/json_functions.md %})) converts a JSON value into a DuckDB [`STRUCT`]({% link docs/current/sql/data_types/struct.md %}) following the structure you give it. [`unnest`]({% link docs/current/sql/query_syntax/unnest.md %}) then expands the top-level fields of that struct into columns:

```sql
CREATE TABLE events_typed AS
    SELECT id, unnest(json_transform(payload, getvariable('payload_structure')))
    FROM events;

DESCRIBE events_typed;
```

```text
┌─────────────┬─────────────────────────────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │             column_type             │  null   │   key   │ default │  extra  │
│   varchar   │               varchar               │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────────────────────────────┼─────────┼─────────┼─────────┼─────────┤
│ id          │ INTEGER                             │ YES     │ NULL    │ NULL    │ NULL    │
│ action      │ VARCHAR                             │ YES     │ NULL    │ NULL    │ NULL    │
│ user        │ STRUCT(country VARCHAR, id INTEGER) │ YES     │ NULL    │ NULL    │ NULL    │
│ ts          │ TIMESTAMP                           │ YES     │ NULL    │ NULL    │ NULL    │
│ duration_ms │ INTEGER                             │ YES     │ NULL    │ NULL    │ NULL    │
│ items       │ STRUCT(sku VARCHAR, qty INTEGER)[]  │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────────────────────────────┴─────────┴─────────┴─────────┴─────────┘
```

The JSON is parsed once, at load time. From here on, the columns are regular DuckDB columns, stored and compressed by type, and queries on them do not touch JSON at all:

```sql
SELECT id, "user".id AS user_id, "user".country, action, ts
FROM events_typed;
```

```text
┌───────┬─────────┬─────────┬──────────┬─────────────────────┐
│  id   │ user_id │ country │  action  │         ts          │
│ int32 │  int32  │ varchar │ varchar  │      timestamp      │
├───────┼─────────┼─────────┼──────────┼─────────────────────┤
│     1 │      17 │ NL      │ click    │ 2026-10-01 10:00:00 │
│     2 │      23 │ BE      │ view     │ 2026-10-01 10:00:05 │
│     3 │      17 │ NULL    │ purchase │ 2026-10-01 10:02:11 │
└───────┴─────────┴─────────┴──────────┴─────────────────────┘
```

## Nested Structs and Name Collisions

Recursive unnesting with [`unnest(..., recursive := true)`]({% link docs/current/sql/query_syntax/unnest.md %}) flattens nested structs in a single pass. By default it names each column after its innermost key, so the `id` inside `user` ends up as a column called `id`, right next to the event's own `id`:

```sql
SELECT id, unnest("user", recursive := true)
FROM events_typed
LIMIT 1;
```

```text
┌───────┬─────────┬───────┐
│  id   │ country │  id   │
│ int32 │ varchar │ int32 │
├───────┼─────────┼───────┤
│     1 │ NL      │    17 │
└───────┴─────────┴───────┘
```

With two columns both named `id`, a later query cannot tell which one you mean. Pass [`keep_parent_names := true`]({% link docs/current/sql/query_syntax/unnest.md %}) to prefix each column with the keys it came from, so names from different levels stay distinct. On the full payload, `user.id` and `user.country` no longer clash with the top-level columns, and you can select them by their prefixed names:

```sql
SELECT id, "user.id", "user.country"
FROM (
    SELECT id, unnest(json_transform(payload, getvariable('payload_structure')), recursive := true, keep_parent_names := true)
    FROM events
    LIMIT 1
);
```

```text
┌───────┬─────────┬──────────────┐
│  id   │ user.id │ user.country │
│ int32 │  int32  │   varchar    │
├───────┼─────────┼──────────────┤
│     1 │      17 │ NL           │
└───────┴─────────┴──────────────┘
```

## Arrays of Objects

In `events_typed`, the `items` array is stored as a `STRUCT(sku VARCHAR, qty INTEGER)[]`, a list of structs, as the `DESCRIBE` output above shows. To get one row per item, [`unnest`]({% link docs/current/sql/query_syntax/unnest.md %}) the list in the `FROM` clause:

```sql
SELECT id, u.item.sku, u.item.qty
FROM events_typed, unnest(items) AS u(item);
```

```text
┌───────┬─────────┬───────┐
│  id   │   sku   │  qty  │
│ int32 │ varchar │ int32 │
├───────┼─────────┼───────┤
│     3 │ A-1     │     2 │
│     3 │ B-7     │     1 │
└───────┴─────────┴───────┘
```

Events without items do not appear here. If you need to keep them, write the [`unnest`]({% link docs/current/sql/query_syntax/unnest.md %}) as a lateral join: `FROM events_typed LEFT JOIN unnest(items) AS u(item) ON true`.

## Values That Do Not Fit

By default, [`json_transform`]({% link docs/current/data/json/json_functions.md %}) does not raise an error on a value it cannot convert. The value becomes `NULL` instead:

```sql
SELECT json_transform('{"qty": "two"}', '{"qty": "INTEGER"}') AS result;
```

```text
┌─────────────────────┐
│       result        │
│ struct(qty integer) │
├─────────────────────┤
│ {'qty': NULL}       │
└─────────────────────┘
```

That is convenient for messy data, but it can hide problems. [`json_transform_strict`]({% link docs/current/data/json/json_functions.md %}) raises an error instead:

```sql
SELECT json_transform_strict('{"qty": "two"}', '{"qty": "INTEGER"}') AS result;
```

```console
Invalid Input Error: Failed to cast value to numerical: "two"
```

Use the strict version while you are working out the structure, and switch to the lenient version once you know which oddities you are willing to accept.

## Should the Column Be `VARCHAR` or `JSON`?

This question comes up regularly in the DuckDB discussions. The [`JSON` type]({% link docs/current/data/json/json_type.md %}) is stored exactly like a `VARCHAR`, so there is no difference in size or scan speed. What it adds is validation on the way in, since an invalid document fails the insert, and the guarantee that the extraction functions do not have to deal with malformed input.

If you will query fields from the column many times, the type of the raw column matters much less than whether you extract the fields at all. Parsing JSON at query time is work that has to be repeated for every query. Turning it into typed columns once, as shown above, does that work a single time.

## Further Reading

For more on working with JSON in DuckDB, see the following blog posts and documentation pages:

* [Shredding Deeply Nested JSON, One Vector at a Time]({% post_url 2023-03-03-json %}), on how DuckDB reads JSON files
* [Reconciling JSON in DuckDB, One Patch at a Time]({% post_url 2026-08-18-reconciling-json %}), on combining JSON documents with `json_merge_patch`
* [JSON Overview]({% link docs/current/data/json/overview.md %}) and [JSON Functions]({% link docs/current/data/json/json_functions.md %})
* [The `JSON` Type]({% link docs/current/data/json/json_type.md %})
* [`unnest`]({% link docs/current/sql/query_syntax/unnest.md %}) and the [`STRUCT` data type]({% link docs/current/sql/data_types/struct.md %})
