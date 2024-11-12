---
layout: docu
title: Struct Data Type
---

Conceptually, a `STRUCT` column contains an ordered list of columns called “entries”. The entries are referenced by name using strings. This document refers to those entry names as keys. Each row in the `STRUCT` column must have the same keys. The names of the struct entries are part of the *schema*. Each row in a `STRUCT` column must have the same layout. The names of the struct entries are case-insensitive.

`STRUCT`s are typically used to nest multiple columns into a single column, and the nested column can be of any type, including other `STRUCT`s and `LIST`s.

`STRUCT`s are similar to PostgreSQL's `ROW` type. The key difference is that DuckDB `STRUCT`s require the same keys in each row of a `STRUCT` column. This allows DuckDB to provide significantly improved performance by fully utilizing its vectorized execution engine, and also enforces type consistency for improved correctness. DuckDB includes a `row` function as a special way to produce a `STRUCT`, but does not have a `ROW` data type. See an example below and the [`STRUCT` functions documentation]({% link docs/sql/functions/struct.md %}) for details.

`STRUCT`s have a fixed schema. It is not possible to change the schema of a `STRUCT` using `UPDATE` operations.

See the [data types overview]({% link docs/sql/data_types/overview.md %}) for a comparison between nested data types.

### Creating Structs

Structs can be created using the [`struct_pack(name := expr, ...)`]({% link docs/sql/functions/struct.md %}) function, the equivalent array notation `{'name': expr, ...}`, using a row variable, or using the `row` function.

Create a struct using the `struct_pack` function. Note the lack of single quotes around the keys and the use of the `:=` operator:

```sql
SELECT struct_pack(key1 := 'value1', key2 := 42) AS s;
```

Create a struct using the array notation:

```sql
SELECT {'key1': 'value1', 'key2': 42} AS s;
```

Create a struct using a row variable:

```sql
SELECT d AS s FROM (SELECT 'value1' AS key1, 42 AS key2) d;
```

Create a struct of integers:

```sql
SELECT {'x': 1, 'y': 2, 'z': 3} AS s;
```

Create a struct of strings with a `NULL` value:

```sql
SELECT {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'} AS s;
```

Create a struct with a different type for each key:

```sql
SELECT {'key1': 'string', 'key2': 1, 'key3': 12.345} AS s;
```

Create a struct of structs with `NULL` values:

```sql
SELECT {
        'birds': {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'},
        'aliens': NULL,
        'amphibians': {'yes': 'frog', 'maybe': 'salamander', 'huh': 'dragon', 'no': 'toad'}
    } AS s;
```

### Adding Field(s)/Value(s) to Structs

Add to a struct of integers:

```sql
SELECT struct_insert({'a': 1, 'b': 2, 'c': 3}, d := 4) AS s;
```

### Retrieving from Structs

Retrieving a value from a struct can be accomplished using dot notation, bracket notation, or through [struct functions]({% link docs/sql/functions/struct.md %}) like `struct_extract`.

Use dot notation to retrieve the value at a key's location. In the following query, the subquery generates a struct column `a`, which we then query with `a.x`.

```sql
SELECT a.x FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

If a key contains a space, simply wrap it in double quotes (`"`).

```sql
SELECT a."x space" FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
```

Bracket notation may also be used. Note that this uses single quotes (`'`) since the goal is to specify a certain string key and only constant expressions may be used inside the brackets (no expressions):

```sql
SELECT a['x space'] FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
```

The struct_extract function is also equivalent. This returns 1:

```sql
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3}, 'x space');
```

#### `STRUCT.*`

Rather than retrieving a single key from a struct, star notation (`*`) can be used to retrieve all keys from a struct as separate columns.
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys.

All keys within a struct can be returned as separate columns using `*`:

```sql
SELECT a.*
FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

<div class="narrow_table"></div>

| x | y | z |
|:---|:---|:---|
| 1 | 2 | 3 |

### Dot Notation Order of Operations

Referring to structs with dot notation can be ambiguous with referring to schemas and tables. In general, DuckDB looks for columns first, then for struct keys within columns. DuckDB resolves references in these orders, using the first match to occur:

#### No Dots

```sql
SELECT part1
FROM tbl;
```

1. `part1` is a column

#### One Dot

```sql
SELECT part1.part2
FROM tbl;
```

1. `part1` is a table, `part2` is a column
2. `part1` is a column, `part2` is a property of that column

#### Two (or More) Dots

```sql
SELECT part1.part2.part3
FROM tbl;
```

1. `part1` is a schema, `part2` is a table, `part3` is a column
2. `part1` is a table, `part2` is a column, `part3` is a property of that column
3. `part1` is a column, `part2` is a property of that column, `part3` is a property of that column

Any extra parts (e.g., `.part4.part5`, etc.) are always treated as properties

### Creating Structs with the `row` Function

The `row` function can be used to automatically convert multiple columns to a single struct column.
When using `row` the keys will be empty strings allowing for easy insertion into a table with a struct column.
Columns, however, cannot be initialized with the `row` function, and must be explicitly named.
For example, inserting values into a struct column using the `row` function:

```sql
CREATE TABLE t1 (s STRUCT(v VARCHAR, i INTEGER));
INSERT INTO t1 VALUES (row('a', 42));
SELECT * FROM t1;
```

The table will contain a single entry:

```sql
{'v': a, 'i': 42}
```

The following produces the same result as above:

```sql
CREATE TABLE t1 AS (
    SELECT row('a', 42)::STRUCT(v VARCHAR, i INTEGER)
);
```

Initializing a struct column with the `row` function will fail:

```sql
CREATE TABLE t2 AS SELECT row('a');
```

```console
Invalid Input Error: A table cannot be created from an unnamed struct
```

When casting structs, the names of fields have to match. Therefore, the following query will fail:

```sql
SELECT a::STRUCT(y INTEGER) AS b
FROM
    (SELECT {'x': 42} AS a);
```

```console
Mismatch Type Error: Type STRUCT(x INTEGER) does not match with STRUCT(y INTEGER). Cannot cast STRUCTs - element "x" in source struct was not found in target struct
```

A workaround for this is to use [`struct_pack`](#creating-structs) instead:

```sql
SELECT struct_pack(y := a.x) AS b
FROM
    (SELECT {'x': 42} AS a);
```

The `row` function can be used to return unnamed structs. For example:

```sql
SELECT row(x, x + 1, y) FROM (SELECT 1 AS x, 'a' AS y) AS s;
```

This produces `(1, 2, a)`.

If using multiple expressions when creating a struct, the `row` function is optional. The following query returns the same result as the previous one:

```sql
SELECT (x, x + 1, y) AS s FROM (SELECT 1 AS x, 'a' AS y);
```

## Comparison and Ordering

The `STRUCT` type can be compared using all the [comparison operators]({% link docs/sql/expressions/comparison_operators.md %}).
These comparisons can be used in [logical expressions]({% link docs/sql/expressions/logical_operators.md %})
such as `WHERE` and `HAVING` clauses, and return [`BOOLEAN` values]({% link docs/sql/data_types/boolean.md %}).

For comparisons, the keys of a `STRUCT` have a fixed positional order, from left to right.
Comparisons behave the same as row comparisons, therefore, matching keys must be at identical positions.

Specifically, for any `STRUCT` comparison, the following rules apply:

* **Equality.** `s1` and `s2` are equal, if all respective values are equal.
* **Less Than**. For the first index `i` where `s1.value[i] != s2.value[i]`:
If `s1.value[i] < s2.value[i]`, `s1` is less than `s2`.

`NULL` values are compared following PostgreSQL's semantics.
Lower nesting levels are used for tie-breaking.

Here are some queries returning `true` for the comparison.

```sql
SELECT {'k1': 2, 'k2': 3} < {'k1': 2, 'k2': 4} AS result;
```

```sql
SELECT {'k1': 'hello'} < {'k1': 'world'} AS result;
```

These queries return `false`.

```sql
SELECT {'k2': 4, 'k1': 3} < {'k2': 2, 'k1': 4} AS result;
```

```sql
SELECT {'k1': [4, 3]} < {'k1': [3, 6, 7]} AS result;
```

These queries return `NULL`.

```sql
SELECT {'k1': 2, 'k2': 3} < {'k1': 2, 'k2': NULL} AS result;
```

This query returns a `Binder Error` because the keys do not match positionally.

```sql
SELECT {'k1': 2, 'k2': 3} < {'k2': 2, 'k1': 4} AS result;
```

```console
Binder Error: Cannot compare values of type STRUCT(k1 INTEGER, k2 INTEGER)
and type STRUCT(k2 INTEGER, k1 INTEGER) - an explicit cast is required
```

## Functions

See [Struct Functions]({% link docs/sql/functions/struct.md %}).
