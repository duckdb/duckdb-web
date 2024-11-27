---
layout: docu
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

The following operations **do not** guarantee that the row order is preserved:

* `FROM` with multiple tables and/or subqueries
* `JOIN`
* `SAMPLE`
* `UNION`
* `GROUP BY`
* `ORDER BY`

## Insertion Order

By default, the following components preserve insertion order:

* [CSV reader]({% link docs/data/csv/overview.md %}#order-preservation)
* [Parquet reader]({% link docs/data/parquet/overview.md %}#order-preservation)
* [JSON reader]({% link docs/data/json/overview.md %}#order-preservation)

Preservation of insertion order is controlled by the `preserve_insertion_order` [configuration option]({% link docs/configuration/overview.md %}).
This setting is `true` by default, indicating that the order should be preserved.
To change this setting, use:

```sql
SET preserve_insertion_order = false;
```
