---
layout: docu
title: MySQL Scanner Extension
---

The [`mysql_scanner` extension](https://github.com/Mytherin/mysql_scanner) allows DuckDB to directly read and write data from/to a running MySQL instance. The data can be queried directly from the underlying MySQL database. Data can be loaded from MySQL tables into DuckDB tables, or vice versa.

> The MySQL Scanner extension is currently in preview and not yet available as a binary package.

## Reading Data from MySQL


To make a MySQL database accessible to DuckDB use the `ATTACH` command:

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysqlscanner (TYPE mysql_scanner)
USE mysqlscanner;
```

The connection string determines the parameters for how to connect to MySQL as a set of `key=value` pairs. Any options not provided are replaced by their default values, as per the table below.

<div class="narrow_table"></div>

| Setting  |   Default    |
|----------|--------------|
| host     | localhost    |
| user     | current user |
| password |              |
| database | NULL         |
| port     | 0            |
| socket   | NULL         |

The tables in the file can be read as if they were normal DuckDB tables, but the underlying data is read directly from MySQL at query time.

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
CREATE TABLE mysql_db.tbl(id INTEGER, name VARCHAR);
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

Many operations on MySQL tables are supported. All these operations directly modify the MySQL database, and the result of subsequent operations can then be read using MySQL.
Note that if modifications are not desired, `ATTACH` can be run with the `READ_ONLY` property which prevents making modifications to the underlying database. For example:

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql_scanner, READ_ONLY);
```

Below is a list of supported operations.

### CREATE TABLE

```sql
CREATE TABLE mysql_db.tbl(id INTEGER, name VARCHAR);
```

### INSERT INTO

```sql
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

### SELECT

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

### COPY

```sql
COPY mysql_db.tbl TO 'data.parquet';
COPY mysql_db.tbl FROM 'data.parquet';
```

### UPDATE

```sql
UPDATE mysql_db.tbl SET name='Woohoo' WHERE id=42;
```

### DELETE

```sql
DELETE FROM mysql_db.tbl WHERE id=42;
```

### ALTER TABLE

```sql
ALTER TABLE mysql_db.tbl ADD COLUMN k INTEGER;
```

### DROP TABLE

```sql
DROP TABLE mysql_db.tbl;
```

### CREATE VIEW

```sql
CREATE VIEW mysql_db.v1 AS SELECT 42;
```

### CREATE SCHEMA/DROP SCHEMA

```sql
CREATE SCHEMA mysql_db.s1;
CREATE TABLE mysql_db.s1.integers(i int);
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
CREATE TABLE mysql_db.tmp(i INTEGER);
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

> Note that DDL statements are not transactional in MySQL.

## Building & Loading the Extension

The extension currently cannot be installed from a binary package. To build it, type:

```bash
make
```

To run, run the bundled `duckdb` shell:

```bash
./build/release/duckdb -unsigned
```

Then, load the MySQL extension like so:

```sql
LOAD 'build/release/extension/mysql_scanner/mysql_scanner.duckdb_extension';
```
