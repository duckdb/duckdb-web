---
layout: docu
title: Friendly SQL
---

DuckDB offers several advanced SQL features as well as extensions to the SQL syntax. We call these colloquially as "friendly SQL".

> Several of these features are also supported in other systems while some are (currently) exclusive to DuckDB.

## Clauses

* [`CREATE OR REPLACE TABLE`](../../sql/statements/create_table#create-or-replace): this clause allows avoiding `DROP TABLE IF EXISTS` statements in scripts.
* [`CREATE TABLE ... AS SELECT` (CTAS)](../../sql/statements/create_table#create-table--as-select-ctas): this clause allows creating a new table from the output of a table without manually defining a schema.
* [`DESCRIBE`](../meta/describe): this clause provides a succinct summary of the schema of a table or query.
* [`FROM`-first syntax with an optional `SELECT` clause](../../sql/query_syntax/from#from-first-syntax): DuckDB allows queries in the form of `FROM tbl` which selects all columns (performing a `SELECT *` statement).
* [`GROUP BY ALL`](../../sql/query_syntax/groupby#group-by-all): this clause allows omitting the group-by columns by inferring them from the list of attributes in the `SELECT` clause.
* [`INSERT INTO ... BY NAME`](../../sql/statements/insert#insert-into--by-name): this variant of the `INSERT` statement allows using column names instead of positions.
* [`ORDER BY ALL`](../../sql/query_syntax/orderby#order-by-all): this clause allows ordering on all columns (e.g., to ensure deterministic results).
* [`PIVOT`](../../sql/statements/pivot) and [`UNPIVOT`](../../sql/statements/unpivot) allow turning long tables to wide tables and vice versa, respectively.
* [`SELECT * EXCLUDE`](../../sql/expressions/star#exclude-clause): the `EXCLUDE` option allows excluding specific columns from the `*` expression.
* [`SELECT * REPLACE`](../../sql/expressions/star#replace-clause): the `EXCLUDE` option allows replacing specific columns with different expressions in a `*` expression.
* [`SUMMARIZE`](../meta/summarize): this clause returns summary statistics for a table or query.
* [`UNION BY NAME`](../../sql/query_syntax/setops#union-all-by-name): this clause performing the `UNION` operation along the names of columns (instead of relying on positions).

## Query Features

* [Column aliases in `WHERE`, `GROUP BY`, and `HAVING`](/2022/05/04/friendlier-sql#column-aliases-in-where--group-by--having)
* [`COLUMNS()` expression](../../sql/expressions/star#columns-expression) can be used to execute the same expression on multiple columns:
    * [with regular expressions](/2023/08/23/even-friendlier-sql#columns-with-regular-expressions)
    * [with `EXCLUDE` and `REPLACE`](/2023/08/23/even-friendlier-sql#columns-with-exclude-and-replace)
    * [with lambda functions](/2023/08/23/even-friendlier-sql#columns-with-lambda-functions)
* Reusable column aliases, e.g.: `SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i)`

## Literals and Identifiers

* [Case-insensitivity while maintaining case of entities in the catalog](../../sql/keywords_and_identifiers#case-sensitivity-of-identifiers)
* [Deduplicating identifiers](../../sql/keywords_and_identifiers#deduplicating-identifiers)
* [Underscores as digit separators in numeric literals](../../sql/keywords_and_identifiers#numeric-literals)

## Data Types

* [`MAP` data type](../../sql/data_types/map)
* [`UNION` data type](../../sql/data_types/union)

## Data Import

* [Auto-detecting the headers and schema of CSV files](../../data//csv/auto_detection)
* Directly querying [CSV files](../../data/csv) and [Parquet files](../../data/parquet)
* Loading from files using the syntax `FROM 'my.csv'`, `FROM 'my.csv.gz'`, `FROM 'my.parquet'`, etc.
* Filename expansion (globbing), e.g.: `FROM 'my-data/part-*.parquet'`

## Functions and Expressions

* [Dot operator for function chaining](../../sql/functions/overview#function-chaining-via-the-dot-operator): `SELECT ('hello').upper()`
* String formatters: [`format()` function with the `fmt` syntax](../../sql/functions/char#fmt-syntax) and the [`printf() function`](../../sql/functions/char#printf-syntax)
* [List comprehensions](/2023/08/23/even-friendlier-sql#list-comprehensions)
* [List slicing](/2022/05/04/friendlier-sql#string-slicing)
* [String slicing](/2022/05/04/friendlier-sql#string-slicing)
* [`STRUCT.*` notation](/2022/05/04/friendlier-sql#struct-dot-notation)
* [Simple `LIST` and `STRUCT` creation](/2022/05/04/friendlier-sql#simple-list-and-struct-creation)

## Join Types

* [`ASOF` joins](../../sql/query_syntax/from#as-of-joins)
* [`LATERAL` joins](../../sql/query_syntax/from#lateral-joins)
* [`POSITIONAL` joins](../../sql/query_syntax/from#positional-joins)

## Trailing Commas

DuckDB allows [trailing commas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas), both when listing entities (e.g., column and table names) and when constructing [`LIST` items](../../sql/data_types/list#creating-lists). For example, the following query works:

```sql
SELECT
    42 AS x,
    ['a', 'b', 'c',] AS y,
    'hello world' AS z,
;
```

## See Also

* [Friendlier SQL with DuckDB](/2022/05/04/friendlier-sql) blog post
* [Even Friendlier SQL with DuckDB](/2023/08/23/even-friendlier-sql) blog post
* [SQL Gymnastics: Bending SQL into flexible new shapes](/2024/03/01/sql-gymnastics) blog post
