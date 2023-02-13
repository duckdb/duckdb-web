---
layout: post
title:  "Announcing DuckDB 0.7.0"
author: Mark Raasveldt
excerpt_separator: <!--more-->
---

<img src="/images/blog/labrador_duck.png"
     alt="Image of the labrador duck"
     width=200px
     />

The DuckDB team is happy to announce the latest DuckDB version (0.7.0) has been released. This release of DuckDB is named "Labradorius" after the [Labrador Duck (Camptorhynchus labradorius)](https://en.wikipedia.org/wiki/Labrador_duck) that was native to North America.

To install the new version, please visit the [installation guide](https://duckdb.org/docs/installation/index). The full release notes can be found [here](https://github.com/duckdb/duckdb/releases/tag/v0.7.0).

<!--more-->

#### What's in 0.7.0
The new release contains many improvements to the JSON support, new SQL features, improvements to data ingestion and export, and other new features. Below is a summary of the most impactful changes, together with the linked PRs that implement the features.

#### Data Ingestion/Export Improvements

**JSON Ingestion.** This version introduces the [`read_json` and `read_json_auto`](https://github.com/duckdb/duckdb/pull/5992) methods. These can be used to ingest JSON files into a tabular format. Similar to `read_csv`, the `read_json` method requires a schema to be specified, while the `read_json_auto` automatically infers the schema of the JSON from the file using sampling. Both [new-line delimited JSON](http://ndjson.org) and regular JSON are supported.

```sql
FROM 'data/json/with_list.json';
```

| id |               name               |
|----|----------------------------------|
| 1  | [O, Brother,, Where, Art, Thou?] |
| 2  | [Home, for, the, Holidays]       |
| 3  | [The, Firm]                      |
| 4  | [Broadcast, News]                |
| 5  | [Raising, Arizona]               |

**Partitioned Parquet/CSV Export.** DuckDB has been able to ingest [hive-partitioned Parquet and CSV files](https://duckdb.org/docs/extensions/httpfs#hive-partitioning) for a while. After this release [DuckDB will also be able to *write* hive-partitioned data](https://github.com/duckdb/duckdb/pull/5964) using the `PARTITION_BY` clause. These files can be exported locally or remotely to S3 compatible storage. Here is a local example:

```sql
COPY orders TO 'orders' (FORMAT PARQUET, PARTITION_BY (year, month));
```

This will cause the Parquet files to be written in the following directory structure:

```
orders
├── year=2021
│    ├── month=1
│    │   ├── file1.parquet
│    │   └── file2.parquet
│    └── month=2
│        └── file3.parquet
└── year=2022
     ├── month=11
     │   ├── file4.parquet
     │   └── file5.parquet
     └── month=12
         └── file6.parquet
```

**Parallel Parquet/CSV Writing.** Parquet and CSV writing are sped up tremendously this release with the [parallel Parquet and CSV writer support](https://github.com/duckdb/duckdb/pull/5756).

| Format  | Old  | New (8T) |
|---------|------|----------|
| CSV     | 2.6s | 0.38s    |
| Parquet | 7.5s | 1.3s     |

Note that currently the parallel writing is currently limited to non-insertion order preserving - which can be toggled by setting the `preserve_insertion_order` setting to false. In a future release we aim to alleviate this restriction and order parallel insertion order preserving writes as well.

#### Multi-Database Support 

**Attach Functionality.** This release adds support for [attaching multiple databases](https://github.com/duckdb/duckdb/pull/5764) to the same DuckDB instance. This easily allows data to be transferred between separate DuckDB database files, and also allows data from separate database files to be combined together in individual queries. Remote DuckDB instances (stored on a network accessible location like Github, for example) may also be attached.

```sql
ATTACH 'new_db.db';
CREATE TABLE new_db.tbl(i INTEGER);
INSERT INTO new_db.tbl SELECT * FROM range(1000);
DETACH new_db;
```

See the [documentation for more information](https://duckdb.org/docs/sql/statements/attach).

**SQLite Storage Back-end.** In addition to adding support for attaching DuckDB databases - this release also adds support for [*pluggable database engines*](https://github.com/duckdb/duckdb/pull/6066). This allows extensions to define their own database and catalog engines that can be attached to the system. Once attached, an engine can support both reads and writes. The [SQLite extension](https://github.com/duckdblabs/sqlite_scanner) makes use of this to add native read/write support for SQLite database files to DuckDB.

```sql
ATTACH 'sqlite_file.db' AS sqlite (TYPE SQLITE);
CREATE TABLE sqlite.tbl(i INTEGER);
INSERT INTO sqlite.tbl VALUES (1), (2), (3);
SELECT * FROM sqlite.tbl;
```

Using this, SQLite database files can be attached, queried and modified as if they are native DuckDB database files. This allows data to be quickly transferred between SQLite and DuckDB - and allows you to use DuckDB's rich SQL dialect to query data stored in SQLite tables.

#### New SQL Features

**Upsert Support.** [Upsert support](https://github.com/duckdb/duckdb/pull/5866) is added with this release using the `ON CONFLICT` clause, as well as the `SQLite` compatible `INSERT OR REPLACE`/`INSERT OR IGNORE` syntax.

```sql
CREATE TABLE movies(id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO movies VALUES (1, 'A New Hope');
FROM movies;
```

| id |    name    |
|----|------------|
| 1  | A New Hope |

```sql
INSERT OR REPLACE INTO movies VALUES (1, 'The Phantom Menace');
FROM movies;
```

| id |        name        |
|----|--------------------|
| 1  | The Phantom Menace |

See the [documentation for more information](https://duckdb.org/docs/sql/statements/insert#on-conflict-clause).

**Lateral Joins.** Support for [lateral joins](https://github.com/duckdb/duckdb/pull/5393) is added in this release. Lateral joins are a more flexible variant of correlated subqueries that make working with nested data easier, as they allow [easier unnesting](https://github.com/duckdb/duckdb/pull/5485) of nested data.  

**Positional Joins.** While SQL formally models unordered sets, in practice the order of datasets does frequently have a meaning. DuckDB offers guarantees around maintaining the order of rows when loading data into tables or when exporting data back out to a file - as well as when executing queries such as `LIMIT` without a corresponding `ORDER BY` clause.

To improve support for this use case - this release [introduces the `POSITIONAL JOIN`](https://github.com/duckdb/duckdb/pull/5867). Rather than joining on the values of rows - this new join type joins rows based on their position in the table.

```sql
CREATE TABLE t1 AS FROM (VALUES (1), (2), (3)) t(i);
CREATE TABLE t2 AS FROM (VALUES (4), (5), (6)) t(k);
SELECT * FROM t1 POSITIONAL JOIN t2;
```

| i | k |
|---|---|
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

#### Python API Improvements

**Query Building.** This release introduces easier incremental query building using the Python API by allowing relations to be queried. This allows you to decompose long SQL queries into multiple smaller SQL queries, and allows you to easily inspect query intermediates.

```
import duckdb
lineitem = duckdb.sql('FROM lineitem.parquet')
lineitem.limit(3).show()
┌────────────┬───────────┬───────────┬───┬───────────────────┬────────────┬──────────────────────┐
│ l_orderkey │ l_partkey │ l_suppkey │ … │  l_shipinstruct   │ l_shipmode │      l_comment       │
│   int32    │   int32   │   int32   │   │      varchar      │  varchar   │       varchar        │
├────────────┼───────────┼───────────┼───┼───────────────────┼────────────┼──────────────────────┤
│          1 │    155190 │      7706 │ … │ DELIVER IN PERSON │ TRUCK      │ egular courts abov…  │
│          1 │     67310 │      7311 │ … │ TAKE BACK RETURN  │ MAIL       │ ly final dependenc…  │
│          1 │     63700 │      3701 │ … │ TAKE BACK RETURN  │ REG AIR    │ riously. regular, …  │
├────────────┴───────────┴───────────┴───┴───────────────────┴────────────┴──────────────────────┤
│ 3 rows                                                                    16 columns (6 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
lineitem_filtered = duckdb.sql('FROM lineitem WHERE l_orderkey>5000')
lineitem_filtered.limit(3).show()
┌────────────┬───────────┬───────────┬───┬────────────────┬────────────┬──────────────────────┐
│ l_orderkey │ l_partkey │ l_suppkey │ … │ l_shipinstruct │ l_shipmode │      l_comment       │
│   int32    │   int32   │   int32   │   │    varchar     │  varchar   │       varchar        │
├────────────┼───────────┼───────────┼───┼────────────────┼────────────┼──────────────────────┤
│       5024 │    165411 │       444 │ … │ NONE           │ AIR        │  to the expre        │
│       5024 │     57578 │        84 │ … │ COLLECT COD    │ REG AIR    │ osits hinder caref…  │
│       5024 │    111009 │      3521 │ … │ NONE           │ MAIL       │ zle carefully saut…  │
├────────────┴───────────┴───────────┴───┴────────────────┴────────────┴──────────────────────┤
│ 3 rows                                                                 16 columns (6 shown) │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
duckdb.sql('SELECT MIN(l_orderkey), MAX(l_orderkey) FROM lineitem_filtered').show()
┌─────────────────┬─────────────────┐
│ min(l_orderkey) │ max(l_orderkey) │
│      int32      │      int32      │
├─────────────────┼─────────────────┤
│            5024 │         6000000 │
└─────────────────┴─────────────────┘
```

Note that everything is lazily evaluated. The Parquet file is not read from disk until the final query is executed - and queries are optimized in their entirety. Executing the decomposed query will be just as fast as executing the long SQL query all at once.

**Python Ingestion APIs.** This release adds several [familiar data ingestion and export APIs](https://github.com/duckdb/duckdb/pull/6015) that follow standard conventions used by other libraries. These functions emit relations as well - which can be directly queried again.

```
lineitem = duckdb.read_csv('lineitem.csv')
lineitem.limit(3).show()
┌────────────┬───────────┬───────────┬───┬───────────────────┬────────────┬──────────────────────┐
│ l_orderkey │ l_partkey │ l_suppkey │ … │  l_shipinstruct   │ l_shipmode │      l_comment       │
│   int32    │   int32   │   int32   │   │      varchar      │  varchar   │       varchar        │
├────────────┼───────────┼───────────┼───┼───────────────────┼────────────┼──────────────────────┤
│          1 │    155190 │      7706 │ … │ DELIVER IN PERSON │ TRUCK      │ egular courts abov…  │
│          1 │     67310 │      7311 │ … │ TAKE BACK RETURN  │ MAIL       │ ly final dependenc…  │
│          1 │     63700 │      3701 │ … │ TAKE BACK RETURN  │ REG AIR    │ riously. regular, …  │
├────────────┴───────────┴───────────┴───┴───────────────────┴────────────┴──────────────────────┤
│ 3 rows                                                                    16 columns (6 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
duckdb.sql('select min(l_orderkey) from lineitem').show()
┌─────────────────┐
│ min(l_orderkey) │
│      int32      │
├─────────────────┤
│               1 │
└─────────────────┘
```

**Polars Integration.** This release adds support for tight integration with the [Polars DataFrame library](https://github.com/pola-rs/polars), similar to our integration with Pandas DataFrames. Results can be converted to Polars DataFrames using the `.pl()` function.


```py
import duckdb
duckdb.sql('select 42').pl()
```

```
shape: (1, 1)
┌─────┐
│ 42  │
│ --- │
│ i32 │
╞═════╡
│ 42  │
└─────┘
```

In addition, Polars DataFrames can be directly queried using the SQL interface.

```py
import duckdb
import polars as pl
df = pl.DataFrame._from_dict({'a': 42})
duckdb.sql('select * from df').pl()
```

```
shape: (1, 1)
┌─────┐
│ a   │
│ --- │
│ i64 │
╞═════╡
│ 42  │
└─────┘
```

**fsspec Filesystem Support.** This release adds support for the [fsspec filesystem API](https://github.com/duckdb/duckdb/pull/5829). [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) allows users to define their own filesystem that they can pass to DuckDB. DuckDB will then use this file system to read and write data to and from. This enables support for storage back-ends that may not be natively supported by DuckDB yet, such as FTP.

#### Storage Improvements

**Delta Compression.** Compression of numeric values in the storage is improved using the new [delta and delta-constant compression](https://github.com/duckdb/duckdb/pull/5491). This compression method is particularly effective when compressing values that are equally spaced out. For example, sequences of numbers (`1, 2, 3, ...`) or timestamps with a fixed interval between them (`12:00:01, 12:00:02, 12:00:03, ...`).

#### Final Thoughts

The full release notes can be [found on Github](https://github.com/duckdb/duckdb/releases/tag/v0.7.0). We would like to thank all of the contributors for their hard work on improving DuckDB.
