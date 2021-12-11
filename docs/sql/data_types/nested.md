---
layout: docu
title: Nested Types
selected: Documentation/Data Types/Nested
expanded: Data Types
---
This section describes functions and operators for examining and manipulating nested values. DuckDB supports three nested data types: lists, structs, and maps.

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:---|:---|:---|:---|:---|
| LIST | An ordered sequence of data values of the same type. | Each row must have the same data type within each LIST, but can have any number of elements. | [1, 2, 3] | VARCHAR[ ] |
| STRUCT | A dictionary of multiple named values, where each key is a string, but the value can be a different type for each key. | Each row must have the same keys. | {'i': 42, 'j': 'a'} | STRUCT<i: INT, j: VARCHAR> |
| MAP | A dictionary of multiple named values, each key having the same type and each value having the same type. Keys and values can be any type and can be different types from one another. | Rows may have different keys. | map([1,2],['a','b']) | MAP<INT, VARCHAR> |


## Lists

A `LIST` column can have values with different lengths, but they must all have the same underlying type.
`LIST`s are typically used to store arrays of numbers, but can contain any uniform data type,
including other `LIST`s and `STRUCT`s.
`LIST`s are similar to Postgres's `ARRAY` type. DuckDB uses the `LIST` terminology, but some [array functions](../functions/nested#list-functions) are provided for Postgres compatibility.

