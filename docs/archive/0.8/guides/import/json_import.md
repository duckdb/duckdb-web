---
layout: docu
title: JSON Import
selected: JSON Import
---

# How to load a JSON file into a table

To read data from a JSON file, use the `read_json_auto` function in the `FROM` clause of a query. 

```sql
SELECT * FROM read_json_auto('input.json');
```

To create a new table using the result from a query, use `CREATE TABLE AS` from a `SELECT` statement.

```sql
CREATE TABLE new_tbl AS SELECT * FROM read_json_auto('input.json');
```
To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement.

```sql
INSERT INTO tbl SELECT * FROM read_json_auto('input.json');
```

Alternatively, the `COPY` statement can also be used to load data from a JSON file into an existing table.

```sql
COPY tbl FROM 'input.json';
```

For additional options, see the [JSON Loading reference](../../data/json) and the [COPY statement documentation](../../sql/statements/copy).
