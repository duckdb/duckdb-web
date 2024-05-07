---
layout: docu
title: CREATE VIEW Statement
railroad: statements/createview.js
---

The `CREATE VIEW` statement defines a new view in the catalog.

## Examples

```sql
```

Create a simple view:

```sql
CREATE VIEW v1 AS SELECT * FROM tbl;
```

Create a view or replace it if a view with that name already exists:

```sql
CREATE OR REPLACE VIEW v1 AS SELECT 42;
```

Create a view and replace the column names:

```sql
CREATE VIEW v1(a) AS SELECT 42;
```

The SQL query behind an existing view can be read using the [`duckdb_views()` function](../../sql/duckdb_table_functions#duckdb_views) like this:

```sql
SELECT sql FROM duckdb_views() WHERE view_name = 'v1';
```

## Syntax

<div id="rrdiagram"></div>

`CREATE VIEW` defines a view of a query. The view is not physically materialized. Instead, the query is run every time the view is referenced in a query.

`CREATE OR REPLACE VIEW` is similar, but if a view of the same name already exists, it is replaced.

If a schema name is given then the view is created in the specified schema. Otherwise it is created in the current schema. Temporary views exist in a special schema, so a schema name cannot be given when creating a temporary view. The name of the view must be distinct from the name of any other view or table in the same schema.
