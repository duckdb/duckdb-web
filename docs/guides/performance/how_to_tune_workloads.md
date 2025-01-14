---
layout: docu
title: Tuning Workloads
redirect_from:
  - /docs/guides/performance/how-to-tune-workloads
---

## Parallelism (Multi-Core Processing)

### The Effect of Row Groups on Parallelism

DuckDB parallelizes the workload based on _[row groups]({% link docs/internals/storage.md %}#row-groups),_ i.e., groups of rows that are stored together at the storage level.
A row group in DuckDB's database format consists of max. 122,880 rows.
Parallelism starts at the level of row groups, therefore, for a query to run on _k_ threads, it needs to scan at least _k_ * 122,880 rows.

### Too Many Threads

Note that in certain cases DuckDB may launch _too many threads_ (e.g., due to HyperThreading), which can lead to slowdowns. In these cases, it’s worth manually limiting the number of threads using [`SET threads = X`]({% link docs/configuration/pragmas.md %}#threads).

## Larger-Than-Memory Workloads (Out-of-Core Processing)

A key strength of DuckDB is support for larger-than-memory workloads, i.e., it is able to process data sets that are larger than the available system memory (also known as _out-of-core processing_).
It can also run queries where the intermediate results cannot fit into memory.
This section explains the prerequisites, scope, and known limitations of larger-than-memory processing in DuckDB.

### Spilling to Disk

Larger-than-memory workloads are supported by spilling to disk.
With the default configuration, DuckDB creates the `⟨database_file_name⟩.tmp` temporary directory (in persistent mode) or the `.tmp` directory (in in-memory mode). This directory can be changed using the [`temp_directory` configuration option]({% link docs/configuration/pragmas.md %}#temp-directory-for-spilling-data-to-disk), e.g.:

```sql
SET temp_directory = '/path/to/temp_dir.tmp/';
```

### Blocking Operators

Some operators cannot output a single row until the last row of their input has been seen.
These are called _blocking operators_ as they require their entire input to be buffered,
and are the most memory-intensive operators in relational database systems.
The main blocking operators are the following:

* _grouping:_ [`GROUP BY`]({% link docs/sql/query_syntax/groupby.md %})
* _joining:_ [`JOIN`]({% link docs/sql/query_syntax/from.md %}#joins)
* _sorting:_ [`ORDER BY`]({% link docs/sql/query_syntax/orderby.md %})
* _windowing:_ [`OVER ... (PARTITION BY ... ORDER BY ...)`]({% link docs/sql/functions/window_functions.md %})

DuckDB supports larger-than-memory processing for all of these operators.

### Limitations

DuckDB strives to always complete workloads even if they are larger-than-memory.
That said, there are some limitations at the moment:

* If multiple blocking operators appear in the same query, DuckDB may still throw an out-of-memory exception due to the complex interplay of these operators.
* Some [aggregate functions]({% link docs/sql/functions/aggregates.md %}), such as `list()` and `string_agg()`, do not support offloading to disk.
* [Aggregate functions that use sorting]({% link docs/sql/functions/aggregates.md %}#order-by-clause-in-aggregate-functions) are holistic, i.e., they need all inputs before the aggregation can start. As DuckDB cannot yet offload some complex intermediate aggregate states to disk, these functions can cause an out-of-memory exception when run on large data sets.
* The `PIVOT` operation [internally uses the `list()` function]({% link docs/sql/statements/pivot.md %}#internals), therefore it is subject to the same limitation.

## Profiling

If your queries are not performing as well as expected, it’s worth studying their query plans:

* Use [`EXPLAIN`]({% link docs/guides/meta/explain.md %}) to print the physical query plan without running the query.
* Use [`EXPLAIN ANALYZE`]({% link docs/guides/meta/explain_analyze.md %}) to run and profile the query. This will show the CPU time that each step in the query takes. Note that due to multi-threading, adding up the individual times will be larger than the total query processing time.

Query plans can point to the root of performance issues. A few general directions:

* Avoid nested loop joins in favor of hash joins.
* A scan that does not include a filter pushdown for a filter condition that is later applied performs unnecessary IO. Try rewriting the query to apply a pushdown.
* Bad join orders where the cardinality of an operator explodes to billions of tuples should be avoided at all costs.

## Prepared Statements

[Prepared statements]({% link docs/sql/query_syntax/prepared_statements.md %}) can improve performance when running the same query many times, but with different parameters. When a statement is prepared, it completes several of the initial portions of the query execution process (parsing, planning, etc.) and caches their output. When it is executed, those steps can be skipped, improving performance. This is beneficial mostly for repeatedly running small queries (with a runtime of < 100ms) with different sets of parameters.

Note that it is not a primary design goal for DuckDB to quickly execute many small queries concurrently. Rather, it is optimized for running larger, less frequent queries.

## Querying Remote Files

DuckDB uses synchronous IO when reading remote files. This means that each DuckDB thread can make at most one HTTP request at a time. If a query must make many small requests over the network, increasing DuckDB's [`threads` setting]({% link docs/configuration/pragmas.md %}#threads) to larger than the total number of CPU cores (approx. 2-5 times CPU cores) can improve parallelism and performance.

### Avoid Reading Unnecessary Data

The main bottleneck in workloads reading remote files is likely to be the IO. This means that minimizing the unnecessarily read data can be highly beneficial.

Some basic SQL tricks can help with this:

* Avoid `SELECT *`. Instead, only select columns that are actually used. DuckDB will try to only download the data it actually needs.
* Apply filters on remote parquet files when possible. DuckDB can use these filters to reduce the amount of data that is scanned.
* Either [sort]({% link docs/sql/query_syntax/orderby.md %}) or [partition]({% link docs/data/partitioning/partitioned_writes.md %}) data by columns that are regularly used for filters: this increases the effectiveness of the filters in reducing IO.

To inspect how much remote data is transferred for a query, [`EXPLAIN ANALYZE`]({% link docs/guides/meta/explain_analyze.md %}) can be used to print out the total number of requests and total data transferred for queries on remote files.

### Avoid Reading Data More Than Once

DuckDB does not cache data from remote files automatically. This means that running a query on a remote file twice will download the required data twice. So if data needs to be accessed multiple times, storing it locally can make sense. To illustrate this, lets look at an example:

Consider the following queries:

```sql
SELECT col_a + col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;
SELECT col_a * col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;
```

These queries download the columns `col_a` and `col_b` from `s3://bucket/file.parquet` twice. Now consider the following queries:

```sql
CREATE TABLE local_copy_of_file AS
    SELECT col_a, col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;

SELECT col_a + col_b FROM local_copy_of_file;
SELECT col_a * col_b FROM local_copy_of_file;
```

Here DuckDB will first copy `col_a` and `col_b` from `s3://bucket/file.parquet` into a local table, and then query the local in-memory columns twice. Note also that the filter `WHERE col_a > 10` is also now applied only once.

An important side note needs to be made here though. The first two queries are fully streaming, with only a small memory footprint, whereas the second requires full materialization of columns `col_a` and `col_b`. This means that in some rare cases (e.g., with a high-speed network, but with very limited memory available) it could actually be beneficial to download the data twice.

## Best Practices for Using Connections

DuckDB will perform best when reusing the same database connection many times. Disconnecting and reconnecting on every query will incur some overhead, which can reduce performance when running many small queries. DuckDB also caches some data and metadata in memory, and that cache is lost when the last open connection is closed. Frequently, a single connection will work best, but a connection pool may also be used.

Using multiple connections can parallelize some operations, although it is typically not necessary. DuckDB does attempt to parallelize as much as possible within each individual query, but it is not possible to parallelize in all cases. Making multiple connections can process more operations concurrently. This can be more helpful if DuckDB is not CPU limited, but instead bottlenecked by another resource like network transfer speed.

## The `preserve_insertion_order` Option

When importing or exporting data sets (from/to the Parquet or CSV formats), which are much larger than the available memory, an out of memory error may occur:

```console
Out of Memory Error: failed to allocate data of size ... (.../... used)
```

In these cases, consider setting the [`preserve_insertion_order` configuration option]({% link docs/configuration/overview.md %}) to `false`:

```sql
SET preserve_insertion_order = false;
```

This allows the systems to re-order any results that do not contain `ORDER BY` clauses, potentially reducing memory usage.

## Persistent vs. In-Memory Tables

DuckDB supports [lightweight compression techniques]({% post_url 2022-10-28-lightweight-compression %}). Currently, these are only applied on persistent (on-disk) databases.

DuckDB does not compress its in-memory tables. The reason for this is that compression is performed during checkpointing, and in-memory tables are not checkpointed.

In some cases, this can result in counter-intuitive performance results where queries are faster on on-disk tables compared to in-memory ones. For example, Q1 of the [TPC-H workload]({% link docs/extensions/tpch.md %}) is faster when running on-disk compared to the in-memory mode:

```sql
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf = 30);
.timer on
PRAGMA tpch(1);
```

| Database setup      | Execution time |
|---------------------|---------------:|
| In-memory database  | 4.80 s         |
| Persistent database | 0.57 s         |
