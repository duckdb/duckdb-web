---
layout: docu
title: Window Functions
selected: Documentation/Window Functions
railroad: expressions/window.js
---
<div id="rrdiagram"></div>

Window functions can only be used in the `SELECT` clause. To share `OVER` specifications between functions, use the statement's `WINDOW` clause and use the `OVER window-name` syntax.

## General-Purpose Window Functions
The table below shows the available general window functions.

| Function | Return Type | Description | Example |
|:---|:---|:---|:---|
| `row_number()` | `bigint` | The number of the current row within the partition, counting from 1. | `row_number()` |
| `rank()` | `bigint` | The rank of the current row *with gaps*; same as `row_number` of its first peer. | `rank()` |
| `dense_rank()` | `bigint` | The rank of the current row *without gaps*; this function counts peer groups. | `dense_rank()` |
| `percent_rank()` | `double` | The relative rank of the current row: `(rank() - 1) / (total partition rows - 1)`. | `percent_rank()` |
| `cume_dist()` | `double` | The cumulative distribution: (number of partition rows preceding or peer with current row) / total partition rows. | `cume_dist()` |
| `ntile(num_buckets integer)` | `bigint` | An integer ranging from 1 to the argument value, dividing the partition as equally as possible. | `ntile(4)` |
| `lag(expr any [, offset integer [, default any ]])` | same type as **expr** | Returns `expr` evaluated at the row that is `offset` rows before the current row within the partition; if there is no such row, instead return `default` (which must be of the same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `null`. | `lag(column, 3, 0)` |
| `lead(expr any [, offset integer [, default any ]])` | same type as **expr** | Returns `expr` evaluated at the row that is `offset` rows after the current row within the partition; if there is no such row, instead return `default` (which must be of the same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `null`. | `lead(column, 3, 0)` |
| `first_value(expr any)` | same type as **expr** | Returns `expr` evaluated at the row that is the first row of the window frame. | `first_value(column)` |
| `last_value(expr any)` | same type as **expr** | Returns `expr` evaluated at the row that is the last row of the window frame. | `last_value(column)` |
| `nth_value(expr any, nth integer)` | same type as **expr** | Returns `expr` evaluated at the nth row of the window frame (counting from 1); null if no such row. | `nth_value(column, 2)` |

## Aggregate Window Functions
All [aggregate functions](aggregates) can be used in a windowing context.

## Evaluation

Windowing works by breaking a relation up into independent *partitions*,
*ordering* those partitions,
and then computing a new column for each row as a function the nearby values.
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

Ordering is also optional, but without it the results are not well-defined.
Each partition is ordered using the same ordering clause.

Here is a table of power generation data.
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

The simplest window function is `ROW_NUMBER()`.
This function just computes the 1-based row number within the partition using the query:

```sql
SELECT "Plant", "Date", row_number() over () AS "Row"
FROM "History"
ORDER BY 1, 2
```

The result will be

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
The distance from the current row is given as an expression either `PRECEDING` or `FOLLOWING` the current row.
This distance can either be specified as an integral number of `ROWS`
or as a `RANGE` delta expression from the value of the ordering expression.
For a `RANGE` specification, there must  be only one ordering expression,
and it has to support addition and subtraction (i.e., numbers or `INTERVAL`s).
The default values for frames are from `UNBOUNDED PRECEDING` to `CURRENT ROW`.
It is invalid for a frame to start after it ends.

#### `ROW` Framing

Here is a simple `ROW` frame query, using an aggregate function:

```sql
SELECT points,
    SUM(points) OVER (
        ROWS BETWEEN 1 PRECEDING
                 AND 1 FOLLOWING) we
FROM results
```
This query computes the `SUM` of each point and the points on either side of it:

<img src="/images/blog/windowing/moving-sum.jpg" alt="Moving SUM of three values" title="Figure 2: A moving SUM of three values" style="max-width:90%;width:90%;height:auto"/>

Notice that at the edge of the partition, there are only two values added together.
This is because frames are cropped to the edge of the partition.

#### `RANGE` Framing

Returning to the power data, suppose the data is noisy.
We might want to compute a 7 day moving average for each plant to smooth out the noise.
To do this, we can use this window query:

```sql
SELECT "Plant", "Date",
    AVG("MWh") OVER (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING)
        AS "MWh 7-day Moving Average"
FROM "Generation History"
ORDER BY 1, 2
```

This query partitions the data by `Plant` (to keep the different power plants' data separate),
orders each plant's partition by `Date` (to put the energy measurements next to each other),
and uses a `RANGE` frame of three days on either side of each day for the `AVG`
(to handle any missing days).
This is the result:

| Plant | Date | MWh 7-day<br>Moving Average |
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

### `WINDOW` Clauses

Multiple different `OVER` clauses can be specified in the same `SELECT`, and each will be computed separately.
Often, however, we want to use the same layout for multiple window functions.
The `WINDOW` clause can be used to define a *named* window that can be shared between multiple window functions:

```sql
SELECT "Plant", "Date",
    MIN("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    AVG("MWh") OVER seven AS "MWh 7-day Moving Average",
    MAX("MWh") OVER seven AS "MWh 7-day Moving Maximum"
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2
```

The three window functions will also share the data layout, which will improve performance.

### Box and Whisker Queries

All aggregates can be used as windowing functions, including the complex statistical functions.
These function implementations have been optimised for windowing,
and we can use the window syntax to write queries that generate the data for moving box-and-whisker plots:

```sql
SELECT "Plant", "Date",
    MIN("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    QUANTILE_CONT("MWh", [0.25, 0.5, 0.75]) OVER seven
        AS "MWh 7-day Moving IQR",
    MAX("MWh") OVER seven AS "MWh 7-day Moving Maximum",
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2
```
