---
layout: docu
railroad: statements/createtable.js
title: CREATE TABLE Statement
---

The `CREATE TABLE` statement creates a table in the catalog.

## Examples

Create a table with two integer columns (`i` and `j`):

```sql
CREATE TABLE t1 (i INTEGER, j INTEGER);
```

Create a table with a primary key:

```sql
CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR);
```

Create a table with a composite primary key:

```sql
CREATE TABLE t1 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));
```

Create a table with various different types, constraints and default values:

```sql
CREATE TABLE t1 (
    i INTEGER NOT NULL DEFAULT 0,
    decimalnr DOUBLE CHECK (decimalnr < 10),
    date DATE UNIQUE,
    time TIMESTAMP
);
```

Create table with `CREATE TABLE ... AS SELECT` (CTAS):

```sql
CREATE TABLE t1 AS
    SELECT 42 AS i, 84 AS j;
```

Create a table from a CSV file (automatically detecting column names and types):

```sql
CREATE TABLE t1 AS
    SELECT *
    FROM read_csv('path/file.csv');
```

We can use the `FROM`-first syntax to omit `SELECT *`:

```sql
CREATE TABLE t1 AS
    FROM read_csv('path/file.csv');
```

Copy the schema of `t2` to `t1`:

```sql
CREATE TABLE t1 AS
    FROM t2
    LIMIT 0;
```

Note that only the column names and types are copied to `t1`, other pieces of information (indexes, constraints, default values, etc.) are not copied.

## Temporary Tables

Temporary tables are session scoped, meaning that only the specific connection that created them can access them and once the connection to DuckDB is closed they will be automatically dropped (similar to PostgreSQL, for example).

They can be created using the `CREATE TEMP TABLE` or the `CREATE TEMPORARY TABLE` statement (see diagram below) and are part of the `temp.main` schema. While discouraged, their names can overlap with the names of the regular database tables. In these cases, temporary tables take priority in name resolution and full qualification is required to refer to a regular table e.g., `memory.main.t1`.

Temporary tables reside in memory rather than on disk even when connecting to a persistent DuckDB, but if the `temp_directory` [configuration]({% link docs/preview/configuration/overview.md %}) is set, data will be spilled to disk if memory becomes constrained.

Create a temporary table from a CSV file (automatically detecting column names and types):

```sql
CREATE TEMP TABLE t1 AS
    SELECT *
    FROM read_csv('path/file.csv');
```

Allow temporary tables to off-load excess memory to disk:

```sql
SET temp_directory = '/path/to/directory/';
```

## `CREATE OR REPLACE`

The `CREATE OR REPLACE` syntax allows a new table to be created or for an existing table to be overwritten by the new table. This is shorthand for dropping the existing table and then creating the new one.

Create a table with two integer columns (i and j) even if t1 already exists:

```sql
CREATE OR REPLACE TABLE t1 (i INTEGER, j INTEGER);
```

## `IF NOT EXISTS`

The `IF NOT EXISTS` syntax will only proceed with the creation of the table if it does not already exist. If the table already exists, no action will be taken and the existing table will remain in the database.

Create a table with two integer columns (`i` and `j`) only if `t1` does not exist yet:

```sql
CREATE TABLE IF NOT EXISTS t1 (i INTEGER, j INTEGER);
```

## `CREATE TABLE ... AS SELECT` (CTAS)

DuckDB supports the `CREATE TABLE ... AS SELECT` syntax, also known as “CTAS”:

```sql
CREATE TABLE nums AS
    SELECT i
    FROM range(0, 3) t(i);
```

This syntax can be used in combination with the [CSV reader]({% link docs/preview/data/csv/overview.md %}), the shorthand to read directly from CSV files without specifying a function, the [`FROM`-first syntax]({% link docs/preview/sql/query_syntax/from.md %}), and the [HTTP(S) support]({% link docs/preview/core_extensions/httpfs/https.md %}), yielding concise SQL commands such as the following:

```sql
CREATE TABLE flights AS
    FROM 'https://duckdb.org/data/flights.csv';
```

The CTAS construct also works with the `OR REPLACE` modifier, yielding `CREATE OR REPLACE TABLE ... AS` statements:

```sql
CREATE OR REPLACE TABLE flights AS
    FROM 'https://duckdb.org/data/flights.csv';
```

### Copying the Schema

You can create a copy of the table's schema (column names and types only) as follows:

```sql
CREATE TABLE t1 AS
    FROM t2
    WITH NO DATA;
```

Or:

```sql
CREATE TABLE t1 AS
    FROM t2
    LIMIT 0;
```

It is not possible to create tables using CTAS statements with constraints (primary keys, check constraints, etc.).

## Check Constraints

