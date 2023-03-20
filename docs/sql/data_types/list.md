---
layout: docu
title: List
selected: Documentation/Data Types/List
expanded: Nested
---

## List Data Type

A `LIST` column can have values with different lengths, but they must all have the same underlying type. `LIST`s are typically used to store arrays of numbers, but can contain any uniform data type, including other `LIST`s and `STRUCT`s.

`LIST`s are similar to Postgres's `ARRAY` type. DuckDB uses the `LIST` terminology, but some [array functions](../functions/nested#list-functions) are provided for Postgres compatibility.

See the [data types overview](../../sql/data_types/overview) for a comparison between nested data types.

Lists can be created using the [`LIST_VALUE(expr, ...)`](../functions/nested#list-functions) function or the equivalent bracket notation `[expr, ...]`. The expressions can be constants or arbitrary expressions.

### Creating Lists
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
### Retrieving from Lists
Retrieving one or more values from a list can be accomplished using brackets and slicing notation, or through [list functions](../functions/nested#list-functions) like `list_extract`. Multiple equivalent functions are provided as aliases for compatibility with systems that refer to lists as arrays. For example, the function `array_slice`.
```sql
-- Retrieve an element from a list using brackets. This returns 'b'
-- Note that we wrap the list creation in parenthesis so that it happens first.
-- This is only needed in our basic examples here, not when working with a list column
-- For example, this can't be parsed: SELECT ['a','b','c'][1]
SELECT (['a','b','c'])[2];
-- Use a negative index to grab the nth element from the end of the list. This returns 'c'
SELECT (['a','b','c'])[-1];
-- Any expression that evaluates to an integer can be used to retrieve a list value
-- This includes using a column to determine which index to retrieve
-- This returns 'b'
SELECT (['a','b','c'])[1 + 1];
-- The list_extract function may also be used in place of brackets for selecting individual elements. 
-- This returns b
SELECT list_extract(['a','b','c'], 2);
-- Retrieve multiple list values using a bracketed slice syntax. This returns ['a','b']
SELECT (['a','b','c'])[1:2];
-- Single sided slices are also supported. Here, grab the first 2 elements. This returns ['a','b']
SELECT (['a','b','c'])[:2];
-- Use a negative index to grab the last 2 elements. This returns ['b','c']
SELECT (['a','b','c'])[-2:];
-- The list_slice function syntax is also supported. This returns ['b','c']
SELECT list_slice(['a','b','c'],2,3);
```

## Ordering
The ordering is defined positionally. `NULL` values compare greater than all other values and are considered equal to each other.

## Null Comparisons
At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_ , however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Functions
See [Nested Functions](../../sql/functions/nested).
