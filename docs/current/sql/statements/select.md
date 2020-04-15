---
layout: default
title: Select Statement
selected: Documentation/SQL/Select
expanded: SQL
railroad: select.js
---
# Select Statement
SELECT - query the contents of the database (read-only)

### Examples
```sql
-- select all columns from the table "tbl"
SELECT * FROM tbl;
-- select the rows from tbl
SELECT j FROM tbl WHERE i=3;
-- perform an aggregate grouped by the column "i"
SELECT i, SUM(j) FROM tbl GROUP BY i;
-- select only the top 3 rows from the tbl
SELECT * FROM tbl ORDER BY i DESC LIMIT 3;
-- join two tables together using the USING clause
SELECT * FROM t1 JOIN t2 USING(a, b);
```

### Syntax
<div id="rrdiagram"></div>

The SELECT statement issues a query to the database.