A `CHECK` constraint is an expression that must be satisfied by the values of every row in the table.

```sql
CREATE TABLE t1 (
    id INTEGER PRIMARY KEY,
    percentage INTEGER CHECK (0 <= percentage AND percentage <= 100)
);
INSERT INTO t1 VALUES (1, 5);
INSERT INTO t1 VALUES (2, -1);
```

```console
Constraint Error:
CHECK constraint failed: t1
```

```sql
INSERT INTO t1 VALUES (3, 101);
```

```console
Constraint Error:
CHECK constraint failed: t1
```

```sql
CREATE TABLE t2 (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER CHECK (x < y));
INSERT INTO t2 VALUES (1, 5, 10);
INSERT INTO t2 VALUES (2, 5, 3);
```

```console
Constraint Error:
CHECK constraint failed: t2
```

`CHECK` constraints can also be added as part of the `CONSTRAINTS` clause:

```sql
CREATE TABLE t3 (
    id INTEGER PRIMARY KEY,
    x INTEGER,
    y INTEGER,
    CONSTRAINT x_smaller_than_y CHECK (x < y)
);
INSERT INTO t3 VALUES (1, 5, 10);
INSERT INTO t3 VALUES (2, 5, 3);
```

```console
Constraint Error:
CHECK constraint failed: t3
```

## Foreign Key Constraints

A `FOREIGN KEY` is a column (or set of columns) that references another table's primary key. Foreign keys check referential integrity, i.e., the referred primary key must exist in the other table upon insertion.

```sql
CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR);
CREATE TABLE t2 (
    id INTEGER PRIMARY KEY,
    t1_id INTEGER,
    FOREIGN KEY (t1_id) REFERENCES t1 (id)
);
```

Example:

```sql
INSERT INTO t1 VALUES (1, 'a');
INSERT INTO t2 VALUES (1, 1);
INSERT INTO t2 VALUES (2, 2);
```

```console
Constraint Error:
Violates foreign key constraint because key "id: 2" does not exist in the referenced table
```

Foreign keys can be defined on composite primary keys:

```sql
CREATE TABLE t3 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));
CREATE TABLE t4 (
    id INTEGER PRIMARY KEY, t3_id INTEGER, t3_j VARCHAR,
    FOREIGN KEY (t3_id, t3_j) REFERENCES t3(id, j)
);
```

Example:

```sql
INSERT INTO t3 VALUES (1, 'a');
INSERT INTO t4 VALUES (1, 1, 'a');
INSERT INTO t4 VALUES (2, 1, 'b');
```

```console
Constraint Error:
Violates foreign key constraint because key "id: 1, j: b" does not exist in the referenced table
```

Foreign keys can also be defined on unique columns:

```sql
CREATE TABLE t5 (id INTEGER UNIQUE, j VARCHAR);
CREATE TABLE t6 (
    id INTEGER PRIMARY KEY,
    t5_id INTEGER,
    FOREIGN KEY (t5_id) REFERENCES t5(id)
);
```

### Limitations

Foreign keys have the following limitations.

Foreign keys with cascading deletes (`FOREIGN KEY ... REFERENCES ... ON DELETE CASCADE`) are not supported.

Inserting into tables with self-referencing foreign keys is currently not supported and will result in the following error:

```console
Constraint Error:
Violates foreign key constraint because key "..." does not exist in the referenced table.
```

## Generated Columns

The `[type] [GENERATED ALWAYS] AS (expr) [VIRTUAL|STORED]` syntax will create a generated column. The data in this kind of column is generated from its expression, which can reference other (regular or generated) columns of the table. Since they are produced by calculations, these columns cannot be inserted into directly.

DuckDB can infer the type of the generated column based on the expression's return type. This allows you to leave out the type when declaring a generated column. It is possible to explicitly set a type, but insertions into the referenced columns might fail if the type cannot be cast to the type of the generated column.

Generated columns come in two varieties: `VIRTUAL` and `STORED`.
The data of virtual generated columns is not stored on disk, instead it is computed from the expression every time the column is referenced (through a select statement).

The data of stored generated columns is stored on disk and is computed every time the data of their dependencies change (through an `INSERT` / `UPDATE` / `DROP` statement).

Currently, only the `VIRTUAL` kind is supported, and it is also the default option if the last field is left blank.

The simplest syntax for a generated column:

The type is derived from the expression, and the variant defaults to `VIRTUAL`:

```sql
CREATE TABLE t1 (x FLOAT, two_x AS (2 * x));
```

Fully specifying the same generated column for completeness:

```sql
CREATE TABLE t1 (x FLOAT, two_x FLOAT GENERATED ALWAYS AS (2 * x) VIRTUAL);
```

## Syntax

<div id="rrdiagram"></div>
