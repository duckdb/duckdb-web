---
layout: docu
title: SHOW and SHOW DATABASE Statements
---

## `SHOW` Statement

The `SHOW` statement is an alias for [`DESCRIBE`]({% link docs/stable/sql/statements/describe.md %}).
It shows the schema of a table, view or query.

## `SHOW DATABASES` Statement

The `SHOW DATABASES` statement show as list of all attached databases:

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
