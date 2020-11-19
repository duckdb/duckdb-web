---
layout: docu
title: Select Statement
selected: Documentation/SQL/Select
expanded: SQL
railroad: statements/select.js
---
The `SELECT` statement retrieves rows from the database.

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
The `SELECT` statement retrieves rows from the database. The canonical order of a select statement is as follows:

```sql
SELECT select_list
FROM tables
WHERE condition
GROUP BY groups
HAVING group_filter
ORDER BY order_expr
LIMIT n
```

Optionally, the `SELECT` statement can be prefixed with a `WITH` clause.

As the `SELECT` statement is so complex, we have split up the syntax diagrams into several parts. The full syntax diagram can be found at the bottom of the page.

## SELECT clause
<div id="rrdiagram3"></div>

The `SELECT` clause specifies the list of columns that will be returned by the query. While it appears first in the clause, *logically* the expressions here are executed only at the end. The `SELECT` clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions.

## FROM clause
<div id="rrdiagram4"></div>

The `FROM` clause specifies the *source* of the data on which the remainder of the query should operate. Logically, the `FROM` clause is where the query starts execution. The `FROM` clause can contain a single table, a combination of multiple tables that are joined together, or another `SELECT` query inside a subquery node.

## WHERE clause
<div id="rrdiagram5"></div>

The `WHERE` clause specifies any filters to apply to the data. This allows you to select only a subset of the data in which you are interested. Logically the `WHERE` clause is applied immediately after the `FROM` clause.

## GROUP BY/HAVING clause
<div id="rrdiagram6"></div>

The `GROUP BY` clause specifies which grouping columns should be used to perform any aggregations in the `SELECT` clause. If the `GROUP BY` clause is specified, the query is always an aggregate query, even if no aggregations are present in the `SELECT` clause.

## WINDOW clause
<div id="rrdiagram7"></div>

The `WINDOW` clause allows you to specify named windows that can be used within window functions. These are useful when you have multiple window functions, as they allow you to avoid repeating the same window clause.

## ORDER BY/LIMIT clause
<div id="rrdiagram8"></div>

`ORDER BY` and `LIMIT` are output modifiers. Logically they are applied at the very end of the function. The `LIMIT` clause restricts the amount of rows fetched, and the `ORDER BY` clause sorts the rows on the sorting criteria in either ascending or descending order.

## VALUES list
<div id="rrdiagram9"></div>

A `VALUES` list is a set of values that is supplied instead of a `SELECT` statement.

## Common Table Expressions
<div id="rrdiagram2"></div>

## Full Syntax Diagram
Below is the full syntax diagram of the `SELECT` statement:

<div id="rrdiagram"></div>

