---
layout: post
title: "Maximizing Your Delta Scan Performance"
author: "Sam Ansmink"
thumb: "/images/blog/thumbs/delta-lake-part-2.png"
image: "/images/blog/thumbs/delta-lake-part-2.png"
excerpt: "We released a new version of the [Delta extension](/docs/stable/extensions/delta), which includes several new features and performance improvements. In this blog post, we’ll put the Delta extension through its paces with some benchmarks and take a deep dive into some of the new performance-related features."
tags: ["extensions"]
---

## Overview

In our [previous]({% post_url 2024-06-10-delta %}) post, we talked about what the Delta Lake table format is all about, and how DuckDB’s Delta extension leverages the [Delta Kernel](https://github.com/delta-io/delta-kernel-rs) library to offer native support. In this blog post, we will focus on how to get the most performance out of reading Delta tables from DuckDB. We’ll start with a small recap of Delta, then demonstrate the performance gains that were made over the past few releases. Finally, we demonstrate three key features available in the latest Delta release that will ensure you get the most out of your Delta reading performance: metadata caching, file skipping and partition information pushdown.

## The Delta Open Table Format

Let’s start off with a small recap of Delta to get back up to speed. [Delta Lake](https://delta.io/) is an [Open Table Format](https://delta.io/blog/open-table-formats/) similar to [Apache Iceberg](https://iceberg.apache.org/) and [Apache Hudi](https://hudi.apache.org/). Open Table Formats are best understood as “a collection of data and metadata files” that aim to provide the flexibility of data lakes while providing some of the consistency guarantees of traditional data warehouses. In the case of Delta, the format consists of Parquet files for data and a mix of Parquet, JSON and binary files for metadata. Besides providing an improved level of consistency, the additional metadata provided by Open Table Formats allows various types of performance optimizations through things like column statistics and file skipping. For a more in-depth explanation, we refer to the [previous Delta blog post]({% post_url 2024-06-10-delta %}).

## The Delta Extension

DuckDB natively supports reading Delta Tables through the [Delta extension]({% link docs/stable/extensions/delta.md %}). This extension is one of the [core DuckDB extensions]({% link docs/stable/extensions/core_extensions.md %}) with >70k weekly downloads. Using this extension to read from a Delta Table is really simple. Since DuckDB v1.2.0, the Delta extension will be automatically installed upon first use and loaded when invoking the `delta_scan` function.

So for example, to read a local Delta table, simply open any DuckDB client and run:

```sql
SELECT * FROM delta_scan('./⟨path_to_your_delta_table⟩');
```

Is your Delta table on someone else’s machine, perhaps in AWS? DuckDB can also query straight from S3! To have DuckDB automatically load your AWS credentials and query a remote Delta table, run:

```sql
CREATE SECRET (TYPE s3, PROVIDER credential_chain);
SELECT * FROM delta_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩');
```

For other cloud providers such as Azure or Google Cloud, check the [extension’s documentation page]({% link docs/stable/extensions/delta.md %}#usage).

## Delta Extension v0.1.0 vs. v0.3.0 Performance Improvements

While the first release (v0.1.0) of the Delta extension already came with various performance-related features such as projection pushdown and constant filter pushdown, the features added since then have massively improved the performance of `delta_scan`. To illustrate this, our first benchmark will use the industry standard [TPC-DS]({% link docs/stable/extensions/tpcds.md %}) benchmark with the scale factor 1 data set (SF1).

### Benchmark Setup

For this benchmark, we started up an [AWS c6id.4xlarge instance](https://instances.vantage.sh/aws/ec2/c6id.4xlarge) (16 vCPUs, 32 GB RAM) and wrote the TPC-DS SF1 dataset to an S3 bucket in the same region (eu-west-1) using [PySpark](https://github.com/duckdb/duckdb-delta/blob/main/scripts/generate_test_data.py).
Each benchmark is run a total of 6 times with the result being the median runtime of the last 5 runs with the first being considered a cold run. The aggregated results are shown in the following table.

|    Result    | Total runtime | Min runtime | Max runtime | Median runtime | Queries timed out |
|--------------|--------------:|------------:|------------:|---------------:|------------------:|
| Delta v0.1.0 | 444.76        | 0.48        | 21.31       | 3.63           | 4                 |
| Delta v0.3.0 | 151.06        | 0.46        | 6.15        | 1.22           | 0                 |

The detailed results of the benchmark are shown in the foldout:
<details markdown='1'>
<summary markdown='span'>
    Detailed TPC-DS SF1 benchmark results, delta extension v0.1.0 vs. v0.3.0
</summary>

<div align="center">
    <a href="/images/blog/delta-performance-fig1.svg"><img src="/images/blog/delta-performance-fig1.svg"
    alt="Detailed TPC-DS SF1 benchmark results, delta extension v0.1.0 vs. v0.3.0"
    width="900"
    /></a></div>
<div align="center"></div>
</details>

### Analysis

We can see from the results that there has been a significant performance improvement all around. In v0.1.0, 4 out of 99 queries hit the benchmark timeout of 30 sec and were excluded from the results. In v0.3.0, all 99 queries completed well within the timeout. Comparing total runtimes (excluding the queries that timed out for v0.1.0) we find a speedup of more than 3×!

Now, without going into too much detail, an important part of the speedup here can be attributed to the **cardinality information propagation** that was added in [PR #77](https://github.com/duckdb/duckdb-delta/pull/77). Having accurate cardinality estimation is essential for DuckDB’s [query optimizer]({% post_url 2024-11-14-optimizers %}) to work well and produce efficient query plans. Specifically, DuckDB’s Join Optimizer uses the cardinality estimates to change the order in which joins are performed. The join order can massively impact the cardinality of the intermediate tuples, which has a big impact on query performance. Especially in workloads like the TPC-DS benchmark, which has many queries that contain a lot of joins, the Join Order Optimizer plays a crucial role. For (a lot) more details, check out [this thesis](https://blobs.duckdb.org/papers/tom-ebergen-msc-thesis-join-order-optimization-with-almost-no-statistics.pdf).

## Further Optimizations

### Attaching Delta Tables

Besides the general performance improvements like cardinality information propagation, several performance-related features have been added to the Delta extension as well. One of those is the ability to attach Delta tables. Using `ATTACH` to query a Delta table has multiple advantages. For starters, by using `ATTACH`, your queries can look a little cleaner when querying the same table multiple times since you don’t have to repeat the full Delta table path every time it is queried. More importantly, though, using `ATTACH` will allow DuckDB to cache/reuse certain parts of the Delta metadata, which can improve query performance. To attach the local Delta table, run:

```sql
ATTACH './⟨path_to_your_delta_table⟩' AS ⟨your_table⟩ (TYPE delta);
```

After attaching the Delta table, you can query the table just by using the alias:

```sql
SELECT * FROM ⟨your_table⟩;
```

By default, DuckDB will automatically cache Delta metadata within the same transaction. That means if a Delta table is scanned multiple times in that transaction, DuckDB can reuse parts of the Delta metadata between the different scans. For example, the following query will only read the Delta metadata once:

```sql
SELECT * FROM t1
UNION ALL
SELECT * FROM t1;
```

For even more performance improvements, DuckDB also supports **persisting this cached Delta metadata _between_ different queries**. To do this, the Delta table can be attached using the `PIN_SNAPSHOT` option. With this option enabled, subsequent queries can reuse the metadata such as in the following code block:

```sql
ATTACH 's3://⟨your_bucket⟩/⟨your_delta_table⟩' AS t2 (
    TYPE delta,
    PIN_SNAPSHOT
);

-- First scan (metadata not yet cached)
SELECT * FROM t1;

-- Second scan (metadata is now cached)
SELECT * FROM t2;
```

Metadata caching can have a significant performance impact, especially in situations where the data is relatively small and the latency high. To illustrate this, we will rerun our TPC-DS experiment to compare three different ways of scanning the Delta table: using `delta_scan`, using `ATTACH`, and using `ATTACH ... (PIN_SNAPSHOT)`. The rest of the benchmark setup is identical to the one in the previous section.

|        result             | total runtime | min runtime | max runtime | median runtime |
|---------------------------|--------------:|------------:|------------:|---------------:|
| `delta_scan`              | 151.06        | 0.46        | 6.15        | 1.22           |
| `ATTACH`                  | 134.26        | 0.43        | 4.28        | 1.19           |
| `ATTACH` (`PIN_SNAPSHOT`) | 102.80        | 0.36        | 4.04        | 0.87           |

The detailed results of the benchmark are shown in the foldout:
<details markdown='1'>
<summary markdown='span'>
    Detailed TPC-DS SF1 benchmark results with different configurations
</summary>

<div align="center">
    <a href="/images/blog/delta-performance-fig2.svg"><img src="/images/blog/delta-performance-fig2.svg"
    alt="Detailed TPC-DS SF1 benchmark results with different configurations"
    width="900"
    /></a></div>
<div align="center"></div>
</details>

The results show that for many TPC-DS queries, using `ATTACH` instead of `delta_scan` can already slightly improve performance for several queries, with overall runtime seeing a 1.13× speedup. When the metadata is fully in cache due to `PIN_SNAPSHOT`, we see an even greater speedup of 1.47×. This, however, comes at the tradeoff of missing any updates to the table that occur after the `ATTACH` statement.

A keen eye looking at the full results will also spot a few cases where the `ATTACH` results are actually slightly worse than the results with raw `delta_scan`. This is something we will explain in the [section on the pushdown / `ATTACH` interplay](#a-note-on-pushdown--attach-performance-interplay).

### File Skipping

Another key performance feature of scanning Delta tables is file skipping. As explained in the introduction, Delta tables contain metadata that contains all sorts of statistics of the data files of the table. These statistics can be used by engines like DuckDB to decide which Parquet files need to be scanned and which ones can be skipped altogether. File skipping is something that is done automatically by DuckDB. File skipping will work for both constant filters and dynamic filters (filters that are calculated during query execution):

```sql
-- constant filter
FROM delta_scan('...')
WHERE col_a > 'some_value';
-- dynamic filter
FROM delta_scan('...')
WHERE col_a > (SELECT max(col_z) FROM other_tbl);
```

In the previous benchmarks, file skipping has only a very limited effect. The overall data is simply not big enough and many queries actually touch large parts of the data anyway.  However, when only a relatively small part of the data is touched in a query, file skipping can have a huge impact on performance. To demonstrate this, we will first generate some test data. We’ll use the same [PySpark-based](https://github.com/duckdb/duckdb-delta/blob/026345b9cf9092e3dd5ae42cc501ec8ed45ca09b/scripts/data_generator/generate_test_data.py) test data generation script as before.

The table has 100 million rows and has a very basic schema with an incrementing `id` column of `INTEGER` type and a `value` column of `VARCHAR` type. If we query the data using DuckDB we will see something like:

```sql
FROM delta_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩');
```

```text
┌──────────┬──────────────┐
│    id    │    value     │
│  int64   │   varchar    │
├──────────┼──────────────┤
│ 49950000 │ val-49950000 │
│ 49950001 │ val-49950001 │
│ 49950002 │ val-49950002 │
│ 49950003 │ val-49950003 │
│      ·   │     ·        │
│      ·   │     ·        │
│      ·   │     ·        │
│    49996 │ val-49996    │
│    49997 │ val-49997    │
│    49998 │ val-49998    │
│    49999 │ val-49999    │
├──────────┴──────────────┤
│     100000000 rows      │
│        (8 shown)        │
└─────────────────────────┘
```

Now, let’s say we are only interested in a specific range of `id`s: maybe we only want `id`s below 100. We will now construct two queries.

For the first query, we will directly read all the parquet files stored in the table using a [glob pattern]({% link docs/stable/data/multiple_files/overview.md %}#multi-file-reads-and-globs):

```sql
FROM parquet_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩/*.parquet')
WHERE id < 100;
```

> We are doing this for illustrative purposes to show us the benefits of file skipping, scanning the raw Parquet files in a Delta table like this only works here because we have no updates, deletes or checkpoints in this table.

For the second query, we directly scan the table using the `delta_scan` table function, selecting only the `id`s we are interested in using a `WHERE` clause:

```sql
FROM delta_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩')
WHERE id < 100;
```

Now when running these queries from a c6id.4xlarge AWS instance on the S3 bucket in the same region, we can see that they perform wildly differently. The `delta_scan` only requires ≈0.5 seconds to complete, whereas the `parquet_scan` takes ≈17 seconds. So what’s going on here exactly?

We can use DuckDB’s `EXPLAIN ANALYZE` statement to get more details here. Let’s start by analyzing the `parquet_scan`:

```sql
EXPLAIN ANALYZE
FROM parquet_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩/*.parquet')
WHERE id < 100;
```

```text
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 17.08s              ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
             ...
┌─────────────┴─────────────┐
│         TABLE_SCAN        │
│    ────────────────────   │
│         Function:         │
│        PARQUET_SCAN       │
│                           │
│        Projections:       │
│             id            │
│           value           │
│                           │
│      Filters: id<100      │
│                           │
│          100 Rows         │
│         (262.39s)         │
└───────────────────────────┘
```

We can see in the `EXPLAIN ANALYZE` output that our filter was properly pushed down, and the scan correctly only produced 100 rows. This all seems fine, right? Well, let’s compare it with the output of `EXPLAIN ANALYZE` for the `delta_scan`:

```sql
EXPLAIN ANALYZE
FROM delta_scan('s3://⟨your_bucket⟩/⟨your_delta_table⟩');
```

```text
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.615s              ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
             ...
┌─────────────┴─────────────┐
│         TABLE_SCAN        │
│    ────────────────────   │
│        Projections:       │
│             id            │
│           value           │
│                           │
│      Filters: id<100      │
│    File Filters: id<100   │
│                           │
│      Scanning Files:      │
│           1/2000          │
│                           │
│          100 Rows         │
│          (0.06s)          │
└───────────────────────────┘
```

For the `delta_scan` function’s `EXPLAIN ANALYZE` output, we can see two new fields: `File Filters`  and `Scanning Files`. This shows us clearly what’s going on. The `id<100` predicate is now used for two things: it’s pushed down into the scans on the individual Parquet files, just like the `parquet_scan`, but it also shows up as a file filter, which is used to reduce the list of files to be scanned altogether! This leads to a **2,000× reduction** of the amount of Parquet metadata to be read, which results in a huge performance boost.

### Partition Information Pushdown

The final DuckDB Delta performance feature is partition information pushdown. Partition information pushdown and the partition-aware aggregation operator are relatively [new](https://github.com/duckdb/duckdb/pull/14329) features introduced in DuckDB v1.2.0. In the v0.3.0 release of the Delta extension this feature was also added, which means that DuckDB can now use the partitioning information to create query plans that can utilize the fact that the data scanned is already partitioned.
To show the performance benefit of partition information, we will, _surprise,_ run another benchmark! This time, we chose the [TPC-H dataset]({% link docs/stable/extensions/tpch.md %}) at scale factor 10 and ran the experiment on a 32 GB MacBook Pro M1 Max. We partitioned the `lineitem` table by the `l_returnflag` and `l_linestatus` columns. We then run [Q1](https://github.com/duckdb/duckdb/blob/v1.2.1/extension/tpch/dbgen/queries/q01.sql) which looks roughly like this:

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) AS sum_qty,
    ...
FROM
    lineitem
    ...
GROUP BY
    l_returnflag,
    l_linestatus
    ...;
```

Note that the query contains a `GROUP BY` statement, which lists the exact columns by which our dataset is already partitioned. Making DuckDB use partitioning-aware operators is done all automatically, so in this case simply running:

```sql
ATTACH './⟨path_to_partitioned_directory⟩/lineitem_sf10' AS lineitem (
    TYPE delta
);
PRAGMA tpch(1);
```

will fire off the TPC-H Q1 on the partitioned Delta dataset. To inspect what’s happening we will again use `EXPLAIN ANALYZE`:

```text
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.477s              ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
             ...
┌─────────────┴─────────────┐
│   PARTITIONED_AGGREGATE   │
│    ────────────────────   │
│          Groups:          │
│             #0            │
│             #1            │
│                           │
│        Aggregates:        │
│          sum(#2)          │
│          sum(#3)          │
│          sum(#4)          │
│          sum(#5)          │
│          avg(#6)          │
│          avg(#7)          │
│          avg(#8)          │
│        count_star()       │
│                           │
│           4 Rows          │
│          (0.65s)          │
└─────────────┬─────────────┘
             ...
```

We can see that DuckDB has detected the partitioning information correctly and is using the `PARTITIONED_AGGREGATE` operator to do the `GROUP BY` efficiently.

Now, as a baseline, we will rerun the same query, but now with partition information pushdown disabled:

```sql
ATTACH './⟨path_to_partitioned_directory⟩/lineitem_sf10' AS lineitem (
    TYPE delta,
    PUSHDOWN_PARTITION_INFO 0
); 
PRAGMA tpch(1);
```

Again, using the `EXPLAIN ANALYZE`, we can see that DuckDB will now use a regular `HASH_GROUP_BY` operator, since the partition information from Delta was not available during query planning.

```text
┌────────────────────────────────────────────────┐
│┌──────────────────────────────────────────────┐│
││              Total Time: 0.552s              ││
│└──────────────────────────────────────────────┘│
└────────────────────────────────────────────────┘
             ...
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│          Groups:          │
│             #0            │
│             #1            │
│                           │
│        Aggregates:        │
│          sum(#2)          │
│          sum(#3)          │
│          sum(#4)          │
│          sum(#5)          │
│          avg(#6)          │
│          avg(#7)          │
│          avg(#8)          │
│        count_star()       │
│                           │
│           4 Rows          │
│          (1.37s)          │
└─────────────┬─────────────┘
             ...
```

Now looking at the performance differences between these two queries, we can see that the overall speedup is only a modest 1.16×, however the aggregation operation itself was sped up by 2.11×! This means that when queries that regularly do heavy group by operations, partitioning the data by these columns can definitely be a very useful tool to have in your performance tuning toolbox.

### A Note on Pushdown / `ATTACH` Performance Interplay

While features such as filter pushdown and partition information pushdown will improve performance for many workloads, it is useful to be aware that there is a somewhat intricate interplay between the metadata caching mechanism from using `ATTACH`, and the pushdown of filters and partition information. At the end of the section on the `ATTACH` feature, we already saw that for some queries, using `ATTACH` is actually slightly slower than using the raw `delta_scan`. Without diving into too much detail, pushing down filters and partitioning information can negatively affect the effectiveness of metadata caching for some queries. This means that on some queries, you may, somewhat counterintuitively, benefit from partially disabling filter pushdown when using `ATTACH`:

```sql
ATTACH './⟨your_delta_table_directory⟩' AS dt (
    TYPE delta, 
    PIN_SNAPSHOT, 
    PUSHDOWN_PARTITION_INFO 0, 
    PUSHDOWN_FILTERS 'none'
);
```

This should be considered an advanced use case, though, and only relevant when optimizing for specific queries. The default settings of `ATTACH` should provide the best overall performance and are recommended for most cases. Furthermore, there is ongoing work in the [underlying `delta-kernel-rs` library used by DuckDB Delta](https://github.com/delta-io/delta-kernel-rs) that aims to reduce this effect by exposing mechanisms to cleverly refresh metadata objects held by DuckDB. As soon as these mechanisms are available, we will add them to the DuckDB Delta extension, likely making these flags obsolete for anything but testing.

## Conclusion

In this blog post, we’ve taken a look at the latest version of the DuckDB Delta extension and put it to the test with some benchmarks. We’ve run queries from the industry standard TPC benchmarks to demonstrate the large performance improvements that were made over the past releases of the Delta extensions.

Furthermore, we’ve taken a look at three specific techniques that can be used while working with Delta tables to improve performance even further:

* Using metadata caching with `ATTACH`
* Using filters and data layout to reduce the number of files that need to be scanned
* Utilizing partitioning information to speed up aggregations

All in all, we think with the v0.3.0 release of the Delta extension, DuckDB can read Delta tables with excellent performance for many different workloads and highly encourage everyone to give the latest version a shot!
