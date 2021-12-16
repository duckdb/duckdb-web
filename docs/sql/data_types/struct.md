---
layout: docu
title: Struct
selected: Documentation/Data Types/Struct
expanded: Nested
---

## Struct Data Type

Conceptually, a `STRUCT` column contains an ordered list of other columns called "entries". The entries are referenced by name using strings. This document refers to those entry names as keys. Each row in the `STRUCT` column must have the same keys. Each key must have the same type of value for each row.

`STRUCT`s are typically used to nest multiple columns into a single column,
and the nested column can be of any type, including other `STRUCT`s and `LIST`s.

`STRUCT`s are similar to Postgres's `ROW` type. The key difference is that DuckDB `STRUCT`s require the same keys in each row of a `STRUCT` column. This allows DuckDB to provide significantly improved performance by fully utilizing its vectorized execution engine, and also enforces type consistency for improved correctness. DuckDB includes a `row` function as a special way to produce a struct, but does not have a `ROW` data type. See an example below and the [nested functions docs](../functions/nested#struct-functions) for details.

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
-- Create a struct from columns and/or expressions using the row function.
-- This returns {'x': 1, 'v2': 2, 'y': a}
SELECT row(x, x + 1, y) FROM (SELECT 1 as x, 'a' as y);
-- If using multiple expressions when creating a struct, the row function is optional
-- This also returns {'x': 1, 'v2': 2, 'y': a}
SELECT (x, x + 1, y) FROM (SELECT 1 as x, 'a' as y);
```
### Retrieving from Structs
Retrieving a value from a struct can be accomplished using dot notation, bracket notation, or through [struct functions](../functions/nested#struct-functions) like `struct_extract`.
```sql
-- Use dot notation to retrieve the value at a key's location. This returns 1
-- The subquery generates a struct column "a", which we then query with a.x
SELECT a.x FROM (SELECT {'x':1, 'y':2, 'z':3} as a);
-- If key contains a space, simply wrap it in double quotes. This returns 1
-- Note: Use double quotes not single quotes 
-- This is because this action is most similar to selecting a column from within the struct
SELECT a."x space" FROM (SELECT {'x space':1, 'y':2, 'z':3} as a);
-- Bracket notation may also be used. This returns 1
-- Note: Use single quotes since the goal is to specify a certain string key. 
-- Only constant expressions may be used inside the brackets (no columns)
SELECT a['x space'] FROM (SELECT {'x space':1, 'y':2, 'z':3} as a);
-- The struct_extract function is also equivalent. This returns 1
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3},'x space');
```
Referring to structs with dot notation can be ambiguous with referring to schemas and tables. In general, DuckDB looks for columns first, then for struct keys within columns. DuckDB resolves references in these orders, using the first match to occur:

#### No dots
```sql
SELECT part1 FROM tbl
```
1. part1 is a column

#### One dot
```sql
SELECT part1.part2 FROM tbl
```
1. part1 is a table, part2 is a column
2. part1 is a column, part2 is a property of that column

#### Two (or more) dots
```sql
SELECT part1.part2.part3 FROM tbl
```
1. part1 is a schema, part2 is a table, part3 is a column
2. part1 is a table, part2 is a column, part3 is a property of that column
3. part1 is a column, part2 is a property of that column, part3 is a property of that column

Any extra parts (e.g. .part4.part5 etc) are always treated as properties

### Creating Structs with the Row function
The `row` function can be used to automatically convert multiple columns to a single struct column. The name of each input column is used as a key, and the value of each column becomes the struct's value at that key.

When converting multiple expressions into a `STRUCT`, the `row` function name is optional - a set of parenthesis is all that is needed.
#### Example data table named t1:

| my_column | another_column |
|:---|:---|
| 1 | a |
| 2 | b |

#### Row function example:
```sql
SELECT 
    row(my_column, another_column) as my_struct_column,
    (my_column, another_column) as identical_struct_column
FROM t1;
```

#### Example Output:

| my_struct_column | identical_struct_column |
|:---|:---|
| {'my_column': 1, 'another_column': a} | {'my_column': 1, 'another_column': a} |
| {'my_column': 2, 'another_column': b} | {'my_column': 2, 'another_column': b} |

The `row` function (or simplified parenthesis syntax) may also be used with arbitrary expressions as input rather than column names. In the case of an expression, a key will be automatically generated in the format of 'vN' where N is a number that refers to its parameter location in the row function (Ex: v1, v2, etc.). This can be combined with column names as an input in the same call to the `row` function. This example uses the same input table as above.

#### Row function example with a column name, a constant, and an expression as input:
```sql
SELECT 
    row(my_column, 42, my_column + 1) as my_struct_column,
    (my_column, 42, my_column + 1) as identical_struct_column
FROM t1;
```
#### Example Output:

| my_struct_column | identical_struct_column |
|:---|:---|
| {'my_column': 1, 'v2': 42, 'v3': 2} | {'my_column': 1, 'v2': 42, 'v3': 2} |
| {'my_column': 2, 'v2': 42, 'v3': 3} | {'my_column': 2, 'v2': 42, 'v3': 3} |

## Comparison with other nested types
DuckDB supports three nested data types: lists, structs, and maps. Each supports different use cases and has a different structure. 

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:---|:---|:---|:---|:---|
| [LIST](/docs/sql/data_types/list) | An ordered sequence of data values of the same type. | Each row must have the same data type within each LIST, but can have any number of elements. | [1, 2, 3] | INT[ ] |
| [STRUCT](/docs/sql/data_types/struct) | A dictionary of multiple named values, where each key is a string, but the value can be a different type for each key. | Each row must have the same keys. | {'i': 42, 'j': 'a'} | STRUCT<i: INT, j: VARCHAR> |
| [MAP](/docs/sql/data_types/map) | A dictionary of multiple named values, each key having the same type and each value having the same type. Keys and values can be any type and can be different types from one another. | Rows may have different keys. | map([1,2],['a','b']) | MAP<INT, VARCHAR> |

## Nesting

`LIST`s, `STRUCT`s, and `MAP`s can be arbitrarily nested to any depth, so long as the type rules are observed.

```sql
-- Struct with lists
SELECT {'birds': ['duck', 'goose', 'heron'], 'aliens': NULL, 'amphibians': ['frog', 'toad']};
-- Struct with list of maps
SELECT {'test': [map([1, 5], [42.1, 45]), map([1, 5], [42.1, 45])]};
```

## Comparison Operators

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
