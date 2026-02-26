---
layout: docu
railroad: expressions/star.js
redirect_from:
  - /docs/sql/expressions/star
title: Star Expression
---

## Syntax

<div id="rrdiagram"></div>

The `*` expression can be used in a `SELECT` statement to select all columns that are projected in the `FROM` clause.

```sql
SELECT *
FROM tbl;
```

### `TABLE.*` and `STRUCT.*`

The `*` expression can be prepended by a table name to select only columns from that table.

```sql
SELECT tbl.*
FROM tbl
JOIN other_tbl USING (id);
```

Similarly, the `*` expression can also be used to retrieve all keys from a struct as separate columns.
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys.
See the [`STRUCT` data type]({% link docs/stable/sql/data_types/struct.md %}) and [`STRUCT` functions]({% link docs/stable/sql/functions/struct.md %}) pages for more details on working with structs.

For example:

```sql
SELECT st.* FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS st);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |


### `EXCLUDE` Clause

`EXCLUDE` allows you to exclude specific columns from the `*` expression.

```sql
SELECT * EXCLUDE (col)
FROM tbl;
```

### `REPLACE` Clause

`REPLACE` allows you to replace specific columns by alternative expressions.

```sql
SELECT * REPLACE (col1 / 1_000 AS col1, col2 / 1_000 AS col2)
FROM tbl;
```

### `RENAME` Clause

`RENAME` allows you to replace specific columns.

```sql
SELECT * RENAME (col1 AS height, col2 AS width)
FROM tbl;
```

### Column Filtering via Pattern Matching Operators

The [pattern matching operators]({% link docs/stable/sql/functions/pattern_matching.md %}) `LIKE`, `GLOB`, `SIMILAR TO` and their variants allow you to select columns by matching their names to patterns.

```sql
SELECT * LIKE 'col%'
FROM tbl;
```

```sql
SELECT * GLOB 'col*'
FROM tbl;
```

```sql
SELECT * SIMILAR TO 'col.'
FROM tbl;
```

## `COLUMNS` Expression


The `COLUMNS` expression is similar to the regular star expression, but additionally allows you to execute the same expression on the resulting columns.

```sql
CREATE TABLE numbers (id INTEGER, number INTEGER);
INSERT INTO numbers VALUES (1, 10), (2, 20), (3, NULL);
SELECT min(COLUMNS(*)), count(COLUMNS(*)) FROM numbers;
```

| id | number | id | number |
|---:|-------:|---:|-------:|
| 1  | 10     | 3  | 2      |

```sql
SELECT
    min(COLUMNS(* REPLACE (number + id AS number))),
    count(COLUMNS(* EXCLUDE (number)))
