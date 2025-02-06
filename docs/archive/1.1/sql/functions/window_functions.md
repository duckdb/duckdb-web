---
layout: docu
railroad: expressions/window.js
redirect_from:
- docs/archive/1.1/sql/window_functions
title: Window Functions
---

<!-- markdownlint-disable MD001 -->

DuckDB supports [window functions](https://en.wikipedia.org/wiki/Window_function_(SQL)), which can use multiple rows to calculate a value for each row.
Window functions are [blocking operators]({% link docs/archive/1.1/guides/performance/how_to_tune_workloads.md %}#blocking-operators), i.e., they require their entire input to be buffered, making them one of the most memory-intensive operators in SQL.

Window function are available in SQL since [SQL:2003](https://en.wikipedia.org/wiki/SQL:2003) and are supported by major SQL database systems.

## Examples

Generate a `row_number` column to enumerate rows:

```sql
SELECT row_number() OVER ()
FROM sales;
```

> Tip If you only need a number for each row in a table, you can use the [`rowid` pseudocolumn]({% link docs/archive/1.1/sql/statements/select.md %}#row-ids).

Generate a `row_number` column to enumerate rows, ordered by `time`:

```sql
SELECT row_number() OVER (ORDER BY time)
FROM sales;
```

Generate a `row_number` column to enumerate rows, ordered by `time` and partitioned by `region`:

```sql
SELECT row_number() OVER (PARTITION BY region ORDER BY time)
FROM sales;
```

Compute the difference between the current and the previous-by-`time` `amount`:

```sql
SELECT amount - lag(amount) OVER (ORDER BY time)
FROM sales;
```

Compute the percentage of the total `amount` of sales per `region` for each row:

```sql
SELECT amount / sum(amount) OVER (PARTITION BY region)
FROM sales;
```

## Syntax

<div id="rrdiagram"></div>

Window functions can only be used in the `SELECT` clause. To share `OVER` specifications between functions, use the statement's `WINDOW` clause and use the `OVER ⟨window-name⟩` syntax.

## General-Purpose Window Functions

The table below shows the available general window functions.

| Name | Description |
|:--|:-------|
| [`cume_dist()`](#cume_dist) | The cumulative distribution: (number of partition rows preceding or peer with current row) / total partition rows. |
| [`dense_rank()`](#dense_rank) | The rank of the current row *without gaps;* this function counts peer groups. |
| [`first_value(expr[ IGNORE NULLS])`](#first_valueexpr-ignore-nulls) | Returns `expr` evaluated at the row that is the first row (with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame. |
| [`lag(expr[, offset[, default]][ IGNORE NULLS])`](#lagexpr-offset-default-ignore-nulls) | Returns `expr` evaluated at the row that is `offset` rows (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) before the current row within the window frame; if there is no such row, instead return `default` (which must be of the Same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `NULL`. |
| [`last_value(expr[ IGNORE NULLS])`](#last_valueexpr-ignore-nulls) | Returns `expr` evaluated at the row that is the last row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame. |
| [`lead(expr[, offset[, default]][ IGNORE NULLS])`](#leadexpr-offset-default-ignore-nulls) | Returns `expr` evaluated at the row that is `offset` rows after the current row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) within the window frame; if there is no such row, instead return `default` (which must be of the Same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `NULL`. |
| [`nth_value(expr, nth[ IGNORE NULLS])`](#nth_valueexpr-nth-ignore-nulls) | Returns `expr` evaluated at the nth row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame (counting from 1); `NULL` if no such row. |
| [`ntile(num_buckets)`](#ntilenum_buckets) | An integer ranging from 1 to `num_buckets`, dividing the partition as equally as possible. |
| [`percent_rank()`](#percent_rank) | The relative rank of the current row: `(rank() - 1) / (total partition rows - 1)`. |
| [`rank_dense()`](#rank_dense) | The rank of the current row *without gaps. |
| [`rank()`](#rank) | The rank of the current row *with gaps;* same as `row_number` of its first peer. |
| [`row_number()`](#row_number) | The number of the current row within the partition, counting from 1. |

#### `cume_dist()`

<div class="nostroke_table"></div>

| **Description** | The cumulative distribution: (number of partition rows preceding or peer with current row) / total partition rows. |
| **Return Type** | `DOUBLE` |
| **Example** | `cume_dist()` |

#### `dense_rank()`

<div class="nostroke_table"></div>

| **Description** | The rank of the current row *without gaps;* this function counts peer groups. |
| **Return Type** | `BIGINT` |
| **Example** | `dense_rank()` |
| **Aliases** | `rank_dense()` |

#### `first_value(expr[ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **Description** | Returns `expr` evaluated at the row that is the first row (with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame. |
| **Return Type** | Same type as `expr` |
| **Example** | `first_value(column)` |

#### `lag(expr[, offset[, default]][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **Description** | Returns `expr` evaluated at the row that is `offset` rows (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) before the current row within the window frame; if there is no such row, instead return `default` (which must be of the Same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `NULL`. |
| **Return Type** | Same type as `expr` |
| **Aliases** | `lag(column, 3, 0)` |

#### `last_value(expr[ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **Description** | Returns `expr` evaluated at the row that is the last row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame. |
| **Return Type** | Same type as `expr` |
| **Example** | `last_value(column)` |

#### `lead(expr[, offset[, default]][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **Description** | Returns `expr` evaluated at the row that is `offset` rows after the current row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) within the window frame; if there is no such row, instead return `default` (which must be of the Same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `NULL`. |
| **Return Type** | Same type as `expr` |
| **Aliases** | `lead(column, 3, 0)` |

#### `nth_value(expr, nth[ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **Description** | Returns `expr` evaluated at the nth row (among rows with a non-null value of `expr` if `IGNORE NULLS` is set) of the window frame (counting from 1); `NULL` if no such row. |
| **Return Type** | Same type as `expr` |
| **Aliases** | `nth_value(column, 2)` |

#### `ntile(num_buckets)`

<div class="nostroke_table"></div>

| **Description** | An integer ranging from 1 to `num_buckets`, dividing the partition as equally as possible. |
| **Return Type** | `BIGINT` |
| **Example** | `ntile(4)` |

#### `percent_rank()`

<div class="nostroke_table"></div>

| **Description** | The relative rank of the current row: `(rank() - 1) / (total partition rows - 1)`. |
| **Return Type** | `DOUBLE` |
| **Example** | `percent_rank()` |

#### `rank_dense()`

<div class="nostroke_table"></div>

| **Description** | The rank of the current row *without gaps*. |
| **Return Type** | `BIGINT` |
| **Example** | `rank_dense()` |
| **Aliases** | `dense_rank()` |

#### `rank()`

<div class="nostroke_table"></div>

| **Description** | The rank of the current row *with gaps;* same as `row_number` of its first peer. |
| **Return Type** | `BIGINT` |
| **Example** | `rank()` |

#### `row_number()`

<div class="nostroke_table"></div>

| **Description** | The number of the current row within the partition, counting from 1. |
| **Return Type** | `BIGINT` |
| **Example** | `row_number()` |

## Aggregate Window Functions

All [aggregate functions]({% link docs/archive/1.1/sql/functions/aggregates.md %}) can be used in a windowing context, including the optional [`FILTER` clause]({% link docs/archive/1.1/sql/query_syntax/filter.md %}).
The `first` and `last` aggregate functions are shadowed by the respective general-purpose window functions, with the minor consequence that the `FILTER` clause is not available for these but `IGNORE NULLS` is.

## DISTINCT Arguments

All aggregate window functions support using a `DISTINCT` clause for the arguments. When the `DISTINCT` clause is
provided, only distinct values are considered in the computation of the aggregate. This is typically used in combination
with the `COUNT` aggregate to get the number of distinct elements; but it can be used together with any aggregate
function in the system.

```sql
-- Count the number of distinct users at a given point in time
SELECT count(DISTINCT name) OVER (ORDER BY time) FROM sales;
-- Concatenate those distinct users into a list
SELECT list(DISTINCT name) OVER (ORDER BY time) FROM sales;
```

## Nulls

All [general-purpose window functions](#general-purpose-window-functions) that accept `IGNORE NULLS` respect nulls by default. This default behavior can optionally be made explicit via `RESPECT NULLS`.

In contrast, all [aggregate window functions](#aggregate-window-functions) (except for `list` and its aliases, which can be made to ignore nulls via a `FILTER`) ignore nulls and do not accept `RESPECT NULLS`. For example, `sum(column) OVER (ORDER BY time) AS cumulativeColumn` computes a cumulative sum where rows with a `NULL` value of `column` have the same value of `cumulativeColumn` as the row that precedes them.

## Evaluation

Windowing works by breaking a relation up into independent *partitions*,
*ordering* those partitions,
and then computing a new column for each row as a function of the nearby values.
Some window functions depend only on the partition boundary and the ordering,
but a few (including all the aggregates) also use a *frame*.
Frames are specified as a number of rows on either side (*preceding* or *following*) of the *current row*.
The distance can either be specified as a number of *rows* or a *range* of values
using the partition's ordering value and a distance.

The full syntax is shown in the diagram at the top of the page,
and this diagram visually illustrates computation environment:

<img src="/images/blog/windowing/framing.svg" alt="The Window Computation Environment" title="Figure 1: The Window Computation Environment" style="max-width:90%;width:90%;height:auto"/>

### Partition and Ordering

Partitioning breaks the relation up into independent, unrelated pieces.
Partitioning is optional, and if none is specified then the entire relation is treated as a single partition.
Window functions cannot access values outside of the partition containing the row they are being evaluated at.

Ordering is also optional, but without it the results of [general-purpose window functions](#general-purpose-window-functions) and [order-sensitive aggregate functions]({% link docs/archive/1.1/sql/functions/aggregates.md %}#order-by-clause-in-aggregate-functions), and the order of [framing](#framing) are not well-defined.
Each partition is ordered using the same ordering clause.

> It is not currently possible to specify the aggregation order of window functions other than via the order in the `OVER` specification. In particular, it is not possible to use an aggregation order different from the frame order, e.g., `last_value(x ORDER BY y) OVER (ORDER BY z)`.

Here is a table of power generation data, available as a CSV file ([`power-plant-generation-history.csv`](/data/power-plant-generation-history.csv)). To load the data, run:

```sql
CREATE TABLE "Generation History" AS
    FROM 'power-plant-generation-history.csv';
```

After partitioning by plant and ordering by date, it will have this layout:

| Plant | Date | MWh |
|:---|:---|---:|
| Boston | 2019-01-02 | 564337 |
| Boston | 2019-01-03 | 507405 |
| Boston | 2019-01-04 | 528523 |
| Boston | 2019-01-05 | 469538 |
| Boston | 2019-01-06 | 474163 |
| Boston | 2019-01-07 | 507213 |
| Boston | 2019-01-08 | 613040 |
| Boston | 2019-01-09 | 582588 |
| Boston | 2019-01-10 | 499506 |
| Boston | 2019-01-11 | 482014 |
| Boston | 2019-01-12 | 486134 |
| Boston | 2019-01-13 | 531518 |
| Worcester | 2019-01-02 | 118860 |
| Worcester | 2019-01-03 | 101977 |
| Worcester | 2019-01-04 | 106054 |
| Worcester | 2019-01-05 | 92182 |
| Worcester | 2019-01-06 | 94492 |
| Worcester | 2019-01-07 | 99932 |
| Worcester | 2019-01-08 | 118854 |
| Worcester | 2019-01-09 | 113506 |
| Worcester | 2019-01-10 | 96644 |
| Worcester | 2019-01-11 | 93806 |
| Worcester | 2019-01-12 | 98963 |
| Worcester | 2019-01-13 | 107170 |

In what follows,
we shall use this table (or small sections of it) to illustrate various pieces of window function evaluation.

The simplest window function is `row_number()`.
This function just computes the 1-based row number within the partition using the query:

```sql
SELECT
    "Plant",
    "Date",
    row_number() OVER (PARTITION BY "Plant" ORDER BY "Date") AS "Row"
FROM "Generation History"
ORDER BY 1, 2;
```

The result will be the following:

| Plant | Date | Row |
|:---|:---|---:|
| Boston | 2019-01-02 | 1 |
| Boston | 2019-01-03 | 2 |
| Boston | 2019-01-04 | 3 |
| ... | ... | ... |
| Worcester | 2019-01-02 | 1 |
| Worcester | 2019-01-03 | 2 |
| Worcester | 2019-01-04 | 3 |
| ... | ... | ... |

Note that even though the function is computed with an `ORDER BY` clause,
the result does not have to be sorted,
so the `SELECT` also needs to be explicitly sorted if that is desired.

### Framing

Framing specifies a set of rows relative to each row where the function is evaluated.
The distance from the current row is given as an expression either `PRECEDING` or `FOLLOWING` the current row in the order specified by the `ORDER BY` clause in the `OVER` specification.
This distance can either be specified as an integral number of `ROWS`
or as a `RANGE` delta expression.
For a `RANGE` specification, there must  be only one ordering expression,
and it has to support addition and subtraction (i.e., numbers or `INTERVAL`s).
The default frame is from `UNBOUNDED PRECEDING` to `UNBOUNDED FOLLOWING` when no `ORDER BY` clause is present and from `UNBOUNDED PRECEDING` to `CURRENT ROW` when an `ORDER BY` clause is present.
It is invalid for a frame to start after it ends.
Using the [`EXCLUDE` clause](#exclude-clause), rows around the current row can be excluded from the frame.

#### `ROW` Framing

Here is a simple `ROW` frame query, using an aggregate function:

```sql
SELECT points,
    sum(points) OVER (
        ROWS BETWEEN 1 PRECEDING
                 AND 1 FOLLOWING) we
FROM results;
```

This query computes the `sum` of each point and the points on either side of it:

<img src="/images/blog/windowing/moving-sum.jpg" alt="Moving SUM of three values" title="Figure 2: A moving SUM of three values" style="max-width:90%;width:90%;height:auto"/>

Notice that at the edge of the partition, there are only two values added together.
This is because frames are cropped to the edge of the partition.

#### `RANGE` Framing

Returning to the power data, suppose the data is noisy.
We might want to compute a 7 day moving average for each plant to smooth out the noise.
To do this, we can use this window query:

```sql
SELECT "Plant", "Date",
    avg("MWh") OVER (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING)
        AS "MWh 7-day Moving Average"
FROM "Generation History"
ORDER BY 1, 2;
```

This query partitions the data by `Plant` (to keep the different power plants' data separate),
orders each plant's partition by `Date` (to put the energy measurements next to each other),
and uses a `RANGE` frame of three days on either side of each day for the `avg`
(to handle any missing days).
This is the result:

| Plant | Date | MWh 7-day Moving Average |
|:---|:---|---:|
| Boston | 2019-01-02 | 517450.75 |
| Boston | 2019-01-03 | 508793.20 |
| Boston | 2019-01-04 | 508529.83 |
| ... | ... | ... |
| Boston | 2019-01-13 | 499793.00 |
| Worcester | 2019-01-02 | 104768.25 |
| Worcester | 2019-01-03 | 102713.00 |
| Worcester | 2019-01-04 | 102249.50 |
| ... | ... | ... |

#### `EXCLUDE` Clause

The `EXCLUDE` clause allows rows around the current row to be excluded from the frame. It has the following options:

* `EXCLUDE NO OTHERS`: exclude nothing (default)
* `EXCLUDE CURRENT ROW`: exclude the current row from the window frame
* `EXCLUDE GROUP`: exclude the current row and all its peers (according to the columns specified by `ORDER BY`) from the window frame
* `EXCLUDE TIES`: exclude only the current row's peers from the window frame

### `WINDOW` Clauses

Multiple different `OVER` clauses can be specified in the same `SELECT`, and each will be computed separately.
Often, however, we want to use the same layout for multiple window functions.
The `WINDOW` clause can be used to define a *named* window that can be shared between multiple window functions:

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    avg("MWh") OVER seven AS "MWh 7-day Moving Average",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum"
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2;
```

The three window functions will also share the data layout, which will improve performance.

Multiple windows can be defined in the same `WINDOW` clause by comma-separating them:

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    avg("MWh") OVER seven AS "MWh 7-day Moving Average",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum",
    min("MWh") OVER three AS "MWh 3-day Moving Minimum",
    avg("MWh") OVER three AS "MWh 3-day Moving Average",
    max("MWh") OVER three AS "MWh 3-day Moving Maximum"
FROM "Generation History"
WINDOW
    seven AS (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING),
    three AS (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 1 DAYS PRECEDING
        AND INTERVAL 1 DAYS FOLLOWING)
ORDER BY 1, 2;
```

The queries above do not use a number of clauses commonly found in select statements, like
`WHERE`, `GROUP BY`, etc. For more complex queries you can find where `WINDOW` clauses fall in
the canonical order of the [`SELECT statement`]({% link docs/archive/1.1/sql/statements/select.md %}).

### Filtering the Results of Window Functions Using `QUALIFY`

Window functions are executed after the [`WHERE`]({% link docs/archive/1.1/sql/query_syntax/where.md %}) and [`HAVING`]({% link docs/archive/1.1/sql/query_syntax/having.md %}) clauses have been already evaluated, so it's not possible to use these clauses to filter the results of window functions
The [`QUALIFY` clause]({% link docs/archive/1.1/sql/query_syntax/qualify.md %}) avoids the need for a subquery or [`WITH` clause]({% link docs/archive/1.1/sql/query_syntax/with.md %}) to perform this filtering.

### Box and Whisker Queries

All aggregates can be used as windowing functions, including the complex statistical functions.
These function implementations have been optimised for windowing,
and we can use the window syntax to write queries that generate the data for moving box-and-whisker plots:

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    quantile_cont("MWh", [0.25, 0.5, 0.75]) OVER seven
        AS "MWh 7-day Moving IQR",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum",
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2;
```