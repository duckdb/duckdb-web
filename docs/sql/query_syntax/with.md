---
layout: docu
title: WITH Clause
selected: Documentation/SQL/Query Syntax/With
expanded: SQL
railroad: query_syntax/with.js
---
The `WITH` clause allows you to specify common table expressions (CTEs). Regular (non-recursive) common-table-expressions are essentially views that are limited in scope to a particular query. CTEs can reference each-other.

### Examples

```sql
-- create a CTE called "cte" and use it in the main query
WITH cte AS (SELECT 42)
SELECT * FROM cte;
-- create two CTEs, where the second CTE references the first CTE
WITH cte AS (SELECT 42 AS i),
     cte2 AS (SELECT i*100 FROM cte)
SELECT * FROM cte2;
```


## Common Table Expressions
<div id="rrdiagram"></div>
