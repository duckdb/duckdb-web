---
layout: post
title: "No Memory? No Problem. External Aggregation in DuckDB"
author: Laurens Kuiper
excerpt: "Since the 0.9.0 release, DuckDB’s fully parallel aggregate hash table can efficiently aggregate over many more groups than fit in memory."
---

Most grouped aggregation queries yield just a few output rows.
For example, “How many flights departed from each European capital in the past ten years?” yields one row per European capital, even if the table containing all the flight information has millions of rows.
This is not always the case, as “How many orders did each customer place in the past ten years?” yields one row per customer, which could be millions, which significantly increaseses the memory consumption of the query.
However, even if the aggregation does not fit in memory, DuckDB can still complete the query.

Not interested in the implementation? [Jump straight to the experiments!](#experiments)

<!--more-->

## Introduction

Around two years ago, we published our first blog post on DuckDB’s hash aggregation, titled [“Parallel Grouped Aggregation in DuckDB”](/2022/03/07/aggregate-hashtable).
So why are we writing another blog post now?

Unlike most database systems, which are servers, DuckDB is used in all kinds of environments, which may not have much memory.
However, some database queries, like aggregations with many unique groups, require a lot of memory.
The laptop I am writing this on has 16 GB of RAM.
What if a query needs 20 GB?
If this happens:
```text
Out of Memory Error: could not allocate block of size X (Y/Z used)
```
The query is aborted.
Sadly, we can’t [download more RAM](https://knowyourmeme.com/memes/download-more-ram).
But luckily, this laptop also has a fast SSD with 1 TB of storage.
In many cases, we don’t need all 20 GB of data to be in memory simultaneously, and we can temporarily place some data in storage.
If we load it back whenever needed, we can still complete the query.
We must be careful to use storage sparingly because despite modern SSDs being fast, they are still much slower than memory.

In a nutshell, that’s what this post is about.
Since the [0.9.0 release](/2023/09/26/announcing-duckdb-090), DuckDB’s hash aggregation can process more unique groups than fit in memory by offloading data to storage.
In this post, we’ll explain how this works.
If you want to know what hash aggregation is, how hash collisions are resolved, or how DuckDB’s hash table is structured, check out [our first blog post on hash aggregation](/2022/03/07/aggregate-hashtable).

## Memory Management

Most database systems store persistent data on “pages”.
Upon request, these pages can be read from the _database file_ in storage, put into memory, and written back again if necessary.
The common wisdom is to make all pages the same size: This allows pages to be swapped and avoids [fragmentation](https://en.wikipedia.org/wiki/Fragmentation_(computing)) in memory and storage.
When the database is started, a portion of memory is allocated and reserved for these pages, called the “buffer pool”.
The database component that is responsible for managing the buffer pool is aptly called the “buffer manager”.

The remaining memory is reserved for short-lived, i.e., _temporary_, memory allocations, such as hash tables for aggregation.
These allocations are done differently, which is good because if there are many unique groups, hash tables may need to be very large, so we wouldn’t have been able to use the fixed-size pages for that anyway.
If we have more temporary data than fits in memory, operators like aggregation have to decide when to selectively write data to a _temporary file_ in storage.

... At least, that’s the traditional way of doing things.
This made little sense for DuckDB.
Why should we manage persistent and temporary data so differently?
The difference is that _persistent_ data should be _persisted_, and _temporary_ data should not.
Why can’t a buffer manager manage both?

DuckDB’s buffer manager is not traditional.
Most persistent and temporary data is stored on fixed-size pages and managed by the buffer manager.
The buffer manager tries to make the best use of your memory.
That means we don’t reserve a portion of memory for a buffer pool.
This allows DuckDB to use all memory for persistent data, not just a portion if that’s what’s best for your workload.
If you’re doing large aggregations that need a lot of memory, DuckDB can evict the persistent data from memory to free up space for a large hash table.

Because DuckDB’s buffer manager manages _all_ memory, both persistent and temporary data, it is much better at choosing when to write temporary data to storage than operators like aggregation could ever be.
Leaving the responsibility of offloading to the buffer manager also saves us the effort of implementing reading and writing data to a temporary file in every operator that needs to process data that does not fit in memory.

Why don’t buffer managers in other database systems manage temporary data?
There are two problems: _Memory Fragmentation_ and _Invalid References_.

### Memory Fragmentation

Hash tables and other data structures used in query operators don’t exactly have a fixed size like the pages used for persistent data.
We also don’t want to have a lot of pages with variable sizes floating around in memory alongside the pages with a fixed size, as this would cause memory fragmentation.

Ideally, we would use the fixed size for _all_ of our memory allocations, but this is not a good idea: Sometimes, the most efficient way to process a query requires allocating, for example, a large array.
So, we settled for using a fixed size for _almost all_ of our allocations.
These short-lived allocations are immediately deallocated after use, unlike the fixed-size pages for persistent data, which are kept around.
These allocations do not cause fragmentation with each other because [jemalloc](https://jemalloc.net), which DuckDB uses for allocating memory when possible, categorizes allocations using size classes and maintains separate arenas for them.

### Invalid References

Temporary data usually cannot be written to storage as-is because it often contains pointers.
For example, DuckDB implements the string type proposed by [Umbra](https://db.in.tum.de/~freitag/papers/p29-neumann-cidr20.pdf), which has a fixed width.
Strings longer than 12 characters are not stored within the string type, but _somewhere else_, and a pointer to this “somewhere else” is stored instead.

This creates a problem when we want to offload data to storage.
Let’s say this “somewhere else” where strings longer than 12 characters are stored is one of those pages that the buffer manager can offload to storage at any time to free up some memory.
If the page is offloaded and then loaded back, it will most likely be loaded into a different address in memory.
The pointers that pointed to the long strings are now _invalid_ because they still point to the previous address!

The usual way of writing data containing pointers to storage is by _serializing_ it first.
When reading it back into memory, it has to be _deserialized_ again.
[(De-)serialization can be an expensive operation](https://www.vldb.org/pvldb/vol10/p1022-muehleisen.pdf), hence why data formats like [Arrow Flight](https://arrow.apache.org/blog/2019/10/13/introducing-arrow-flight/) exist, which try to minimize the cost.
However, we can’t use Arrow here because Arrow is a column-major layout, but [a row-major layout is more efficient for hash tables](https://ir.cwi.nl/pub/13807/13807B.pdf).

We could create a row-major version of Arrow Flight, but we can just avoid (de-)serialization altogether:
We’ve created a specialized row-major _page layout_ that actually uses the old invalidated pointers to _recompute_ new valid pointers after reading the data back into memory.

The page layout places fixed-size rows and variable-size data like strings on separate pages.
The size of the rows is fixed for a query: After a SQL query is issued, DuckDB creates and executes a query plan.
So, even before executing the said plan, we already know which columns we need, their types, and how wide these types are.

As shown in the image below, a small amount of “MetaData” is needed to recompute the pointers.
The fixed-size rows are stored in “Row Pages”, and variable-size rows in “Var Pages”.

<p align="center">
    <img src="/images/external_aggregation/TupleDataCollection.svg"
        alt="DuckDB's spillable page layout"
        width=600
        />
</p>

Remember that there are pointers within the fixed-size rows pointing to variable-size data.
The MetaData describes which fixed-size rows point to which Var Page and the last known address of the Var Page.
For example, MetaData 1 describes 5 rows stored in Row Page 1 at offset 0, with variable-size data stored in Var Page 1, which had an address of `0x42`.

Let’s say the buffer manager decides to offload Var Page 1.
When we request Var Page 1 again, it’s loaded into address `0x500`.
The pointers within those 5 rows are now invalid.
For example, one of the rows contains the pointer `0x48`, which means that it is stored at offset `0x48 - 0x42 = 6` in Var Page 1.
We can recompute the pointer by adding the offset to the new address of the page: `0x500 + 6 = 0x506`.
Pointer recomputation is done for rows with their strings stored on the same Row and Var Page, so we create a new MetaData every time a Row Page or Var Page is full.

The advantage of pointer recomputation over (de-)serialization is that it can be done lazily.
We can check whether the Var Page was offloaded by comparing the pointer in the MetaData with the current pointer to the page.
We don’t have to recompute the pointers if they are the same.

## External Aggregation

Now that we’ve figured out how to deal with temporary data, it’s finally time to talk about hash aggregation.
The first big challenge is to perform the aggregation in parallel.

DuckDB uses [Morsel-Driven Parallelism](https://db.in.tum.de/~leis/papers/morsels.pdf) parallelize query execution, which essentially means that query operators, such as aggregation, must be parallelism-aware.
This differs from [plan-driven parallelism](https://dl.acm.org/doi/pdf/10.1145/93605.98720), keeping operators unaware of parallelism.

To briefly summarize [our first blog post on aggregation](/2022/03/07/aggregate-hashtable): In DuckDB, all active threads have their own thread-local hash table, which they sink input data into.
This will keep threads busy until all input data has been read.
Multiple threads will likely have the _exact same group_ in their hash table.
Therefore, the thread-local hash tables must be combined to complete the grouped aggregation.
This can be done in parallel by partitioning the hash tables and assigning each thread to combine the data from each partition.
For the most part, we still use this same approach.
You’ll see this in the image below, which illustrates our new implementation.

<p align="center">
    <img src="/images/external_aggregation/OOCHA.svg"
        alt="TODO"
        width=600
        />
</p>

We call the first phase _Thread-Local Pre-Aggregation_.
The input data are _morsels_, chunks of around 100,000 rows.
These are assigned to active threads, which sink them into their thread-local hash table until all input data has been read.
We use _linear probing_ to resolve collisions and _salt_ to reduce the overhead of dealing with said collisions.
This is explained in [our first blog post on aggregation](/2022/03/07/aggregate-hashtable), so I won’t repeat it here.

Now that we’ve explained what _hasn’t_ changed, we can talk about what _has_ changed.
The first difference compared to last time is the way that we partition.
Before, if we had, for example, 32 threads, each thread would create 32 hash tables, one for each partition.
This totals a whopping 1024 hash tables, which did not scale well when even more threads were active.
Now, each thread has one hash table, _but the data within each hash table is partitioned_.
The data is also stored on the specialized page layout we presented earlier so that it can easily be offloaded to storage.

The second difference is that the hash tables are not _resized_ during Thread-Local Pre-Aggregation.
We keep the hash tables’ size small, reducing the amount of cache misses during this phase.
This means that the hash table will be full at some point.
When it’s full, we reset it and start over.
We can do this because we’ll finish the aggregation later in the second phase.
When we reset the hash table, we “unpin” the pages that store the actual data, which tells our buffer manager it can write them to storage when it needs to free up memory.

Together, these two changes result in a low memory requirement during the first phase.
Each thread only needs to keep a small hash table in memory.
We may collect a lot of data by filling up the hash table many times, but the buffer manager can offload almost all of it if needed.

For the second phase, _Partition-Wise Aggregation_, the thread-local partitioned data is exchanged, and each thread combines the data of a single partition into a hash table.
This phase is mostly the same as before, except that we now sometimes create many more partitions than threads.
Why? The hash table for one partition might fit in memory, but 8 threads could be combining a partition simultaneously, and we might not be able to fit 8 partitions in memory.
The easy solution to this problem is to _over-partition_.
If we make more partitions than threads, for example, 32 partitions, the size of the partitions will be smaller, and the 8 threads will combine only 8 out of the 32 partitions simultaneously, which won’t require nearly as much memory.

<a name="experiments"></a>

## Experiments

Aggregations that result in only a few unique groups can easily fit in memory.
To evaluate our external hash aggregation implementation, we need aggregations that have many unique groups.
For this purpose, we will use the [H2O.ai database-like ops benchmark](https://duckdblabs.github.io/db-benchmark/), which [we've resurrected](/2023/04/14/h2oai), and [now maintain](/2023/11/03/db-benchmark-update).
Specifically, we will use the `G1_1e9_2e0_0_0.csv` file, which is 50 GB.
The source code for this benchmark can be found [here](https://github.com/duckdblabs/db-benchmark).

We use the following queries from the benchmark to load the data:
```sql
SET preserve_insertion_order = false;
CREATE TABLE y (
    id1 VARCHAR, id2 VARCHAR, id3 VARCHAR,
    id4 INT, id5 INT, id6 INT, v1 INT, v2 INT,
    v3 FLOAT);
COPY y FROM 'G1_1e9_2e0_0_0.csv' (FORMAT CSV, AUTO_DETECT true);
CREATE TYPE id1ENUM AS ENUM (SELECT id1 FROM y);
CREATE TYPE id2ENUM AS ENUM (SELECT id2 FROM y);
CREATE TABLE x (
    id1 id1ENUM, id2 id2ENUM, id3 VARCHAR,
    id4 INT, id5 INT, id6 INT, v1 INT, v2 INT,
    v3 FLOAT);
INSERT INTO x (SELECT * FROM y);
DROP TABLE IF EXISTS y;
```

The H2O.ai aggregation benchmark consists of 10 queries, which vary in the number of unique groups:
```sql
-- Query 1: ~100 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id1, sum(v1) AS v1
FROM x
GROUP BY id1;
```
```sql
-- Query 2: ~10,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id1, id2, sum(v1) AS v1
FROM x
GROUP BY id1, id2;
```
```sql
-- Query 3: ~10,000,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id3, sum(v1) AS v1, avg(v3) AS v3
FROM x
GROUP BY id3;
```
```sql
-- Query 4: ~100 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id4, avg(v1) AS v1, avg(v2) AS v2, avg(v3) AS v3
FROM x
GROUP BY id4;
```
```sql
-- Query 5: ~1,000,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id6, sum(v1) AS v1, sum(v2) AS v2, sum(v3) AS v3
FROM x
GROUP BY id6;
```
```sql
-- Query 6: ~10,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT
    id4,
    id5,
    quantile_cont(v3, 0.5) AS median_v3,
    stddev(v3) AS sd_v3
FROM x
GROUP BY id4, id5;
```
```sql
-- Query 7: ~10,000,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id3, max(v1)-min(v2) AS range_v1_v2
FROM x
GROUP BY id3;
```
```sql
-- Query 8: ~10,000,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id6, v3 AS largest2_v3
FROM (
    SELECT id6, v3, row_number() OVER (
          PARTITION BY id6
          ORDER BY v3 DESC) AS order_v3
    FROM x
    WHERE v3 IS NOT NULL) sub_query
WHERE order_v3 <= 2;
```
```sql
-- Query 9: ~10,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id2, id4, pow(corr(v1, v2), 2) AS r2
FROM x
GROUP BY id2, id4;
```
```sql
-- Query 10: ~1,000,000,000 unique groups
CREATE OR REPLACE TABLE ans AS
SELECT id1, id2, id3, id4, id5, id6, sum(v3) AS v3, count(*) AS count
FROM x
GROUP BY id1, id2, id3, id4, id5, id6;
```

The [results on the benchmark page](https://duckdblabs.github.io/db-benchmark/) are obtained using the `c6id.metal` AWS EC2 instance.
On this instance, all the queries easily fit in memory, and having many threads doesn't hurt performance either.
DuckDB only takes 8.58 seconds to complete even the largest query, query 10, which returns 1 billion unique groups.
However, many people will not use such a beefy machine to crunch numbers.
On my laptop, a 2020 MacBook Pro, some smaller queries will fit in memory, like query 1, but query 10 will definitely not.

The following table is a summary of the hardware used.

| Specs       | `c6id.metal` | Laptop |  Ratio |
|:------------|-------------:|-------:|-------:|
| Memory      |       256 GB |  16 GB |    16x |
| CPU cores   |           64 |      8 |     8x |
| CPU threads |          128 |      8 |    16x |
| Hourly cost |        $6.45 |  $0.00 |    NaN |

Although the CPU cores of the AWS EC2 instance are not directly comparable with those of my laptop, the instance clearly has much more compute power and memory available.
Despite the large differences in hardware, DuckDB can complete all 10 queries without a problem:

| Query | `c6id.metal` | Laptop |  Ratio |
|------:|-------------:|-------:|-------:|
|     1 |         0.08 |   0.74 |  9.25x |
|     2 |         0.09 |   0.76 |  8.44x |
|     3 |         8.01 | 156.63 | 19.55x |
|     4 |         0.26 |   2.07 |  7.96x |
|     5 |         6.72 | 145.00 | 21.58x |
|     6 |        17.12 |  19.28 |  1.13x |
|     7 |         6.33 | 124.85 | 19.72x |
|     8 |         6.53 | 126.35 | 19.35x |
|     9 |         0.32 |   1.90 |  5.94x |
|    10 |         8.58 | 264.14 | 30.79x |

The runtime of the queries is reported in seconds, and was obtained by taking the median of 3 runs on my laptop using DuckDB 0.10.1.
The `c6id.metal` instance results were obtained from the [benchmark website](https://duckdblabs.github.io/db-benchmark/).
Despite being unable to _fit_ all unique groups in my laptop's memory, DuckDB can _compute_ all unique groups and return them.
The largest query, query 10, takes almost 4.5 minutes to complete.
This is over 30x longer than with the beefy `c6id.metal` instance.
The large difference is, of course, explained by the large differences in hardware.
Interestingly, this is still faster than Spark on the `c6id.metal` instance, which takes 603.05 seconds!

## Conclusion

DuckDB is constantly improving its larger-than-memory query processing capabilities.
In this blog post, we showed some of the tricks DuckDB uses for spilling and loading data from storage.
These tricks are implemented in DuckDB's external hash aggregation, released since 0.9.0.
We took the hash aggregation for a spin on the H2O.ai benchmark, and DuckDB could complete all 50 GB queries on a laptop with only 16 GB of memory.
