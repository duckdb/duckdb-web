---
layout: docu
title: Array
---

An `ARRAY` column stores fixed-sized arrays. All fields in the column must have the same length and the same underlying type. `ARRAY`s are typically used to store arrays of numbers, but can contain any uniform data type, including `ARRAY`, `LIST` and `STRUCT` types.

To store variable-length lists, use the [`LIST` type](list). See the [data types overview](../../sql/data_types/overview) for a comparison between nested data types.

> The `ARRAY` type in PostgreSQL allows variable-length fields. DuckDB's `ARRAY` type is fixed-length.

## Creating Arrays

Arrays can be created using the [`array_value(expr, ...)`](../functions/nested#list-functions) function.

```sql
-- Construct with the 'array_value' function
SELECT array_value(1, 2, 3);
-- You can always implicitly cast an array to a list (and use list functions, like list_extract, '[i]')
SELECT array_value(1, 2, 3)[2];
-- You can cast from a list to an array, but the dimensions have to match up!
SELECT [3, 2, 1]::INT[3];
-- Arrays can be nested
SELECT array_value(array_value(1, 2), array_value(3, 4), array_value(5, 6));
-- Arrays can store structs
SELECT array_value({'a': 1, 'b': 2}, {'a': 3, 'b': 4});
```

## Defining an Array Field

Arrays can be created using the `<TYPE_NAME>[<LENGTH>]` syntax. For example, to create an array field for 3 integers, run:

```sql
CREATE TABLE array_table(id INT, arr INT[3]);
INSERT INTO array_table VALUES (10, [1, 2, 3]), (20, [4, 5, 6]);
```

## Retrieving from Arrays

Retrieving one or more values from an array can be accomplished using brackets and slicing notation, or through [list functions](../functions/nested#list-functions) like `list_extract` and `array_extract`. Using the example in [Defining an Array Field](#defining-an-array-field).

The following queries for extracting the second element of an array are equivalent:

```sql
SELECT id, arr[1] AS element FROM array_table;
SELECT id, list_extract(arr, 1) AS element FROM array_table;
SELECT id, array_extract(arr, 1) AS element FROM array_table;
```

```text
┌───────┬─────────┐
│  id   │ element │
│ int32 │  int32  │
├───────┼─────────┤
│    10 │       1 │
│    20 │       4 │
└───────┴─────────┘
```

Slicing notation returns a `LIST`:

```sql
SELECT id, arr[1:2] AS elements FROM array_table;
```

```text
┌───────┬──────────┐
│  id   │ elements │
│ int32 │ int32[]  │
├───────┼──────────┤
│    10 │ [1, 2]   │
│    20 │ [4, 5]   │
└───────┴──────────┘
```

## Ordering

The ordering is defined using a lexicographical order. `NULL` values compare greater than all other values and are considered equal to each other.

## Functions

See [Nested Functions](../../sql/functions/nested).
