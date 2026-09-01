---
layout: docu
railroad: statements/createview.js
redirect_from:
- /docs/preview/sql/statements/create_view
- /docs/sql/statements/create_view
- /docs/stable/sql/statements/create_view
title: CREATE VIEW Statement
---

The `CREATE VIEW` statement defines a new view in the catalog.

## Examples

Create a simple view:

```sql
CREATE VIEW view1 AS SELECT * FROM tbl;
```

Create a view or replace it if a view with that name already exists:

```sql
CREATE OR REPLACE VIEW view1 AS SELECT 42;
```

Create a view and replace the column names:

```sql
CREATE VIEW view1(a) AS SELECT 42;
```

Create a secure view (hides internals from functions such as `stats()` and `EXPLAIN ANALYZE`):

```sql
CREATE SECURE VIEW users AS
    SELECT username FROM all_users WHERE access_level = 'standard';
```

The SQL query behind an existing view can be read using the [`duckdb_views()` function]({% link docs/current/sql/meta/duckdb_table_functions.md %}#duckdb_views) like this:

```sql
SELECT sql FROM duckdb_views() WHERE view_name = 'view1';
```

## Syntax

<div id="rrdiagram"></div>

`CREATE VIEW` defines a view of a query. The view is not physically materialized. Instead, the query is run every time the view is referenced in a query.

`CREATE OR REPLACE VIEW` is similar, but if a view of the same name already exists, it is replaced.

`CREATE SECURE VIEW` defines a view that does not leak information about the underlying tables through statistics or query plans. Regular views can expose data that the view query would filter out (for example via `stats()`). Secure views return `NULL` for those internals and show a `Secure View` node in `EXPLAIN ANALYZE`.

If a schema name is given then the view is created in the specified schema. Otherwise, it is created in the current schema. Temporary views exist in a special schema, so a schema name cannot be given when creating a temporary view. The name of the view must be distinct from the name of any other view or table in the same schema.
