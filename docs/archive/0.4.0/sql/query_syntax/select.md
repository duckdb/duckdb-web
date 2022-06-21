---
layout: docu
title: SELECT Clause
selected: Documentation/SQL/Query Syntax/Select
expanded: SQL
railroad: query_syntax/select.js
blurb: The SELECT clause specifies the list of columns that will be returned by the query.
---
The `SELECT` clause specifies the list of columns that will be returned by the query. While it appears first in the clause, *logically* the expressions here are executed only at the end. The `SELECT` clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions.

### Examples

```sql
-- select all columns from the table called "table_name"
SELECT * FROM table_name;
-- select all unique cities from the addresses table
SELECT DISTINCT city FROM addresses;
-- return the total number of rows in the addresses table
SELECT COUNT(*) FROM addresses;
-- select all columns except the city column from the addresses table
SELECT * EXCLUDE (city) FROM addresses;
-- select all columns from the addresses table, but replace city with LOWER(city)
SELECT * REPLACE (LOWER(city) AS city) FROM addresses;
```

### Syntax
<div id="rrdiagram"></div>
