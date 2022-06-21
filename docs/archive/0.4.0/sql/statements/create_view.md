---
layout: docu
title: Create View
selected: Documentation/SQL/Create View
expanded: SQL
railroad: statements/createview.js
---
The `CREATE VIEW` statement defines a new view in the catalog.

### Examples
```sql
-- create a simple view
CREATE VIEW v1 AS SELECT * FROM tbl;
-- create a view or replace it if a view with that name already exists
CREATE OR REPLACE VIEW v1 AS SELECT 42;
-- create a view and replace the column names
CREATE VIEW v1(a) AS SELECT 42;
```

### Syntax
<div id="rrdiagram"></div>

`CREATE VIEW` defines a view of a query. The view is not physically materialized. Instead, the query is run every time the view is referenced in a query.

`CREATE OR REPLACE VIEW` is similar, but if a view of the same name already exists, it is replaced.

If a schema name is given then the view is created in the specified schema. Otherwise it is created in the current schema. Temporary views exist in a special schema, so a schema name cannot be given when creating a temporary view. The name of the view must be distinct from the name of any other view or table in the same schema.

