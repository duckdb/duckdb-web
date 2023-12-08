---
layout: docu
title: Schema
---

## Types

It is important to use the correct type for encoding columns (e.g., `BIGINT`, `DATE`, `DATETIME`). While it is always possible to use string types (`VARCHAR`, etc.) to encode more specific values (such as datetime values), this is not recommended as strings are generally slower to process.

When loading CSV files, you may leverage the CSV reader's [auto-detection mechanism](../../data/csv/auto_detection) to get the correct types for CSV inputs.

If you run in a memory-constrained environment, using smaller data types (e.g. `TINYINT`) can reduce the amount of memory and disk space required to complete a query. DuckDB’s [bitpacking compression](/2022/10/28/lightweight-compression.html#bit-packing) means small values stored in larger data types will not take up larger sizes on disk, but they will take up more memory during processing.

_**Best Practice:**_ Use the most restrictive types possible when creating columns. Avoid using strings for encoding more specific data items.

### Microbenchmark: Using Timestamps

We illustrate the difference using the `creationDate` column of the LDBC `Comment` table on scale factor 300. This table has approx. 554 million unordered timestamp values. We run a simple aggregation query that returns the average day-of-the month from the timestamps on four configurations, which differ on the column type (`DATETIME` vs. `VARCHAR`) and on whether the column is ordered. The results of the microbenchmark are as follows:

<div class="narrow_table"></div>

| Column Type | Storage Size | Query Time |
|---|---|---|
| `DATETIME` | 3.3 GB | 0.904 s |
| `VARCHAR` | 5.2 GB | 3.919 s |

The results show that using the `DATETIME` value yields smaller storage sizes and faster processing. 

## Indexing

DuckDB has two types of indexes: zonemaps and ART indexes.

### Zonemaps

DuckDB automatically creates [zonemaps](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as min-max indexes) for the columns of all [general-purpose data types](../../sql/data_types/overview). These indexes are used for predicate pushdown into scan operators and computing aggregations. This means that if a filter criterion (like `where column1 = 123`) is in use, DuckDB can skip any row group whose min-max values range does not contain that filter value (e.g., a block with a min-max of 1000-2000 will be omitted when comparing for `= 123` or `< 400`). 

#### The Effect of Ordering on Zonemaps

The more ordered the data within a column, the more useful the zonemap indexes will be. For example, in the worst case, a column could contain a random number on every row. DuckDB will be unlikely to be able to skip any row groups. The best case of ordered data commonly arises with `DATETIME` columns. If specific columns will be queried with selective filters, it is best to pre-order data by those columns when inserting it. Even an imperfect ordering will still be helpful.

### Microbenchmark: The Effect of Ordering

For an example, let’s repeat the [microbenchmark for timestamps](#microbenchmark-using-timestamps) with a timestamp column that sorted using an ascending order vs. an unordered one.

| Column Type | Ordered | Storage Size | Query Time |
|---|---|---|---|
| `DATETIME` | yes | 1.3 GB | 0.578 s |
| `DATETIME` | no | 3.3 GB | 0.904 s |

The results show that simply keeping the column order allows the computation to be 1.5x faster.

#### Ordered Integers

Another practical way to exploit ordering is to use the `INTEGER` type with automatic increments rather than `UUID` for columns that will be queried using selective filters. `UUID`s will likely be inserted in a random order, so many row groups in the table will need to be scanned to find a specific `UUID` value, while an ordered `INTEGER` column will allow all row groups to be skipped except the one that contains the value.

### ART Indexes

DuckDB allows defining [Adaptive Radix Tree (ART) indexes](https://db.in.tum.de/~leis/papers/ART.pdf) in two ways.
First, such an index is created implicitly for columns with a `PRIMARY KEY`, a `FOREIGN KEY`, and a `UNIQUE` constraint.
Second, explicitly running a [the `CREATE INDEX` and `CREATE UNIQUE INDEX` statements](../../sql/indexes) create an ART index on the target column(s).

The tradeoffs of having an ART index on a column are as follows:

1. It enables constraint checking upon changes (inserts, updates, and deletes) for non-bulky changes.
2. Having an ART index makes changes to the affected column(s) slower compared to non-indexed performance. That is because of index maintenance for these operations.

Regarding query performance, an ART index has the following effects:

1. It speeds up point queries and other highly selective queries using the indexed column(s), where the filtering condition returns approx. 0.1% of all rows or fewer. When in doubt, use [`EXPLAIN`](../meta/explain) to verify that your query plan uses the index scan.
2. An ART index has no effect on the performance of join, aggregation, and sorting queries.

Indexes are serialized to disk and deserialized lazily, i.e., when the database is reopened, operations using the index will only load the required parts of the index.

_**Best Practices:**_
* Only use primary keys, foreign keys, or UNIQUE constraints, if these are necessary for enforcing constraints on your data.
* Do not define explicit indexes unless you have highly-selective queries.
* If you define an ART index, do so after bulk loading the data to the table.

## Constraints

DuckDB allows defining [constraints](../../sql/constraints) such as `UNIQUE`, `PRIMARY KEY`, and `FOREIGN KEY`. These constraints can be beneficial for ensuring data integrity but they have a negative effect on load performance as they necessitate building indexes and performing checks. Moreover, they _very rarely improve the performance of queries_ as DuckDB does not rely on these indexes for join and aggregation operators (see [indexing](#indexing) for more details).

_**Best Practice:**_ Do not define constraints unless your goal is to ensure data integrity.

### Microbenchmark: The Effect of Primary Keys

We illustrate the difference using the LDBC `Comment` table at scale factor 300. This table has approx. 554 million entries. We first create the schema without a primary key, then load the data. In the second experiment, we create the schema with a primary key, then load the data. In both cases, we take the data from `.csv.gz` files, and measure the time required to perform the loading.

<div class="narrow_table"></div>

|      Operation           | Execution Time |
|--------------------------|----------------|
| Load without primary key | 92.168s        |
| Load with primary key    | 286.765s       |
| `CREATE UNIQUE INDEX`    | 123.038s       |

The results show that loading the data with a primary key defined adds a significant overhead: in fact, it takes significantly longer than loading the data without a primary key and running `CREATE UNIQUE INDEX` after loading the data.
