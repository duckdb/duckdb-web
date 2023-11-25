---
layout: docu
title: List Type
---

A `LIST` column encodes lists of values. Fields in the column can have values with different lengths, but they must all have the same underlying type. `LIST`s are typically used to store arrays of numbers, but can contain any uniform data type, including other `LIST`s and `STRUCT`s.

`LIST`s are similar to PostgreSQL's `ARRAY` type. DuckDB uses the `LIST` terminology, but some [array functions](../functions/nested#list-functions) are provided for PostgreSQL compatibility.

See the [data types overview](../../sql/data_types/overview) for a comparison between nested data types.

> For storing fixed-length lists, DuckDB uses the [`ARRAY` type](array).

## Creating Lists

Lists can be created using the [`list_value(expr, ...)`](../functions/nested#list-functions) function or the equivalent bracket notation `[expr, ...]`. The expressions can be constants or arbitrary expressions. To create a list from a table column, use the [`list`](../aggregates.md#general-aggregate-functions) aggregate function.

```sql
-- List of integers
SELECT [1, 2, 3];
-- List of strings with a NULL value
SELECT ['duck', 'goose', NULL, 'heron'];
-- List of lists with NULL values
SELECT [['duck', 'goose', 'heron'], NULL, ['frog', 'toad'], []];
-- Create a list with the list_value function
SELECT list_value(1, 2, 3);
-- Create a table with an integer list column and a varchar list column
CREATE TABLE list_table (int_list INT[], varchar_list VARCHAR[]);
```

## Retrieving from Lists

Retrieving one or more values from a list can be accomplished using brackets and slicing notation, or through [list functions](../functions/nested#list-functions) like `list_extract`. Multiple equivalent functions are provided as aliases for compatibility with systems that refer to lists as arrays. For example, the function `array_slice`.
```sql
-- Note that we wrap the list creation in parenthesis so that it happens first.
-- This is only needed in our basic examples here, not when working with a list column
-- For example, this can't be parsed: SELECT ['a', 'b', 'c'][1]
```

| example                                    | result     |
|:-------------------------------------------|:-----------|
| `SELECT (['a', 'b', 'c'])[3]`              | 'c'        |
| `SELECT (['a', 'b', 'c'])[-1]`             | 'c'        |
| `SELECT (['a', 'b', 'c'])[2 + 1]`          | 'c'        |
| `SELECT list_extract(['a', 'b', 'c'], 3)`  | 'c'        |
| `SELECT (['a', 'b', 'c'])[1:2]`            | ['a', 'b'] |
| `SELECT (['a', 'b', 'c'])[:2]`             | ['a', 'b'] |
| `SELECT (['a', 'b', 'c'])[-2:]`            | ['b', 'c'] |
| `SELECT list_slice(['a', 'b', 'c'], 2, 3)` | ['b', 'c'] |

## Ordering

The ordering is defined positionally. `NULL` values compare greater than all other values and are considered equal to each other.

## Null Comparisons

At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_ , however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Functions

See [Nested Functions](../../sql/functions/nested).
