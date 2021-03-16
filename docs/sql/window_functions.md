---
layout: docu
title: Window Functions
selected: Documentation/Window Functions
railroad: expressions/window.js
---
<div id="rrdiagram"></div>

Window functions can only be used in the `SELECT` clause. To share `OVER` specifications between functions, use the statement's `WINDOW` clause. 

## General-Purpose Window Functions
The table below shows the available general window functions.

| Function | Return Type | Description | Example |
|:---|:---|:---|:---|
| `row_number()` | `bigint` | The number of the current row within its partition, counting from 1. | `row_number()` |
| `rank()` | `bigint` | The rank of the current row *with gaps*; same as `row_number` of its first peer. | `rank()` |
| `dense_rank()` | `bigint` | The rank of the current row *without gaps*; this function counts peer groups. | `dense_rank()` |
| `percent_rank()` | `double` | The relative rank of the current row: `(rank() - 1) / (total partition rows - 1)`. | `percent_rank()` |
| `cume_dist()` | `double` | The cumulative distribution: (number of partition rows preceding or peer with current row) / total partition rows. | `cume_dist()` |
| `ntile(num_buckets integer)` | `bigint` | An integer ranging from 1 to the argument value, dividing the partition as equally as possible. | `ntile(4)` |
| `lag(expr any [, offset integer [, default any ]])` | same type as **expr** | Returns `expr` evaluated at the row that is `offset` rows before the current row within the partition; if there is no such row, instead return `default` (which must be of the same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `null`. | `lag(column, 3, 0)` |
| `lead(expr any [, offset integer [, default any ]])` | same type as **expr** | Returns `expr` evaluated at the row that is `offset` rows before the current row within the partition; if there is no such row, instead return `default` (which must be of the same type as `expr`). Both `offset` and `default` are evaluated with respect to the current row. If omitted, `offset` defaults to `1` and default to `null`. | `lead(column, 3, 0)` |
| `first_value(expr any)` | same type as **expr** | Returns `expr` evaluated at the row that is the first row of the window frame. | `first_value(column)` |
| `last_value(expr any)` | same type as **expr** | Returns `expr` evaluated at the row that is the last row of the window frame. | `last_value(column)` |
| `nth_value(expr any, nth integer)` | same type as **expr** | Returns `expr` evaluated at the nth row of the window frame (counting from 1); null if no such row. | `nth_value(column, 2)` |

## Aggregate Window Functions
All [aggregate functions](docs/sql/aggregates) can be used in a windowing context.
