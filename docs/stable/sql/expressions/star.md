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
SELECT table_name.*
FROM table_name
JOIN other_table_name USING (id);
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

`EXCLUDE` allows us to exclude specific columns from the `*` expression.

```sql
SELECT * EXCLUDE (col)
FROM tbl;
```

### `REPLACE` Clause

`REPLACE` allows us to replace specific columns by alternative expressions.

```sql
SELECT * REPLACE (col1 / 1_000 AS col1, col2 / 1_000 AS col2)
FROM tbl;
```

### `RENAME` Clause

`RENAME` allows us to replace specific columns.

```sql
SELECT * RENAME (col1 AS height, col2 AS width)
FROM tbl;
```

### Column Filtering via Pattern Matching Operators

The [pattern matching operators]({% link docs/stable/sql/functions/pattern_matching.md %}) `LIKE`, `GLOB`, `SIMILAR TO` and their variants allow us to select columns by matching their names to patterns.

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


The `COLUMNS` expression is similar to the regular star expression, but additionally allows us to execute the same expression on the resulting columns. 

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
    SELECT 0 AS x, 1 AS y, 2 AS z
    UNION ALL
    SELECT 1 AS x, 2 AS y, 3 AS z
    UNION ALL
    SELECT 2 AS x, 3 AS y, 4 AS z
)
WHERE COLUMNS(*) > 1; -- equivalent to: x > 1 AND y > 1 AND z > 1
```

| x | y | z |
|--:|--:|--:|
| 2 | 3 | 4 |

### Regular Expressions in a `COLUMNS` Expression

`COLUMNS` expressions don't currently support the pattern matching operators, but they do supports regular expression matching by simply passing a string constant in place of the star:

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

For example, to select the first three letters of colum names, run:

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

### `COLUMNS` Lambda Function

`COLUMNS` also supports passing in a lambda function. The lambda function will be evaluated for all columns present in the `FROM` clause, and only columns that match the lambda function will be returned. This allows the execution of arbitrary expressions in order to select and rename columns.

```sql
SELECT COLUMNS(c -> c LIKE '%num%') FROM numbers;
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

## `*COLUMNS` Unpacked Columns

The `*COLUMNS` clause is a variation of `COLUMNS`, which supports all of the previously mentioned capabilities.
The difference is in how the expression expands.

`*COLUMNS` will expand in-place, much like the [iterable unpacking behavior in Python](https://peps.python.org/pep-3132/), which inspired the `*` syntax.
This implies that the expression expands into the parent expression.
An example that shows this difference between `COLUMNS` and `*COLUMNS`:

With `COLUMNS`:

```sql
SELECT coalesce(COLUMNS(['a', 'b', 'c'])) AS result
FROM (SELECT NULL a, 42 b, true c);
```

| result | result | result |
|--------|-------:|-------:|
| NULL   | 42     | true   |

With `*COLUMNS`, the expression expands in its parent expression `coalesce`, resulting in a single result column:

```sql
SELECT coalesce(*COLUMNS(['a', 'b', 'c'])) AS result
FROM (SELECT NULL AS a, 42 AS b, true AS c);
```

| result |
|-------:|
| 42     |

`*COLUMNS` also works with the `(*)` argument:

```sql
SELECT coalesce(*COLUMNS(*)) AS result
FROM (SELECT NULL a, 42 AS b, true AS c);
```

| result |
|-------:|
| 42     |

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
