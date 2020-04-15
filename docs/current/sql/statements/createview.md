---
layout: default
title: Create View
selected: Documentation/SQL/Create View
expanded: SQL
railroad: createview.js
---
# Create View Statement
CREATE View - this statement creates an empty view in the catalog.

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
