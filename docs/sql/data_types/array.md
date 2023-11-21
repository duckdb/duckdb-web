---
layout: docu
title: Array
---

An `ARRAY` column stores fixed-sized arrays. All fields in the column must have the same length and the same underlying type. `ARRAY`s are typically used to store arrays of numbers, but can contain any uniform data type, including `ARRAY`, `LIST` and `STRUCT` types.

Arrays can be used to store vectors such as [word embeddings](https://en.wikipedia.org/wiki/Word_embedding) or image embeddings.

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

## Retrieving Values from Arrays

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

## Functions

All [`LIST` functions](../functions/nested#list-functions) work with the `ARRAY` type. Additionally, several `ARRAY`-native functions are also supported.
In the following, `l1` stands for the 3-element list created by `array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT)` and `l2` stands for `array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT)`.

| Function | Description | Example | Result |
|----|-----|-------|---|
| *`array_value`*`(`*`index`*`)`                          | Create an `ARRAY` containing the argument values.                                                                                                                                         | `array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT)` | `[1.0, 2.0, 3.0]`   |
| *`array_cross_product`*`(`*`array1`*, *`array2`*`)`     | Compute the cross product of two arrays of size 3. The array elements can not be `NULL`.                                                                                                  | `array_cross_product(l1, l2)`                     | `[-1.0, 2.0, -1.0]` |
| *`array_cosine_similarity`*`(`*`array1`*, *`array2`*`)` | Compute the cosine similarity between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments. | `array_cosine_similarity(l1, l2)`                 | `0.9925833`         |
| *`array_distance`*`(`*`array1`*, *`array2`*`)`          | Compute the distance between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments.          | `array_distance(l1, l2)`                          | `1.7320508`         |
| *`array_inner_product`*`(`*`array1`*, *`array2`*`)`     | Compute the inner product between two arrays of the same size. The array elements can not be `NULL`. The arrays can have any size as long as the size is the same for both arguments.     | `array_inner_product(l1, l2)`                     | `20.0`              |
| *`array_dot_product`*`(`*`array1`*, *`array2`*`)`       | Alias for *`array_inner_product`*`(`*`array1`*, *`array2`*`)`.                                                                                                                            | `array_dot_product(l1, l2)`                       | `20.0`              |

## Examples

```sql
-- create sample data
CREATE TABLE x(i INT, v FLOAT[3]);
CREATE TABLE y(i INT, v FLOAT[3]);
INSERT INTO x VALUES (1, array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT));
INSERT INTO y VALUES (1, array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT));
-- compute cross product
SELECT array_cross_product(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
-- compute cosine similarity
SELECT array_cosine_similarity(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
```

## Ordering

The ordering of `ARRAY` instances is defined using a lexicographical order. `NULL` values compare greater than all other values and are considered equal to each other.

## Functions

See [Nested Functions](../../sql/functions/nested).
