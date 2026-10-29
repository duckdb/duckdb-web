---
layout: docu
redirect_from:
- /docs/stable/sql/statements/show
- /docs/current/sql/statements/show
- /docs/lts/sql/statements/show
- /docs/preview/sql/statements/show
title: SHOW, SHOW DATABASES, and SHOW SCHEMAS Statements
---

## `SHOW` Statement

The `SHOW` statement can also show the schema of a table, view, or query, like [`DESCRIBE`]({% link docs/2.0/sql/statements/describe.md %}).

> Deprecated Using `SHOW` to describe a table, view, or query is deprecated as of DuckDB 2.0 and prints a warning. Use [`DESCRIBE`]({% link docs/2.0/sql/statements/describe.md %}) instead.

> New The following feature was introduced in DuckDB 2.0.

`SHOW` can also print a [configuration setting]({% link docs/2.0/configuration/overview.md %}) when the name is not a table (PostgreSQL-style):

```sql
SET threads = 42;
SHOW threads;
```

| threads |
|---------|
| 42      |

If both a table and a setting share the name, `SHOW` describes the table and prints a deprecation warning (use [`DESCRIBE`]({% link docs/2.0/guides/meta/describe.md %}) for tables). `DESCRIBE` never resolves a setting.

The `show_behavior` setting configures how `SHOW` resolves a bare identifier:

* `'auto'` (default): describe a table if one exists, otherwise show the setting.
* `'table'`: always describe a table.
* `'setting'`: always show a setting.

```sql
SET show_behavior = 'setting';
```

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

| database_name | schema_name | current |
|---------------|-------------|---------|
| memory        | main        | true    |

The `current` column indicates which schema is the default schema (set via the [`USE` statement]({% link docs/2.0/sql/statements/use.md %})).
