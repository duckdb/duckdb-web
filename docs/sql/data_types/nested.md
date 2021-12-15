---
layout: docu
title: Nested Types
selected: Documentation/Data Types/Nested
expanded: Data Types
---
This section describes functions and operators for examining and manipulating nested values. DuckDB supports three nested data types: lists, structs, and maps.

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:---|:---|:---|:---|:---|
| LIST | An ordered sequence of data values of the same type. | Each row must have the same data type within each LIST, but can have any number of elements. | [1, 2, 3] | INT[ ] |
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
-- Create a table with an integer list column and a varchar list column
CREATE TABLE list_table (int_list INT[], varchar_list VARCHAR[]);
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


## Maps
`MAP`s are similar to `STRUCT`s in that they are an ordered list of "entries" where a key maps to a value. However, `MAP`s do not need to have the same keys present on each row, and thus open additional use cases. `MAP`s are useful when the schema is unknown beforehand, and when adding or removing keys in subsequent rows. Their flexibility is a key differentiator.

`MAP`s must have a single type for all keys, and a single type for all values. Keys and values can be any type, and the type of the keys does not need to match the type of the values (Ex: a `MAP` of `INT`s to `VARCHAR`s). `MAP`s may also have duplicate keys. This is possible and useful because maps are ordered. `MAP`s are also more forgiving when extracting values, as they return an empty list if a key is not found rather than throwing an error as structs do.

In contrast, `STRUCT`s must have string keys, but each key may have a value of a different type. `STRUCT`s may not have duplicate keys.

To construct a `MAP`, use the `map` function. Provide a list of keys as the first parameter, and a list of values for the second.

### Creating Maps
```sql
-- A map with integer keys and varchar values. This returns {1=a, 5=e}
select map([1, 5], ['a', 'e']);
-- A map with integer keys and numeric values. This returns {1=42.001, 5=-32.100} 
select map([1, 5], [42.001, -32.1]);
-- Keys and/or values can also be nested types.
-- This returns {[a, b]=[1.1, 2.2], [c, d]=[3.3, 4.4]}
select map([['a', 'b'], ['c', 'd']], [[1.1, 2.2], [3.3, 4.4]]);
-- Create a table with a map column that has integer keys and double values
CREATE TABLE map_table (map_col MAP(INT,DOUBLE));
```
### Retrieving from Maps
`MAP`s use bracket notation for retrieving values. This is due to the variety of types that can be used as a `MAP`'s key. Selecting from a `MAP` also returns a `LIST` rather than an individual value.
```sql
-- Use bracket notation to retrieve a list containing the value at a key's location. This returns [42]
-- Note that the expression in bracket notation must match the type of the map's key
SELECT map([100, 5], [42, 43])[100];
-- To retrieve the underlying value, use list selection syntax to grab the 0th element.
-- This returns 42
SELECT map([100, 5], [42, 43])[100][0];
-- If the element is not in the map, an empty list will be returned. Returns []
-- Note that the expression in bracket notation must match the type of the map's key else an error is returned
SELECT map([100, 5], [42, 43])[123];
-- The element_at function can also be used to retrieve a map value. This returns [42]
SELECT element_at(map([100, 5], [42, 43]),100);
```

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
