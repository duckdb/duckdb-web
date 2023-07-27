---
layout: docu
title: Parquet Import
selected: Parquet Import
---

# How to load a Parquet file into a table

To read data from a Parquet file, use the `read_parquet` function in the `FROM` clause of a query. 

```sql
SELECT * FROM read_parquet('input.parquet');
```

To create a new table using the result from a query, use `CREATE TABLE AS` from a `SELECT` statement.

```sql
CREATE TABLE new_tbl AS SELECT * FROM read_parquet('input.parquet');
```
To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement.

```sql
INSERT INTO tbl SELECT * FROM read_parquet('input.parquet');
```

Alternatively, the `COPY` statement can also be used to load data from a Parquet file into an existing table.

```sql
COPY tbl FROM 'input.parquet' (FORMAT PARQUET);
```

For additional options, see the [Parquet Loading reference](../../data/parquet).
