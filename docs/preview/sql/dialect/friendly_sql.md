---
layout: docu
title: Friendly SQL
---

DuckDB offers several advanced SQL features and syntactic sugar to make SQL queries more concise. We refer to these colloquially as “friendly SQL”.

> Several of these features are also supported in other systems while some are (currently) exclusive to DuckDB.

## Clauses

* Creating tables and inserting data:
    * [`CREATE OR REPLACE TABLE`]({% link docs/preview/sql/statements/create_table.md %}#create-or-replace): avoid `DROP TABLE IF EXISTS` statements in scripts.
    * [`CREATE TABLE ... AS SELECT` (CTAS)]({% link docs/preview/sql/statements/create_table.md %}#create-table--as-select-ctas): create a new table from the output of a table without manually defining a schema.
    * [`INSERT INTO ... BY NAME`]({% link docs/preview/sql/statements/insert.md %}#insert-into--by-name): this variant of the `INSERT` statement allows using column names instead of positions.
    * [`INSERT OR IGNORE INTO ...`]({% link docs/preview/sql/statements/insert.md %}#insert-or-ignore-into): insert the rows that do not result in a conflict due to `UNIQUE` or `PRIMARY KEY` constraints.
    * [`INSERT OR REPLACE INTO ...`]({% link docs/preview/sql/statements/insert.md %}#insert-or-replace-into): insert the rows that do not result in a conflict due to `UNIQUE` or `PRIMARY KEY` constraints. For those that result in a conflict, replace the columns of the existing row to the new values of the to-be-inserted row.
* Describing tables and computing statistics:
    * [`DESCRIBE`]({% link docs/preview/guides/meta/describe.md %}): provides a succinct summary of the schema of a table or query.
    * [`SUMMARIZE`]({% link docs/preview/guides/meta/summarize.md %}): returns summary statistics for a table or query.
* Making SQL clauses more compact and readable:
    * [`FROM`-first syntax with an optional `SELECT` clause]({% link docs/preview/sql/query_syntax/from.md %}#from-first-syntax): DuckDB allows queries in the form of `FROM tbl` which selects all columns (performing a `SELECT *` statement).
    * [`GROUP BY ALL`]({% link docs/preview/sql/query_syntax/groupby.md %}#group-by-all): omit the group-by columns by inferring them from the list of attributes in the `SELECT` clause.
    * [`ORDER BY ALL`]({% link docs/preview/sql/query_syntax/orderby.md %}#order-by-all): shorthand to order on all columns (e.g., to ensure deterministic results).
    * [`SELECT * EXCLUDE`]({% link docs/preview/sql/expressions/star.md %}#exclude-clause): the `EXCLUDE` option allows excluding specific columns from the `*` expression.
    * [`SELECT * REPLACE`]({% link docs/preview/sql/expressions/star.md %}#replace-clause): the `REPLACE` option allows replacing specific columns with different expressions in a `*` expression.
    * [`UNION BY NAME`]({% link docs/preview/sql/query_syntax/setops.md %}#union-all-by-name): perform the `UNION` operation along the names of columns (instead of relying on positions).
    * [Prefix aliases in the `SELECT` and `FROM` clauses]({% link docs/preview/sql/query_syntax/select.md %}): write `x: 42` instead of `42 AS x` for improved readability.
* Transforming tables:
    * [`PIVOT`]({% link docs/preview/sql/statements/pivot.md %}) to turn long tables to wide tables.
    * [`UNPIVOT`]({% link docs/preview/sql/statements/unpivot.md %}) to turn wide tables to long tables.
* Defining SQL-level variables:
    * [`SET VARIABLE`]({% link docs/preview/sql/statements/set.md %}#set-variable)
    * [`RESET VARIABLE`]({% link docs/preview/sql/statements/set.md %}#reset-variable)

## Query Features

* [Column aliases in `WHERE`, `GROUP BY`, and `HAVING`]({% post_url 2022-05-04-friendlier-sql %}#column-aliases-in-where--group-by--having). (Note that column aliases cannot be used in the `ON` clause of [`JOIN` clauses]({% link docs/preview/sql/query_syntax/from.md %}#joins).)
* [`COLUMNS()` expression]({% link docs/preview/sql/expressions/star.md %}#columns-expression) can be used to execute the same expression on multiple columns:
    * [with regular expressions]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-regular-expressions)
    * [with `EXCLUDE` and `REPLACE`]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-exclude-and-replace)
    * [with lambda functions]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-lambda-functions)
* Reusable column aliases (also known as “lateral column aliases”), e.g.: `SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i)`
* Advanced aggregation features for analytical (OLAP) queries:
    * [`FILTER` clause]({% link docs/preview/sql/query_syntax/filter.md %})
    * [`GROUPING SETS`, `GROUP BY CUBE`, `GROUP BY ROLLUP` clauses]({% link docs/preview/sql/query_syntax/grouping_sets.md %})
* [`count()` shorthand]({% link docs/preview/sql/functions/aggregates.md %}) for `count(*)`

## Literals and Identifiers

* [Case-insensitivity while maintaining case of entities in the catalog]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#case-sensitivity-of-identifiers)
* [Deduplicating identifiers]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#deduplicating-identifiers)
* [Underscores as digit separators in numeric literals]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#numeric-literals)

## Data Types

* [`MAP` data type]({% link docs/preview/sql/data_types/map.md %})
* [`UNION` data type]({% link docs/preview/sql/data_types/union.md %})

## Data Import

* [Auto-detecting the headers and schema of CSV files]({% link docs/preview/data/csv/auto_detection.md %})
* Directly querying [CSV files]({% link docs/preview/data/csv/overview.md %}) and [Parquet files]({% link docs/preview/data/parquet/overview.md %})
* Loading from files using the syntax `FROM 'my.csv'`, `FROM 'my.csv.gz'`, `FROM 'my.parquet'`, etc.
* [Filename expansion (globbing)]({% link docs/preview/sql/functions/pattern_matching.md %}#globbing), e.g.: `FROM 'my-data/part-*.parquet'`

## Functions and Expressions

* [Dot operator for function chaining]({% link docs/preview/sql/functions/overview.md %}#function-chaining-via-the-dot-operator): `SELECT ('hello').upper()`
* String formatters:
    the [`format()` function with the `fmt` syntax]({% link docs/preview/sql/functions/char.md %}#fmt-syntax) and
    the [`printf() function`]({% link docs/preview/sql/functions/char.md %}#printf-syntax)
* [List comprehensions]({% post_url 2023-08-23-even-friendlier-sql %}#list-comprehensions)
* [List slicing]({% post_url 2022-05-04-friendlier-sql %}#string-slicing)
* [String slicing]({% post_url 2022-05-04-friendlier-sql %}#string-slicing)
* [`STRUCT.*` notation]({% post_url 2022-05-04-friendlier-sql %}#struct-dot-notation)
* [Simple `LIST` and `STRUCT` creation]({% post_url 2022-05-04-friendlier-sql %}#simple-list-and-struct-creation)

## Join Types

* [`ASOF` joins]({% link docs/preview/sql/query_syntax/from.md %}#as-of-joins)
* [`LATERAL` joins]({% link docs/preview/sql/query_syntax/from.md %}#lateral-joins)
* [`POSITIONAL` joins]({% link docs/preview/sql/query_syntax/from.md %}#positional-joins)

## Trailing Commas

DuckDB allows [trailing commas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas),
both when listing entities (e.g., column and table names) and when constructing [`LIST` items]({% link docs/preview/sql/data_types/list.md %}#creating-lists).
For example, the following query works:

```sql
SELECT
    42 AS x,
    ['a', 'b', 'c',] AS y,
    'hello world' AS z,
;
```

## "Top-N in Group" Queries

Computing the "top-N rows in a group" ordered by some criteria is a common task in SQL that unfortunately often requires a complex query involving window functions and/or subqueries.

To aid in this, DuckDB provides the aggregate functions [`max(arg, n)`]({% link docs/preview/sql/functions/aggregates.md %}#maxarg-n), [`min(arg, n)`]({% link docs/preview/sql/functions/aggregates.md %}#minarg-n), [`arg_max(arg, val, n)`]({% link docs/preview/sql/functions/aggregates.md %}#arg_maxarg-val-n), [`arg_min(arg, val, n)`]({% link docs/preview/sql/functions/aggregates.md %}#arg_minarg-val-n), [`max_by(arg, val, n)`]({% link docs/preview/sql/functions/aggregates.md %}#max_byarg-val-n) and [`min_by(arg, val, n)`]({% link docs/preview/sql/functions/aggregates.md %}#min_byarg-val-n) to efficiently return the "top" `n` rows in a group based on a specific column in either ascending or descending order.

For example, let's use the following table:

```sql
SELECT * FROM t1;
```

```text
┌─────────┬───────┐
│   grp   │  val  │
│ varchar │ int32 │
├─────────┼───────┤
│ a       │     2 │
│ a       │     1 │
│ b       │     5 │
│ b       │     4 │
│ a       │     3 │
│ b       │     6 │
└─────────┴───────┘
```

We want to get a list of the top-3 `val` values in each group `grp`. The conventional way to do this is to use a window function in a subquery:

```sql
SELECT array_agg(rs.val), rs.grp
FROM
    (SELECT val, grp, row_number() OVER (PARTITION BY grp ORDER BY val DESC) AS rid
    FROM t1 ORDER BY val DESC) AS rs
WHERE rid < 4
GROUP BY rs.grp;
```

```text
┌───────────────────┬─────────┐
│ array_agg(rs.val) │   grp   │
│      int32[]      │ varchar │
├───────────────────┼─────────┤
│ [3, 2, 1]         │ a       │
│ [6, 5, 4]         │ b       │
└───────────────────┴─────────┘
```

But in DuckDB, we can do this much more concisely (and efficiently!):

```sql
SELECT max(val, 3) FROM t1 GROUP BY grp;
```

```text
┌─────────────┐
│ max(val, 3) │
│   int32[]   │
├─────────────┤
│ [3, 2, 1]   │
│ [6, 5, 4]   │
└─────────────┘
```

## Related Blog Posts

* [“Friendlier SQL with DuckDB”]({% post_url 2022-05-04-friendlier-sql %}) blog post
* [“Even Friendlier SQL with DuckDB”]({% post_url 2023-08-23-even-friendlier-sql %}) blog post
* [“SQL Gymnastics: Bending SQL into Flexible New Shapes”]({% post_url 2024-03-01-sql-gymnastics %}) blog post