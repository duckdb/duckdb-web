---
layout: docu
redirect_from:
- docs/archive/0.9.2/extensions/sqlite_scanner
- docs/archive/0.9.2/extensions/sqlite
- docs/archive/0.9.1/extensions/sqlite
- docs/archive/0.9.0/extensions/sqlite
title: SQLite Extension
---

The SQLite extension allows DuckDB to directly read and write data from a SQLite database file. The data can be queried directly from the underlying SQLite tables. Data can be loaded from SQLite tables into DuckDB tables, or vice versa.

## Installing and Loading

To install the `sqlite` extension, run:

```sql
INSTALL sqlite;
```

The extension is loaded automatically upon first use. If you prefer to load it manually, run:

```sql
LOAD sqlite;
```

## Usage

To make a SQLite file accessible to DuckDB, use the `ATTACH` statement, which supports read & write.

For example with the [`sakila.db` file](https://github.com/duckdb/sqlite_scanner/blob/main/data/db/sakila.db):

```sql
ATTACH 'sakila.db' (TYPE SQLITE);
USE sakila;
```

The tables in the file can be read as if they were normal DuckDB tables, but the underlying data is read directly from the SQLite tables in the file at query time.


```sql
SHOW TABLES;
```

```text
┌────────────────────────┐
│          name          │
├────────────────────────┤
│ actor                  │
│ address                │
│ category               │
│ city                   │
│ country                │
│ customer               │
│ customer_list          │
│ film                   │
│ film_actor             │
│ film_category          │
│ film_list              │
│ film_text              │
│ inventory              │
│ language               │
│ payment                │
│ rental                 │
│ sales_by_film_category │
│ sales_by_store         │
│ staff                  │
│ staff_list             │
│ store                  │
└────────────────────────┘
```

You can query the tables using SQL, e.g. using the example queries from [`sakila-examples.sql`](https://github.com/duckdb/sqlite_scanner/blob/main/data/sql/sakila-examples.sql):

```sql
SELECT
    cat.name AS category_name,
    sum(ifnull(pay.amount, 0)) AS revenue
FROM category cat
LEFT JOIN film_category flm_cat
       ON cat.category_id = flm_cat.category_id
LEFT JOIN film fil
       ON flm_cat.film_id = fil.film_id
LEFT JOIN inventory inv
       ON fil.film_id = inv.film_id
LEFT JOIN rental ren
       ON inv.inventory_id = ren.inventory_id
LEFT JOIN payment pay
       ON ren.rental_id = pay.rental_id
GROUP BY cat.name
ORDER BY revenue DESC
LIMIT 5;
```

## Data Types

SQLite is a [weakly typed database system](https://www.sqlite.org/datatype3.html). As such, when storing data in a SQLite table, types are not enforced. The following is valid SQL in SQLite:

```sql
CREATE TABLE numbers (i INTEGER);
INSERT INTO numbers VALUES ('hello');
```

DuckDB is a strongly typed database system, as such, it requires all columns to have defined types and the system rigorously checks data for correctness.

When querying SQLite, DuckDB must deduce a specific column type mapping. DuckDB follows SQLite's [type affinity rules](https://www.sqlite.org/datatype3.html#type_affinity) with a few extensions.

1. If the declared type contains the string "INT" then it is translated into the type `BIGINT`
2. If the declared type of the column contains any of the strings "CHAR", "CLOB", or "TEXT" then it is translated into `VARCHAR`.
3. If the declared type for a column contains the string "BLOB" or if no type is specified then it is translated into `BLOB`.
4. If the declared type for a column contains any of the strings "REAL", "FLOA", "DOUB", "DEC" or "NUM" then it is translated into `DOUBLE`.
5. If the declared type is "DATE", then it is translated into `DATE`.
6. If the declared type contains the string "TIME", then it is translated into `TIMESTAMP`.
7. If none of the above apply, then it is translated into `VARCHAR`.

As DuckDB enforces the corresponding columns to contain only correctly typed values, we cannot load the string "hello" into a column of type `BIGINT`. As such, an error is thrown when reading from the "numbers" table above:

```text
Error: Mismatch Type Error: Invalid type in column "i": column was declared as integer, found "hello" of type "text" instead.
```

This error can be avoided by setting the `sqlite_all_varchar` option:

```sql
SET GLOBAL sqlite_all_varchar=true;
```

When set, this option overrides the type conversion rules described above, and instead always converts the SQLite columns into a `VARCHAR` column. Note that this setting must be set *before* `sqlite_attach` is called.


## Opening SQLite Databases Directly

SQLite databases can also be opened directly and can be used transparently instead of a DuckDB database file. In any client, when connecting, a path to a SQLite database file can be provided and the SQLite database will be opened instead.

For example, with the shell:

```sql
$ > duckdb data/db/sakila.db 
D SHOW tables;
┌────────────┐
│    name    │
│  varchar   │
├────────────┤
│ actor      │
│ address    │
│ category   │
│    ·       │
│ staff_list │
│ store      │
├────────────┤
│  21 rows   │
│ (5 shown)  │
└────────────┘
```


## Writing Data to SQLite

In addition to reading data from SQLite, the extension also allows you to create new SQLite database files, create tables, ingest data into SQLite and make other modifications to SQLite database files using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a SQLite database to Parquet, or read data from a Parquet file into SQLite.

Below is a brief example of how to create a new SQLite database and load data into it.

```sql
ATTACH 'new_sqlite_database.db' AS sqlite_db (TYPE SQLITE);
CREATE TABLE sqlite_db.tbl(id INTEGER, name VARCHAR);
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

The resulting SQLite database can then be read into from SQLite.

```sql
$r > sqlite3 new_sqlite_database.db 
SQLite version 3.39.5 2022-10-14 20:58:05
sqlite> SELECT * FROM tbl;
id  name  
--  ------
42  DuckDB
```

Many operations on SQLite tables are supported. All these operations directly modify the SQLite database, and the result of subsequent operations can then be read using SQLite.

Below is a list of supported operations.

### CREATE TABLE

```sql
CREATE TABLE sqlite_db.tbl(id INTEGER, name VARCHAR);
```

### INSERT INTO

```sql
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

### SELECT

```sql
SELECT * FROM sqlite_db.tbl;
┌───────┬─────────┐
│  id   │  name   │
│ int64 │ varchar │
├───────┼─────────┤
│    42 │ DuckDB  │
└───────┴─────────┘
```

### COPY

```sql
COPY sqlite_db.tbl TO 'data.parquet';
COPY sqlite_db.tbl FROM 'data.parquet';
```

### UPDATE

```sql
UPDATE sqlite_db.tbl SET name='Woohoo' WHERE id=42;
```

### DELETE

```sql
DELETE FROM sqlite_db.tbl WHERE id=42;
```

### ALTER TABLE

```sql
ALTER TABLE sqlite_db.tbl ADD COLUMN k INTEGER;
```

### DROP TABLE

```sql
DROP TABLE sqlite_db.tbl;
```

### CREATE VIEW

```sql
CREATE VIEW sqlite_db.v1 AS SELECT 42;
```

### Transactions

```sql
CREATE TABLE sqlite_db.tmp(i INTEGER);
BEGIN;
INSERT INTO sqlite_db.tmp VALUES (42);
SELECT * FROM sqlite_db.tmp;
┌───────┐
│   i   │
│ int64 │
├───────┤
│    42 │
└───────┘
ROLLBACK;
SELECT * FROM sqlite_db.tmp;
┌────────┐
│   i    │
│ int64  │
├────────┤
│ 0 rows │
└────────┘
```

> The old sqlite_attach function is deprecated. It is recommended to switch over to the new ATTACH syntax.

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdb/sqlite_scanner)