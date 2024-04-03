---
layout: docu
title: INSERT Statement
railroad: statements/insert.js
---

The `INSERT` statement inserts new data into a table.

### Examples

```sql
-- insert the values (1), (2), (3) into "tbl"
INSERT INTO tbl VALUES (1), (2), (3);
-- insert the result of a query into a table
INSERT INTO tbl SELECT * FROM other_tbl;
-- insert values into the "i" column, inserting the default value into other columns
INSERT INTO tbl (i) VALUES (1), (2), (3);
-- explicitly insert the default value into a column
INSERT INTO tbl (i) VALUES (1), (DEFAULT), (3);
-- assuming tbl has a primary key/unique constraint, do nothing on conflict
INSERT OR IGNORE INTO tbl (i) VALUES (1);
-- or update the table with the new values instead
INSERT OR REPLACE INTO tbl (i) VALUES (1);
```

### Syntax

<div id="rrdiagram"></div>

`INSERT INTO` inserts new rows into a table. One can insert one or more rows specified by value expressions, or zero or more rows resulting from a query.

## Insert Column Order

It's possible to provide an optional insert column order, this can either be `BY POSITION` (the default) or `BY NAME`.
Each column not present in the explicit or implicit column list will be filled with a default value, either its declared default value or `NULL` if there is none.

If the expression for any column is not of the correct data type, automatic type conversion will be attempted.

### `INSERT INTO ... [BY POSITION]`

The order that values are inserted into the columns of the table is determined by the order that the columns were declared in.
That is, the values supplied by the `VALUES` clause or query are associated with the column list left-to-right.
This is the default option, that can be explicitly specified using the `BY POSITION` option.
For example:

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl VALUES (5, 42);
-- specifying "BY POSITION" is optional and is equivalent to the default behavior
INSERT INTO tbl BY POSITION VALUES (5, 42);
```

To use a different order, column names can be provided as part of the target, for example:

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl (b, a) VALUES (5, 42);
-- adding "BY POSITION" results in the same behavior
INSERT INTO tbl BY POSITION (b, a) VALUES (5, 42);
```

This will insert `5` into `b` and `42` into `a`.

### `INSERT INTO ... BY NAME`

Using the `BY NAME` modifier, the names of the column list of the `SELECT` statement are matched against the column names of the table to determine the order that values should be inserted into the table. This allows inserting even in cases when the order of the columns in the table differs from the order of the values in the `SELECT` statement or certain columns are missing.

For example:

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl BY NAME (SELECT 42 AS b, 32 AS a);
INSERT INTO tbl BY NAME (SELECT 22 AS b);
SELECT * FROM tbl;
```

|  a   | b  |
|-----:|---:|
| 32   | 42 |
| NULL | 22 |

It's important to note that when using `INSERT INTO ... BY NAME`, the column names specified in the `SELECT` statement must match the column names in the table. If a column name is misspelled or does not exist in the table, an error will occur. Columns that are missing from the `SELECT` statement will be filled with the default value.

## `ON CONFLICT` Clause

An `ON CONFLICT` clause can be used to perform a certain action on conflicts that arise from `UNIQUE` or `PRIMARY KEY` constraints.
An example for such a conflict is shown in the following example:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl VALUES (1, 84);
```

This raises as an error and leaves the table with a single row `<i: 1, j: 42>`.

```text
Error: Constraint Error: Duplicate key "i: 1" violates primary key constraint.
```

There are two supported actions: `DO NOTHING` and `DO UPDATE SET ...`

### `DO NOTHING` Clause

The `DO NOTHING` clause causes the error(s) to be ignored, and the values are not inserted or updated.
For example:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO NOTHING;
```

These statements finish successfully and leaves the table with the row `<i: 1, j: 42>`.

#### Shorthand for `DO NOTHING`

The `INSERT OR IGNORE INTO ...` statement is a shorter syntax alternative to `INSERT INTO ... ON CONFLICT DO NOTHING`.
For example, the following statements are equivalent:

```sql
INSERT OR IGNORE INTO tbl VALUES (1, 84);
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO NOTHING;
```

### `DO UPDATE` Clause (Upsert)

The `DO UPDATE` clause causes the `INSERT` to turn into an `UPDATE` on the conflicting row(s) instead.
The `SET` expressions that follow determine how these rows are updated. The expressions can use the special virtual table `EXCLUDED`, which contains the conflicting values for the row.
Optionally you can provide an additional `WHERE` clause that can exclude certain rows from the update.
The conflicts that don't meet this condition are ignored instead.

Because we need a way to refer to both the **to-be-inserted** tuple and the **existing** tuple, we introduce the special `EXCLUDED` qualifier.
When the `EXCLUDED` qualifier is provided, the reference refers to the **to-be-inserted** tuple, otherwise it refers to the **existing** tuple.
This special qualifier can be used within the `WHERE` clauses and `SET` expressions of the `ON CONFLICT` clause.

#### Examples

An example using `DO UPDATE` is the following:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
SELECT * FROM tbl;
```

| i | j  |
|--:|---:|
| 1 | 84 |

