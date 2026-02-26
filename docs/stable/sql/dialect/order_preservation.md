---
layout: docu
redirect_from:
  - /docs/sql/dialect/order_preservation
title: Order Preservation
---

For many operations, DuckDB preserves the order of rows, similarly to data frame libraries such as Pandas.

## Example

Take the following table for example:

```sql
CREATE TABLE tbl AS
    SELECT *
    FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) t(x, y);

SELECT *
FROM tbl;
```

| x | y |
|--:|---|
| 1 | a |
| 2 | b |
| 3 | c |

Let's take the following query that returns the rows where `x` is an odd number:

```sql
SELECT *
FROM tbl
WHERE x % 2 == 1;
```

| x | y |
|--:|---|
| 1 | a |
| 3 | c |

Because the row `(1, 'a')` occurs before `(3, 'c')` in the original table, it is guaranteed to come before that row in this table too.

## Clauses

The following clauses guarantee that the original row order is preserved:

* `COPY` (see [Insertion Order](#insertion-order))
* `FROM` with a single table
* `LIMIT`
* `OFFSET`
* `SELECT`
* `UNION ALL`
* `WHERE`
* Window functions with an empty `OVER` clause
* Common table expressions and table subqueries as long as they only contain the aforementioned components

> Tip `row_number() OVER ()` allows turning the original row order into an explicit column that can be referenced in the operations that don't preserve row order by default. On materialized tables, the `rowid` pseudo-column can be used to the same effect.

The following operations **do not** guarantee that the row order is preserved:

* `FROM` with multiple tables and/or subqueries
* `JOIN`
* `UNION`
* `USING SAMPLE`
* Whole-table aggregation (the input order, that is, the order in which rows are fed into [order-sensitive aggregate functions](https://duckdb.org/docs/sql/functions/aggregates.html#order-by-clause-in-aggregate-functions) is not guaranteed unless explicitly specified in the aggregate function)
* `GROUP BY` (neither in- nor output order are guaranteed)
* `ORDER BY` (specifically, `ORDER BY` may not use a [stable algorithm](https://en.m.wikipedia.org/wiki/Stable_algorithm))
* Scalar subqueries

## Insertion Order

By default, the following components preserve insertion order:

* [CSV reader]({% link docs/stable/data/csv/overview.md %}#order-preservation) (`read_csv` function)
* [JSON reader]({% link docs/stable/data/json/overview.md %}#order-preservation) (`read_json` function)
* [Parquet reader]({% link docs/stable/data/parquet/overview.md %}#order-preservation) (`read_parquet` function)

Preservation of insertion order is controlled by the `preserve_insertion_order` [configuration option]({% link docs/stable/configuration/overview.md %}).
This setting is `true` by default, indicating that the order should be preserved.
To change this setting, use:

```sql
SET preserve_insertion_order = false;
```
