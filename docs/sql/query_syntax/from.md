---
layout: docu
title: FROM Clause
selected: Documentation/SQL/Query Syntax/From
expanded: SQL
railroad: query_syntax/from.js
---
The `FROM` clause specifies the *source* of the data on which the remainder of the query should operate. Logically, the `FROM` clause is where the query starts execution. The `FROM` clause can contain a single table, a combination of multiple tables that are joined together, or another `SELECT` query inside a subquery node.

### Examples

```sql
-- select all columns from the table called "table_name"
SELECT * FROM table_name;
-- select all columns from the table called "table_name" in the schema "schema_name
SELECT * FROM schema_name.table_name;
-- select the column "i" from the table function "range", where the first column of the range function is renamed to "i"
SELECT t.i FROM range(100) AS t(i);
-- select all columns from the CSV file called "test.csv"
SELECT * FROM 'test.csv';
-- select all columns from a subquery
SELECT * FROM (SELECT * FROM table_name);
-- join two tables together
SELECT * FROM table_name JOIN other_table ON (table_name.key = other_table.key);
-- select a 10% sample from a table
SELECT * FROM table_name TABLESAMPLE 10%;
-- select a sample of 10 rows from a table
SELECT * FROM table_name TABLESAMPLE 10 ROWS;
```

### Syntax
<div id="rrdiagram"></div>
