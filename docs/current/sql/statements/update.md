---
layout: default
title: Update Statement
selected: Documentation/SQL/Update
expanded: SQL
railroad: update.js
---
# Update Statement
UPDATE - change the value of rows in a

### Examples
```sql
-- for every row where "i" is NULL, set the value to 0 instead
UPDATE tbl SET i=0 WHERE i IS NULL;
-- set all values of "i" to 1 and all values of "j" to 2
UPDATE tbl SET i=1, j = 2;
```

### Syntax
<div id="rrdiagram"></div>
