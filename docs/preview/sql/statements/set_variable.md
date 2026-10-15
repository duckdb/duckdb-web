---
layout: docu
railroad: statements/setvariable.js
title: SET VARIABLE and RESET VARIABLE Statements
---

DuckDB supports the definition of SQL-level variables using the `SET VARIABLE` and `RESET VARIABLE` statements.

## Variable Scopes

DuckDB supports two levels of variable scopes:

| Scope | Description |
|---|---|
| `SESSION` | Variables with a `SESSION` scope are local to you and only affect the current session. | 
| `GLOBAL` | Variables with a `GLOBAL` scope are specific [configuration option variables]({% link docs/preview/configuration/overview.md %}#global-configuration-options) that affect the entire DuckDB instance and all sessions. For example, see [Set a Global Variable]({% link docs/preview/sql/statements/set.md %}#set-a-global-variable). |

## `SET VARIABLE`

The `SET VARIABLE` statement assigns a value to a variable, which can be accessed using the `getvariable` call:

```sql
SET VARIABLE my_var = 30;
SELECT 20 + getvariable('my_var') AS total;
```

| total |
|------:|
| 50    |

> New The `$⟨variable⟩` shorthand is introduced in DuckDB 2.0.

As a shorthand for `getvariable`, a variable can be referenced directly with the `$⟨variable⟩` syntax anywhere an expression is allowed:

```sql
SET VARIABLE my_var = 30;
SELECT 20 + $my_var AS total;
```

Variable names that are not valid identifiers can be quoted, for example `$"my var"`.

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
SET VARIABLE list_of_files = (SELECT list(file) FROM csv_files);

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

The `getvariable` function can also be used in a [`COLUMNS` expression]({% link docs/preview/sql/expressions/star.md %}#columns-expression):

```sql
SET VARIABLE column_to_exclude = 'col1';
CREATE TABLE tbl AS SELECT 12 AS col0, 34 AS col1, 56 AS col2;
SELECT COLUMNS(c -> c != getvariable('column_to_exclude')) FROM tbl;
```

| col0 | col2 |
|-----:|-----:|
| 12   | 56   |

### The `$name` Shorthand

> New Referencing a variable with the `$name` shorthand is introduced in DuckDB 2.0.

As a shorthand for `getvariable`, you can reference a session variable directly with `$name`:

```sql
SET VARIABLE my_var = 30;
SELECT 20 + $my_var AS total;
```

| total |
|------:|
| 50    |

For a variable that is set, `$name` and `getvariable('name')` return the same value:

```sql
SELECT $my_var = getvariable('my_var') AS same;
```

| same |
|------|
| true |

The two forms differ when the variable is not set: `getvariable` returns `NULL`, while a `$name` reference raises an error.

```sql
SELECT $undefined_var;
```

```console
Invalid Input Error:
Values were not provided for the following parameters: undefined_var
```

This is because `$name` is a [prepared statement parameter]({% link docs/preview/sql/query_syntax/prepared_statements.md %}) that is filled from the session variable of the same name. This also lets variables act as [default values for prepared statements]({% link docs/preview/sql/query_syntax/prepared_statements.md %}#session-variables-as-default-values).

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
