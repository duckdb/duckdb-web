---
layout: docu
title: SELECT Statement
railroad: statements/select.js
blurb: The SELECT statement retrieves rows from the database.
---

The `SELECT` statement retrieves rows from the database.

### Examples

Select all columns from the table `tbl`:

```sql
SELECT * FROM tbl;
```

Select the rows from `tbl`:

```sql
SELECT j FROM tbl WHERE i = 3;
```

Perform an aggregate grouped by the column `i`:

```sql
SELECT i, sum(j) FROM tbl GROUP BY i;
```

Select only the top 3 rows from the `tbl`:

```sql
SELECT * FROM tbl ORDER BY i DESC LIMIT 3;
```

Join two tables together using the `USING` clause:

```sql
SELECT * FROM t1 JOIN t2 USING (a, b);
```

Use column indexes to select the first and third column from the table `tbl`:

```sql
SELECT #1, #3 FROM tbl;
```

Select all unique cities from the addresses table:

```sql
SELECT DISTINCT city FROM addresses;
```

Return a `STRUCT` by using a row variable:

```sql
SELECT d
FROM (SELECT 1 AS a, 2 AS b) d;
```

### Syntax

The `SELECT` statement retrieves rows from the database. The canonical order of a `SELECT` statement is as follows, with less common clauses being indented:

```sql
SELECT ⟨select_list⟩
FROM ⟨tables⟩
    USING SAMPLE ⟨sample_expression⟩
WHERE ⟨condition⟩
GROUP BY ⟨groups⟩
HAVING ⟨group_filter⟩
    WINDOW ⟨window_expression⟩
    QUALIFY ⟨qualify_filter⟩
ORDER BY ⟨order_expression⟩
LIMIT ⟨n⟩;
```

Optionally, the `SELECT` statement can be prefixed with a [`WITH` clause]({% link docs/sql/query_syntax/with.md %}).

As the `SELECT` statement is so complex, we have split up the syntax diagrams into several parts. The full syntax diagram can be found at the bottom of the page.

## `SELECT` Clause

<div id="rrdiagram3"></div>

The [`SELECT` clause]({% link docs/sql/query_syntax/select.md %}) specifies the list of columns that will be returned by the query. While it appears first in the clause, *logically* the expressions here are executed only at the end. The `SELECT` clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions. The `DISTINCT` keyword ensures that only unique tuples are returned.

> Column names are case-insensitive. See the [Rules for Case Sensitivity]({% link docs/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity) for more details.

## `FROM` Clause

<div id="rrdiagram4"></div>

The [`FROM` clause]({% link docs/sql/query_syntax/from.md %}) specifies the *source* of the data on which the remainder of the query should operate. Logically, the `FROM` clause is where the query starts execution. The `FROM` clause can contain a single table, a combination of multiple tables that are joined together, or another `SELECT` query inside a subquery node.

## `SAMPLE` Clause

<div id="rrdiagram10"></div>

The [`SAMPLE` clause]({% link docs/sql/query_syntax/sample.md %}) allows you to run the query on a sample from the base table. This can significantly speed up processing of queries, at the expense of accuracy in the result. Samples can also be used to quickly see a snapshot of the data when exploring a data set. The `SAMPLE` clause is applied right after anything in the `FROM` clause (i.e., after any joins, but before the where clause or any aggregates). See the [Samples]({% link docs/sql/samples.md %}) page for more information.

## `WHERE` Clause

<div id="rrdiagram5"></div>

The [`WHERE` clause]({% link docs/sql/query_syntax/where.md %}) specifies any filters to apply to the data. This allows you to select only a subset of the data in which you are interested. Logically the `WHERE` clause is applied immediately after the `FROM` clause.

## `GROUP BY` and `HAVING` Clauses

<div id="rrdiagram6"></div>

The [`GROUP BY` clause]({% link docs/sql/query_syntax/groupby.md %}) specifies which grouping columns should be used to perform any aggregations in the `SELECT` clause. If the `GROUP BY` clause is specified, the query is always an aggregate query, even if no aggregations are present in the `SELECT` clause.

## `WINDOW` Clause

<div id="rrdiagram7"></div>

The [`WINDOW` clause]({% link docs/sql/query_syntax/window.md %}) allows you to specify named windows that can be used within window functions. These are useful when you have multiple window functions, as they allow you to avoid repeating the same window clause.

## `QUALIFY` Clause

<div id="rrdiagram11"></div>

The [`QUALIFY` clause]({% link docs/sql/query_syntax/qualify.md %}) is used to filter the result of [`WINDOW` functions]({% link docs/sql/functions/window_functions.md %}).

## `ORDER BY`, `LIMIT` and `OFFSET` Clauses

<div id="rrdiagram8"></div>

[`ORDER BY`]({% link docs/sql/query_syntax/orderby.md %}), [`LIMIT` and `OFFSET`]({% link docs/sql/query_syntax/limit.md %}) are output modifiers.
Logically they are applied at the very end of the query.
The `ORDER BY` clause sorts the rows on the sorting criteria in either ascending or descending order.
The `LIMIT` clause restricts the amount of rows fetched, while the `OFFSET` clause indicates at which position to start reading the values.

## `VALUES` List

<div id="rrdiagram9"></div>

[A `VALUES` list]({% link docs/sql/query_syntax/values.md %}) is a set of values that is supplied instead of a `SELECT` statement.

## Row IDs

For each table, the [`rowid` pseudocolumn](https://docs.oracle.com/cd/B19306_01/server.102/b14200/pseudocolumns008.htm) returns the row identifiers based on the physical storage.

```sql
CREATE TABLE t (id INTEGER, content VARCHAR);
INSERT INTO t VALUES (42, 'hello'), (43, 'world');
SELECT rowid, id, content FROM t;
```

| rowid | id | content |
|------:|---:|---------|
| 0     | 42 | hello   |
| 1     | 43 | world   |

In the current storage, these identifiers are contiguous unsigned integers (0, 1, ...) if no rows were deleted. Deletions introduce gaps in the rowids which may be reclaimed later:

```sql
CREATE OR REPLACE TABLE t AS (FROM range(10) r(i));
DELETE FROM t WHERE i % 2 = 0;
SELECT rowid FROM t;
```

| rowid |
|------:|
| 1     |
| 3     |
| 5     |
| 7     |
| 9     |

It is strongly to *avoid using rowids as identifiers*.

> Tip The `rowid` values are stable within a transaction.

> If there is a user-defined column named `rowid`, it shadows the `rowid` pseudocolumn.

## Common Table Expressions

<div id="rrdiagram2"></div>

## Full Syntax Diagram

Below is the full syntax diagram of the `SELECT` statement:

<div id="rrdiagram"></div>
