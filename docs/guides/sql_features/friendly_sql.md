---
layout: docu
title: Friendly SQL
---

DuckDB offers several advanced SQL features as well as extensions to the SQL syntax. We call these colloquially as "friendly SQL".

> Several of these features are also supported in other systems while some are (currently) exclusive to DuckDB.

## Clauses

* [`CREATE OR REPLACE TABLE`]({% link docs/sql/statements/create_table.md %}#create-or-replace): this clause allows avoiding `DROP TABLE IF EXISTS` statements in scripts.
* [`CREATE TABLE ... AS SELECT` (CTAS)]({% link docs/sql/statements/create_table.md %}#create-table--as-select-ctas): this clause allows creating a new table from the output of a table without manually defining a schema.
* [`DESCRIBE`]({% link docs/guides/meta/describe.md %}): this clause provides a succinct summary of the schema of a table or query.
* [`FROM`-first syntax with an optional `SELECT` clause]({% link docs/sql/query_syntax/from.md %}#from-first-syntax): DuckDB allows queries in the form of `FROM tbl` which selects all columns (performing a `SELECT *` statement).
* [`GROUP BY ALL`]({% link docs/sql/query_syntax/groupby.md %}#group-by-all): this clause allows omitting the group-by columns by inferring them from the list of attributes in the `SELECT` clause.
* [`INSERT INTO ... BY NAME`]({% link docs/sql/statements/insert.md %}#insert-into--by-name): this variant of the `INSERT` statement allows using column names instead of positions.
* [`ORDER BY ALL`]({% link docs/sql/query_syntax/orderby.md %}#order-by-all): this clause allows ordering on all columns (e.g., to ensure deterministic results).
* [`PIVOT`]({% link docs/sql/statements/pivot.md %}) and [`UNPIVOT`]({% link docs/sql/statements/unpivot.md %}) allow turning long tables to wide tables and vice versa, respectively.
* [`SELECT * EXCLUDE`]({% link docs/sql/expressions/star.md %}#exclude-clause): the `EXCLUDE` option allows excluding specific columns from the `*` expression.
* [`SELECT * REPLACE`]({% link docs/sql/expressions/star.md %}#replace-clause): the `EXCLUDE` option allows replacing specific columns with different expressions in a `*` expression.
* [`SUMMARIZE`]({% link docs/guides/meta/summarize.md %}): this clause returns summary statistics for a table or query.
* [`UNION BY NAME`]({% link docs/sql/query_syntax/setops.md %}#union-all-by-name): this clause performing the `UNION` operation along the names of columns (instead of relying on positions).

## Query Features

* [Column aliases in `WHERE`, `GROUP BY`, and `HAVING`]({% link _posts/2022-05-04-friendlier-sql.md %}#column-aliases-in-where--group-by--having)
* [`COLUMNS()` expression]({% link docs/sql/expressions/star.md %}#columns-expression) can be used to execute the same expression on multiple columns:
    * [with regular expressions]({% link _posts/2023-08-23-even-friendlier-sql.md %}#columns-with-regular-expressions)
    * [with `EXCLUDE` and `REPLACE`]({% link _posts/2023-08-23-even-friendlier-sql.md %}#columns-with-exclude-and-replace)
    * [with lambda functions]({% link _posts/2023-08-23-even-friendlier-sql.md %}#columns-with-lambda-functions)
* Reusable column aliases, e.g.: `SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i)`

## Literals and Identifiers

* [Case-insensitivity while maintaining case of entities in the catalog]({% link docs/sql/keywords_and_identifiers.md %}#case-sensitivity-of-identifiers)
* [Deduplicating identifiers]({% link docs/sql/keywords_and_identifiers.md %}#deduplicating-identifiers)
* [Underscores as digit separators in numeric literals]({% link docs/sql/keywords_and_identifiers.md %}#numeric-literals)

## Data Types

* [`MAP` data type]({% link docs/sql/data_types/map.md %})
* [`UNION` data type]({% link docs/sql/data_types/union.md %})

## Data Import

* [Auto-detecting the headers and schema of CSV files]({% link docs/data/csv/auto_detection.md %})
* Directly querying [CSV files]({% link docs/data/csv/overview.md %}) and [Parquet files]({% link docs/data/parquet/overview.md %})
* Loading from files using the syntax `FROM 'my.csv'`, `FROM 'my.csv.gz'`, `FROM 'my.parquet'`, etc.
* Filename expansion (globbing), e.g.: `FROM 'my-data/part-*.parquet'`

## Functions and Expressions

* [Dot operator for function chaining]({% link docs/sql/functions/overview.md %}#function-chaining-via-the-dot-operator): `SELECT ('hello').upper()`
* String formatters: [`format()` function with the `fmt` syntax]({% link docs/sql/functions/char.md %}#fmt-syntax) and the [`printf() function`]({% link docs/sql/functions/char.md %}#printf-syntax)
* [List comprehensions]({% link _posts/2023-08-23-even-friendlier-sql.md %}#list-comprehensions)
* [List slicing]({% link _posts/2022-05-04-friendlier-sql.md %}#string-slicing)
* [String slicing]({% link _posts/2022-05-04-friendlier-sql.md %}#string-slicing)
* [`STRUCT.*` notation]({% link _posts/2022-05-04-friendlier-sql.md %}#struct-dot-notation)
* [Simple `LIST` and `STRUCT` creation]({% link _posts/2022-05-04-friendlier-sql.md %}#simple-list-and-struct-creation)

## Join Types

* [`ASOF` joins]({% link docs/sql/query_syntax/from.md %}#as-of-joins)
* [`LATERAL` joins]({% link docs/sql/query_syntax/from.md %}#lateral-joins)
* [`POSITIONAL` joins]({% link docs/sql/query_syntax/from.md %}#positional-joins)

## Trailing Commas

DuckDB allows [trailing commas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas), both when listing entities (e.g., column and table names) and when constructing [`LIST` items]({% link docs/sql/data_types/list.md %}#creating-lists). For example, the following query works:

```sql
SELECT
    42 AS x,
    ['a', 'b', 'c',] AS y,
    'hello world' AS z,
;
```

## See Also

* [Friendlier SQL with DuckDB]({% link _posts/2022-05-04-friendlier-sql.md %}) blog post
* [Even Friendlier SQL with DuckDB]({% link _posts/2023-08-23-even-friendlier-sql.md %}) blog post
* [SQL Gymnastics: Bending SQL into flexible new shapes]({% link _posts/2024-03-01-sql-gymnastics.md %}) blog post
