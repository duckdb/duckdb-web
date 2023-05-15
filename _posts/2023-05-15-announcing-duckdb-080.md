---
layout: post
title:  "Announcing DuckDB 0.8.0"
author: Mark Raasveldt and Hannes Mühleisen
excerpt_separator: <!--more-->
---

<img src="/images/blog/mottled_duck.jpg"
     alt="Image of the Mottled Duck"
     width=200px
     />

The DuckDB team is happy to announce the latest DuckDB release (0.8.0). This release is named “Fulvigula” after the [Mottled Duck](https://en.wikipedia.org/wiki/Mottled_duck) (Anas Fulvigula) native to the Gulf of Mexico.

To install the new version, please visit the [installation guide](https://duckdb.org/docs/installation/index). The full release notes can be found [here](https://github.com/duckdb/duckdb/releases/tag/v0.8.0).

<!--more-->

#### What's new in 0.8.0
There have been too many changes to discuss them each in detail, but we would like to highlight the new PIVOT statement, parallel import/export, time series join, recursive globbing, lazy-loading storage metadata, user-defined functions for Python, Arrow Database Connectivity Support and the Swift Integration. Below is a summary of those new features with examples, starting with two breaking changes in our SQL dialect.


#### Breaking SQL Changes
[#7174](https://github.com/duckdb/duckdb/pull/7174): The **default sort order** in `ORDER BY` switched from `NULLS FIRST` to `NULLS LAST` because this is more intuitive, especially in conjunction with `LIMIT`. 

In this example, we can see how the two `NULL` values are now last in the resut:

```sql
CREATE TABLE bigdata AS (VALUES (NULL), (42), (NULL), (43));
FROM bigdata ORDER BY ALL;
```

| col0 |
|------|
| 42   |
| 43   |
| NULL |
| NULL |

[#7082](https://github.com/duckdb/duckdb/pull/7082): The **division operator** `/` will now always lead to a floating point result even with integer parameters. The new operator `//` retains the old semantics. This change is consistent with Python 3. 


```sql
SELECT 42/5, 42//5;
```

| (42 / 5) | (42 // 5) |
|----------|-----------|
| 8.4      | 8         |




#### PIVOT Statement
There are many shapes and sizes of data, and we do not always have control over the process. While SQL in general is well-suited for reshaping datasets, turning columns into rows or rows into columns is rather tedious to achieve in vanilla SQL. With this release, DuckDB introduces a `PIVOT` statement that allows pivoting tables according to arbitrary columns and possibly with aggregation. Here is a short example:

```sql
CREATE TABLE sales AS FROM (FROM (VALUES(2021, 42), (2022, 84)) v(year, amount));
PIVOT sales on YEAR USING SUM(amount);
```

| 2021 | 2022 |
|------|------|
| 42   | 84   |

We have [updated the DuckDB documentation](https://duckdb.org/docs/sql/statements/pivot.html) with more examples.


#### Parallel Reading and Writing of CSV, Parquet and JSON
DuckDB has had an experimental parallel CSV reader since the last release. In this release, this parallel CSV reader has been vastly improved and is now the default [#6977](https://github.com/duckdb/duckdb/pull/6977). This should greatly speed up ingestion of CSV files into DuckDB. We have also added support for parallel writing of Parquet [#7375](https://github.com/duckdb/duckdb/pull/7375), CSV [#7368](https://github.com/duckdb/duckdb/pull/7368) and JSON files.

Here are some quick benchmark on a MacBook numbers using the TPC-H lineitem table (scale factor 1, roughly 6M rows):

|            | From Parquet | To Parquet | From CSV | To CSV | 
|------------|--------------|------------|----------|--------|
| 10 threads |         0.3 s|       0.7 s|      1.1s|    0.5s|  
| 1 thread   |         1.7 s|       2.3 s|      3.9s|    2.7s|


<details markdown='1'>
<summary markdown='span'>
Script to run this experiment on your computer with the DuckDB shell.
</summary>

```
INSTALL tpch; LOAD tpch;
CALL dbgen(sf=1);
.timer on

COPY lineitem TO 'lineitem1.parquet';
COPY lineitem TO 'lineitem1.csv';
CREATE OR REPLACE TEMPORARY TABLE lineitem2 AS FROM 'lineitem1.csv';
CREATE OR REPLACE TEMPORARY TABLE lineitem2 AS FROM 'lineitem1.parquet';

PRAGMA threads=1;

COPY lineitem TO 'lineitem2.parquet';
COPY lineitem TO 'lineitem2.csv';
CREATE OR REPLACE TEMPORARY TABLE lineitem2 AS FROM 'lineitem2.csv';
CREATE OR REPLACE TEMPORARY TABLE lineitem2 AS FROM 'lineitem2.parquet';
```
</details>




#### `ASOF` Joins for Time Series
When joining for example time series data with background fact tables, the columns often do not exactly match. Yet a millisecond difference in timestamp is often irrelevant, and the join should be performed anyways. To support this use case, DuckDB adds the so-called ASOF join, which performs a more fuzzy join to find the “closest” join partner instead. Internally, the ASOF join uses DuckDB’s [efficient range join](https://duckdb.org/2022/05/27/iejoin.html) operator. Here's a quick example:

```sql
CREATE TABLE a AS (VALUES ('2023-05-15 10:31:00'::TIMESTAMP), ('2023-05-15 11:31:00'::TIMESTAMP));
CREATE TABLE b AS (VALUES ('2023-05-15 10:30:00'::TIMESTAMP), ('2023-05-15 11:30:00'::TIMESTAMP));
```

If we perform a "normal" `LEFT JOIN`, the value in `b` will not find a JOIN partner:

```sql
FROM a LEFT JOIN b ON a.col0 = b.col0;
```

|        a.col0         | b.col0 |
|---------------------|------|
| 2023-05-15 10:36:00 | NULL |
| 2023-05-15 11:36:00 | NULL |


```sql
FROM a ASOF JOIN b ON a.col0 >= b.col0;
```

But with the ASOF join and a more tolerant predicate, the join can be performed:

|        a.col0         |        b.col0         |
|---------------------|---------------------|
| 2023-05-15 10:31:00 | 2023-05-15 10:30:00 |
| 2023-05-15 11:31:00 | 2023-05-15 11:30:00 |


Please [check our documentation](https://duckdb.org/docs/guides/sql_features/asof_join.html) for a more in-depth explanation.




#### Recursive File Globbing using `**`
DuckDB has supported wildcards (“Globbing”) in file names for the CSV or Parquet reader for a while, this release adds support for recursive globbing where an arbitrary number of subdirectories can be matched using the `**` operator (double-star) similar to what Spark supports. [The documentation has been updated](https://duckdb.org/docs/data/multiple_files/overview), too. 


#### Lazy-Loading Storage Metadata
DuckDB’s internal storage format stores some metadata internally, which schemas, tables, columns exist, what are their types, and where in the file they are stored. In addition, we keep some basic statistics to support efficient query execution like min-max indices. In the past, DuckDB would load this metadata immediately once the database was opened. However, once the data gets very big, the metadata can also get quite large, leading to a noticeable delay on database startup. Since the DuckDB database engine often only exists during the runtime of a single query, this overhead cannot be amortized by a long overall system runtime. In this release, we have optimized the metadata handling of DuckDB to only read metadata as its being accessed, meaning that startup is near-instantaneous and the metadata is only loaded for columns that are actually used in queries.

https://github.com/duckdb/duckdb/pull/6841
https://github.com/duckdb/duckdb/pull/6715

#### User-Defined Scalar Functions for Python
Sometimes it is more convenient to implement data transformations as Python code rather than in plain SQL. Arbitrary Python functions can now be registered as scalar functions within SQL queries. This will only work when using DuckDB from Python, because it uses the actual Python runtime that DuckDB is running within. While plain Python values can be passed to the function, there is also a vectorized variant that uses PyArrow under the hood to do so efficiently. 

https://github.com/duckdb/duckdb/pull/7171

#### Arrow Database Connectivity Support (ADBC) 
ADBC is a database API standard for database access libraries that uses Apache Arrow to transfer query result sets and to ingest data. Using Arrow for this is particularly beneficial for columnar data management systems which traditionally suffered a performance hit by emulating row-based APIs such as JDBC/ODBC. From this release, DuckDB natively supports ADBC. We’re happy to be one of the first systems to offer native support, and DuckDB’s in-process design fits nicely with ADBC.

https://arrow.apache.org/blog/2023/01/05/introducing-arrow-adbc/
https://github.com/duckdb/duckdb/pull/7086

#### Swift Integration
DuckDB has gained another official language integration: Swift. Swift is a language developed by Apple that most notably is used to create Apps for Apple devices, but also increasingly used for server-side development. The DuckDB Swift API allows developers on all swift platforms to harness DuckDB using a native Swift interface with support for Swift features like strong typing and concurrency.

https://duckdb.org/2023/04/21/swift.html



#### Final Thoughts
The full release notes can be [found on Github](https://github.com/duckdb/duckdb/releases/tag/v0.8.0). We would like to thank all of the contributors for their hard work on improving DuckDB.
