---
layout: docu
title: Indexing
---

DuckDB has two types of indexes: zonemaps and ART indexes.

## Zonemaps

DuckDB automatically creates [zonemaps](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as min-max indexes) for the columns of all [general-purpose data types](../../sql/data_types/overview#general-purpose-data-types). These indexes are used for predicate pushdown into scan operators and computing aggregations. This means that if a filter criterion (like `WHERE column1 = 123`) is in use, DuckDB can skip any row group whose min-max range does not contain that filter value (e.g., a block with a min-max range of 1000 to 2000 will be omitted when comparing for `= 123` or `< 400`).

### The Effect of Ordering on Zonemaps

The more ordered the data within a column, the more useful the zonemap indexes will be. For example, in the worst case, a column could contain a random number on every row. DuckDB will be unlikely to be able to skip any row groups. The best case of ordered data commonly arises with `DATETIME` columns. If specific columns will be queried with selective filters, it is best to pre-order data by those columns when inserting it. Even an imperfect ordering will still be helpful.

### Microbenchmark: The Effect of Ordering

For an example, let’s repeat the [microbenchmark for timestamps](schema#microbenchmark-using-timestamps) with a timestamp column that sorted using an ascending order vs. an unordered one.

<div class="narrow_table"></div>

| Column type | Ordered | Storage size | Query time |
|---|---|---|---|
| `DATETIME` | yes | 1.3 GB | 0.6 s |
| `DATETIME` | no | 3.3 GB | 0.9 s |

The results show that simply keeping the column order allows for improved compression, yielding a 2.5x smaller storage size.
It also allows the computation to be 1.5x faster.

### Ordered Integers

Another practical way to exploit ordering is to use the `INTEGER` type with automatic increments rather than `UUID` for columns that will be queried using selective filters. `UUID`s will likely be inserted in a random order, so many row groups in the table will need to be scanned to find a specific `UUID` value, while an ordered `INTEGER` column will allow all row groups to be skipped except the one that contains the value.

## ART Indexes

DuckDB allows defining [Adaptive Radix Tree (ART) indexes](https://db.in.tum.de/~leis/papers/ART.pdf) in two ways.
First, such an index is created implicitly for columns with `PRIMARY KEY`, `FOREIGN KEY`, and `UNIQUE` [constraints](schema#constraints).
Second, explicitly running a the [`CREATE INDEX`](../../sql/indexes) statement creates an ART index on the target column(s).

The tradeoffs of having an ART index on a column are as follows:

1. It enables efficient constraint checking upon changes (inserts, updates, and deletes) for non-bulky changes.
2. Having an ART index makes changes to the affected column(s) slower compared to non-indexed performance. That is because of index maintenance for these operations.

Regarding query performance, an ART index has the following effects:

1. It speeds up point queries and other highly selective queries using the indexed column(s), where the filtering condition returns approx. 0.1% of all rows or fewer. When in doubt, use [`EXPLAIN`](../meta/explain) to verify that your query plan uses the index scan.
2. An ART index has no effect on the performance of join, aggregation, and sorting queries.

Indexes are serialized to disk and deserialized lazily, i.e., when the database is reopened, operations using the index will only load the required parts of the index. Therefore, having an index will not cause any slowdowns when opening an existing database.

> Bestpractice We recommend following these guidelines:
>
> * Only use primary keys, foreign keys, or unique constraints, if these are necessary for enforcing constraints on your data.
> * Do not define explicit indexes unless you have highly selective queries.
> * If you define an ART index, do so after bulk loading the data to the table. Adding an index prior to loading, either explicitly or via primary/foreign keys, is [detrimental to load performance](schema#microbenchmark-the-effect-of-primary-keys).

<!--
## Microbenchmark: The Timing of Index Creation

| `CREATE UNIQUE INDEX`    | 123.0s       |
The results show that loading the data with a primary key defined adds a significant overhead: in fact, it takes significantly longer than loading the data without a primary key and running `CREATE UNIQUE INDEX` after loading the data.
-->