FROM numbers;
```

| id | min(number := (number + id)) | id |
|---:|-----------------------------:|---:|
| 1  | 11                           | 3  |

`COLUMNS` expressions can also be combined, as long as they contain the same star expression:

```sql
SELECT COLUMNS(*) + COLUMNS(*) FROM numbers;
```

| id | number |
|---:|-------:|
| 2  | 20     |
| 4  | 40     |
| 6  | NULL   |


### `COLUMNS` Expression in a `WHERE` Clause

`COLUMNS` expressions can also be used in `WHERE` clauses. The conditions are applied to all columns and are combined using the logical `AND` operator.

```sql
SELECT *
FROM (
    SELECT 'a', 'a'
    UNION ALL
    SELECT 'a', 'b'
    UNION ALL
    SELECT 'b', 'b'
) _(x, y)
WHERE COLUMNS(*) = 'a'; -- equivalent to: x = 'a' AND y = 'a'
```

| x | y |
|--:|--:|
| a | a |

To combine conditions using the logical `OR` operator, you can `UNPACK` the `COLUMNS` expression into the variadic `greatest` function.

```sql
SELECT *
FROM (
    SELECT 'a', 'a'
    UNION ALL
    SELECT 'a', 'b'
    UNION ALL
    SELECT 'b', 'b'
) _(x, y)
WHERE greatest(UNPACK(COLUMNS(*) = 'a')); -- equivalent to: x = 'a' OR y = 'a'
```

| x | y |
|--:|--:|
| a | a |
| a | b |

### Regular Expressions in a `COLUMNS` Expression

`COLUMNS` expressions don't currently support the pattern matching operators, but they do support regular expression matching by simply passing a string constant in place of the star:

```sql
SELECT COLUMNS('(id|numbers?)') FROM numbers;
```

| id | number |
|---:|-------:|
| 1  | 10     |
| 2  | 20     |
| 3  | NULL   |

### Renaming Columns with Regular Expressions in a `COLUMNS` Expression

The matches of capture groups in regular expressions can be used to rename matching columns.
The capture groups are one-indexed; `\0` is the original column name.

For example, to select the first three letters of column names, run:

```sql
SELECT COLUMNS('(\w{3}).*') AS '\1' FROM numbers;
```

| id | num  |
|---:|-----:|
| 1  | 10   |
| 2  | 20   |
| 3  | NULL |

To remove a colon (`:`) character in the middle of a column name, run:

```sql
CREATE TABLE tbl ("Foo:Bar" INTEGER, "Foo:Baz" INTEGER, "Foo:Qux" INTEGER);
SELECT COLUMNS('(\w*):(\w*)') AS '\1\2' FROM tbl;
```

To add the original column name to the expression alias, run:

```sql
SELECT min(COLUMNS(*)) AS "min_\0" FROM numbers;
```

| min_id | min_number |
|-------:|-----------:|
|      1 |         10 |

### `COLUMNS` Lambda Function

`COLUMNS` also supports passing in a lambda function. The lambda function will be evaluated for all columns present in the `FROM` clause, and only columns that match the lambda function will be returned. This allows the execution of arbitrary expressions in order to select and rename columns.

```sql
SELECT COLUMNS(lambda c: c LIKE '%num%') FROM numbers;
```

| number |
|-------:|
| 10     |
| 20     |
| NULL   |


### `COLUMNS` List

`COLUMNS` also supports passing in a list of column names.

```sql
SELECT COLUMNS(['id', 'num']) FROM numbers;
```

| id | num  |
|---:|-----:|
| 1  | 10   |
| 2  | 20   |
| 3  | NULL |

## Unpacking a `COLUMNS` Expression

By wrapping a `COLUMNS` expression in `UNPACK`, the columns expand into a parent expression,  much like the [iterable unpacking behavior in Python](https://peps.python.org/pep-3132/).

Without `UNPACK`, operations on the `COLUMNS` expression are applied to each column separately:

```sql
SELECT coalesce(COLUMNS(['a', 'b', 'c'])) AS result
FROM (SELECT NULL a, 42 b, true c);
```

| result | result | result |
|--------|-------:|-------:|
| NULL   | 42     | true   |

With `UNPACK`, the `COLUMNS` expression is expanded into its parent expression, `coalesce` in the example above, which results in a single column:

```sql
SELECT coalesce(UNPACK(COLUMNS(['a', 'b', 'c']))) AS result
FROM (SELECT NULL AS a, 42 AS b, true AS c);
```

| result |
|-------:|
| 42     |

The `UNPACK` keyword may be replaced by `*`, [matching Python syntax](https://peps.python.org/pep-3132/), when it is applied directly to the `COLUMNS` expression without any intermediate operations.

```sql
SELECT coalesce(*COLUMNS(*)) AS result
FROM (SELECT NULL a, 42 AS b, true AS c);
```

| result |
|-------:|
| 42     |

> Warning In the following example, replacing `UNPACK` by `*` results in a syntax error:
> 
> ```sql
> SELECT greatest(UNPACK(COLUMNS(*) + 1)) AS result
> FROM (SELECT 1 AS a, 2 AS b, 3 AS c);
> ```
> 
> | result |
> |-------:|
> | 4      |

## `STRUCT.*`

The `*` expression can also be used to retrieve all keys from a struct as separate columns.
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys.
See the [`STRUCT` data type]({% link docs/stable/sql/data_types/struct.md %}) and [`STRUCT` functions]({% link docs/stable/sql/functions/struct.md %}) pages for more details on working with structs.

For example:

```sql
SELECT st.* FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS st);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |
