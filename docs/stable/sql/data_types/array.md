---
layout: docu
redirect_from:
  - /docs/sql/data_types/array
title: Array Type
---

An `ARRAY` column stores fixed-sized arrays. All fields in the column must have the same length and the same underlying type. Arrays are typically used to store arrays of numbers, but can contain any uniform data type, including `ARRAY`, [`LIST`]({% link docs/stable/sql/data_types/list.md %}) and [`STRUCT`]({% link docs/stable/sql/data_types/struct.md %}) types.

Arrays can be used to store vectors such as [word embeddings](https://en.wikipedia.org/wiki/Word_embedding) or image embeddings.

To store variable-length lists, use the [`LIST` type]({% link docs/stable/sql/data_types/list.md %}). See the [data types overview]({% link docs/stable/sql/data_types/overview.md %}) for a comparison between nested data types.

> The `ARRAY` type in PostgreSQL allows variable-length fields. DuckDB's `ARRAY` type is fixed-length.

## Creating Arrays

Arrays can be created using the [`array_value(expr, ...)` function]({% link docs/stable/sql/functions/array.md %}#array_valueindex).

Construct with the `array_value` function:

```sql
SELECT array_value(1, 2, 3);
```

You can always implicitly cast an array to a list (and use list functions, like `list_extract`, `[i]`):

```sql
SELECT array_value(1, 2, 3)[2];
```

You can cast from a list to an array (the dimensions have to match):

```sql
SELECT [3, 2, 1]::INTEGER[3];
```

Arrays can be nested:

```sql
SELECT array_value(array_value(1, 2), array_value(3, 4), array_value(5, 6));
```

Arrays can store structs:

```sql
SELECT array_value({'a': 1, 'b': 2}, {'a': 3, 'b': 4});
```

## Defining an Array Field

Arrays can be created using the `⟨TYPE_NAME⟩[⟨LENGTH⟩]`{:.language-sql .highlight} syntax. For example, to create an array field for 3 integers, run:

```sql
CREATE TABLE array_table (id INTEGER, arr INTEGER[3]);
INSERT INTO array_table VALUES (10, [1, 2, 3]), (20, [4, 5, 6]);
```

## Retrieving Values from Arrays

Retrieving one or more values from an array can be accomplished using brackets and slicing notation, or through [list functions]({% link docs/stable/sql/functions/list.md %}#list-functions) like `list_extract` and `array_extract`. Using the example in [Defining an Array Field](#defining-an-array-field).

The following queries for extracting the first element of an array are equivalent:

```sql
SELECT id, arr[1] AS element FROM array_table;
SELECT id, list_extract(arr, 1) AS element FROM array_table;
SELECT id, array_extract(arr, 1) AS element FROM array_table;
```

| id | element |
|---:|--------:|
| 10 | 1       |
| 20 | 4       |

Using the slicing notation returns a `LIST`:

```sql
SELECT id, arr[1:2] AS elements FROM array_table;
```

| id | elements |
|---:|----------|
| 10 | [1, 2]   |
| 20 | [4, 5]   |

## Functions

All [`LIST` functions]({% link docs/stable/sql/functions/list.md %}) work with the `ARRAY` type. Additionally, several `ARRAY`-native functions are also supported.
See the [`ARRAY` functions]({% link docs/stable/sql/functions/array.md %}#array-native-functions).

## Examples

Create sample data:

```sql
CREATE TABLE x (i INTEGER, v FLOAT[3]);
CREATE TABLE y (i INTEGER, v FLOAT[3]);
INSERT INTO x VALUES (1, array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT));
INSERT INTO y VALUES (1, array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT));
```

Compute cross product:

```sql
SELECT array_cross_product(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
```

Compute cosine similarity:

```sql
SELECT array_cosine_similarity(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
```

## Ordering

The ordering of `ARRAY` instances is defined using a lexicographical order. `NULL` values compare greater than all other values and are considered equal to each other.

## See Also

For more functions, see [List Functions]({% link docs/stable/sql/functions/list.md %}).
