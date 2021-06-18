---
layout: docu
title: Nested Types
selected: Documentation/Data Types/Nested
expanded: Data Types
---
| Name | Description |
|:---|:---|
| LIST | An ordered sequence of data values of the same type. |
| STRUCT | A dictionary of multiple named values, each name having the same type. |


## Lists

A `LIST` column can have values with different lengths, but they must all have the same underlying type.
`LIST`s are typically used to store arrays of numbers, but can contain any uniform data type,
including other `LIST`s and `STRUCT`s.
`LIST`s are similar to Postgres's `ARRAY` type.

Lists can be created using the [`LIST_VALUE(expr, ...)`](../functions/nested#listfunctions) function
or the equivalent array notation `[expr, ...]` notation.
The expressions can be constants or arbitrary expressions.

```sql
-- List of integers
SELECT [1, 2, 3];
-- List of strings with a NULL value
SELECT ['duck', 'goose', NULL, 'heron'];
-- List of lists with NULL values
SELECT [['duck', 'goose', 'heron'], NULL, ['frog', 'toad'], []];
```

## Structs

Conceptually, a `STRUCT` column contains an ordered list of other columns called "entries".
The entries are referenced by name using strings.
Each value in the `STRUCT` column must have the same entry names,
and each entry must have the same type.
`STRUCT`s are typically used to nest multiple columns into a single column,
and the nested column can be of any type, including other `STRUCT`s and `LIST`s.
`STRUCT`s are similar to Postgres's `ROW` type.

Structs can be created using the [`STRUCT_PACK(name := expr, ...)`](../functions/nested#structfunctions) function
or the equivalent array notation `{'name': expr, ...}` notation.
The expressions can be constants or arbitrary expressions.

```
-- Struct of integers
SELECT {'x': 1, 'y': 2, 'z': 3};
-- Struct of strings with a NULL value
SELECT {'yes:' 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'};
-- Struct of structs with NULL values
SELECT {'birds':
            {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'},
        'aliens':
            NULL,
        'amphibians':
            {'yes':'frog', 'maybe': 'salamander', 'huh': 'dragon', 'no':'toad'}
        };
```

## Nesting

`LIST`s and `STRUCT`s can be arbitrarily nested to any depth, so long as the type rules are observed.

```
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
