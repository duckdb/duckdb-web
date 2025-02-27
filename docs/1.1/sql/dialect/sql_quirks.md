---
layout: docu
title: SQL Quirks
---

Like all programming languages and libraries, DuckDB has its share of idiosyncrasies and inconsistencies.  
Some are vestiges of our feathered friend's evolution; others are inevitable because we strive to adhere to the [SQL Standard](https://blog.ansi.org/sql-standard-iso-iec-9075-2023-ansi-x3-135/) and specifically to PostgreSQL's dialect (see the [“PostgreSQL Compatibility”]({% link docs/1.1/sql/dialect/postgresql_compatibility.md %}) page for exceptions).
The rest may simply come down to different preferences, or we may even agree on what _should_ be done but just haven’t gotten around to it yet.

Acknowledging these quirks is the best we can do, which is why we have compiled below a list of examples.

## Aggregating Empty Groups

On empty groups, the aggregate functions `sum`, `list`, and `string_agg` all return `NULL` instead of `0`, `[]` and `''`, respectively. This is dictated by the SQL Standard and obeyed by all SQL implementations we know. This behavior is inherited by the list aggregate [`list_sum`]({% link docs/1.1/sql/functions/list.md %}#list_-rewrite-functions), but not by the DuckDB original [`list_dot_product`]({% link docs/1.1/sql/functions/list.md %}#list_dot_productlist1-list2) which returns `0` on empty lists.

## Indexing

To comply with standard SQL, one-based indexing is used almost everywhere, e.g., array and string indexing and slicing, and window functions (`row_number`, `rank`, `dense_rank`). However, similarly to PostgreSQL, [JSON features use a zero-based indexing]({% link docs/1.1/data/json/overview.md %}#indexing).

> While list functions use a 1-based indexing, `list_reduce` uses a 0-based indexing. This is a [known issue](https://github.com/duckdb/duckdb/issues/14619).

## Expressions

### Results That May Surprise You

<!-- markdownlint-disable MD056 -->

| Expression                 | Result  | Note                                                                          |
|----------------------------|---------|-------------------------------------------------------------------------------|
| `-2^2`                     | `4.0`   | PostgreSQL compatibility means the unary minus has higher precedence than the exponentiation operator. Use additional parentheses, e.g., `-(2^2)` or the [`pow` function]({% link docs/1.1/sql/functions/numeric.md %}#powx-y), e.g. `-pow(2, 2)`, to avoid mistakes. |
| `'t' = true`               | `true`  | Compatible with PostgreSQL.                                                   |
| `1 = '1'`                  | `true`  | Compatible with PostgreSQL.                                                   |
| `1 = ' 1'`                 | `true`  | Compatible with PostgreSQL.                                                   |
| `1 = '01'`                 | `true`  | Compatible with PostgreSQL.                                                   |
| `1 = ' 01 '`               | `true`  | Compatible with PostgreSQL.                                                   |
| `1 = true`                 | `true`  | Not compatible with PostgreSQL.                                               |
| `1 = '1.1'`                | `true`  | Not compatible with PostgreSQL.                                               |
| `1 IN (0, NULL)`           | `NULL`  | Makes sense if you think of the `NULL`s in the input and output as `UNKNOWN`. |
| `1 in [0, NULL]`           | `false` |                                                                               |
| `concat('abc', NULL)`      | `abc`   | Compatible with PostgreSQL. `list_concat` behaves similarly.                  |
| `'abc' || NULL`            | `NULL`  |                                                                               |

<!-- markdownlint-enable MD056 -->

### `NaN` Values

`'NaN'::FLOAT = 'NaN'::FLOAT` and `'NaN'::FLOAT > 3` violate IEEE-754 but mean floating point data types have a total order, like all other data types (beware the consequences for `greatest` / `least`).

### `age` Function

`age(x)` is `current_date - x` instead of `current_timestamp - x`. Another quirk inherited from PostgreSQL.

### Extract Functions

`list_extract` / `map_extract` return `NULL` on non-existing keys. `struct_extract` throws an error because keys of structs are like columns.

## Clauses

### Automatic Column Deduplication in `SELECT`

Column names are deduplicated with the first occurrence shadowing the others:

```sql
CREATE TABLE tbl AS SELECT 1 AS a;
SELECT a FROM (SELECT *, 2 AS a FROM tbl);
```

| a |
|--:|
| 1 |

### Case Insensitivity for `SELECT`ing Columns

Due to case-insensitivity, it's not possible to use `SELECT a FROM 'file.parquet'` when a column called `A` appears before the desired column `a` in `file.parquet`.

### `USING SAMPLE`

The `USING SAMPLE` clause is syntactically placed after the `WHERE` and `GROUP BY` clauses (same as the `LIMIT` clause) but is semantically applied before both (unlike the `LIMIT` clause).