Lists can be created using the [`LIST_VALUE(expr, ...)`](../functions/nested#list-functions) function
or the equivalent bracket notation `[expr, ...]`.
The expressions can be constants or arbitrary expressions.

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
```
### Retrieving from Lists
Retrieving one or more values from a list can be accomplished using brackets and slicing notation, or through [list functions](../functions/nested#list-functions) like `list_extract`. Multiple equivalent functions are provided as aliases for compatibility with systems that refer to lists as arrays. For example, the function `array_slice`.
```sql
-- Retrieve an element from a list using brackets. This returns 'c'
-- Note that we wrap the list creation in parenthesis so that it happens first.
-- This is only needed in our basic examples here, not when working with a list column
-- For example, this can't be parsed: SELECT ['a','b','c'][1]
SELECT (['a','b','c'])[2];
-- Use a negative index to grab the nth element from the end of the list. This returns 'c'
SELECT (['a','b','c'])[-1];
-- Any expression that evaluates to an integer can be used to retrieve a list value
-- This includes using a column to determine which index to retrieve
-- This returns 'c'
SELECT (['a','b','c'])[1 + 1];
-- The list_extract function may also be used in place of brackets for selecting individual elements. 
-- This returns c
SELECT list_extract(['a','b','c'], 2);
-- Retrieve multiple list values using a bracketed slice syntax. This returns ['b','c']
SELECT (['a','b','c'])[1:3];
-- Single sided slices are also supported. Here, grab the first 2 elements. This returns ['a','b']
SELECT (['a','b','c'])[:2];
-- Use a negative index to grab the last 2 elements. This returns ['b','c']
SELECT (['a','b','c'])[-2:];
-- The array_slice function is also supported. This returns ['b','c']
SELECT array_slice(['a','b','c'],1,3);
```
## Structs

Conceptually, a `STRUCT` column contains an ordered list of other columns called "entries".
The entries are referenced by name using strings. This document refers to those entry names as keys.
Each row in the `STRUCT` column must have the same keys. Each key must have the same type of value for each row.
`STRUCT`s are typically used to nest multiple columns into a single column,
and the nested column can be of any type, including other `STRUCT`s and `LIST`s.
`STRUCT`s are similar to Postgres's `ROW` type. DuckDB also includes a `row` function as a special way to produce a struct, but does not have a `ROW` data type. See an example below and the [nested functions docs](../functions/nested#struct-functions) for details.

Structs can be created using the [`STRUCT_PACK(name := expr, ...)`](../functions/nested#struct-functions) function
or the equivalent array notation `{'name': expr, ...}` notation.
The expressions can be constants or arbitrary expressions.

### Creating Structs
```sql
-- Struct of integers
SELECT {'x': 1, 'y': 2, 'z': 3};
-- Struct of strings with a NULL value
SELECT {'yes:' 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'};
-- Struct with a different type for each key
SELECT {'key1': 'string', 'key2': 1, 'key3': 12.345};
-- Struct using the struct_pack function. 
-- Note the lack of single quotes around the keys and the use of the := operator
SELECT struct_pack(key1 := 'value1',key2 := 42);
-- Struct of structs with NULL values
SELECT {'birds':
            {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'},
        'aliens':
            NULL,
        'amphibians':
            {'yes':'frog', 'maybe': 'salamander', 'huh': 'dragon', 'no':'toad'}
        };
```
### Retrieving from Structs
Retrieving a value from a struct can be accomplished using dot notation, bracket notation, or through [struct functions](../functions/nested#struct-functions) like `struct_extract`.
```sql
-- Use dot notation to retrieve the value at a key's location. This returns 1
-- Note that we wrap the struct creation in parenthesis so that it happens first.
-- This is only needed in our basic examples here, not when working with a struct column
SELECT ({'x': 1, 'y': 2, 'z': 3}).x;
-- If key contains a space, simply wrap it in double quotes. This returns 1
-- Note: Use double quotes not single quotes 
-- This is because this action is most similar to selecting a column from within the struct
SELECT ({'x space': 1, 'y': 2, 'z': 3})."x space";
-- Bracket notation may also be used. This returns 1
-- Note: Use single quotes since the goal is to specify a certain string key. 
-- Only constant expressions may be used inside the brackets (no columns)
SELECT ({'x space': 1, 'y': 2, 'z': 3})['x space'];
-- The struct_extract function is also equivalent. This returns 1
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3},'x space');
```

### Creating Structs with the Row function
The `row` function can be used to automatically convert multiple columns to a single struct column. The name of each input column is used as a key, and the value of each column becomes the struct's value at that key. Using a `row` function on the columns of this example table produces the output below.
#### Example data table named t1:
| my_column | another_column |
|:---|:---|
| 1 | a |
| 2 | b |

#### Row function example:
```sql
SELECT 
    row(my_column,another_column) as my_struct_column
FROM t1;
```

#### Example Output:
| my_struct_column |
|:---|
| {'my_column': 1, 'another_column': a} |
| {'my_column': 2, 'another_column': b} |

The `row` function may also be used with arbitrary expressions as input rather than column names. In the case of an expression, a key will be automatically generated in the format of 'vN' where N is an incrementing number (Ex: v1, v2, etc.). This can be combined with column names as an input in the same call to the `row` function. This example uses the same input table as above.

#### Row function example with a column name, a constant, and an expression as input:
```sql
SELECT 
    row(my_column,42,my_column + 1) as my_struct_column
FROM t1;
```
#### Example Output:
| my_struct_column |
|:---|
| {'my_column': 1, 'v2': 42, 'v3': 2} |
| {'my_column': 2, 'v2': 42, 'v3': 3} |


## Maps


## Nesting

`LIST`s and `STRUCT`s can be arbitrarily nested to any depth, so long as the type rules are observed.

```sql
-- Struct with lists
SELECT {'birds': ['duck', 'goose', 'heron'], 'aliens': NULL, 'amphibians': ['frog', 'toad']};
```

## Comparison

Nested types can be compared using all the [comparison operators](../expressions/comparison_operators).
These comparisons can be used in [logical expressions](../expressions/logical_operators)
for both `WHERE` and `HAVING` clauses, as well as for creating [Boolean values](./boolean).

The ordering is defined positionally in the same way that words can be ordered in a dictionary.
`NULL` values compare greater than all other values and are considered equal to each other.

At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_ , however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Grouping and Joining

Nested types can be used in `GROUP BY` clauses and as expressions for `JOIN`s.

## Functions
See [Nested Functions](/docs/sql/functions/nested).
