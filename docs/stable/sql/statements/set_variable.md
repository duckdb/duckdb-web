---
layout: docu
railroad: statements/setvariable.js
redirect_from:
- /docs/sql/statements/set_variable
title: SET VARIABLE and RESET VARIABLE Statements
---

DuckDB supports the definition of SQL-level variables using the `SET VARIABLE` and `RESET VARIABLE` statements.

## `SET VARIABLE`

The `SET VARIABLE` statement assigns a value to a variable, which can be accessed using the `getvariable` call:

```sql
SET VARIABLE my_var = 30;
SELECT 20 + getvariable('my_var') AS total;
```

| total |
|------:|
| 50    |

If `SET VARIABLE` is invoked on an existing variable, it will overwrite its value:

```sql
SET VARIABLE my_var = 30;
SET VARIABLE my_var = 100;
SELECT 20 + getvariable('my_var') AS total;
```

| total |
|------:|
| 120   |

Variables can have different types:

```sql
SET VARIABLE my_date = DATE '2018-07-13';
SET VARIABLE my_string = 'Hello world';
SET VARIABLE my_map = MAP {'k1': 10, 'k2': 20};
```

Variables can also be assigned to results of queries:

```sql
-- write some CSV files
COPY (SELECT 42 AS a) TO 'test1.csv';
COPY (SELECT 84 AS a) TO 'test2.csv';

-- add a list of CSV files to a table
CREATE TABLE csv_files (file VARCHAR);
INSERT INTO csv_files VALUES ('test1.csv'), ('test2.csv');

-- initialize a variable with the list of csv files
SET VARIABLE list_of_files = (SELECT LIST(file) FROM csv_files);

-- read the CSV files
SELECT * FROM read_csv(getvariable('list_of_files'), filename := True);
```

| a    | filename    |
|-----:|------------:|
| 42   | test.csv    |
| 84   | test2.csv   |

If a variable is not set, the `getvariable` function returns `NULL`:

```sql
SELECT getvariable('undefined_var') AS result;
```

| result |
|--------|
| NULL   |

The `getvariable` function can also be used in a [`COLUMNS` expression]({% link docs/stable/sql/expressions/star.md %}#columns-expression):

```sql
SET VARIABLE column_to_exclude = 'col1';
CREATE TABLE tbl AS SELECT 12 AS col0, 34 AS col1, 56 AS col2;
SELECT COLUMNS(c -> c != getvariable('column_to_exclude')) FROM tbl;
```

| col0 | col2 |
|-----:|-----:|
| 12   | 56   |

### Syntax

<div id="rrdiagram1"></div>

## `RESET VARIABLE`

The `RESET VARIABLE` statement unsets a variable.

```sql
SET VARIABLE my_var = 30;
RESET VARIABLE my_var;
SELECT getvariable('my_var') AS my_var;
```

| my_var |
|--------|
| NULL   |

### Syntax

<div id="rrdiagram2"></div>