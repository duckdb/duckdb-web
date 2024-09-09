---
layout: post
title: "Announcing DuckDB 1.1.0"
author: The DuckDB team
thumb: "/images/blog/thumbs/240909.svg"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 1.1.0, codenamed “Eatoni”."
---

To install the new version, please visit the [installation guide]({% link docs/installation/index.html %}).
For the release notes, see the [release page](https://github.com/duckdb/duckdb/releases/tag/v1.1.0).

> Some packages (R, Java) take a few extra days to release due to the reviews required in the release pipelines.

We are proud to release DuckDB 1.1.0, our first release since we released version 1.0.0 three months ago.
This release is codenamed “Eatoni” after the [Eaton's pintail (Anas eatoni)](https://en.wikipedia.org/wiki/Eaton%27s_pintail),
a dabbling duck that occurs only on two very remote island groups in the southern Indian Ocean.

## What's New in 1.1.0

There have been far too many changes to discuss them each in detail, but we would like to highlight several particularly exciting features!

Below is a summary of those new features with examples.

* [Breaking SQL Changes](#breaking-sql-changes)
* [Community Extensions](#community-extensions)
* [Friendly SQL](#friendly-sql)
    * [Unpacked Columns](#unpacked-columns)
    * [`query` and `query_table` Functions](#query-and-query_table-functions)
* [Performance](#performance)
    * [Dynamic Filter Pushdown from Joins](#dynamic-filter-pushdown-from-joins)
    * [Automatic CTE Materialization](#automatic-cte-materialization)
    * [Parallel Streaming Queries](#parallel-streaming-queries)
    * [Parallel Union By Name](#parallel-union-by-name)
    * [Nested ART Rework (Foreign Key Load Speed-Up)](#nested-art-rework-foreign-key-load-speed-up)
    * [Window Function Improvements](#window-function-improvements)
* [Spatial Features](#spatial-features)
    * [GeoParquet](#geoparquet)
    * [R-Tree](#r-tree)
* [Final Thoughts](#final-thoughts)

## Breaking SQL Changes

[**IEEE-754 semantics for division by zero.**](https://github.com/duckdb/duckdb/pull/13493) The [IEEE-754 floating point standard](https://en.wikipedia.org/wiki/IEEE_754) states that division by zero returns `inf`. Previously, DuckDB would return `NULL` when dividing by zero, also for floating point division. Starting with this release, DuckDB will return `inf` instead.

```sql
SELECT 1 / 0 AS division_by_zero;
```

```text
┌──────────────────┐
│ division_by_zero │
│      double      │
├──────────────────┤
│              inf │
└──────────────────┘
```

The `ieee_floating_point_ops` can be set to `false` to revert this behavior:

```sql
SET ieee_floating_point_ops = false;
SELECT 1 / 0 AS division_by_zero;
```

```text
┌──────────────────┐
│ division_by_zero │
│      double      │
├──────────────────┤
│             NULL │
└──────────────────┘
```

[**Error when scalar subquery returns multiple values.**](https://github.com/duckdb/duckdb/pull/13514) Scalar subqueries can only return a single value per input row. Previously, DuckDB would match SQLite's behavior and select an arbitrary row to return when multiple rows were returned. In practice this behavior often led to confusion. Starting with this release, an error is returned instead, matching the behavior of Postgres. The subquery can be wrapped with `ARRAY` to collect all of the results of the subquery in a list.

```sql
SELECT (SELECT unnest(range(10)));
```

```console
Invalid Input Error: More than one row returned by a subquery used as
an expression - scalar subqueries can only return a single row.
```

```sql
SELECT ARRAY(SELECT unnest(range(10))) AS subquery_result;
```

```text
┌────────────────────────────────┐
│        subquery_result         │
│            int64[]             │
├────────────────────────────────┤
│ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] │
└────────────────────────────────┘
```

The `scalar_subquery_error_on_multiple_rows` setting can be set to `false` to revert this behavior.

```sql
SET scalar_subquery_error_on_multiple_rows = false;
SELECT (SELECT unnest(range(10))) AS result;
```
```text
┌────────┐
│ result │
│ int64  │
├────────┤
│      0 │
└────────┘
```

## Community Extensions

Recently we introduced [Community Extensions]({% post_url 2024-07-05-community-extensions %}). Community extensions allow anyone to build extensions for DuckDB, that are then built and distributed by us. The [list of community extensions](https://community-extensions.duckdb.org/list_of_extensions.html) has been growing since then.

In this release, we have been working towards making community extensions easier to build and produce. This release includes a new method of registering extensions [using the C API](https://github.com/duckdb/duckdb/pull/12682) in addition to a lot of extensions to the C API allowing [scalar functions](https://github.com/duckdb/duckdb/pull/11786), [aggregate functions](https://github.com/duckdb/duckdb/pull/13229) and [custom types](https://github.com/duckdb/duckdb/pull/13499) to be defined. These changes will enable building extensions against a stable API, that are smaller in size, that will work across different DuckDB versions. In addition, these changes will enable building extensions in other programming languages in the future.

## Friendly SQL

[**Histogram.**](https://github.com/duckdb/duckdb/pull/12590) This version introduces the `histogram` function that can be used to compute histograms over columns of a dataset. The histogram function works for columns of any type, and allows for various different binning strategies and a custom amount of bins.

```sql
FROM histogram(
    'https://blobs.duckdb.org/data/ontime.parquet',
    UniqueCarrier,
    bin_count := 5
);
```

```text
┌────────────────┬────────┬──────────────────────────────────────────────────────────────────────────────────┐
│      bin       │ count  │                                       bar                                        │
│    varchar     │ uint64 │                                     varchar                                      │
├────────────────┼────────┼──────────────────────────────────────────────────────────────────────────────────┤
│ AA             │ 677215 │ ██████████████████████████████████████████████████████▏                          │
│ DL             │ 696931 │ ███████████████████████████████████████████████████████▊                         │
│ OO             │ 521956 │ █████████████████████████████████████████▊                                       │
│ UA             │ 435757 │ ██████████████████████████████████▉                                              │
│ WN             │ 999114 │ ████████████████████████████████████████████████████████████████████████████████ │
│ (other values) │ 945484 │ ███████████████████████████████████████████████████████████████████████████▋     │
└────────────────┴────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

[**SQL variables.**](https://github.com/duckdb/duckdb/pull/13084) This release introduces support for variables that can be defined in SQL. Variables can hold a single value of any type – including nested types like lists or structs. Variables can be set as literals, or from scalar subqueries.

The value stored within variables can be read using `getvariable`. When used in a query, `getvariable` is treated as a literal during query planning and optimization. This allows variables to be used in places where we normally cannot read values from within tables, for example, when specifying which CSV files to read:

```sql
SET VARIABLE list_of_files = (SELECT LIST(file) FROM csv_files);
SELECT * FROM read_csv(getvariable('list_of_files'), filename := true);
```

```text
┌───────┬───────────┐
│   a   │ filename  │
│ int64 │  varchar  │
├───────┼───────────┤
│    42 │ test.csv  │
│    84 │ test2.csv │
└───────┴───────────┘
```

### Unpacked Columns

The [`COLUMNS` expression]({% link docs/sql/expressions/star.md %}#columns-expression) allows users to write dynamic SQL over a set of columns without needing to explicitly list the columns in the SQL string. Instead, the columns can be selected through either a regex or computed with a [lambda function]({% post_url 2024-08-08-friendly-lists-and-their-buddies-the-lambdas %}).

This release expands this capability by [allowing the `COLUMNS` expression to be *unpacked* into a function](https://github.com/duckdb/duckdb/pull/11872).
This is especially useful when combined with nested functions like `struct_pack` or `list_value`.

```sql
CREATE TABLE many_measurements(
    id INTEGER, m1 INTEGER, m2 INTEGER, m3 INTEGER
);
INSERT INTO many_measurements VALUES (1, 10, 100, 20);

SELECT id, struct_pack(*COLUMNS('m\d')) AS measurements
FROM many_measurements;
```

```text
┌───────┬────────────────────────────────────────────┐
│  id   │                measurements                │
│ int32 │ struct(m1 integer, m2 integer, m3 integer) │
├───────┼────────────────────────────────────────────┤
│     1 │ {'m1': 10, 'm2': 100, 'm3': 20}            │
└───────┴────────────────────────────────────────────┘
```

### `query` and `query_table` Functions

The [`query` and `query_table` functions](https://github.com/duckdb/duckdb/pull/10586) take a string literal, and convert it into a `SELECT` subquery or a table reference. Note that these functions can only take literal strings. As such, they are not as powerful (or dangerous) as a generic `eval`.

These functions are conceptually simple, but enable powerful and more dynamic SQL. For example, they allow passing in a table name as a prepared statement parameter:

```sql
CREATE TABLE my_table(i INT);
INSERT INTO my_table VALUES (42);

PREPARE select_from_table AS SELECT * FROM query_table($1);
EXECUTE select_from_table('my_table');
```

```text
┌───────┐
│   i   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

When combined with the `COLUMNS` expression, we can write very generic SQL-only macros. For example, below is a custom version of `SUMMARIZE` that computes the `min` and `max` of every column in a table:

```sql
CREATE OR REPLACE MACRO my_summarize(table_name) AS TABLE
SELECT
    unnest([*COLUMNS('alias_.*')]) AS column_name,
    unnest([*COLUMNS('min_.*')]) AS min_value,
    unnest([*COLUMNS('max_.*')]) AS max_value
FROM (
    SELECT
        any_value(alias(COLUMNS(*))) AS "alias_\0",
        min(COLUMNS(*))::VARCHAR AS "min_\0",
        max(COLUMNS(*))::VARCHAR AS "max_\0"
    FROM query_table(table_name::VARCHAR)
);

SELECT *
FROM my_summarize('https://blobs.duckdb.org/data/ontime.parquet')
LIMIT 3;
```

```text
┌─────────────┬───────────┬───────────┐
│ column_name │ min_value │ max_value │
│   varchar   │  varchar  │  varchar  │
├─────────────┼───────────┼───────────┤
│ year        │ 2017      │ 2017      │
│ quarter     │ 1         │ 3         │
│ month       │ 1         │ 9         │
└─────────────┴───────────┴───────────┘
```

## Performance

### Dynamic Filter Pushdown from Joins

This release adds a *very cool* optimization for joins: DuckDB now [automatically creates filters](https://github.com/duckdb/duckdb/pull/12908) for the larger table in the join during execution. Say we are joining two tables `A` and `B`. `A` has 100 rows, and `B` has one million rows. We are joining on a shared key `i`. If there were any filter on `i`, DuckDB would already push that filter into the scan, greatly reducing the cost to complete the query. But we are now filtering on another column from `A`, namely `j`:

```sql
CREATE TABLE A AS SELECT range i, range j FROM range(100);
CREATE TABLE B AS SELECT a.range i FROM range(100) a, range(10_000) b;
SELECT count(*) FROM A JOIN B USING (i) WHERE j > 90;
```

DuckDB will execute this join by building a hash table on the smaller table A, and then probe said hash table with the contents of B. DuckDB will now observe the values of i during construction of the hash table on A. It will then create a min-max range filter of those values of i and then *automatically* apply that filter to the values of i in B! That way, we early remove (in this case) 90% of data from the large table before even looking at the hash table. In this example, this leads to a roughly 10× improvement in query performance. The optimization can also be observed in the output of `EXPLAIN ANALYZE`.

### Automatic CTE Materialization

Common Table Expressions (CTE) are a convenient way to break up complex queries into manageable pieces without endless nesting of subqueries. Here is a small example for a CTE:

```sql
WITH my_cte AS (SELECT range AS i FROM range(10))
SELECT i FROM my_cte WHERE i > 5;
```

Sometimes, the same CTE is referenced multiple times in the same query. Previously, the CTE would be “copied” wherever it appeared. This creates a potential performance problem: if computing the CTE is computationally expensive, it would be better to cache (“materialize”) its results instead of computing the result multiple times in different places within the same query. However, different filter conditions might apply for different instantiations of the CTE, which could drastically reduce their computation cost. A classical no-win scenario in databases. It was [already possible]({% link docs/sql/query_syntax/with.md %}) to explicitly mark a CTE as materialized using the `MATERIALIZED` keyword, but that required manual intervention.

This release adds a feature where DuckDB [automatically decides](https://github.com/duckdb/duckdb/pull/12290) whether a CTE result should be materialized or not using a heuristic. The heuristic currently is that if the CTE performs aggregation and is queried more than once, it should be materialized. We plan to expand that heuristic in the future.

### Parallel Streaming Queries

DuckDB has two different methods for fetching results: *materialized* results and *streaming* results. Materialized results fetch all of the data that is present in a result at once, and return it. Streaming results instead allow iterating over the data in incremental steps. Streaming results are critical when working with large result sets as they do not require the entire result set to fit in memory. However, in previous releases, the final streaming phase was limited to a single thread.

Parallelism is critical for obtaining good query performance on modern hardware, and this release adds support for [parallel streaming of query results](https://github.com/duckdb/duckdb/pull/11494). The system will use all available threads to fill up a query result buffer of a limited size (a few megabytes). When data is consumed from the result buffer, the threads will restart and start filling up the buffer again. The size of the buffer can be configured through the `streaming_buffer_size` parameter.

Below is a small benchmark using [`ontime.parquet`](https://blobs.duckdb.org/data/ontime.parquet) to illustrate the performance benefits that can be obtained using the Python streaming result interface:

```python
import duckdb
duckdb.sql("SELECT * FROM 'ontime.parquet' WHERE flightnum = 6805;").fetchone()
```

| v1.0   | v1.1   |
|-------:|-------:|
| 1.17 s | 0.12 s |

### Parallel Union By Name

The `union_by_name` parameter allows combination of – for example – CSV files that have the same columns in them but not in the same order. This release [adds support for parallelism](https://github.com/duckdb/duckdb/pull/12957) when using `union_by_name`. This greatly improves reading performance when using the union by name feature on multiple files.

### Nested ART Rework (Foreign Key Load Speed-Up)

We have [greatly improved](https://github.com/duckdb/duckdb/pull/13373) index insertion and deletion performance for foreign keys. Normally, we directly inline row identifiers into the tree structure. However, this is impossible for indexes that contain a lot of duplicates, as is the case with foreign keys. Instead, we now actually create another index entry for each key that is itself another “recursive” index tree in its own right. That way, we can achieve good insertion and deletion performance inside index entries. The performance results of this change are drastic, consider the following example where a has 100 rows and b has one million rows that all reference a:

```sql
CREATE TABLE a (i INTEGER, PRIMARY KEY (i));
CREATE TABLE b (i INTEGER, FOREIGN KEY (i) REFERENCES a(i));

INSERT INTO a FROM range(100);
INSERT INTO b SELECT a.range FROM range(100) a, range(10_000) b;
```

On the previous version, this would take ca. 10s on a MacBook to complete. It now takes 0.2s thanks to the new index structure, a ca. 50x improvement!

### Window Function Improvements

Window functions see a lot of use in DuckDB, which is why we are continuously improving performance of executing Window functions over large datasets.

The [`DISTINCT`](https://github.com/duckdb/duckdb/pull/12311) and [`FILTER`](https://github.com/duckdb/duckdb/pull/12250) window function modifiers can now be executed in streaming mode. Streaming mode means that the input data for the operator does not need to be completely collected and buffered before the operator can execute. For large intermediate results, this can have a very large performance impact. For example, the following query will now use the streaming window operator:

```sql
SELECT
    sum(DISTINCT i)
        FILTER (i % 3 = 0)
        OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
FROM range(10) tbl(i);
```

We have [also implemented streaming mode](https://github.com/duckdb/duckdb/pull/12685) for positive `lead` offsets.

We can now [push filters on columns through window functions that are partitioned by the same column](https://github.com/duckdb/duckdb/pull/10932). For example, consider the following scenario:

```sql
CREATE TABLE tbl2 AS SELECT range i FROM range(10);
SELECT i
FROM (SELECT i, SUM(i) OVER (PARTITION BY i) FROM tbl)
WHERE i > 5;
```

Previously, the filter on `i` could not be pushed into the scan on `tbl`. But we now recognize that pushing this filter “through” the window is safe and the optimizer will do so. This can be verified through `EXPLAIN`:

```text
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
              …
┌─────────────┴─────────────┐
│           WINDOW          │
│    ────────────────────   │
│        Projections:       │
│ sum(i) OVER (PARTITION BY │
│             i)            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         SEQ_SCAN          │
│    ────────────────────   │
│            tbl            │
│                           │
│       Projections: i      │
│                           │
│          Filters:         │
│   i>5 AND i IS NOT NULL   │
│                           │
│          ~2 Rows          │
└───────────────────────────┘
```

The blocking (non-streaming) version of the window operator [now processes input data in parallel](https://github.com/duckdb/duckdb/pull/12907). This greatly reduces the footprint of the window operator.

See also [Richard's talk on the topic](https://www.youtube.com/watch?v=QubE0u8Kq7Y&list=PLzIMXBizEZjhbacz4PWGuCUSxizmLei8Y&index=8) at [DuckCon #5]({% post_url 2024-08-15-duckcon5 %}) in Seattle a few weeks ago.

## Spatial Features

### GeoParquet

GeoParquet is an extension format of the ubiquitous Parquet format that standardizes how to encode vector geometries and their metadata in Parquet files. This can be used to store geographic data sets in Parquet files efficiently. When the [`spatial` extension]({% link docs/extensions/spatial.md %}) is installed and loaded, reading from a GeoParquet file through DuckDB's normal Parquet reader will now [automatically convert geometry columns to the `GEOMETRY` type](https://github.com/duckdb/duckdb/pull/12503), for example:

```sql
INSTALL spatial;
LOAD spatial;

FROM 'https://blobs.duckdb.org/data/geoparquet-example.parquet'
SELECT GEOMETRY g
LIMIT 10;
```

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                       g                                                        │
│                                                    geometry                                                    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ MULTIPOLYGON (((180 -16.067132663642447, 180 -16.555216566639196, 179.36414266196414 -16.801354076946883, 17…  │
│ POLYGON ((33.90371119710453 -0.95, 34.07261999999997 -1.059819999999945, 37.69868999999994 -3.09698999999994…  │
│ POLYGON ((-8.665589565454809 27.656425889592356, -8.665124477564191 27.589479071558227, -8.684399786809053 2…  │
│ MULTIPOLYGON (((-122.84000000000003 49.000000000000114, -122.97421000000001 49.00253777777778, -124.91024 49…  │
│ MULTIPOLYGON (((-122.84000000000003 49.000000000000114, -120 49.000000000000114, -117.03121 49, -116.04818 4…  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### R-Tree

The spatial extension accompanying this release also implements initial support for creating “R-Tree” spatial indexes. An R-Tree index stores the approximate bounding boxes of each geometry in a column into an auxiliary hierarchical tree-like data structure where every “node” contains a bounding box covering all of its child nodes. This makes it really fast to check what geometries intersect a specific region of interest as you can quickly prune out a lot of candidates by recursively moving down the tree.

Support for spatial indexes has been a long-requested feature on the spatial extension roadmap, and now that we have one, a ton of new use cases and directions for further development are opening up. However, as of now they are only used to accelerate simple  queries that select from a table with a filter using one out of a hardcoded set of spatial predicate functions applied on an indexed geometry column and a constant geometry. This makes R-Tree indexes useful when you have a very large table of geometries that you repeatedly query, but you don't want to perform a full table scan when you're only interested in the rows whose geometries intersect or fit within a certain region anyway. Here is an example where we can see that the `RTREE_INDEX_SCAN` operator is used:

```sql
INSTALL spatial;
LOAD spatial;

-- Create a table with 10_000_000 random points
CREATE TABLE t1 AS SELECT point::GEOMETRY AS geom
FROM st_generatepoints(
        {min_x: 0, min_y: 0, max_x: 10_000, max_y: 10_000}::BOX_2D,
        10_000_000,
        1337
    );

-- Create an index on the table
CREATE INDEX my_idx ON t1 USING RTREE (geom);

-- Perform a query with a "spatial predicate" on the indexed geometry
-- column. Note how the second argument in this case,
-- the ST_MakeEnvelope call is a "constant"
SELECT count(*)
FROM t1
WHERE ST_Within(geom, ST_MakeEnvelope(450, 450, 650, 650));
```

```text
3986
```

R-Tree indexes mostly share the same feature-set as DuckDB's built-in ART index. They are buffer-managed, persistent, lazily-loaded from disk and support inserts, updates and deletes to the base table. Although they can not be used to enforce constraints.

## Final Thoughts

These were a few highlights – but there are many more features and improvements in this release. The full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.1.0).

We would like to thank again our amazing community for using DuckDB, building cool projects on DuckDB and improving DuckDB by providing us feedback. Your contributions truly mean a lot!
