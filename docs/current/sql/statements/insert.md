---
layout: default
title: Insert Statement
selected: Documentation/SQL/Insert
expanded: SQL
railroad: insert.js
---
# Insert Statement
INSERT INTO - insert a set of rows into a single table of the database.

### Examples
```sql
-- insert the values (1), (2), (3) into "tbl
INSERT INTO tbl VALUES (1), (2), (3);
-- insert the result of a query into a table
INSERT INTO tbl SELECT * FROM other_tbl;
-- insert values into the "i" column, inserting the default value into other columns
INSERT INTO tbl(i) VALUES (1), (2), (3);
-- explicitly insert the default value into a column
INSERT INTO tbl(i) VALUES (1), (DEFAULT), (3);
```

### Syntax
<div id="rrdiagram"></div>
