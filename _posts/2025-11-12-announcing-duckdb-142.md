---
layout: post
title: "Announcing DuckDB 1.4.2 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-2-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-2-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.2, the second patch release of our LTS edition. The new release ships several bugfixes and performance optimizations as well as some new Iceberg and CLI features."
tags: ["release"]
---

In this blog post, we highlight a few important fixes and convenience improvements in DuckDB v1.4.2, the second patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}). To see the complete list of updates, please consult the [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.2).

To install the new version, please visit the [installation page]({% link install/index.html %}). Note that it can take a few hours to days for some client libraries (e.g., Go, R, Rust, Java) to be released due to the extra changes and review rounds required.

## Features and Improvements

### Iceberg Improvements

Similarly to the [v1.4.1 release blog post]({% post_url 2025-10-07-announcing-duckdb-141 %}#iceberg-improvements), we can start with some good news for our Iceberg users: DuckDB v1.4.2 ships a number of improvements for the [`iceberg` extension]({% link docs/stable/core_extensions/iceberg/overview.md %}). Insert, update, and delete statements are all supported now:

<!-- markdownlint-disable MD040 -->

<details markdown='1'>
<summary markdown='span'>
Click to see the SQL code sample for Iceberg updates.
</summary>
```sql
ATTACH '⟨warehouse_name⟩' AS iceberg_catalog (
    TYPE iceberg,
    ⟨other options⟩
);

CREATE TABLE iceberg_catalog.default.simple_table
    (col1 INTEGER, col2 VARCHAR);

INSERT INTO iceberg_catalog.default.simple_table
    VALUES (1, 'hello'), (2, 'world'), (3, 'duckdb is great');

DELETE FROM iceberg_catalog.default.simple_table
WHERE col1 = 2;

UPDATE iceberg_catalog.default.simple_table
SET col1 = col1 + 5
WHERE col1 = 1;
```
</details>

<!-- markdownlint-enable MD040 -->

We will publish a separate blog post on these improvements shortly. Stay tuned!

### Logger and Profiler Improvements

#### Time HTTP Requests

The logger can now log the time of HTTP requests ([`#19691`](https://github.com/duckdb/duckdb/pull/19691)).
For example, if we query the Dutch railway tariffs table as a Parquet file ([`tariffs.parquet`](https://blobs.duckdb.org/tariffs.parquet)),
we can see multiple HTTP requests: a `HEAD` request and three `GET` requests:

```sql
CALL enable_logging('HTTP');
CREATE TABLE railway_tariffs AS
    FROM 'https://blobs.duckdb.org/tariffs.parquet';
SELECT request.type, request.url, request.duration_ms
FROM duckdb_logs_parsed('HTTP');
```

```text
┌─────────┬──────────────────────────────────────────┬─────────────┐
│  type   │                   url                    │ duration_ms │
│ varchar │                 varchar                  │    int64    │
├─────────┼──────────────────────────────────────────┼─────────────┤
│ HEAD    │ https://blobs.duckdb.org/tariffs.parquet │         177 │
│ GET     │ https://blobs.duckdb.org/tariffs.parquet │         103 │
│ GET     │ https://blobs.duckdb.org/tariffs.parquet │         176 │
│ GET     │ https://blobs.duckdb.org/tariffs.parquet │         182 │
└─────────┴──────────────────────────────────────────┴─────────────┘
```

#### Accessing the Profiler's Output from the Logger

[The logger can now access the profiler's output `#19572`](https://github.com/duckdb/duckdb/pull/19572).
This means that if both the profiler and the logger are enabled, you can log information such as the execution time of queries:

```sql
-- Enable profiling to JSON file
-- This is necessary to make sure that queries are profiled
PRAGMA profiling_output = 'profiling_output.json';
PRAGMA enable_profiling = 'json';

-- Enable logging to an in-memory table
CALL enable_logging();

-- Run some queries
CREATE TABLE small AS FROM range(1_000_000);
CREATE TABLE big AS FROM range(1_000_000_000);

PRAGMA disable_profiling;

SELECT query_id, type, metric, value::DECIMAL(15, 3) AS value
FROM duckdb_logs_parsed('Metrics')
WHERE metric = 'CPU_TIME';
```

You can see in the output that the first `CREATE` statement took about 3 milliseconds, while the second one took 3.3 seconds.

```text
┌──────────┬─────────┬──────────┬───────────────┐
│ query_id │  type   │  metric  │     value     │
│  uint64  │ varchar │ varchar  │ decimal(15,3) │
├──────────┼─────────┼──────────┼───────────────┤
│        8 │ Metrics │ CPU_TIME │         0.003 │
│        9 │ Metrics │ CPU_TIME │         3.267 │
└──────────┴─────────┴──────────┴───────────────┘
```

#### Profiler Metrics

The profiler now supports [several new metrics]({% link docs/stable/dev/profiling.md %}#metrics).
These allow you the get a deeper understanding on where the execution time is spent in queries.

### Performance Improvements

DuckDB v1.4.2 also ships some small performance improvements:

* [`#19477` DuckDB now buffers WAL index deletes, not only appends](https://github.com/duckdb/duckdb/pull/19477)
* [`#19644` Detaching from a database is now faster](https://github.com/duckdb/duckdb/pull/19644)

### Vortex Support

DuckDB now supports the [Vortex file format](https://vortex.dev/) through the `vortex` extension.
First, install and load the extension:

```sql
INSTALL vortex;
LOAD vortex;
```

Then, you can write Vortex files as follows:

```sql
COPY (SELECT * FROM generate_series(0, 3) t(i))
TO 'my.vortex' (FORMAT vortex);
```

And read them using the `read_vortex` function:

```sql
SELECT * FROM read_vortex('my.vortex');
```

```text
┌───────┐
│   i   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
└───────┘
```

## Fixes

We fixed several crashes, internal errors, incorrect results and regressions.
We also fixed several issues discovered by our [fuzzer](https://github.com/duckdb/duckdb-fuzzer/).

### Crashes and Internal Errors

* [`#19238` `MERGE INTO` Iceberg table with `TIMESTAMPTZ` columns crashes](https://github.com/duckdb/duckdb/issues/19238)
* [`#19355` Unknown expression type invalidates database](https://github.com/duckdb/duckdb/issues/19355)
* [`#19357` Expected unified vector format of type `VARCHAR`, but found type `INT32`](https://github.com/duckdb/duckdb/issues/19357)
* [`#19455` `MERGE INTO` failed: logical operator type mismatch](https://github.com/duckdb/duckdb/issues/19455)
* [`#19498` Window function crash with `pdqsort_loop`](https://github.com/duckdb/duckdb/issues/19498)
* [`#19700` RLE select bug](https://github.com/duckdb/duckdb/issues/19700)

### Incorrect Results

* [`#17757` UUID Comparison in aggregation filter broken on Linux](https://github.com/duckdb/duckdb/issues/17757)
* [`#19327` Wrong result for `DISTINCT` and `LEFT JOIN`](https://github.com/duckdb/duckdb/issues/19327)
* [`#19377` Array with values shows null depending on query](https://github.com/duckdb/duckdb/issues/19377)

### Regressions

* [`#19333` DuckDB hangs when using `ATTACH IF NOT EXISTS` on subsequent connections to databases that have previously attached a database file](https://github.com/duckdb/duckdb/issues/19333)

### Storage

* [`#19424` Fix issue in MetadataManager triggered when doing concurrent reads while checkpointing](https://github.com/duckdb/duckdb/pull/19424)
* [`#19527` Ensure that DuckDB outputs the expected `STORAGE_VERSION`](https://github.com/duckdb/duckdb/pull/19527)
* [`#19543` Error when setting `force_compression = 'zstd'` in an in-memory environment database](https://github.com/duckdb/duckdb/pull/19543)

### Issues Discovered by the Fuzzer

* [`duckdb-fuzzer#3389`](https://github.com/duckdb/duckdb-fuzzer/issues/3389)
* [`duckdb-fuzzer#4208`](https://github.com/duckdb/duckdb-fuzzer/issues/4208)
* [`duckdb-fuzzer#4296`](https://github.com/duckdb/duckdb-fuzzer/issues/4296)
