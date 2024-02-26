---
layout: docu
title: Struct Data Type
---

Conceptually, a `STRUCT` column contains an ordered list of columns called "entries". The entries are referenced by name using strings. This document refers to those entry names as keys. Each row in the `STRUCT` column must have the same keys. The names of the struct entries are part of the *schema*. Each row in a `STRUCT` column must have the same layout. The names of the struct entries are case-insensitive.

`STRUCT`s are typically used to nest multiple columns into a single column, and the nested column can be of any type, including other `STRUCT`s and `LIST`s.

`STRUCT`s are similar to PostgreSQL's `ROW` type. The key difference is that DuckDB `STRUCT`s require the same keys in each row of a `STRUCT` column. This allows DuckDB to provide significantly improved performance by fully utilizing its vectorized execution engine, and also enforces type consistency for improved correctness. DuckDB includes a `row` function as a special way to produce a `STRUCT`, but does not have a `ROW` data type. See an example below and the [nested functions docs](../functions/nested#struct-functions) for details.

See the [data types overview](../../sql/data_types/overview) for a comparison between nested data types.

### Creating Structs

Structs can be created using the [`struct_pack(name := expr, ...)`](../functions/nested#struct-functions) function or the equivalent array notation `{'name': expr, ...}` notation. The expressions can be constants or arbitrary expressions.

```sql
-- Struct of integers
SELECT {'x': 1, 'y': 2, 'z': 3};
-- Struct of strings with a NULL value
SELECT {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'};
-- Struct with a different type for each key
SELECT {'key1': 'string', 'key2': 1, 'key3': 12.345};
-- Struct using the struct_pack function. 
-- Note the lack of single quotes around the keys and the use of the := operator
SELECT struct_pack(key1 := 'value1', key2 := 42);
-- Struct of structs with NULL values
SELECT {'birds':
            {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'},
        'aliens':
            NULL,
        'amphibians':
            {'yes':'frog', 'maybe': 'salamander', 'huh': 'dragon', 'no':'toad'}
        };
-- Create a struct from columns and/or expressions using the row function.
-- This returns {'': 1, '': 2, '': a}
SELECT row(x, x + 1, y) FROM (SELECT 1 AS x, 'a' AS y);
-- If using multiple expressions when creating a struct, the row function is optional
-- This also returns {'': 1, '': 2, '': a}
SELECT (x, x + 1, y) FROM (SELECT 1 AS x, 'a' AS y);
```

### Adding Field(s)/Value(s) to Structs

```sql
-- Add to a Struct of integers
SELECT struct_insert({'a': 1, 'b': 2, 'c': 3}, d := 4);
```

### Retrieving from Structs

Retrieving a value from a struct can be accomplished using dot notation, bracket notation, or through [struct functions](../functions/nested#struct-functions) like `struct_extract`.

```sql
-- Use dot notation to retrieve the value at a key's location. This returns 1
-- The subquery generates a struct column "a", which we then query with a.x
SELECT a.x FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
-- If key contains a space, simply wrap it in double quotes. This returns 1
-- Note: Use double quotes not single quotes 
-- This is because this action is most similar to selecting a column from within the struct
SELECT a."x space" FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
-- Bracket notation may also be used. This returns 1
-- Note: Use single quotes since the goal is to specify a certain string key. 
-- Only constant expressions may be used inside the brackets (no columns)
SELECT a['x space'] FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
-- The struct_extract function is also equivalent. This returns 1
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3}, 'x space');
```

#### `Struct.*`

Rather than retrieving a single key from a struct, star notation (`*`) can be used to retrieve all keys from a struct as separate columns. 
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys.

```sql
-- All keys within a struct can be returned as separate columns using *
SELECT a.* FROM (SELECT {'x':1, 'y':2, 'z':3} AS a);
```

<div class="narrow_table"></div>

| x | y | z |
|:---|:---|:---|
| 1 | 2 | 3 |

### Dot Notation Order of Operations

Referring to structs with dot notation can be ambiguous with referring to schemas and tables. In general, DuckDB looks for columns first, then for struct keys within columns. DuckDB resolves references in these orders, using the first match to occur:

#### No Dots

```sql
SELECT part1 FROM tbl
```
1. part1 is a column

#### One Dot

```sql
SELECT part1.part2 FROM tbl
```
1. part1 is a table, part2 is a column
2. part1 is a column, part2 is a property of that column

#### Two (or More) Dots

```sql
SELECT part1.part2.part3 FROM tbl
```
1. part1 is a schema, part2 is a table, part3 is a column
2. part1 is a table, part2 is a column, part3 is a property of that column
3. part1 is a column, part2 is a property of that column, part3 is a property of that column

Any extra parts (e.g., .part4.part5 etc) are always treated as properties

### Creating Structs with the `row` Function

The `row` function can be used to automatically convert multiple columns to a single struct column.
When using `row` the keys will be empty strings allowing for easy insertion into a table with a struct column.
Columns, however, cannot be initialized with the `row` function, and must be explicitly named.
For example:

```sql
-- Inserting values into a struct column using the row function
CREATE TABLE t1 (s STRUCT(v VARCHAR, i INTEGER));
INSERT INTO t1 VALUES (ROW('a', 42));
-- The table will contain a single entry:
-- {'v': a, 'i': 42}

-- The following produces the same result as above
CREATE TABLE t1 AS (
    SELECT ROW('a', 42)::STRUCT(v VARCHAR, i INTEGER)
);

-- Initializing a struct column with the row function will fail
CREATE TABLE t2 AS SELECT ROW('a');
-- The following error is thrown:
-- "Error: Invalid Input Error: A table cannot be created from an unnamed struct"
```

When casting structs, the names of fields have to match. Therefore, the following query will fail:

```sql
SELECT a::STRUCT(y INTEGER) AS b
FROM
    (SELECT {'x': 42} AS a);
```

```text
Error: Mismatch Type Error: Type STRUCT(x INTEGER) does not match with STRUCT(y INTEGER). Cannot cast STRUCTs with different names
```

A workaround for this would be to use [`struct_pack`](#creating-structs) instead:

```sql
SELECT struct_pack(y := a.x) AS b
FROM
    (SELECT {'x': 42} AS a);
```

> This behavior was introduced in DuckDB v0.9.0. Previously, this query ran successfully and returned struct `{'y': 42}` as column `b`.

## Comparison Operators

Nested types can be compared using all the [comparison operators](../expressions/comparison_operators).
These comparisons can be used in [logical expressions](../expressions/logical_operators)
for both `WHERE` and `HAVING` clauses, as well as for creating [`BOOLEAN` values](boolean).

The ordering is defined positionally in the same way that words can be ordered in a dictionary.
`NULL` values compare greater than all other values and are considered equal to each other.

At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_, however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Functions

See [Nested Functions](../../sql/functions/nested).
