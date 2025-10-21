---
layout: docu
redirect_from:
- /docs/sql/data_types/struct
title: Struct Data Type
---

Conceptually, a `STRUCT` column contains an ordered list of columns called “entries”. The entries are referenced by name using strings. This document refers to those entry names as keys. Each row in the `STRUCT` column must have the same keys. The names of the struct entries are part of the *schema*. Each row in a `STRUCT` column must have the same layout. The names of the struct entries are case-insensitive.

`STRUCT`s are typically used to nest multiple columns into a single column, and the nested column can be of any type, including other `STRUCT`s and `LIST`s.

`STRUCT`s are similar to PostgreSQL's `ROW` type. The key difference is that DuckDB `STRUCT`s require the same keys in each row of a `STRUCT` column. This allows DuckDB to provide significantly improved performance by fully utilizing its vectorized execution engine, and also enforces type consistency for improved correctness. DuckDB includes a `row` function as a special way to produce a `STRUCT`, but does not have a `ROW` data type. See an example below and the [`STRUCT` functions documentation]({% link docs/stable/sql/functions/struct.md %}) for details.

See the [data types overview]({% link docs/stable/sql/data_types/overview.md %}) for a comparison between nested data types.

### Creating Structs

Structs can be created using the [`struct_pack(name := expr, ...)`]({% link docs/stable/sql/functions/struct.md %}) function, the equivalent array notation `{'name': expr, ...}`, using a row variable, or using the `row` function.

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

### Adding or Updating Fields of Structs

To add new fields or update existing ones, you can use `struct_update`:

```sql
SELECT struct_update({'a': 1, 'b': 2}, b := 3, c := 4) AS s;
```

Alternatively, `struct_insert` also allows adding new fields but not updating existing ones.

### Retrieving from Structs

Retrieving a value from a struct can be accomplished using dot notation, bracket notation, or through [struct functions]({% link docs/stable/sql/functions/struct.md %}) like `struct_extract`.

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

The `struct_extract` function is also equivalent. This returns 1:

```sql
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3}, 'x space');
```

#### `unnest` / `STRUCT.*`

Rather than retrieving a single key from a struct, the `unnest` special function can be used to retrieve all keys from a struct as separate columns.
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys:

```sql
SELECT unnest(a)
FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |

The same can be achieved with the star notation (`*`), which additionally allows [modifications of the returned columns]({% link docs/stable/sql/expressions/star.md %}):

```sql
SELECT a.* EXCLUDE ('y')
FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

| x | z |
|--:|--:|
| 1 | 3 |

> Warning The star notation is currently limited to top-level struct columns and non-aggregate expressions.

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
Invalid Input Error:
A table cannot be created from an unnamed struct
```

When casting between structs, the names of at least one field have to match. Therefore, the following query will fail:

```sql
SELECT a::STRUCT(y INTEGER) AS b
FROM
    (SELECT {'x': 42} AS a);
```

```console
Binder Error:
STRUCT to STRUCT cast must have at least one matching member
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

The `STRUCT` type can be compared using all the [comparison operators]({% link docs/stable/sql/expressions/comparison_operators.md %}).
These comparisons can be used in [logical expressions]({% link docs/stable/sql/expressions/logical_operators.md %})
such as `WHERE` and `HAVING` clauses, and return [`BOOLEAN` values]({% link docs/stable/sql/data_types/boolean.md %}).

Comparisons are done in lexicographical order, with individual entries being compared as usual except that `NULL` values are treated as larger than all other values.

Specifically:

* If all values of `s1` and `s2` compare equal, then `s1` and `s2` compare equal.
* else, if `s1.value[i] < s2.value[i] OR s2.value[i] is NULL` for the first index `i` where `s1.value[i] != s2.value[i]`, then `s1` is less than `s2`, and vice versa.

Structs of different types are implicitly cast to a struct type with the union of the involved keys, following the rules for [combination casting]({% link docs/stable/sql/data_types/typecasting.md %}#structs).

The following queries return `true`:

```sql
SELECT {'k1': 0, 'k2': 0} < {'k1': 1, 'k2': 0};
```

```sql
SELECT {'k1': 'hello'} < {'k1': 'world'};
```

```sql
SELECT {'k1': 0, 'k2': 0} < {'k1': 0, 'k2': NULL};
```

```sql
SELECT {'k1': 0} < {'k2': 0};
```

```sql
SELECT  {'k1': 0, 'k2': 0} < {'k2': 0, 'k3': 0};
```

```sql
SELECT {'k1': 1, 'k2': 0} > {'k3': 0, 'k1': 0};
```

The following queries return `false`:

```sql
SELECT {'k1': 1, 'k2': 0} < {'k1': 0, 'k2': 1};
```

```sql
SELECT {'k1': [0]} < {'k1': [0, 0]};
```

```sql
SELECT {'k1': 1} > {'k2': 0};
```

```sql
SELECT {'k1': 0, 'k2': 0} < {'k3': 0, 'k1': 1};
```

```sql
SELECT  {'k1': 1, 'k2': 0} > {'k2': 0, 'k3': 0};
```

## Updating the Schema

Starting with DuckDB v1.3.0, it's possible to update the sub-schema of structs
using the [`ALTER TABLE` clause]({% link docs/stable/sql/statements/alter_table.md %}).

To follow the examples, initialize the `test` table as follows:

```sql
CREATE TABLE test (s STRUCT(i INTEGER, j INTEGER));
INSERT INTO test VALUES (ROW(1, 1)), (ROW(2, 2));
```

### Adding a Field

Add field `k INTEGER` to struct `s` in table `test`:

```sql
ALTER TABLE test ADD COLUMN s.k INTEGER;
FROM test;
```

```text
┌─────────────────────────────────────────┐
│                    s                    │
│ struct(i integer, j integer, k integer) │
├─────────────────────────────────────────┤
│ {'i': 1, 'j': 1, 'k': NULL}             │
│ {'i': 2, 'j': 2, 'k': NULL}             │
└─────────────────────────────────────────┘
```

### Dropping a Field

Drop field `i` from struct `s` in table `test`:

```sql
ALTER TABLE test DROP COLUMN s.i;
FROM test;
```

```text
┌──────────────────────────────┐
│              s               │
│ struct(j integer, k integer) │
├──────────────────────────────┤
│ {'j': 1, 'k': NULL}          │
│ {'j': 2, 'k': NULL}          │
└──────────────────────────────┘
```

### Renaming a Field

Renaming field `j` of struct `s` to `v1` in table test`:

```sql
ALTER TABLE test RENAME s.j TO v1;
FROM test;
```

```text
┌───────────────────────────────┐
│               s               │
│ struct(v1 integer, k integer) │
├───────────────────────────────┤
│ {'v1': 1, 'k': NULL}          │
│ {'v1': 2, 'k': NULL}          │
└───────────────────────────────┘
```

## Functions

See [Struct Functions]({% link docs/stable/sql/functions/struct.md %}).