Rearranging columns and using `BY NAME` is also possible:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl (j, i) VALUES (168, 1) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl BY NAME (SELECT 1 AS i, 336 AS j) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
SELECT * FROM tbl;
```

| i |  j  |
|--:|----:|
| 1 | 336 |

#### Shorthand

The `INSERT OR REPLACE INTO ...` statement is a shorter syntax alternative to `INSERT INTO ... DO UPDATE SET c1 = EXCLUDED.c1, c2 = EXCLUDED.c2, ...`.
That is, it updates every column of the **existing** row to the new values of the **to-be-inserted** row.
For example, given the following input table:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl VALUES (1, 42);
```

These statements are equivalent:

```sql
INSERT OR REPLACE INTO tbl VALUES (1, 84);
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl (j, i) VALUES (84, 1) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl BY NAME (SELECT 84 AS j, 1 AS i) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
```

#### Limitations

When the `ON CONFLICT ... DO UPDATE` clause is used and a conflict occurs, DuckDB internally assigns `NULL` values to the row's columns that are unaffected by the conflict, then re-assigns their values. If the affected columns use a `NOT NULL` constraint, this will trigger a `NOT NULL constraint failed` error. For example:

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, val1 DOUBLE, val2 DOUBLE NOT NULL);
CREATE TABLE t2 (id INT PRIMARY KEY, val1 DOUBLE);
INSERT INTO t1 VALUES (1, 2, 3);
INSERT INTO t2 VALUES (1, 5);

INSERT INTO t1 BY NAME (SELECT id, val1 FROM t2)
    ON CONFLICT DO UPDATE
    SET val1 = EXCLUDED.val1;
```

This fails with the following error:

```text
Constraint Error: NOT NULL constraint failed: t1.val2
```

### Defining a Conflict Target

A conflict target may be provided as `ON CONFLICT (confict_target)`. This is a group of columns that an index or uniqueness/key constraint is defined on. If the conflict target is omitted, or `PRIMARY KEY` constraint(s) on the table are targeted.

Specifying a conflict target is optional unless using a [`DO UPDATE`](#do-update-clause-upsert) and there are multiple unique/primary key constraints on the table.

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT UNIQUE, k INT);
INSERT INTO tbl
    VALUES (1, 20, 300);
SELECT * FROM tbl;
```

| i | j  |  k  |
|--:|---:|----:|
| 1 | 20 | 300 |

```sql
INSERT INTO tbl
    VALUES (1, 40, 700)
    ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k;
```

| i | j  |  k   |
|--:|---:|-----:|
| 1 | 20 | 1400 |

```sql
INSERT INTO tbl
    VALUES (1, 20, 900)
    ON CONFLICT (j) DO UPDATE SET k = 5 * EXCLUDED.k;
```

| i | j  |  k   |
|--:|---:|-----:|
| 1 | 20 | 4500 |

When a conflict target is provided, you can further filter this with a `WHERE` clause, that should be met by all conflicts.

```sql
INSERT INTO tbl
    VALUES (1, 40, 700)
    ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k WHERE k < 100;
```

### Multiple Tuples Conflicting on the Same Key

Having multiple tuples conflicting on the same key is not supported. For example:

```sql
CREATE TABLE tbl (i INT PRIMARY KEY, j INT);
INSERT INTO tbl
    VALUES (1, 42);
INSERT INTO tbl
    VALUES (1, 84), (1, 168)
    ON CONFLICT DO NOTHING;
```

Running this returns the following message.

```text
Error: Invalid Input Error: ON CONFLICT DO UPDATE can not update the same row twice in the same command.
Ensure that no rows proposed for insertion within the same command have duplicate constrained values
```

## `RETURNING` Clause

The `RETURNING` clause may be used to return the contents of the rows that were inserted. This can be useful if some columns are calculated upon insert. For example, if the table contains an automatically incrementing primary key, then the `RETURNING` clause will include the automatically created primary key. This is also useful in the case of generated columns.

Some or all columns can be explicitly chosen to be returned and they may optionally be renamed using aliases. Arbitrary non-aggregating expressions may also be returned instead of simply returning a column. All columns can be returned using the `*` expression, and columns or expressions can be returned in addition to all columns returned by the `*`.

For example:

```sql
CREATE TABLE t1 (i INT);
INSERT INTO t1
    SELECT 42
    RETURNING *;
```

<div class="narrow_table"></div>

| i  |
|---:|
| 42 |

A more complex example that includes an expression in the `RETURNING` clause:

```sql
CREATE TABLE t2 (i INT, j INT);
INSERT INTO t2
    SELECT 2 AS i, 3 AS j
    RETURNING *, i * j AS i_times_j;
```

<div class="narrow_table"></div>

| i | j | i_times_j |
|--:|--:|----------:|
| 2 | 3 | 6         |

The next example shows a situation where the `RETURNING` clause is more helpful. First, a table is created with a primary key column. Then a sequence is created to allow for that primary key to be incremented as new rows are inserted. When we insert into the table, we do not already know the values generated by the sequence, so it is valuable to return them. For additional information, see the [`CREATE SEQUENCE` page](create_sequence).

```sql
CREATE TABLE t3 (i INT PRIMARY KEY, j INT);
CREATE SEQUENCE 't3_key';
INSERT INTO t3
    SELECT nextval('t3_key') AS i, 42 AS j
    UNION ALL
    SELECT nextval('t3_key') AS i, 43 AS j
    RETURNING *;
```

<div class="narrow_table"></div>

| i | j  |
|--:|---:|
| 1 | 42 |
| 2 | 43 |
