---
layout: docu
title: CSV Import
---

To read data from a CSV file, use the `read_csv` function in the `FROM` clause of a query:

```sql
SELECT * FROM read_csv('input.csv');
```

Alternatively, you can omit the `read_csv` function and let DuckDB infer it from the extension:

```sql
SELECT * FROM 'input.csv';
```

To create a new table using the result from a query, use [`CREATE TABLE ... AS SELECT` statement]({% link docs/lts/sql/statements/create_table.md %}#create-table--as-select-ctas):

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM read_csv('input.csv');
```

We can use DuckDB's [optional `FROM`-first syntax]({% link docs/lts/sql/query_syntax/from.md %}) to omit `SELECT *`:

```sql
CREATE TABLE new_tbl AS
    FROM read_csv('input.csv');
```

To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement:

```sql
INSERT INTO tbl
    SELECT * FROM read_csv('input.csv');
```

Alternatively, the `COPY` statement can also be used to load data from a CSV file into an existing table:

```sql
COPY tbl FROM 'input.csv';
```

For additional options, see the [CSV import reference]({% link docs/lts/data/csv/overview.md %}) and the [`COPY` statement documentation]({% link docs/lts/sql/statements/copy.md %}).
