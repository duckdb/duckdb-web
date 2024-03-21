---
layout: docu
title: MySQL Extension
github_repository: https://github.com/duckdb/duckdb_mysql
---

The [`mysql` extension](https://github.com/duckdb/duckdb_mysql) allows DuckDB to directly read and write data from/to a running MySQL instance. The data can be queried directly from the underlying MySQL database. Data can be loaded from MySQL tables into DuckDB tables, or vice versa.

## Installing and Loading

To install the `mysql` extension, run:

```sql
INSTALL mysql;
```

The extension is loaded automatically upon first use. If you prefer to load it manually, run:

```sql
LOAD mysql;
```

## Reading Data from MySQL

To make a MySQL database accessible to DuckDB use the `ATTACH` command:

```sql
ATTACH 'host=localhost user=root port=0 database=mysql' AS mysqldb (TYPE mysql)
USE mysqldb;
```

The connection string determines the parameters for how to connect to MySQL as a set of `key=value` pairs. Any options not provided are replaced by their default values, as per the table below.

<div class="narrow_table"></div>

|  Setting   |   Default    |
|------------|--------------|
| `database` | `NULL`       |
| `host`     | `localhost`  |
| `password` |              |
| `port`     | `0`          |
| `socket`   | `NULL`       |
| `user`     | current user |

The tables in the MySQL database can be read as if they were normal DuckDB tables, but the underlying data is read directly from MySQL at query time.

```sql
SHOW TABLES;
```
```text
┌───────────────────────────────────────┐
│                 name                  │
│                varchar                │
├───────────────────────────────────────┤
│ signed_integers                       │
└───────────────────────────────────────┘
```

```sql
SELECT * FROM signed_integers;
```
```text
┌──────┬────────┬──────────┬─────────────┬──────────────────────┐
│  t   │   s    │    m     │      i      │          b           │
│ int8 │ int16  │  int32   │    int32    │        int64         │
├──────┼────────┼──────────┼─────────────┼──────────────────────┤
│ -128 │ -32768 │ -8388608 │ -2147483648 │ -9223372036854775808 │
│  127 │  32767 │  8388607 │  2147483647 │  9223372036854775807 │
│ NULL │   NULL │     NULL │        NULL │                 NULL │
└──────┴────────┴──────────┴─────────────┴──────────────────────┘
```

It might be desirable to create a copy of the MySQL databases in DuckDB to prevent the system from re-reading the tables from MySQL continuously, particularly for large tables.

Data can be copied over from MySQL to DuckDB using standard SQL, for example:

```sql
CREATE TABLE duckdb_table AS FROM mysqlscanner.mysql_table;
```

## Writing Data to MySQL

In addition to reading data from MySQL, create tables, ingest data into MySQL and make other modifications to a MySQL database using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a MySQL database to Parquet, or read data from a Parquet file into MySQL.

Below is a brief example of how to create a new table in MySQL and load data into it.

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql_scanner);
CREATE TABLE mysql_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

Many operations on MySQL tables are supported. All these operations directly modify the MySQL database, and the result of subsequent operations can then be read using MySQL.
Note that if modifications are not desired, `ATTACH` can be run with the `READ_ONLY` property which prevents making modifications to the underlying database. For example:

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql_scanner, READ_ONLY);
```

## Supported Operations

Below is a list of supported operations.

### `CREATE TABLE`

```sql
CREATE TABLE mysql_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM mysql_db.tbl;
```
```text
┌───────┬─────────┐
│  id   │  name   │
│ int64 │ varchar │
├───────┼─────────┤
│    42 │ DuckDB  │
└───────┴─────────┘
```

### `COPY`

```sql
COPY mysql_db.tbl TO 'data.parquet';
COPY mysql_db.tbl FROM 'data.parquet';
```

You may also create a full copy of the database using the [`COPY FROM DATABASE` statement](../sql/statements/copy#copy-from-database--to):

```sql
COPY FROM DATABASE mysql_db TO my_duckdb_db;
```

### `UPDATE`

```sql
UPDATE mysql_db.tbl
SET name = 'Woohoo'
WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM mysql_db.tbl
WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE mysql_db.tbl
ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE mysql_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW mysql_db.v1 AS SELECT 42;
```

### `CREATE SCHEMA` and `DROP SCHEMA`

```sql
CREATE SCHEMA mysql_db.s1;
CREATE TABLE mysql_db.s1.integers (i INT);
INSERT INTO mysql_db.s1.integers VALUES (42);
SELECT * FROM mysql_db.s1.integers;
```
```text
┌───────┐
│   i   │
│ int32 │
├───────┤
│    42 │
└───────┘
```
```sql
DROP SCHEMA mysql_db.s1;
```

### Transactions

```sql
CREATE TABLE mysql_db.tmp (i INTEGER);
BEGIN;
INSERT INTO mysql_db.tmp VALUES (42);
SELECT * FROM mysql_db.tmp;
```
```text
┌───────┐
│   i   │
│ int64 │
├───────┤
│    42 │
└───────┘
```
```sql
ROLLBACK;
SELECT * FROM mysql_db.tmp;
```
```text
┌────────┐
│   i    │
│ int64  │
├────────┤
│ 0 rows │
└────────┘
```

> The DDL statements are not transactional in MySQL.

## Settings

|                 Name                 |                          Description                           |  Default  |
|--------------------------------------|----------------------------------------------------------------|-----------|
| `mysql_bit1_as_boolean`              | Whether or not to convert `BIT(1)` columns to `BOOLEAN`        | `true`    |
| `mysql_debug_show_queries`           | DEBUG SETTING: print all queries sent to MySQL to stdout       | `false`   |
| `mysql_experimental_filter_pushdown` | Whether or not to use filter pushdown (currently experimental) | `false`   |
| `mysql_tinyint1_as_boolean`          | Whether or not to convert `TINYINT(1)` columns to `BOOLEAN`    | `true`    |

## Schema Cache

To avoid having to continuously fetch schema data from MySQL, DuckDB keeps schema information - such as the names of tables, their columns, etc -  cached. If changes are made to the schema through a different connection to the MySQL instance, such as new columns being added to a table, the cached schema information might be outdated. In this case, the function `mysql_clear_cache` can be executed to clear the internal caches.

```sql
CALL mysql_clear_cache();
```
