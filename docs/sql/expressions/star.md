---
layout: docu
title: Star Expression
railroad: expressions/star.js
---

## Examples

Select all columns present in the `FROM` clause:

```sql
SELECT * FROM table_name;
```

Count the number of rows in a table:

```sql
SELECT count(*) FROM table_name;
```

DuckDB offers a shorthand for `count(*)` expressions where the `*` may be omitted:

```sql
SELECT count() FROM table_name;
```

Select all columns from the table called `table_name`:

```sql
SELECT table_name.*
FROM table_name
JOIN other_table_name USING (id);
```

Select all columns except the city column from the addresses table:

```sql
SELECT * EXCLUDE (city)
FROM addresses;
```

Select all columns from the addresses table, but replace city with `lower(city)`:

```sql
SELECT * REPLACE (lower(city) AS city)
FROM addresses;
```

Select all columns matching the given expression:

```sql
SELECT COLUMNS(c -> c LIKE '%num%')
FROM addresses;
```

Select all columns matching the given regex from the table:

```sql
SELECT COLUMNS('number\d+')
FROM addresses;
```

Select columns using a list:

```sql
SELECT COLUMNS(['city', 'zip_code'])
FROM addresses;
```

## Syntax

<div id="rrdiagram"></div>

## Star Expression

The `*` expression can be used in a `SELECT` statement to select all columns that are projected in the `FROM` clause.

```sql
SELECT *
FROM tbl;
```

The `*` expression can be modified using the `EXCLUDE` and `REPLACE`.

### `EXCLUDE` Clause

`EXCLUDE` allows us to exclude specific columns from the `*` expression.

```sql
SELECT * EXCLUDE (col)
FROM tbl;
```

### `REPLACE` Clause

`REPLACE` allows us to replace specific values in columns as specified by an expression.

```sql
SELECT * REPLACE (col / 1_000 AS col)
FROM tbl;
```

## `COLUMNS` Expression

The `COLUMNS` expression can be used to execute the same expression on the values in multiple columns. For example:

```sql
CREATE TABLE numbers (id INTEGER, number INTEGER);
INSERT INTO numbers VALUES (1, 10), (2, 20), (3, NULL);
SELECT min(COLUMNS(*)), count(COLUMNS(*)) FROM numbers;
```

| id | number | id | number |
|---:|-------:|---:|-------:|
| 1  | 10     | 3  | 2      |

The `*` expression in the `COLUMNS` statement can also contain `EXCLUDE` or `REPLACE`, similar to regular star expressions.

```sql
SELECT
    min(COLUMNS(* REPLACE (number + id AS number))),
    count(COLUMNS(* EXCLUDE (number)))
FROM numbers;
```

| id | min(number := (number + id)) | id |
|---:|-----------------------------:|---:|
| 1  | 11                           | 3  |

`COLUMNS` expressions can also be combined, as long as the `COLUMNS` contains the same (star) expression:

```sql
SELECT COLUMNS(*) + COLUMNS(*) FROM numbers;
```

| id | number |
|---:|-------:|
| 2  | 20     |
| 4  | 40     |
| 6  | NULL   |

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

## `COLUMNS` Regular Expression

`COLUMNS` supports passing a regex in as a string constant:

```sql
SELECT COLUMNS('(id|numbers?)') FROM numbers;
```

| id | number |
|---:|-------:|
| 1  | 10     |
| 2  | 20     |
| 3  | NULL   |

### Renaming Columns Using a `COLUMNS` Expression

The matches of capture groups can be used to rename columns selected by a regular expression.
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

## `COLUMNS` Lambda Function

`COLUMNS` also supports passing in a lambda function. The lambda function will be evaluated for all columns present in the `FROM` clause, and only columns that match the lambda function will be returned. This allows the execution of arbitrary expressions in order to select and rename columns.

```sql
SELECT COLUMNS(c -> c LIKE '%num%') FROM numbers;
```

| number |
|-------:|
| 10     |
| 20     |
| NULL   |

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
See the [`STRUCT` data type]({% link docs/sql/data_types/struct.md %}) and [`STRUCT` functions]({% link docs/sql/functions/struct.md %}) pages for more details on working with structs.

For example:

```sql
SELECT st.* FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS st);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |
