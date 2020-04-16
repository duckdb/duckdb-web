---
layout: default
title: DROP Statement
selected: Documentation/SQL/DROP
expanded: SQL
railroad: drop.js
---
# DROP Statement
DROP - delete a catalog entry.

### Examples
```sql
-- delete the table with the name "tbl"
DROP TABLE tbl;
-- drop the view with the name "v1"; do not throw an error if the view does not exist
DROP VIEW IF EXISTS v1;
```

### Syntax
<div id="rrdiagram"></div>
