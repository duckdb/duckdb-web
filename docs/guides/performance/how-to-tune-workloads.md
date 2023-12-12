---
layout: docu
title: Tuning Workloads
---

## Parallelism (Multi-Core Processing)

### The Effect of Row Groups on Parallelism

DuckDB parallelizes the workload based on _[row groups](/internals/storage#row-groups),_ i.e., groups of rows that are stored together at the storage level.
A row group in DuckDB's database format consists of max. 122,880 rows.
Parallelism starts at the level of row groups, therefore, for a query to run on _k_ threads, it needs to scan at least _k_ * 122,880 rows.

### Too Many Threads

Note that in certain cases DuckDB may launch _too many threads_ (e.g., due to HyperThreading), which can lead to slowdowns. In these cases, it’s worth manually limiting the number of threads using [`SET threads = X`](../../sql/pragmas#memory_limit-threads).

## Larger-Than-Memory Workloads (Out-of-Core Processing)

A key strength of DuckDB is support for larger-than-memory workloads, i.e., it is able to process data sets that are larger than the available system memory (also known as _out-of-core processing_).
It can also run queries where the intermediate results cannot fit into memory.
This section explains the prerequisites, scope, and known limitations of larger-than-memory processing in DuckDB.

### Prerequisites

Spilling to disk is automatically supported when connected to a [persistent database file](../../api/cli/overview#in-memory-vs-persistent-database).

When running in in-memory mode, DuckDB cannot use disk to offload data if it does not fit into main memory.
To enable offloading in the absence of a persistent database file, use the [`SET temp_directory` statement](../../sql/pragmas#temp_directory-for-spilling-data-to-disk):

```sql
SET temp_directory = '/path/to/temp.tmp'
```

### Operators

Some operators cannot output a single row until the last row of their input has been seen.
These are called _blocking operators_ as they require their entire input to be buffered,
and are the most memory-instensive operators in relational database systems.
The main blocking operators are the following:
* _sorting:_ [`ORDER BY`](../../sql/query_syntax/orderby),
* _grouping:_ [`GROUP BY`](../../sql/query_syntax/groupby),
* _windowing:_ [`OVER ... (PARTITION BY ... ORDER BY ...)`](../../sql/window_functions),
* _joining:_ [`JOIN`](../../sql/query_syntax/from#joins).

DuckDB supports larger-than-memory processing for all of these operators.

### Limitations

DuckDB strives to always complete workloads even if they are larger-than-memory.
That said, there are some limitations:

* If multiple blocking operators appear in the same query, DuckDB may still throw an out-of-memory exception due to the complex interplay of these operators.
* Currently, some [aggregate functions](../../sql/aggregates), such as `list()` and `string_agg()`, do not support offloading to disk.
* The `PIVOT` operation [internally uses the `list()` function](../../sql/statements/pivot#internals), therefore it is subject to the same limitation.

## Profiling

If your queries are not performing as well as expected, it’s worth studying their query plans:
* Use [`EXPLAIN`](../meta/explain) to print the physical query plan without running the query.
* Use [`EXPLAIN ANALYZE`](../meta/explain_analyze) to run and profile the query. This will show the CPU time that each step in the query takes. Note that due to multi-threading, adding up the individual times will be larger than the total query processing time.

Query plans can point to the root of performance issues. A few general directions:
* Avoid nested loop joins in favor or hash joins.
* A scan that does not include a filter pushdown for a filter condition that is later applied performs unnecessary IO. Try rewriting the query to apply a pushdown.
* Bad join orders where the cardinality of an operator explodes to billions of tuples should be avoided at all costs.

## Prepared Statements

[Prepared statements](../../sql/query_syntax/prepared_statements) can improve performance when running the same query many times, but with different parameters. When a statement is prepared, it completes several of the initial portions of the query execution process (parsing, planning, etc.) and caches their output. When it is executed, those steps can be skipped, improving performance. This is beneficial mostly for repeatedly running small queries (with a runtime of < 100ms) with different sets of parameters.

Note that it is not a primary design goal for DuckDB to quickly execute many small queries concurrently. Rather, it is optimized for running larger, less frequent queries.

## Querying Remote Files

DuckDB uses synchronous IO when reading remote files. This means that each DuckDB thread can make at most one HTTP request at a time. If a query must make many small requests over the network, increasing DuckDB's [`threads` setting](../../sql/pragmas#memory_limit-threads) to larger than the total number of CPU cores (approx. 2-5 times CPU cores) can improve parallelism and performance.

## Best Practices for Using Connections

DuckDB will perform best when reusing the same database connection many times. Disconnecting and reconnecting on every query will incur some overhead, which can reduce performance when running many small queries. DuckDB also caches some data and metadata in memory, and that cache is lost when the last open connection is closed. Frequently, a single connection will work best, but a connection pool may also be used. 

Using multiple connections can parallelize some operations, although it is typically not necessary. DuckDB does attempt to parallelize as much as possible within each individual query, but it is not possible to parallelize in all cases. Making multiple connections can process more operations concurrently. This can be more helpful if DuckDB is not CPU limited, but instead bottlenecked by another resource like network transfer speed.

## The `preserve_insertion_order` Option

When importing or exporting data sets that are much larger than the available memory, out of memory errors may occur. In these cases, it’s worth setting the [`preserve_insertion_order` configuration option](../../sql/configuration) to `false`:

```sql
SET preserve_insertion_order = false;
```

This allows the systems to re-order any results that do not contain `ORDER BY` clauses, potentially reducing memory usage.
