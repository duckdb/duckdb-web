---
github_repository: https://github.com/duckdb/duckdb-sqlite
layout: docu
redirect_from:
- docs/archive/1.1/extensions/sqlite_scanner
title: SQLite Extension
---

The SQLite extension allows DuckDB to directly read and write data from a SQLite database file. The data can be queried directly from the underlying SQLite tables. Data can be loaded from SQLite tables into DuckDB tables, or vice versa.

## Installing and Loading

The `sqlite` extension will be transparently [autoloaded]({% link docs/archive/1.1/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL sqlite;
LOAD sqlite;
```

## Usage

To make a SQLite file accessible to DuckDB, use the `ATTACH` statement with the `SQLITE` or `SQLITE_SCANNER` type. Attached SQLite databases support both read and write operations.

For example, to attach to the [`sakila.db` file](https://github.com/duckdb/sqlite_scanner/raw/main/data/db/sakila.db), run:

```sql
ATTACH 'sakila.db' (TYPE SQLITE);
USE sakila;
```

The tables in the file can be read as if they were normal DuckDB tables, but the underlying data is read directly from the SQLite tables in the file at query time.

```sql
SHOW TABLES;
```

<div class="monospace_table"></div>

|          name          |
|------------------------|
| actor                  |
| address                |
| category               |
| city                   |
| country                |
| customer               |
| customer_list          |
| film                   |
| film_actor             |
| film_category          |
| film_list              |
| film_text              |
| inventory              |
| language               |
| payment                |
| rental                 |
| sales_by_film_category |
| sales_by_store         |
| staff                  |
| staff_list             |
| store                  |

You can query the tables using SQL, e.g., using the example queries from [`sakila-examples.sql`](https://github.com/duckdb/sqlite_scanner/blob/main/data/sql/sakila-examples.sql):

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

1. If the declared type contains the string `INT` then it is translated into the type `BIGINT`
2. If the declared type of the column contains any of the strings `CHAR`, `CLOB`, or `TEXT` then it is translated into `VARCHAR`.
3. If the declared type for a column contains the string `BLOB` or if no type is specified then it is translated into `BLOB`.
4. If the declared type for a column contains any of the strings `REAL`, `FLOA`, `DOUB`, `DEC` or `NUM` then it is translated into `DOUBLE`.
5. If the declared type is `DATE`, then it is translated into `DATE`.
6. If the declared type contains the string `TIME`, then it is translated into `TIMESTAMP`.
7. If none of the above apply, then it is translated into `VARCHAR`.

As DuckDB enforces the corresponding columns to contain only correctly typed values, we cannot load the string “hello” into a column of type `BIGINT`. As such, an error is thrown when reading from the “numbers” table above:

```console
Mismatch Type Error: Invalid type in column "i": column was declared as integer, found "hello" of type "text" instead.
```

This error can be avoided by setting the `sqlite_all_varchar` option:

```sql
SET GLOBAL sqlite_all_varchar = true;
```

When set, this option overrides the type conversion rules described above, and instead always converts the SQLite columns into a `VARCHAR` column. Note that this setting must be set *before* `sqlite_attach` is called.

## Opening SQLite Databases Directly

SQLite databases can also be opened directly and can be used transparently instead of a DuckDB database file. In any client, when connecting, a path to a SQLite database file can be provided and the SQLite database will be opened instead.

For example, with the shell, a SQLite database can be opened as follows:

```bash
duckdb sakila.db
```

```sql
SELECT first_name
FROM actor
LIMIT 3;
```

| first_name |
|------------|
| PENELOPE   |
| NICK       |
| ED         |

## Writing Data to SQLite

In addition to reading data from SQLite, the extension also allows you to create new SQLite database files, create tables, ingest data into SQLite and make other modifications to SQLite database files using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a SQLite database to Parquet, or read data from a Parquet file into SQLite.

Below is a brief example of how to create a new SQLite database and load data into it.

```sql
ATTACH 'new_sqlite_database.db' AS sqlite_db (TYPE SQLITE);
CREATE TABLE sqlite_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

The resulting SQLite database can then be read into from SQLite.

```bash
sqlite3 new_sqlite_database.db
```

```sql
SQLite version 3.39.5 2022-10-14 20:58:05
sqlite> SELECT * FROM tbl;
```

```text
id  name  
--  ------
42  DuckDB
```

Many operations on SQLite tables are supported. All these operations directly modify the SQLite database, and the result of subsequent operations can then be read using SQLite.

## Concurrency

DuckDB can read or modify a SQLite database while DuckDB or SQLite reads or modifies the same database from a different thread or a separate process. More than one thread or process can read the SQLite database at the same time, but only a single thread or process can write to the database at one time. Database locking is handled by the SQLite library, not DuckDB. Within the same process, SQLite uses mutexes. When accessed from different processes, SQLite uses file system locks. The locking mechanisms also depend on SQLite configuration, like WAL mode. Refer to the [SQLite documentation on locking](https://www.sqlite.org/lockingv3.html) for more information.

> Warning Linking multiple copies of the SQLite library into the same application can lead to application errors. See [sqlite_scanner Issue #82](https://github.com/duckdb/sqlite_scanner/issues/82) for more information.

## Supported Operations

Below is a list of supported operations.

### `CREATE TABLE`

```sql
CREATE TABLE sqlite_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM sqlite_db.tbl;
```

| id |  name  |
|---:|--------|
| 42 | DuckDB |

### `COPY`

```sql
COPY sqlite_db.tbl TO 'data.parquet';
COPY sqlite_db.tbl FROM 'data.parquet';
```

### `UPDATE`

```sql
UPDATE sqlite_db.tbl SET name = 'Woohoo' WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM sqlite_db.tbl WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE sqlite_db.tbl ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE sqlite_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW sqlite_db.v1 AS SELECT 42;
```

### Transactions

```sql
CREATE TABLE sqlite_db.tmp (i INTEGER);
```

```sql
BEGIN;
INSERT INTO sqlite_db.tmp VALUES (42);
SELECT * FROM sqlite_db.tmp;
```

| i  |
|---:|
| 42 |

```sql
ROLLBACK;
SELECT * FROM sqlite_db.tmp;
```

| i |
|--:|
|   |

> Deprecated The old `sqlite_attach` function is deprecated. It is recommended to switch over to the new [`ATTACH` syntax]({% link docs/archive/1.1/sql/statements/attach.md %}).