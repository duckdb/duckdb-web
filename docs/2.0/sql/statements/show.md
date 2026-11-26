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

## `SHOW VARIABLES`

The `SHOW VARIABLES`-statement lists the name, value (as `VARCHAR`) and data type of all [SQL-level variables]({% link docs/2.0/sql/statements/set_variable.md %}) existing in the current session.

```sql
SET VARIABLE int_var = 42;
SET VARIABLE txt_var = 'Hello';
SHOW VARIABLES;
```

| name    | value | type    |
|---------|-------|---------|
| int_var | 42    | INTEGER |
| txt_var | Hello | VARCHAR |  

> SQL-level variables that were unset by a `RESET VARIABLE`-statement cease to exist and are therefore not listed.

The list of existing SQL-level variables is also available as [`duckdb_variables()`-metadata query]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_variables).

## `SHOW EXTERNAL RESOURCES` Statement

<!-- ref: duckdb/duckdb#23736 duckdb/duckdb-web#7004 duckdb/duckdb#28398 duckdb/duckdb-web#7677 duckdb/duckdb#28383 -->

The `SHOW EXTERNAL RESOURCES` statement lists the [resource registrations]({% link docs/2.0/resources/resource_registrations.md %}) of the DuckDB instance. With `ALL`, it also lists the underlying resources that the list callbacks of the external resource types report (see [Discovery]({% link docs/2.0/resources/resource_registrations.md %}#discovery)):

```sql
SHOW [ALL] EXTERNAL RESOURCES [WITH TYPE ⟨type⟩];
```

Since DuckDB 2.0.1, `WITH TYPE` limits the listing to one external resource type, written as described in [External Resource Type Names]({% link docs/2.0/resources/resource_types.md %}#external-resource-type-names). Without `ALL`, an external resource type without resource registrations gives an empty result; with `ALL`, an external resource type that is not registered is an error.

Since DuckDB 2.0.1, `SHOW EXTERNAL RESOURCES` is a query, so it can be used as a subquery or in a CTE.

## `SHOW EXTERNAL RESOURCE TYPES` Statement

<!-- ref: duckdb/duckdb#28522 -->

> New The `SHOW EXTERNAL RESOURCE TYPES` statement was introduced in DuckDB 2.0.1.

The `SHOW EXTERNAL RESOURCE TYPES` statement lists the registered [external resource types]({% link docs/2.0/resources/resource_types.md %}), with the same columns as the `duckdb_external_resource_types()` function. It is a query, so it can be used as a subquery:

```sql
CREATE MACRO b_create(p) AS TABLE SELECT MAP {'id': 'b1'} AS handle;
CALL register_external_resource_type('b@st', kind := 'storage', create_function := 'b_create');
SELECT name, kind FROM (SHOW EXTERNAL RESOURCE TYPES);
```

| name | kind    |
|------|---------|
| b@st | storage |
