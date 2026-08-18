---
layout: post
title: "A Preview of DuckDB v2.0"
author: "Mark Raasveldt and Hannes Mühleisen"
thumb: "/images/blog/thumbs/duckdb-preview-2-0.svg"
image: "/images/blog/thumbs/duckdb-preview-2-0.png"
excerpt: "DuckDB v2.0 is coming this fall. In this post, we preview its headline features: DuckDB as a server, triggers, the VARIANT type, asynchronous I/O, a new SQL parser, a new storage format, and much more."
tags: ["release"]
---

DuckDB v2.0 will be named “Cyanoptera” after the [cinnamon teal](https://en.wikipedia.org/wiki/Cinnamon_teal) *(Anas cyanoptera),* a strikingly reddish-brown duck found in the western Americas.

A major version bump is not something we do lightly, and it is not just ceremony: v2.0 ships a new SQL parser, a new default storage format, a reworked C API, and a small number of carefully chosen breaking changes. But above all, it is a feature release, built from over 10,000 commits since we released v1.5 in March. Where last year was the year of the lakehouse, this release kicks off the year of DuckDB as a server. We previewed many of these features in the [“State of the Duck” talk at DuckCon #7](https://www.youtube.com/watch?v=iFPKNQu0FtE), if you prefer to watch instead of read.

DuckDB is moving rather quickly, and we can only cover a small fraction of the changes here. Condensing all new features down to a shortlist is always a fight over what gets in, and yes, we know that what follows is technically a listicle *(Ten Things Coming to DuckDB v2.0, Number Eight Will Shock You).* We are not proud of the format, but it works, so here it is, starting with the SQL-level features and working down into the engine.

## 1. DuckDB as a Server: Quack and `CONNECT`

DuckDB has been an in-process database since day one. But people have asked us – very persistently – for a client/server mode, and we have finally caved. The [`quack` extension](https://github.com/duckdb/duckdb-quack) implements DuckDB's native protocol for talking to other DuckDBs. It was [released as a preview]({% post_url 2026-05-12-quack-remote-protocol %}) shortly before DuckCon #7, graduates to stable in v2.0, and it is a big part of where DuckDB is headed: any DuckDB process can serve its databases over the network, and any other DuckDB can attach to it and route queries there using the new `CONNECT` statement. For example:

<!-- markdownlint-disable MD001 -->

<div class="duck-diagram" markdown="1">

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB server

```sql
CALL quack_serve(
    token = 'my_token'
);
```

</div>

<div class="duck-diagram-arrow">quack:</div>

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB client

```sql
ATTACH 'quack:server.example.com'
    AS qk (TOKEN 'my_token');

CONNECT qk;
SELECT count(*) FROM events;
-- executes on the server,
-- results stream back
DISCONNECT;
```

</div>

</div>

<!-- markdownlint-enable MD001 -->

`CONNECT` is the successor to the `remote.query($$...$$)` workaround we showed when Quack was first revealed – we looked at that syntax and said: no, this cannot be it. And `CONNECT` is not limited to Quack: it points your session at any remote database that supports it, and the new remote pushdown optimizer ([#22914](https://github.com/duckdb/duckdb/pull/22914)) ships SQL directly to PostgreSQL and MySQL instead of pulling tables over the wire:

```sql
CONNECT 'postgres://localhost/mydb';
SELECT count(*) FROM orders; -- runs on the PostgreSQL server
DISCONNECT;
```

If you have worked with analytical systems in the past, you may assume that DuckDB cannot handle transactional workloads. But DuckDB has been built as a transactional, multi-connection database with full MVCC and transaction isolation since day one. Most users just never needed that in a single-user scenario. It turns out DuckDB handles transactions well: it's fast enough to compete with general-purpose databases like PostgreSQL on quite a few workloads, and the client/server pattern finally lets that machinery shine in multi-tenant, long-running deployments.

Running DuckDB long-term also comes with new challenges, which is why v2.0 pushes on better metrics, logs, and observability (see, e.g., the metrics layer rework in [#22799](https://github.com/duckdb/duckdb/pull/22799)) that let you look at a DuckDB instance and see what it is actually doing. People even built standalone clients for the Quack protocol within weeks of the preview. We thought we were extending DuckDB to talk to other DuckDBs; the world said no, no, no, and built their own clients. Who would have thought.

## 2. `VARIANT` Becomes a First-Class Citizen

The `VARIANT` type shipped in [DuckDB v1.5]({% post_url 2026-03-09-announcing-duckdb-150 %}), and the way to think about it is JSON on steroids. Basically, imagine if JSON were fast. Like JSON, a `VARIANT` column can store differently-shaped data in every row. Unlike JSON, it is not a text format: DuckDB automatically detects the common structure hidden in your semi-structured data and “shreds” it, so it compresses well in storage and executes fast in queries, all without you ever declaring a schema. This makes `VARIANT` a natural fit for real-time log ingestion, where streams of JSON-ish records share structure but evolve over time.

In v2.0, this pipeline works end to end: shredded execution straight from storage ([#20912](https://github.com/duckdb/duckdb/pull/20912)), extraction pushdown into scans ([#22478](https://github.com/duckdb/duckdb/pull/22478)), shredded `VARIANT` reading *and* writing for Parquet, and a family of `variant_*` functions:

```sql
CREATE TABLE events (payload VARIANT);
INSERT INTO events
VALUES ('{"user": {"id": 42, "tags": ["a", "b"]}}'::JSON::VARIANT);

SELECT variant_type(payload), variant_keys(payload)
FROM events;

SELECT *
FROM events
WHERE variant_contains(payload, {'user': {'id': 42}}::VARIANT);
```

Longer term, likely soon after v2.0 (but don't hold us to it), we plan to back the regular `JSON` type with `VARIANT`, so existing JSON workloads get all of these benefits without changing a single query.

## 3. Triggers

Triggers have been a long-standing feature request, and DuckDB v2.0 delivers them in full: `BEFORE` and `AFTER` triggers, `FOR EACH ROW` and `FOR EACH STATEMENT`, transition tables via `REFERENCING OLD/NEW TABLE`, multiple triggers per event, `RETURNING` on triggered tables, and `DROP TRIGGER`.

The classic use case is audit tables: something happens in the system, and a trigger records what changed. For example:

```sql
CREATE TABLE target (id INTEGER, val INTEGER);
CREATE TABLE audit (id INTEGER, old_val INTEGER, new_val INTEGER);

CREATE TRIGGER trg_audit AFTER UPDATE ON target
REFERENCING OLD TABLE AS o NEW TABLE AS n
FOR EACH STATEMENT
    INSERT INTO audit
    SELECT n.id, o.val, n.val
    FROM o
    JOIN n ON o.id = n.id;

INSERT INTO target VALUES (1, 10), (2, 20);
UPDATE target SET val = val * 10 WHERE id <= 2;
SELECT * FROM audit;
```

|   id | old_val | new_val |
| ---: | ------: | ------: |
|    1 |      10 |     100 |
|    2 |      20 |     200 |

Triggers fit naturally with long-running DuckDB services, and we are also planning to use them internally to build several upcoming features. They are fully exposed at the SQL level too, so you can build your own cool stuff with them.

## 4. SQL Dialect Additions

As always, DuckDB's SQL dialect keeps growing. A few favorites from this release cycle:

With **`NEAREST` joins** ([#24137](https://github.com/duckdb/duckdb/pull/24137)), top-k similarity search becomes a join clause, handy for vector and embedding workloads:

```sql
SELECT q.user_id, t.product_id
FROM users q
    INNER JOIN products t APPROX NEAREST 2
    BY SIMILARITY array_cosine_similarity(q.embedding, t.embedding);
```

**DML inside CTEs** ([#21634](https://github.com/duckdb/duckdb/pull/21634), [#21997](https://github.com/duckdb/duckdb/pull/21997), [#24217](https://github.com/duckdb/duckdb/pull/24217)) lets you use `INSERT`, `UPDATE`, `DELETE`, and `COPY` as pipeline steps:

```sql
WITH moved AS MATERIALIZED (
    DELETE FROM staging RETURNING *
)
INSERT INTO archive SELECT * FROM moved;
```

**Nested schemas** ([#23492](https://github.com/duckdb/duckdb/pull/23492), [#24222](https://github.com/duckdb/duckdb/pull/24222)) allow schemas within schemas:

```sql
CREATE SCHEMA finance;
CREATE SCHEMA finance.reports;
CREATE TABLE finance.reports.q3 (revenue DECIMAL);
```

The new **variable syntax** ([#21194](https://github.com/duckdb/duckdb/pull/21194)) lets you write `$x` anywhere an expression is allowed, no more [`getvariable(...)` verbiage]({% link docs/current/sql/functions/utility.md %}#getvariablevariable_name):

```sql
SET VARIABLE threshold = 100;
SELECT * FROM orders WHERE amount > $threshold;
```

The **JSON mutation functions** `json_set`, `json_insert`, `json_replace`, and `json_remove` ([#23786](https://github.com/duckdb/duckdb/pull/23786)) finally let you modify JSON documents in place:

```sql
SELECT json_set('{"a":1}', '$.b', '2');
```

| json_set('{"a":1}', '$.b', '2') |
| ------------------------------- |
| {"a":1,"b":2}                   |

And **recursive CTEs with [`USING KEY`]({% post_url 2025-05-23-using-key %}) aggregation** ([#19481](https://github.com/duckdb/duckdb/pull/19481)) enable iterative algorithms in pure SQL, backed by the rewritten recursive CTE engine described below:

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a, avg(b)) AS (
    SELECT 1, 5
    UNION
    SELECT a, b - 1 FROM tbl WHERE b > 0
)
TABLE tbl;
```

|    a |    b |
| ---: | ---: |
|    1 |  2.5 |

There is more: SQL-standard `FETCH FIRST 2 ROWS ONLY` ([#23533](https://github.com/duckdb/duckdb/pull/23533)), `OVERLAY()` ([#22456](https://github.com/duckdb/duckdb/pull/22456)), `UNNEST` in `GROUP BY` ([#23644](https://github.com/duckdb/duckdb/pull/23644)), and well-defined `MERGE` / `UPDATE ... FROM` semantics for multi-matched rows ([#24058](https://github.com/duckdb/duckdb/pull/24058)).

## 5. Asynchronous I/O

Interacting with object stores like S3 is central to the DuckDB experience: your data has to come from somewhere, and it often sits in object storage. DuckDB has long been able to read from object stores in parallel, but synchronous access placed a limit on how fast this could go. DuckDB v2.0 introduces asynchronous I/O throughout the engine. We described the design in detail in [a dedicated blog post]({% post_url 2026-07-31-asynchronous-io %}).

Thanks to asynchronous access, the I/O layer now scales independently from the query processing layer, which means far more parallelism for remote reads and dramatically faster queries on network storage. Parquet support came first ([#23662](https://github.com/duckdb/duckdb/pull/23662)), with CSV ([#23961](https://github.com/duckdb/duckdb/pull/23961)) and DuckDB's own file format ([#24654](https://github.com/duckdb/duckdb/pull/24654)) following, along with asynchronous Parquet writes ([#23283](https://github.com/duckdb/duckdb/pull/23283)) and new `MMAP` and `DIRECT_IO` modes ([#22988](https://github.com/duckdb/duckdb/pull/22988)). Local storage benefits a little too, but network storage is where you will see the big gains.

## 6. Faster Queries Across the Board

As with every release, a lot of work went into making your existing queries faster without you doing anything. To pick some highlights: partial aggregates are now pushed below joins ([#22572](https://github.com/duckdb/duckdb/pull/22572)) and redundant aggregations are reused ([#24543](https://github.com/duckdb/duckdb/pull/24543)), the recursive CTE engine has been rewritten ([#22211](https://github.com/duckdb/duckdb/pull/22211)), aggregations now spill to disk when they outgrow memory ([#24499](https://github.com/duckdb/duckdb/pull/24499)), and the Windows CLI got approximately 2.2× faster at multi-threaded result materialization ([#24036](https://github.com/duckdb/duckdb/pull/24036)).

How much faster can this get? Here is a microbenchmark you can run on a laptop: single-source reachability over a graph with one million edges, written as a plain [recursive CTE]({% link docs/current/sql/query_syntax/with.md %}).

```sql
CREATE TABLE edges AS
    SELECT (range % 100_000)::INTEGER AS src,
           ((range * 13 + 7) % 100_000)::INTEGER AS dst
    FROM range(1_000_000);

WITH RECURSIVE reachable(node) AS (
    SELECT 0
    UNION
    SELECT dst FROM edges, reachable WHERE src = node
)
SELECT count(*) FROM reachable;
```

| Version               | Run time |
| --------------------- | -------: |
| DuckDB v1.5.4         |   4.90 s |
| DuckDB v2.0 (preview) |   0.12 s |

As you can see, DuckDB v2.0 is about 40× faster (!) for the same recursive query.

Row-group pruning has been massively expanded: [min-max indexes (zone maps)]({% link docs/current/sql/indexes.md %}#min-max-index-zonemap %}) and [Parquet Bloom filters]({% post_url 2025-03-07-parquet-bloom-filters-in-duckdb %}) now skip data for structs, lists, decimals, UUIDs, `IN` filters, and even function predicates:

```sql
-- these now prune row groups instead of scanning them:
SELECT * FROM logs WHERE contains(message, 'ERROR');
SELECT * FROM t WHERE substr(code, 1, 3) = 'NL-';
SELECT * FROM 'data/*.parquet' WHERE id IN (1, 5, 9);
```

Query planning also becomes **partition-aware** ([#22336](https://github.com/duckdb/duckdb/pull/22336)). [Lakehouse formats]({% link docs/current/lakehouse_formats.md %}) (DuckLake, Iceberg and plain Hive-partitioned Parquet on S3) are all partitioned, and exploiting that partitioning is often the difference between scanning a dataset and skipping most of it. In v2.0, the planner and optimizer take full advantage of existing partitioning, and partitioned writes have been reworked as well ([#22225](https://github.com/duckdb/duckdb/pull/22225), [#22620](https://github.com/duckdb/duckdb/pull/22620)).

## 7. Storage Format v2.0

DuckDB v2.0 bumps the default [storage format version]({% link docs/current/internals/storage.md %}) to v2.0.0 ([#22875](https://github.com/duckdb/duckdb/pull/22875)).

Column metadata is now loaded lazily ([#22333](https://github.com/duckdb/duckdb/pull/22333)), so wide tables open faster too. The `DICT_FSST` string compression method is enabled by default ([#23733](https://github.com/duckdb/duckdb/pull/23733)), deletes are stored compactly ([#24336](https://github.com/duckdb/duckdb/pull/24336)), and the storage layer performs much stronger corruption validation on read. In short: databases with big indexes and wide tables open faster and use far less memory. The new storage format also allows checkpoint vacuuming to compact tables with ART indexes by incrementally remapping entries whose row IDs change, avoiding a full index rebuild ([#23653](https://github.com/duckdb/duckdb/pull/23653)).

Later this year, ART indexes will be buffer-managed ([#21458](https://github.com/duckdb/duckdb/pull/21458), [#23605](https://github.com/duckdb/duckdb/pull/23605)). This will allow ART index buffers to be evicted under memory pressure, and remove the restriction on the ART index fitting completely within memory.

## 8. A Brand New SQL Parser

DuckDB has famously always used a parser derived from PostgreSQL's. We have decided that enough is enough: v2.0 ships our own modern, extensible PEG-based parser ([#22194](https://github.com/duckdb/duckdb/pull/22194)), an idea we first explored in our 2024 post on [runtime-extensible parsers]({% post_url 2024-11-22-runtime-extensible-parsers %}). This change ties into the extension ecosystem: extensions can now hook into the grammar itself, so expect extensions that expose entirely new SQL syntax. It also brings better error messages with precise source locations, and the first dialect compatibility mode:

```sql
SET dialect_compatibility_mode = 'spark';
```

You should not actually notice anything from the parser swap as we designed it to be compatible with the old one. If you do notice, please file an issue.

## 9. Timezones, Calendars, and Collations Without ICU

Timezone-aware timestamps, calendars, and collations in DuckDB have always been powered by the ICU library. ICU is a fine library, but we only ever used a small slice of it, while still carrying it around in every DuckDB distribution. In v2.0, the ICU library is gone entirely: the `icu` extension now implements timezones, calendars, and collations itself ([#24463](https://github.com/duckdb/duckdb/pull/24463), [#24403](https://github.com/duckdb/duckdb/pull/24403)), with the timezone data built directly from the IANA database and compressed down to around 45 kB. Everything keeps working exactly as before:

```sql
SELECT '2026-08-14 12:00:00'::TIMESTAMPTZ AT TIME ZONE 'Europe/Paris';
SELECT * FROM names ORDER BY name COLLATE de;
```

Besides being much smaller and easier to keep up to date, the new implementation is also simply faster. Here's a quick microbenchmark on a MacBook that converts 25 million timestamps to a timezone and filters 5 million strings with a German collation:

| Query                                       | v1.5.4 (ICU) | v2.0 (native) | Speedup |
| ------------------------------------------- | -----------: | ------------: | ------: |
| `ts AT TIME ZONE 'Europe/Paris'`, 25 M rows |       0.24 s |        0.11 s |    2.2× |
| Filter with `COLLATE de`, 5 M rows          |       0.15 s |        0.06 s |    2.6× |

## 10. Write Extensions Once, Host Them Yourself

Extensions are one of the best things about DuckDB, but today, most of them, including our own, build against the [unstable C++ API]({% link docs/current/clients/cpp.md %}). Extension authors are required to rebuild and publish their extensions for every DuckDB release, even if the extension itself does not change. This is often a non-trivial operation for the extension author and a non-trivial coordination effort for the DuckDB team. Not rebuilding an extension means it can't be installed on the latest version of DuckDB.

DuckDB v2.0 will ship with a revamped C API (see [#24702](https://github.com/duckdb/duckdb/pull/24702) for part 1). The API will have a versioned [specification expressed in YAML](https://github.com/duckdb/duckdb/tree/main/api_spec) that uses an also versioned specification _schema_, and tooling for code generation ([#24135](https://github.com/duckdb/duckdb/pull/24135)). The schema lets us tag every symbol with its lifecycle and stability guarantees ([#24435](https://github.com/duckdb/duckdb/pull/24435)). A large part of the API will be marked stable and frozen, providing a stable ABI across DuckDB versions.

The API itself improves over the pre-2.0 C API in a number of ways. It provides coherent error handling and a unified set of conventions around naming and ownership. It covers a much larger feature surface, including scalar, aggregate, table, cast, and copy functions with named parameters and varargs, parsing and inspecting SQL statements, prepared statements, replacement scans, custom filesystems, direct access to vector buffers, values and types, and more. It supports streaming query result consumption. With this API we want to provide the primitives to access DuckDB's most powerful features.

You won't need to program against the C API directly, though. We also provide a C++ API on top of it. It is a thin layer that compiles into your extension and talks only to the stable C ABI, so the binary you ship stays independent of DuckDB versions. It gives you a convenient, typed, well-documented way to access DuckDB's API. We're also working on bindings that provide the same for extension writers using Rust.

So what will an extension using the C++ API look like? Here is a complete example, though the details may still change: a single file that registers a vectorized scalar function.

```cpp
#include "duckdb_cpp.hpp"

using namespace duckdb_api;

DUCKDB_CPP_EXTENSION_ENTRYPOINT(extension) {
    // add_numbers(a BIGINT, b BIGINT DEFAULT 2): adds two BIGINTs, one vector at a time
    ScalarFunction function;
    function.SetName("add_numbers")
        .SetSignature(FunctionSignature::Create()
                        .AddParameter("a", LogicalType::BIGINT())
                        .AddParameterDefault("b", LogicalType::BIGINT(), Value::Bigint(2))
                        .SetReturnType(LogicalType::BIGINT()))
        .SetExecCallback([](ScalarFunction::ExecInput &input) {
            auto chunk = input.GetInputChunk();
            auto a = chunk.GetVector(0).GetView();
            auto b = chunk.GetVector(1).GetView();
            auto out = input.GetResultVector().GetDataMutable<int64_t>();
            for (idx_t i = 0; i < chunk.GetRowCount(); i++) {
                out[i] = a.Data<int64_t>()[a.SelAt(i)] + b.Data<int64_t>()[b.SelAt(i)];
            }
        })
        .Register(extension);
}
```

You can use it as follows:

```sql
LOAD add_numbers;
SELECT add_numbers(40, 2);           -- 42
SELECT add_numbers(40);              -- 42: b falls back to its default
SELECT add_numbers(b := 2, a := 40); -- 42: named arguments work too
SELECT add_numbers(40, NULL);        -- NULL, without the function doing anything
```

You do not need re-target or rebuild it every time a new DuckDB version comes out. And nowadays, with all the AI tooling around, building an extension has never been easier.

So you have written your extension. But how should you distribute it? Until now, DuckDB could only install extensions from the built-in repositories (`core`, `core_nightly`, `community`, ...). In v2.0, you will be able to register your own trusted repositories ([#24777](https://github.com/duckdb/duckdb/pull/24777), currently work-in-progress), so an organization can host and sign its own extensions and have them install and load just like the built-in ones:

```sql
SET allow_extension_repositories = 'allowed';
CREATE EXTENSION REPOSITORY my_repo FROM 'https://extensions.example.org';
INSTALL my_ext FROM my_repo;
LOAD my_repo/my_ext;
```

A repository is a name, a URL prefix, and one or more RSA public keys that are trusted to sign the extensions served from it. The prefix can point at anything DuckDB can read: a local path, `https`, `s3`, you name it. At `CREATE` time, DuckDB fetches the repository's public keys and pins them into the repository definition, printing each key's SHA-256 fingerprint so you can compare it against one published out of band. If you would rather not trust the network at all, you can pass the key directly:

```sql
CREATE EXTENSION REPOSITORY my_repo FROM 's3://my-bucket/extensions'
    USING PUBLIC KEY '-----BEGIN PUBLIC KEY----- ...';
```

Pinned repositories survive restarts, support key rotation by trusting multiple keys, and can be audited at any time through the `duckdb_extension_repositories()` table function, or removed again with `DROP EXTENSION REPOSITORY`. Together with the stable C API, the extension story rounds out nicely: write your extension once, sign it, host it wherever you like, and `INSTALL` it anywhere.

## Bonus: DuckDB Foundation – Advisory Board

Starting this fall, we will add a stakeholder advisory board to the [DuckDB Foundation](https://duckdb.foundation/). The advisory board will provide input on the development roadmap of DuckDB, DuckLake, and Quack. This allows key stakeholders to have a say in the projects' direction.

## Final Thoughts

These are only a few highlights, and this post is only a preview. Some details may still shift before the release this fall, and there are many more features and improvements that we could not cover here. DuckDB v2.0 will also come with a small set of breaking changes, including the new default storage format and the completed lambda syntax transition, which we will cover in detail in the release announcement.

There have been more than 10,000 commits by many contributors since we released v1.5. We would like to thank our community for the detailed issue reports, feedback, and contributions that shaped this release. If you want a taste before the fall, the [preview builds]({% link install/preview.md %}) have most of these features today, and if something breaks, you know where [the issue tracker](https://github.com/duckdb/duckdb/issues) is.
