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

## `SHOW EXTERNAL RESOURCES` Statement

> New Support for listing external resources was introduced in DuckDB 2.0.

`SHOW EXTERNAL RESOURCES` lists external resources that are currently registered in the session.
`SHOW ALL EXTERNAL RESOURCES` also discovers remote resources by calling each registered resource type's list callback (equivalent to `duckdb_external_resources(discover := true)`).

```sql
SHOW EXTERNAL RESOURCES;
SHOW ALL EXTERNAL RESOURCES;
```

### Filtering by Type

Append `WITH TYPE` to restrict the listing (and, with `ALL`, discovery) to one resource type.
This is syntactic sugar for the `type` argument of `duckdb_external_resources`, so the statement can also be used as a subquery:

```sql
SHOW EXTERNAL RESOURCES WITH TYPE 'aws:s3tables:table-bucket';
SHOW ALL EXTERNAL RESOURCES WITH TYPE 'aws:s3tables:table-bucket';

SELECT count(*)
FROM (SHOW ALL EXTERNAL RESOURCES WITH TYPE 'aws:s3tables:table-bucket');
```

A bare identifier is accepted as the type name when the type is a plain name (no special characters).
Quoted string literals are matched exactly.

Without `ALL`, `WITH TYPE` only filters already-registered resources and does not run discovery callbacks.
With `SHOW ALL ... WITH TYPE`, discovering an unknown type returns an error.

