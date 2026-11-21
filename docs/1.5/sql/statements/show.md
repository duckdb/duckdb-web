---
layout: docu
title: SHOW, SHOW DATABASES, and SHOW SCHEMAS Statements
---

## `SHOW` Statement

The `SHOW` statement is an alias for [`DESCRIBE`]({% link docs/1.5/sql/statements/describe.md %}).
It shows the schema of a table, view, or query.

## `SHOW DATABASES` Statement

The `SHOW DATABASES` statement shows a list of all attached databases:

```sql
ATTACH 'my.duckdb' AS my_database;
SHOW DATABASES;
```

| database_name |
|---------------|
| memory        |
| my_database   |

```sql
DETACH my_database;
SHOW DATABASES;
```

| database_name |
|---------------|
| memory        |

## `SHOW SCHEMAS` Statement

> This statement was introduced in DuckDB 1.5.

The `SHOW SCHEMAS` statement shows a list of all schemas across non-internal databases:

```sql
SHOW SCHEMAS;
```

| database_name | schema_name        | current |
|---------------|--------------------|---------|
| memory        | main               | true    |
| memory        | pg_catalog         | false   |
| memory        | information_schema | false   |

The `current` column indicates which schema is the default schema (set via the [`USE` statement]({% link docs/1.5/sql/statements/use.md %})).

## `SHOW VARIABLES`

The `SHOW VARIABLES`-statement lists the name, value (as `VARCHAR`) and data type of all [SQL-level variables]({% link docs/1.5/sql/statements/set_variable.md %}) existing in the current session.

```sql
SET VARIABLE int_var = 42;
SET VARIABLE txt_var = 'Hello';
SHOW VARIABLES;
```

| name    | value | type    |
|---------|-------|---------|
| int_var | 42    | INTEGER |
| txt_var | Hello | VARCHAR |  

> Note: SQL-level variables that were unset by a `RESET VARIABLE`-statement cease to exist and are therefore not listed.

The list of existing SQL-level variables is also available as [`duckdb_variables()`-metadata query]({% link docs/1.5/sql/meta/duckdb_table_functions.md %}#duckdb_variables).