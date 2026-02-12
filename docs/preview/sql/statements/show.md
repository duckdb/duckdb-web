---
layout: docu
title: SHOW, SHOW DATABASES, and SHOW SCHEMAS Statements
---

## `SHOW` Statement

The `SHOW` statement is an alias for [`DESCRIBE`]({% link docs/preview/sql/statements/describe.md %}).
It shows the schema of a table, view or query.

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

> This statement was introduced in DuckDB v1.5.

The `SHOW SCHEMAS` statement shows a list of all schemas across non-internal databases:

```sql
SHOW SCHEMAS;
```

| database_name | schema_name        | current |
|---------------|--------------------|---------|
| memory        | main               | true    |
| memory        | pg_catalog         | false   |
| memory        | information_schema | false   |

The `current` column indicates which schema is the default schema (set via the [`USE` statement]({% link docs/preview/sql/statements/use.md %})).
