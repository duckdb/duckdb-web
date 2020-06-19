---
layout: docu
title: Parquet
---
Parquet files are compressed columnar files that are efficient to load and process. They are typically produced from Spark, but can be produced in other manners as well. DuckDB includes an efficient Parquet reader in the form of the `parquet_scan` function.

```sql
SELECT * FROM parquet_scan('test.parquet');
```

Unlike CSV files, parquet files are structured and as such are unambiguous to read. No parameters need to be passed to this function. The `parquet_scan` function will figure out the column names and column types present in the file and emit them.

You can also insert the data into a table or create a table from the parquet file directly. This will load the data from the parquet file and insert it into the database.

```sql
-- insert the data from the parquet file in the table
INSERT INTO people SELECT * FROM parquet_scan('test.parquet');
-- create a table directly from a parquet file
CREATE TABLE people AS SELECT * FROM parquet_scan('test.parquet');
```

If you wish to keep the data stored inside the parquet file, but want to query the parquet file directly, you can create a view over the `parquet_scan` function. You can then query the parquet file as if it were a built-in table.

```sql
-- create a view over the parquet file
CREATE VIEW people AS SELECT * FROM parquet_scan('test.parquet');
-- query the parquet file
SELECT * FROM people;
```

# Partial Reading
DuckDB supports projection pushdown into the Parquet file itself. That is to say, when querying a Parquet file, only the columns required for the query are read. This allows you to read only the part of the Parquet file that you are interested in. This will be done automatically by the system.