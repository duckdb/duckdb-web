---
layout: docu
title: Schema
---

## Types

It is important to use the correct type for encoding columns (e.g., `BIGINT`, `DATE`, `DATETIME`). While it is always possible to use string types (`VARCHAR`, etc.) to encode more specific values, this is not recommended. Strings use more space and are slower to process in operations such as filtering, join, and aggregation.

When loading CSV files, you may leverage the CSV reader's [auto-detection mechanism](../../data/csv/auto_detection) to get the correct types for CSV inputs.

If you run in a memory-constrained environment, using smaller data types (e.g. `TINYINT`) can reduce the amount of memory and disk space required to complete a query. DuckDB’s [bitpacking compression](/2022/10/28/lightweight-compression.html#bit-packing) means small values stored in larger data types will not take up larger sizes on disk, but they will take up more memory during processing.

_**Best Practice:**_ Use the most restrictive types possible when creating columns. Avoid using strings for encoding more specific data items.

### Microbenchmark: Using Timestamps

We illustrate the difference in aggregation speed using the [`creationDate` column of the LDBC Comment table on scale factor 300](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet). This table has approx. 554 million unordered timestamp values. We run a simple aggregation query that returns the average day-of-the month from the timestamps in two configurations.

First, we use a `DATETIME` to encode the values and run the query using the [`extract` datetime function](../../sql/functions/timestamp):

```sql
SELECT avg(extract('day' FROM creationDate)) FROM Comment;
```

Second, we use the `VARCHAR` type and use string operations:

```sql
SELECT avg(CAST(creationDate[9:10] AS INT)) FROM Comment;
```

The results of the microbenchmark are as follows:

<div class="narrow_table"></div>

| Column Type | Storage Size | Query Time |
| ----------- | ------------ | ---------- |
| `DATETIME`  | 3.3 GB       | 0.9 s      |
| `VARCHAR`   | 5.2 GB       | 3.9 s      |

The results show that using the `DATETIME` value yields smaller storage sizes and faster processing. 

### Microbenchmark: Joining on Strings

We illustrate the difference caused by joining on different types by computing a self-join on the [LDBC Comment table at scale factor 100](https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst). The table has 64-bit integer identifiers used as the `id` attribute of each row. We perform the following join operation:

```sql
SELECT count(*) AS count
FROM Comment c1
JOIN Comment c2 ON c1.ParentCommentId = c2.id;
```

In the first experiment, we use the correct (most restrictive) types, i.e., both the `id` and the `ParentCommentId` columns are defined as `BIGINT`.
In the second experiment, we define all columns with the `VARCHAR` type.
While the results of the queries are the same for all both experiments, their runtime vary significantly.
The results below show that joining on `BIGINT` columns is approx. 1.8× faster than performing the same join on `VARCHAR`-typed columns encoding the same value.

<div class="narrow_table"></div>

| Join Column Payload Type | Join Column Schema Type | Example Value                            | Query Time |
| ------------------------ | ----------------------- | ---------------------------------------- | ---------- |
| `BIGINT`                 | `BIGINT`                | `70368755640078`                         | 1.2 s      |
| `BIGINT`                 | `VARCHAR`               | `'70368755640078'`                       | 2.1 s      |

## Constraints

DuckDB allows defining [constraints](../../sql/constraints) such as `UNIQUE`, `PRIMARY KEY`, and `FOREIGN KEY`. These constraints can be beneficial for ensuring data integrity but they have a negative effect on load performance as they necessitate building indexes and performing checks. Moreover, they _very rarely improve the performance of queries_ as DuckDB does not rely on these indexes for join and aggregation operators (see [indexing](indexing) for more details).

_**Best Practice:**_ Do not define constraints unless your goal is to ensure data integrity.

## Microbenchmark: The Effect of Primary Keys

We illustrate the effect of using primary keys with the [LDBC Comment table at scale factor 300](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst). This table has approx. 554 million entries. We first create the schema without a primary key, then load the data. In the second experiment, we create the schema with a primary key, then load the data. In both cases, we take the data from `.csv.gz` files, and measure the time required to perform the loading.

<div class="narrow_table"></div>

| Operation                | Execution Time |
| ------------------------ | -------------- |
| Load without primary key | 92.168s        |
| Load with primary key    | 286.765s       |
