---
layout: docu
title: CSV Import
selected: CSV Import
---

# How to load a CSV file into a table

To read data from a CSV file, use the `read_csv_auto` function in the `FROM` clause of a query. 

```sql
SELECT * FROM read_csv_auto('input.csv');
```

To create a new table using the result from a query, use `CREATE TABLE AS` from a `SELECT` statement.

```sql
CREATE TABLE new_tbl AS SELECT * FROM read_csv_auto('input.csv');
```
To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement.

```sql
INSERT INTO tbl SELECT * FROM read_csv_auto('input.csv');
```

Alternatively, the `COPY` statement can also be used to load data from a CSV file into an existing table.

```sql
COPY tbl FROM 'input.csv';
```

For additional options, see the [CSV Loading reference](/docs/data/csv) and the [COPY statement documentation](/docs/sql/statements/copy).
