---
layout: docu
title: SQLite Scanner
selected: Documentation/SQLite Scanner
---

The `sqlite` extension allows DuckDB to directly read data from a SQLite database file. The data can be queried directly from the underlying SQLite tables, or read into DuckDB tables.

## Loading the Extension

In order to use the SQLite extension it must first be installed and loaded. This can be done using the following commands:

```sql
INSTALL sqlite;
LOAD sqlite;
```

## Usage

To make a SQLite file accessible to DuckDB, use the `ATTACH` command, for example with the bundled `sakila.db` file:

```sql
CALL sqlite_attach('sakila.db');
```

The tables in the file are registered as views in DuckDB, you can list them as follows:

```sql
PRAGMA show_tables;
```
```
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

Then you can query those views normally using SQL, e.g. using the example queries from sakila-examples.sql

```sql
SELECT cat.name category_name, 
       Sum(Ifnull(pay.amount, 0)) revenue 
FROM   category cat 
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
GROUP  BY cat.name 
ORDER  BY revenue DESC 
LIMIT  5; 
```

## Querying individual tables

Instead of attaching, you can also query individual tables using the `sqlite_scan` function.

```sql
SELECT * FROM sqlite_scan('sakila.db', 'film');
```

## Data Types

SQLite is a [weakly typed database system](https://www.sqlite.org/datatype3.html). As such, when storing data in a SQLite table, types are not enforced. The following is valid SQL in SQLite:

```sql
CREATE TABLE numbers(i INTEGER);
INSERT INTO numbers VALUES ('hello');
```

DuckDB is a strongly typed database system, as such, it requires all columns to have defined types and the system rigorously checks data for correctness.

When querying SQLite using DuckDB, a mapping of column types must be chosen. DuckDB follows SQLite's [type affinity rules](https://www.sqlite.org/datatype3.html#type_affinity) with a few extensions.

1. If the declared type contains the string "INT" then it is translated into the type `BIGINT`
2. If the declared type of the column contains any of the strings "CHAR", "CLOB", or "TEXT" then it is translated into `VARCHAR`.
3. If the declared type for a column contains the string "BLOB" or if no type is specified then it is translated into `BLOB`.
4. If the declared type for a column contains any of the strings "REAL", "FLOA", "DOUB", "DEC" or "NUM" then it is translated into `DOUBLE`.
5. If the declared type is "DATE", then it is translated into `DATE`.
6. If the declared type contains the string "TIME", then it is translated into `TIMESTAMP`.
7. If none of the above apply, then it is translated into `VARCHAR`.

As DuckDB enforces the corresponding columns to contain only correctly typed values, we cannot load the string "hello" into a column of type `BIGINT`. As such, an error is thrown when reading from the "numbers" table above:

> Error: Mismatch Type Error: Invalid type in column "i": column was declared as integer, found "hello" of type "text" instead.

This error can be avoided by setting the `sqlite_all_varchar` option:

```sql
SET GLOBAL sqlite_all_varchar=true;
```

When set, this option overrides the type conversion rules described above, and instead always converts the SQLite columns into a `VARCHAR` column. Note that this setting must be set *before* `sqlite_attach` is called.

## Running more than once

If you want to run the `sqlite_scan` procedure more than once in the same DuckDB session, you'll need to pass in the `overwrite` flag, as shown below:

```sql
CALL sqlite_attach('sakila.db', overwrite=true);
```

## Extra Information
See [the repo](https://github.com/duckdblabs/sqlite_scanner) for the source code of the extension.
