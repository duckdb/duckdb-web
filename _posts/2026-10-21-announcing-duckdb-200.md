---
layout: post
title: "Announcing DuckDB 2.0.0"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-0.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-0.png"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 2.0.0, codenamed “Cyanoptera”. This release ships DuckDB as a server, triggers, a first-class `VARIANT` type, asynchronous I/O, a brand new SQL parser, a new default storage format and much more, built from close to 20,000 commits since v1.5."
tag: release
---

We are proud to release DuckDB v2.0.0, codenamed “Cyanoptera” after the [cinnamon teal](https://en.wikipedia.org/wiki/Cinnamon_teal) _(Anas cyanoptera),_ a strikingly reddish-brown duck found in the western Americas.

DuckDB v2.0 is above all a feature release, built from over 10,000 commits since we released [v1.5]({% post_url 2026-03-09-announcing-duckdb-150 %}) in March. Where last year was the year of the lakehouse, this release kicks off the year of DuckDB as a server. It also ships a new SQL parser, a new default storage format, a reworked C API, and a small number of breaking changes.

In this blog post, we summarize the highlights and then walk through the breaking changes and how to migrate. We previewed many of these features in [“A Preview of DuckDB v2.0”]({% post_url 2026-08-17-duckdb-20-highlights %}), which covers each one in more depth. For the complete release notes, see the [release page on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.0).

> To install the new version, please visit the [installation page]({% link install/index.html %}). Note that it can take a few days to release some extensions and client libraries (e.g., Go, R, Java) due to the extra changes and review rounds required.

With this release, we have two DuckDB lines available. To ensure a smooth transition and allow sufficient time for testing, we extended the support period of DuckDB v1.5 until March 2027. For details, see the [release calendar]({% link release_calendar.md %}).

To find your way around the documentation for all of the new features, we also published a [“What's New in the Docs for 2.0”](/docs/preview/whats_new_in_the_docs) page that links each feature below to its documentation.

## Highlights

### DuckDB as a Server: Quack and `CONNECT`

DuckDB has been an in-process database since day one, but v2.0 lets it run as a server too. The [`quack` extension]({% link docs/preview/core_extensions/quack.md %}) implements DuckDB's native protocol, so any DuckDB process can serve its databases over the network and any other DuckDB can attach to it and route queries there using the new `CONNECT` statement:

```sql
ATTACH 'quack:server.example.com' AS qk (TOKEN 'my_token');
CONNECT qk;
SELECT count(*) FROM events; -- executes on the server, results stream back
DISCONNECT;
```

`CONNECT` is not limited to Quack: it points your session at any remote database that supports it, and the new remote pushdown optimizer ships SQL directly to PostgreSQL and MySQL instead of pulling tables over the wire.

### `VARIANT` Becomes a First-Class Citizen

The [`VARIANT` type]({% link docs/preview/sql/data_types/variant.md %}) stores semi-structured, schema-less data such as JSON while keeping the performance of columnar execution. Think of it as JSON on steroids: a `VARIANT` column can store differently-shaped data in every row, but unlike JSON it is not a text format. DuckDB detects the common structure in your data and “shreds” it, so it compresses well and executes fast. In v2.0 the pipeline works end to end, from shredded execution straight out of storage to shredded `VARIANT` reading and writing for Parquet, backed by a family of `variant_*` functions.

```sql
CREATE TABLE events (payload VARIANT);
INSERT INTO events
VALUES ('{"user": {"id": 42, "tags": ["a", "b"]}}'::JSON::VARIANT);

SELECT variant_type(payload), variant_keys(payload)
FROM events;
```

### Triggers

DuckDB v2.0 delivers triggers in full: `BEFORE` and `AFTER` triggers, `FOR EACH ROW` and `FOR EACH STATEMENT`, transition tables via `REFERENCING OLD/NEW TABLE`, multiple triggers per event, `RETURNING` on triggered tables and `DROP TRIGGER`. The classic use case is audit tables, where a trigger records what changed in response to a table modification.

```sql
CREATE TRIGGER trg_audit AFTER UPDATE ON target
REFERENCING OLD TABLE AS o NEW TABLE AS n
FOR EACH STATEMENT
    INSERT INTO audit
    SELECT n.id, o.val, n.val
    FROM o JOIN n ON o.id = n.id;
```

### SQL Dialect Additions

As always, DuckDB's SQL dialect keeps growing. A few favorites from this release cycle:

* `NEAREST` joins turn top-k similarity search into a join clause, handy for vector and embedding workloads.
* Data-modifying CTEs let you use `INSERT`, `UPDATE`, `DELETE` and `COPY` as pipeline steps.
* Nested schemas allow schemas within schemas, e.g., `CREATE SCHEMA finance.reports`.
* The `$⟨variable⟩` shorthand lets you write `$x` anywhere an expression is allowed, instead of `getvariable(...)`.
* JSON mutation functions `json_set`, `json_insert`, `json_replace` and `json_remove` modify JSON documents in place.

There is more: SQL-standard `FETCH FIRST`, `UNNEST` in `GROUP BY` and well-defined `MERGE` / `UPDATE ... FROM` semantics for multi-matched rows.

### Asynchronous I/O

DuckDB v2.0 introduces [asynchronous I/O]({% link docs/preview/data/io.md %}) throughout the engine. The I/O layer now scales independently from the query processing layer, issuing reads in the background and keeping multiple requests in flight. This means far more parallelism for remote reads and dramatically faster queries on object storage such as [`s3://`]({% link docs/preview/core_extensions/httpfs/s3api.md %}). 

We described the design in detail in a [dedicated blog post]({% post_url 2026-07-31-asynchronous-io %}).

### Faster Queries Across the Board

As with every release, a lot of work went into making your existing queries faster without you doing anything. Partial aggregates are now pushed below joins, redundant aggregations are reused, the recursive CTE engine has been rewritten, aggregations spill to disk when they outgrow memory, and row-group pruning has been massively expanded across structs, lists, decimals, UUIDs, `IN` filters and even function predicates. 

In a [microbenchmark]({% post_url 2026-08-17-duckdb-20-highlights %}#6-faster-queries-across-the-board) of single-source reachability over a graph with one million edges, DuckDB v2.0 runs a plain recursive CTE about 40× faster than v1.5. We explain how in a [dedicated blog post]({% post_url 2026-08-25-how-duckdb-runs-recursive-ctes-faster %}).

### Storage Format v2.0

DuckDB v2.0 bumps the default [storage format version]({% link docs/preview/internals/storage.md %}) to v2.0.0. Column metadata is now loaded lazily, so wide tables open faster; the `DICT_FSST` string compression method is enabled by default; deletes are stored compactly; and the storage layer performs much stronger corruption validation on read. Databases with big indexes and wide tables open faster and use far less memory. 

Because the new format is not backward compatible, see the [migration section](#migrating-to-v20) below.

### A Brand New SQL Parser

DuckDB has always used a parser derived from PostgreSQL's. In v2.0 we ship our own modern, extensible [PEG-based parser]({% post_url 2026-08-20-duckdb-20-peg-parser %}). Extensions can now hook into the grammar itself, so expect extensions that expose entirely new SQL syntax, and error messages now come with precise source locations. The new parser is designed to be compatible with the old one, so you should not notice the swap. If you do, please file an issue.


### Write Extensions Once, Host Them Yourself

DuckDB v2.0 ships a revamped, stable C API with a versioned ABI, so an extension built once keeps working across releases, along with a thin C++ API on top of it. 

You can also register and host your own trusted [extension repositories](https://github.com/duckdb/duckdb/pull/24777), so an organization can host and sign its own extensions and have them install and load just like the built-in ones.

## Other Changes


### Timezones, Calendars, and Collations Without ICU

Timezone-aware timestamps, calendars and collations have always been powered by the ICU library. In v2.0, the ICU library is gone entirely: the `icu` extension now implements timezones, calendars and collations itself, with the timezone data built directly from the IANA database and compressed down to around 45 kB. 

Everything keeps working exactly as before, and the native implementation is also faster.

TODO: let us know if you find anything

### C and C++ Extension API

Extensions built against the old unstable C++ API must be rebuilt against v2.0.0. Before upgrading, confirm that v2.0.0-compatible builds exist for any third-party extensions you depend on.

## Migrating to v2.0

DuckDB v2.0 comes with a small set of breaking changes. For most users, upgrading is straightforward, but complex deployments running many DuckDB processes need more care. The storage format is the most likely source of problems. We recommend testing v2.0.0 on a shadow system before switching production over, and if your workload is mission-critical, you may want to wait for the first patch releases. 

For the full details, see the [migration guide]({% linkn docs/preview/operations_manual/migration.md %}).

### ICU Removed from the Core Build

The ICU library dependency has been removed from the core build; timezones, calendars and collations are now handled natively by the `icu` extension, with no change in behavior. No query changes are needed, but custom builds no longer bundle ICU.

### Storage Format

The new storage format is not backward compatible with earlier versions. A file written by v2.0.0 cannot be read by older DuckDB versions, which will report an IO error. In multi-process deployments, a single v2.0.0 write can make a shared file unreadable to older processes, so roll out carefully and ensure version compatibility.

If you still need to write files that older versions can read, use the `-storage-version` CLI argument, the `storage_compatibility_version` configuration option or the `STORAGE_VERSION` option on `ATTACH`. To convert an existing database, open it with the older version and `EXPORT DATABASE`, then `IMPORT DATABASE` with v2.0.0. `COPY FROM DATABASE` is also supported.

### Lambda Syntax

The old single-arrow lambda syntax (`x -> x + 1`) is now disabled by default. Use the Python-style syntax instead:

```sql
SELECT list_transform([1, 2, 3], lambda x: x + 1);
```

You can temporarily re-enable the old syntax with `SET lambda_syntax = 'ENABLE_SINGLE_ARROW';`. Both the flag and the single-arrow syntax will be removed entirely in v2.1.

### SQL Parser Fallback Option

The new PEG-based parser is intended to be compatible with the old PostgreSQL-derived one. If a query that parsed previously now fails, please file an issue. In the meantime, you can revert to the old parser via the `legacy_parser` extension:

```sql
INSTALL legacy_parser;
LOAD legacy_parser;
SET enable_legacy_parser = true;
```

### Amalgamation Build Deprecated

The amalgamation build, which bundles DuckDB's entire source code into a single header and a single source file, is now deprecated. The amalgamation has grown too large to be realistically useful in most cases.

## Summary

These were a few highlights, but there are many more features and improvements in this release. There have almost 20,000 commits by many contributors since v1.5. The full [release notes can be found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.0). 

We would like to thank our community for the detailed issue reports and feedback that have driven this release, and our special thanks go to our contributors!
