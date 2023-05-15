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
There have been too many changes to discuss them each in detail, but we would like to highlight the new pivot and unpivot statements, improvements to parallel data import/export, time series joins, recursive globbing, lazy-loading of storage metadata, user-defined functions for Python, Arrow Database Connectivity Support and the Swift Integration. Below is a summary of those new features with examples, starting with two breaking changes in our SQL dialect.


#### Breaking SQL Changes
This release includes two breaking changes to the SQL dialect: The [division operator uses floating point division by default](https://github.com/duckdb/duckdb/pull/7082), and the [default null sort order is changed from `NULLS FIRST` to `NULLS LAST`](https://github.com/duckdb/duckdb/pull/7174). The old behavior can be restored using the following settings:

```sql
SET integer_division=true;
SET default_null_order='nulls_first';
```

[**Division Operator**](https://github.com/duckdb/duckdb/pull/7082). The division operator `/` will now always perform a floating point division even with integer parameters. The new operator `//` retains the old semantics and can be used to perform integer division. This makes DuckDB's division operator less error prone for beginners, and consistent with the division operator in Python 3 and other systems in the OLAP space like Spark, Snowflake and BigQuery.


```sql
SELECT 42 / 5, 42 // 5;
```

| (42 / 5) | (42 // 5) |
|----------|-----------|
| 8.4      | 8         |

[**Default Null Sort Order**](https://github.com/duckdb/duckdb/pull/7174). The default null sort order is changed from `NULLS FIRST` to `NULLS LAST`. The reason for this change is that `NULLS LAST` sort-order is more intuitive when combined with `LIMIT`. With `NULLS FIRST`, Top-N queries always return the `NULL` values first. With `NULLS LAST`, the actual Top-N values are returned instead.

```sql
CREATE TABLE bigdata(col INTEGER);
INSERT INTO bigdata VALUES (NULL), (42), (NULL), (43);
FROM bigdata ORDER BY col DESC LIMIT 3;
```

| v0.7.1 | v0.8.0 |
|--------|--------|
| NULL   | 43     |
| NULL   | 42     |
| 43     | NULL   |

#### New SQL Features

[**Pivot and Unpivot**](https://github.com/duckdb/duckdb/pull/6387). There are many shapes and sizes of data, and we do not always have control over the process in which data is generated. While SQL is well-suited for reshaping datasets, turning columns into rows or rows into columns is tedious in vanilla SQL. With this release, DuckDB introduces the `PIVOT` and `UNPIVOT` statements that allow reshaping data sets so that rows are turned into columns or vice versa. Here is a short example:

```sql
CREATE TABLE sales(year INT, amount INT);
INSERT INTO sales VALUES (2021, 42), (2022, 100), (2021, 42);
PIVOT sales ON year USING SUM(amount);
```

| 2021 | 2022 |
|------|------|
| 84   | 100  |

The [documentation contains more examples](/docs/sql/statements/pivot.html).


[**ASOF Joins for Time Series**](https://github.com/duckdb/duckdb/pull/6719). When joining time series data with background fact tables, the timestamps often do not exactly match. In this case it is often desirable to join rows so that the timestamp is joined with the *nearest timestamp*. The ASOF join can be used for this purpose - it performs a fuzzy join to find the closest join partner for each row instead of requiring an exact match.


```sql
CREATE TABLE a(ts TIMESTAMP);
CREATE TABLE b(ts TIMESTAMP);
INSERT INTO a VALUES (TIMESTAMP '2023-05-15 10:31:00'), (TIMESTAMP '2023-05-15 11:31:00');
INSERT INTO b VALUES (TIMESTAMP '2023-05-15 10:30:00'), (TIMESTAMP '2023-05-15 11:30:00');

FROM a ASOF JOIN b ON a.ts >= b.ts;
```

|        a.ts         |        b.ts         |
|---------------------|---------------------|
| 2023-05-15 10:31:00 | 2023-05-15 10:30:00 |
| 2023-05-15 11:31:00 | 2023-05-15 11:30:00 |


Please [refer to the documentation](/docs/guides/sql_features/asof_join.html) for a more in-depth explanation.



#### Data Integration Improvements

[**Default Parallel CSV Reader.**](https://github.com/duckdb/duckdb/pull/6977). In this release, the parallel CSV reader has been vastly improved and is now the default CSV reader. We would like to thank everyone that has tried out the experimental reader for their valuable feedback and reports. The `experimental_parallel_csv` flag has been deprecated and is no longer required. The parallel CSV reader enables much more efficient reading of large CSV files. 

```sql
CREATE TABLE lineitem AS FROM lineitem.csv;
```

| v0.7.1 | v0.8.0 |
|--------|--------|
| 4.1s   | 1.2s   |

**Parallel [Parquet](https://github.com/duckdb/duckdb/pull/7375), [CSV and JSON Writing](https://github.com/duckdb/duckdb/pull/7368).** This release includes support for parallel *order-preserving* writing of Parquet, CSV and JSON files. As a result, writing to these file formats is parallel by default, also without disabling insertion order preservation, and writing to these formats is greatly sped up.

```sql
COPY lineitem TO 'lineitem.csv';
COPY lineitem TO 'lineitem.parquet';
COPY lineitem TO 'lineitem.json';
```

| Format  | v0.7.1 | v0.8.0 |
|---------|--------|--------|
| CSV     | 3.9s   | 0.6s   |
| Parquet | 8.1s   | 1.2s   |
| JSON    | 4.4s   | 1.1s   |

[**Recursive File Globbing using `**`**](https://github.com/duckdb/duckdb/pull/6627). This release adds support for recursive globbing where an arbitrary number of subdirectories can be matched using the `**` operator (double-star).

```sql
FROM 'data/glob/crawl/stackoverflow/**/*.csv';
```

[The documentation has been updated](/docs/data/multiple_files/overview) with various examples of this syntax.


#### Storage Improvements

[**Lazy-Loading Table Metadata**.](https://github.com/duckdb/duckdb/pull/6715). DuckDB’s internal storage format stores metadata for every row group in a table, such as min-max indices and where in the file every row group is stored. In the past, DuckDB would load this metadata immediately once the database was opened. However, once the data gets very big, the metadata can also get quite large, leading to a noticeable delay on database startup. In this release, we have optimized the metadata handling of DuckDB to only read table metadata as its being accessed. As a result, startup is near-instantaneous even for large databases, and metadata is only loaded for columns that are actually used in queries.

|         Query          | v0.6.1 | v0.7.1 | v0.8.0  | Parquet |
|------------------------|--------|--------|-------|---------|
| SELECT 42              | 1.60s | 0.31s  | 0.02s | -       |
| FROM lineitem LIMIT 1; | 1.62s | 0.32s  | 0.03s | 0.27s   |


#### Clients

[**User-Defined Scalar Functions for Python**](https://github.com/duckdb/duckdb/pull/7171). Arbitrary Python functions can now be registered as scalar functions within SQL queries. This will only work when using DuckDB from Python, because it uses the actual Python runtime that DuckDB is running within. While plain Python values can be passed to the function, there is also a vectorized variant that uses PyArrow under the hood for higher efficiency and better parallelism.

```py
import duckdb

from duckdb.typing import *
from faker import Faker

def random_date():
     fake = Faker()
     return fake.date_between()

duckdb.create_function('random_date', random_date, [], DATE)
res = duckdb.sql('select random_date()').fetchall()
print(res)
# [(datetime.date(2019, 5, 15),)]
```

[**Arrow Database Connectivity Support (ADBC)**](https://github.com/duckdb/duckdb/pull/7086). ADBC is a database API standard for database access libraries that uses Apache Arrow to transfer query result sets and to ingest data. Using Arrow for this is particularly beneficial for columnar data management systems which traditionally suffered a performance hit by emulating row-based APIs such as JDBC/ODBC. From this release, DuckDB natively supports ADBC. We’re happy to be one of the first systems to offer native support, and DuckDB’s in-process design fits nicely with ADBC.

[**Swift Integration**](https://duckdb.org/2023/04/21/swift.html). DuckDB has gained another official language integration: Swift. Swift is a language developed by Apple that most notably is used to create Apps for Apple devices, but also increasingly used for server-side development. The DuckDB Swift API allows developers on all swift platforms to harness DuckDB using a native Swift interface with support for Swift features like strong typing and concurrency.

#### Final Thoughts
The full release notes can be [found on Github](https://github.com/duckdb/duckdb/releases/tag/v0.8.0). We would like to thank all of the contributors for their hard work on improving DuckDB.
