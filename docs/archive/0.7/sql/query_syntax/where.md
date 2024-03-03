---
layout: docu
title: WHERE Clause
selected: Documentation/SQL/Query Syntax/Where
expanded: SQL
railroad: query_syntax/where.js
---
The `WHERE` clause specifies any filters to apply to the data. This allows you to select only a subset of the data in which you are interested. Logically the `WHERE` clause is applied immediately after the `FROM` clause.

## Examples
```sql
-- select all rows that have id equal to 3
SELECT *
FROM table_name
WHERE id=3;
-- select all rows that match the given case-insensitive LIKE expression
SELECT *
FROM table_name
WHERE name ILIKE '%mark%';
-- select all rows that match the given composite expression
SELECT *
FROM table_name
WHERE id=3 OR id=7;
```

## Syntax
<div id="rrdiagram"></div>
