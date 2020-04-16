---
layout: default
title: Update Statement
selected: Documentation/SQL/Update
expanded: SQL
railroad: statements/update.js
---
# Update Statement
The UPDATE statement modifies the values of rows in a table.

### Examples
```sql
-- for every row where "i" is NULL, set the value to 0 instead
UPDATE tbl SET i=0 WHERE i IS NULL;
-- set all values of "i" to 1 and all values of "j" to 2
UPDATE tbl SET i=1, j = 2;
```

### Syntax
<div id="rrdiagram"></div>

UPDATE changes the values of the specified columns in all rows that satisfy the condition. Only the columns to be modified need be mentioned in the SET clause; columns not explicitly modified retain their previous values.

