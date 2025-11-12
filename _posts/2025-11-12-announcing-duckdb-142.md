---
layout: post
title: "Announcing DuckDB 1.4.2 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-2-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-2-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.2, the second patch release of our LTS edition. The new release ships several bugfixes and performance optimizations as well as some new Iceberg and CLI features."
tags: ["release"]
---

In this blog post, we highlight a few important fixes and convenience improvements in DuckDB v1.4.2, the second bugfix release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).

To install the new version, please visit the [installation page]({% link install/index.html %}). Note that it can take a few hours to days for some client libraries (e.g., Go, R, Rust, Java) to be released to the extra changes and review rounds required.

In this blog post, we will highlight a few important features and fixes. To see the complete list of updates, please consult the [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.2).

## Features and Improvements

### Iceberg Improvements

Similarly to the [v1.4.1 release blog post]({% post_url 2025-10-07-announcing-duckdb-141 %}#iceberg-improvement), we can start with some good news for our Iceberg users: DuckDB v1.4.2 ships a number of improvements for the [`iceberg` extension]({% link docs/stable/core_extensions/iceberg/overview.md %}). Insert, update, and delete statements are all supported now:

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

We will publish a separate blog post on these improvements shortly. Stay tuned!

### Dynamic Prompts in the CLI

DuckDB v1.4.2 introduces dynamic prompts for the CLI. By default, these show the database and schema that you are currently connected to:

```batch
duckdb
```

```sql
«memory» D ATTACH 'my_database.duckdb';
«memory» D USE my_database;
«my_database» D CREATE SCHEMA my_schema;
«my_database» D USE my_schema;
«my_database.my_schema» D ...
```

The prompt also works when attaching to data lakes:

```sql
«memory» D ATTACH 'https://blobs.duckdb.org/datalake/tpch-sf1.ducklake'
             AS tpch_sf1;
«memory» D USE tpch_sf1;
«tpch_sf1» D ...
```

These prompts can be configured using bracket codes to have a maximum length, run a custom query, use different colors, etc.
See details in the [pull request](https://github.com/duckdb/duckdb/pull/19579).

### Logger Improvements

#### Time HTTP requests

The logger can now log time of HTTP requests ([`#19691`](https://github.com/duckdb/duckdb/pull/19691)):

```sql
CALL enable_logging('HTTP');
FROM 'https://blobs.duckdb.org/train-services-2025-10.csv';
SELECT request.type, request.url, request.start_time, request.duration_ms
FROM duckdb_logs_parsed('HTTP');
```

```text
TODO
```

#### Access the Profiler's Output from the Logger

If both profiler and logger are enabled, then you can [access profiler output also via logger (`#19572`)](https://github.com/duckdb/duckdb/pull/19572).
This means that you can log information such as the execution time of queries:

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

### Performance Improvements

DuckDB v1.4.2 also ships some small performance improvements:

* [`#19477` DuckDB now buffers WAL index deletes, not only appends](https://github.com/duckdb/duckdb/pull/19477)
* [`#19644` Detaching from a database is now faster](https://github.com/duckdb/duckdb/pull/19644)

## Fixes

We fixed several crashes, internal errors, incorrect results and regressions.
Additionally, we fixed several issues reported by our [fuzzer](https://github.com/duckdb/duckdb-fuzzer/).

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
