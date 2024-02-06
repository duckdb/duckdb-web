---
layout: post
title:  "Announcing DuckDB 0.9.0"
author: Mark Raasveldt and Hannes Mühleisen
excerpt_separator: <!--more-->
excerpt: ""
---

<img src="/images/blog/yellow-billed-duck.jpg"
     alt="Image of the Yellow Billed Duck"
     width=200px
     />

The DuckDB team is happy to announce the latest DuckDB release (0.9.0). This release is named Undulata after the [Yellow-billed duck](https://en.wikipedia.org/wiki/Yellow-billed_duck) native to Africa.

To install the new version, please visit the [installation guide](https://duckdb.org/docs/installation/index). The full release notes can be found [here](https://github.com/duckdb/duckdb/releases/tag/v0.9.0).

<!--more-->

#### What's new in 0.9.0

There have been too many changes to discuss them each in detail, but we would like to highlight several particularly exciting features! 

* Out-Of-Core Hash Aggregate
* Storage Improvements
* Index Improvements
* DuckDB-WASM Extensions
* Extension Auto-Loading
* Improved AWS Support
* Iceberg Support
* Azure Support
* PySpark-Compatible API

Below is a summary of those new features with examples, starting with a change in our SQL dialect that is designed to produce more intuitive results by default.


#### Breaking SQL Changes

[**Struct Auto-Casting**](https://github.com/duckdb/duckdb/pull/8942). Previously the names of struct entries were ignored when determining auto-casting rules. As a result, struct field names could be silently renamed. Starting with this release, this will result in an error instead.

```sql
CREATE TABLE structs(s STRUCT(i INT));
INSERT INTO structs VALUES ({'k': 42});
-- Mismatch Type Error: Type STRUCT(k INTEGER) does not match with STRUCT(i INTEGER). Cannot cast STRUCTs with different names
```

Unnamed structs constructed using the `ROW` function can still be inserted into struct fields.

```sql
INSERT INTO structs VALUES (ROW(42));
```

#### Core System Improvements

**[Out-Of-Core Hash Aggregates](https://github.com/duckdb/duckdb/pull/7931)** and **[Hash Aggregate Performance Improvements.](https://github.com/duckdb/duckdb/pull/8475)** When working with large data sets, memory management is always a potential pain point. By using a streaming execution engine and buffer manager, DuckDB supports many operations on larger than memory data sets. DuckDB also aims to support queries where *intermediate* results do not fit into memory by using disk-spilling techniques.

In this release, support for disk-spilling techniques is further extended through the support for out-of-core hash aggregates. Now, hash tables constructed during `GROUP BY` queries or `DISTINCT` operations that do not fit in memory due to a large number of unique groups will spill data to disk instead of throwing an out-of-memory exception. Due to the clever use of radix partitioning, performance degradation is gradual, and performance cliffs are avoided. Only the subset of the table that does not fit into memory will be spilled to disk.

The performance of our hash aggregate has also improved in general, especially when there are many groups. For example, we compute the number of unique rows in a data set with 30 million rows and 15 columns by using the following query:

```sql
SELECT COUNT(*) FROM (SELECT DISTINCT * FROM tbl);
```
If we keep all the data in memory, the query should use around 6GB. However, we can still complete the query if less memory is available. In the table below, we can see how the runtime is affected by lowering the memory limit:

<div class="narrow_table"></div>

|  memory limit |  v0.8.1  |  v0.9.0  |
|:-------------:|:--------:|:--------:|
| 10.0GB        | 8.52s    | 2.91s    |
| 9.0GB         | 8.52s    | 3.45s    |
| 8.0GB         | 8.52s    | 3.45s    |
| 7.0GB         | 8.52s    | 3.47s    |
| 6.0GB         | OOM      | 3.41s    |
| 5.0GB         | OOM      | 3.67s    |
| 4.0GB         | OOM      | 3.87s    |
| 3.0GB         | OOM      | 4.20s    |
| 2.0GB         | OOM      | 4.39s    |
| 1.0GB         | OOM      | 4.91s    |

**[Compressed Materialization.](https://github.com/duckdb/duckdb/pull/7644)** DuckDB's streaming execution engine has a low memory footprint, but more memory is required for operations such as grouped aggregation. The memory footprint of these operations can be reduced by compression. DuckDB already uses [many compression techniques in its storage format](/2022/10/28/lightweight-compression.html), but many of these techniques are too costly to use during query execution. However, certain lightweight compression techniques are so cheap that the benefit of the reducing memory footprint outweight the cost of (de)compression.

In this release, we add support for compression of strings and integer types right before data goes into the grouped aggregation and sorting operators. By using statistics, both types are compressed to the smallest possible integer type. For example, if we have the following table:

```text
┌───────┬─────────┐
│  id   │  name   │
│ int32 │ varchar │
├───────┼─────────┤
│   300 │ alice   │
│   301 │ bob     │
│   302 │ eve     │
│   303 │ mallory │
│   304 │ trent   │
└───────┴─────────┘
```

The `id` column uses a 32-bit integer. From our statistics we know that the minimum value is 300, and the maximum value is 304. We can subtract 300 and cast to an 8-bit integer instead, reducing the width from 4 bytes down to 1.

The `name` column uses our internal string type, which is 16 bytes wide. However, our statistics tell us that the longest string here is only 7 bytes. We can fit this into a 64-bit integer like so:
```text
alice   -> alice005
bob     -> bob00003
eve     -> eve00003
mallory -> mallory7
trent   -> trent005
```

This reduces the width from 16 bytes down to 8. To support sorting of compressed strings, we flip the bytes on big-endian machines so that our comparison operators are still correct:
```text
alice005 -> 500ecila
bob00003 -> 30000bob
eve00003 -> 30000eve
mallory7 -> 7yrollam
trent005 -> 500tnert
```

By reducing the size of query intermediates, we can prevent/reduce spilling data to disk, reducing the need for costly I/O operations, thereby improving query performance.

**Window Function Performance Improvements ([#7831](https://github.com/duckdb/duckdb/pull/7831), [#7996](https://github.com/duckdb/duckdb/pull/7996), [#8050](https://github.com/duckdb/duckdb/pull/8050), [#8491](https://github.com/duckdb/duckdb/pull/8491)).** This release features many improvements to the performance of Window functions due to improved vectorization of the code, more re-use of partial aggregates and improved parallelism through work stealing of tasks. As a result, performance of [Window functions has improved significantly, particularly in scenarios where there are no or few partitions](https://github.com/duckdb/duckdb/issues/7809#issuecomment-1679387022).

```sql
SELECT
    SUM(driver_pay) OVER (
        ORDER BY dropoff_datetime ASC
        RANGE BETWEEN
        INTERVAL 3 DAYS PRECEDING AND
        INTERVAL 0 DAYS FOLLOWING
    )
FROM tripdata;
```

<div class="narrow_table"></div>

| Version | Time (s) |
| -- | --: |
| v0.8.0 | 33.8 |
| v0.9.0 | 3.8 |

#### Storage Improvements

[**Vacuuming of Deleted Row Groups**](https://github.com/duckdb/duckdb/pull/7794). Starting with this release, when deleting data using `DELETE` statements, entire row groups that are deleted will be automatically cleaned up. Support is also added to [truncate the database file on checkpoint](https://github.com/duckdb/duckdb/pull/7824) which allows the database file to be reduced in size after data is deleted. Note that this only occurs if the deleted row groups are located at the end of the file. The system does not yet move around data in order to reduce the size of the file on disk. Instead, free blocks earlier on in the file are re-used to store later data.

**Index Storage Improvements ([#7930](https://github.com/duckdb/duckdb/pull/7930), [#8112](https://github.com/duckdb/duckdb/pull/8112), [#8437](https://github.com/duckdb/duckdb/pull/8437), [#8703](https://github.com/duckdb/duckdb/pull/8703))**. Many improvements have been made to both the in-memory footprint, and the on-disk footprint of ART indexes. In particular for indexes created to maintain `PRIMARY KEY`, `UNIQUE` or `FOREIGN KEY` constraints the storage and in-memory footprint is drastically reduced.

```sql
CREATE TABLE integers(i INTEGER PRIMARY KEY);
INSERT INTO integers FROM range(10000000);
```

<div class="narrow_table"></div>

| Version | Size |
| -- | --: |
| v0.8.0 | 278MB |
| v0.9.0 | 78MB |

In addition, due to improvements in the manner in which indexes are stored on disk they can now be written to disk incrementally instead of always requiring a full rewrite. This allows for much quicker checkpointing for tables that have indexes.


#### Extensions

[**Extension Auto-Loading**](https://github.com/duckdb/duckdb/pull/8732). Starting from this release, DuckDB supports automatically installing and loading of trusted extensions. As many workflows rely on core extensions that are not bundled, such as `httpfs`, many users found themselves having to remember to load the required extensions up front. With this change, the extensions will instead be automatically loaded (and optionally installed) when used in a query.

For example, in Python the following code snippet now works without needing to explicitly load the `httpfs` or `json` extensions.

```py
import duckdb

duckdb.sql("FROM 'https://raw.githubusercontent.com/duckdb/duckdb/main/data/json/example_n.ndjson'")
```

The set of autoloadable extensions is limited to official extensions distributed by DuckDB Labs, and can be [found here](https://github.com/duckdb/duckdb/blob/8feb03d274892db0e7757cd62c145b18dfa930ec/scripts/generate_extensions_function.py#L298). The behavior can also be disabled using the `autoinstall_known_extensions` and `autoload_known_extensions` settings, or through the more general `enable_external_access` setting. See the [configuration options](https://duckdb.org/docs/sql/configuration.html).

[**DuckDB-WASM Extensions**](https://github.com/duckdb/duckdb-wasm/pull/1403). This release adds support for loadable extensions to DuckDB-WASM. Previously, any extensions that you wanted to use with the WASM client had to be baked in. With this release, extensions can be loaded dynamically instead. When an extension is loaded, the WASM bundle is downloaded and the functionality of the extension is enabled. Give it a try in our [WASM shell](https://shell.duckdb.org).

```sql
LOAD inet;
SELECT '127.0.0.1'::INET;
```

[**AWS Extension**](https://github.com/duckdb/duckdb_aws). This release marks the launch of the DuckDB AWS extension. This extension contains AWS related features that rely on the AWS SDK. Currently, the extension contains one function, `LOAD_AWS_CREDENTIALS`, which uses the AWS [Credential Provider Chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html#credentialProviderChain) to automatically fetch and set credentials:

```sql
CALL load_aws_credentials();
SELECT * FROM "s3://some-bucket/that/requires/authentication.parquet";
```

[See the documentation for more information](https://duckdb.org/docs/extensions/aws).

[**Experimental Iceberg Extension**](https://github.com/duckdb/duckdb_iceberg). This release marks the launch of the DuckDB Iceberg extension. This extension adds support for reading tables stored in the [Iceberg format](https://iceberg.apache.org).

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', ALLOW_MOVED_PATHS=true);
```

[See the documentation for more information](https://duckdb.org/docs/extensions/iceberg).

[**Experimental Azure Extension**](https://github.com/duckdb/duckdb_azure). This release marks the launch of the DuckDB Azure extension. This extension allows for DuckDB to natively read data stored on Azure, in a similar manner to how it can read data stored on S3.

```sql
SET azure_storage_connection_string = '<your_connection_string>';
SELECT * FROM 'azure://<my_container>/*.csv';
```

[See the documentation for more information](https://duckdb.org/docs/extensions/azure).


#### Clients

[**Experimental PySpark API**](https://github.com/duckdb/duckdb/pull/8083). This release features the addition of an experimental Spark API to the Python client. The API aims to be fully compatible with the PySpark API, allowing you to use the Spark API as you are familiar with but while utilizing the power of DuckDB. All statements are translated to DuckDB's internal plans using our [relational API](https://duckdb.org/docs/archive/0.8.1/api/python/relational_api) and executed using DuckDB's query engine.

```py
from duckdb.experimental.spark.sql import SparkSession as session
from duckdb.experimental.spark.sql.functions import lit, col
import pandas as pd

spark = session.builder.getOrCreate()

pandas_df = pd.DataFrame({
    'age': [34, 45, 23, 56],
    'name': ['Joan', 'Peter', 'John', 'Bob']
})

df = spark.createDataFrame(pandas_df)
df = df.withColumn(
    'location', lit('Seattle')
)
res = df.select(
    col('age'),
    col('location')
).collect()

print(res)
#[
#    Row(age=34, location='Seattle'),
#    Row(age=45, location='Seattle'),
#    Row(age=23, location='Seattle'),
#    Row(age=56, location='Seattle')
#]
```

Note that the API is currently experimental and features are still missing. We are very interested in feedback. Please report any functionality that you are missing, either through Discord or on Github.


#### Final Thoughts

The full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v0.9.0). We would like to thank all of the contributors for their hard work on improving DuckDB.
