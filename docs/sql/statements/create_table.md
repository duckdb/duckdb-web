---
layout: docu
title: Create Table
railroad: statements/createtable.js
---
The `CREATE TABLE` statement creates a table in the catalog.

### Examples

```sql
-- create a table with two integer columns (i and j)
CREATE TABLE t1(i INTEGER, j INTEGER);
-- create a table with a primary key
CREATE TABLE t1(id INTEGER PRIMARY KEY, j VARCHAR);
-- create a table with a composite primary key
CREATE TABLE t1(id INTEGER, j VARCHAR, PRIMARY KEY(id, j));
-- create a table with various different types and constraints
CREATE TABLE t1(i INTEGER NOT NULL, decimalnr DOUBLE CHECK(decimalnr<10), date DATE UNIQUE, time TIMESTAMP);
-- create a table from the result of a query
CREATE TABLE t1 AS SELECT 42 AS i, 84 AS j;
-- create a table from a CSV file using AUTO-DETECT (i.e., Automatically detecting column names and types)
CREATE TABLE t1 AS SELECT * FROM read_csv_auto ('path/file.csv');
-- we can use the FROM-first syntax to omit 'SELECT *'
CREATE TABLE t1 AS FROM read_csv_auto ('path/file.csv');
```

### Temporary Tables

Temporary tables can be created using a `CREATE TEMP TABLE` statement (see diagram below). 
Temporary tables are session scoped (similar to Postgres for example), meaning that only the specific connection that created them can access them, and once the connection to DuckDB is closed they will be automatically dropped. 
Temporary tables reside in memory rather than on disk (even when connecting to a persistent DuckDB), but if the `temp_directory` [configuration](../../sql/configuration) is set when connecting or with a `SET` command, data will be spilled to disk if memory becomes constrained. 

```sql
-- create a temporary table from a CSV file using AUTO-DETECT (i.e., Automatically detecting column names and types)
CREATE TEMP TABLE t1 AS SELECT * FROM read_csv_auto ('path/file.csv');

-- allow temporary tables to off-load excess memory to disk
SET temp_directory='/path/to/directory/';
```

### Create or Replace

The `CREATE OR REPLACE` syntax allows a new table to be created or for an existing table to be overwritten by the new table. This is shorthand for dropping the existing table and then creating the new one.

```sql
-- create a table with two integer columns (i and j) even if t1 already exists
CREATE OR REPLACE TABLE t1(i INTEGER, j INTEGER);
```

### If Not Exists

The `IF NOT EXISTS` syntax will only proceed with the creation of the table if it does not already exist. If the table already exists, no action will be taken and the existing table will remain in the database. 

```sql
-- create a table with two integer columns (i and j) only if t1 does not exist yet. 
CREATE TABLE IF NOT EXISTS t1(i INTEGER, j INTEGER);
```

### Check Constraints

A `CHECK` constraint is an expression that must be satisfied by the values of every row in the table.

```sql
CREATE TABLE t1(
    id INTEGER PRIMARY KEY,
    percentage INTEGER CHECK(0 <= percentage AND percentage <= 100)
);
INSERT INTO t1 VALUES (1, 5);
INSERT INTO t1 VALUES (2, -1);
-- Error: Constraint Error: CHECK constraint failed: t1
INSERT INTO t1 VALUES (3, 101);
-- Error: Constraint Error: CHECK constraint failed: t1
```

```sql
CREATE TABLE t2(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER CHECK(x < y));
INSERT INTO t2 VALUES (1, 5, 10);
INSERT INTO t2 VALUES (2, 5, 3);
-- Error: Constraint Error: CHECK constraint failed: t2
```

`CHECK` constraints can also be added as part of the `CONSTRAINTS` clause:

```sql
CREATE TABLE t3(
    id INTEGER PRIMARY KEY,
    x INTEGER,
    y INTEGER,
    CONSTRAINT x_smaller_than_y CHECK(x < y)
);
INSERT INTO t3 VALUES (1, 5, 10);
INSERT INTO t3 VALUES (2, 5, 3);
-- Error: Constraint Error: CHECK constraint failed: t3
```

### Foreign Key Constraints

A `FOREIGN KEY` is a column (or set of columns) that references another table's primary key. Foreign keys check referential integrity, i.e., the referred primary key must exist in the other table upon insertion.

```sql
CREATE TABLE t1(id INTEGER PRIMARY KEY, j VARCHAR);
CREATE TABLE t2(
    id INTEGER PRIMARY KEY,
    t1_id INTEGER,
    FOREIGN KEY (t1_id) REFERENCES t1(id)
);

-- example
INSERT INTO t1 VALUES (1, 'a');
INSERT INTO t2 VALUES (1, 1);
INSERT INTO t2 VALUES (2, 2);
-- Error: Constraint Error: Violates foreign key constraint because key "id: 2" does not exist in the referenced table
```

Foreign keys can be defined on composite primary keys:

```sql
CREATE TABLE t3(id INTEGER, j VARCHAR, PRIMARY KEY(id, j));
CREATE TABLE t4(
    id INTEGER PRIMARY KEY, t3_id INTEGER, t3_j VARCHAR,
    FOREIGN KEY (t3_id, t3_j) REFERENCES t3(id, j)
);

-- example
INSERT INTO t3 VALUES (1, 'a');
INSERT INTO t4 VALUES (1, 1, 'a');
INSERT INTO t4 VALUES (2, 1, 'b');
-- Error: Constraint Error: Violates foreign key constraint because key "id: 1, j: b" does not exist in the referenced table
```

Foreign keys can also be defined on unique columns:

```sql
CREATE TABLE t5(id INTEGER UNIQUE, j VARCHAR);
CREATE TABLE t6(id INTEGER PRIMARY KEY, t5_id INTEGER, FOREIGN KEY (t5_id) REFERENCES t5(id));
```

> Foreign keys with cascading deletes (`FOREIGN KEY ... REFERENCES ... ON DELETE CASCADE`) are not supported.

### Generated Columns

The `[type] [GENERATED ALWAYS] AS ( expr ) [VIRTUAL|STORED]` syntax will create a generated column. The data in this kind of column is generated from its expression, which can reference other (regular or generated) columns of the table. Since they are produced by calculations, these columns can not be inserted into directly.

DuckDB can infer the type of the generated column based on the expression's return type. This allows you to leave out the type when declaring a generated column. It is possible to explicitly set a type, but insertions into the referenced columns might fail if the type can not be cast to the type of the generated column.
  
Generated columns come in two varieties: `VIRTUAL` and `STORED`.  
The data of virtual generated columns is not stored on disk, instead it is computed from the expression every time the column is referenced (through a select statement).  

The data of stored generated columns is stored on disk and is computed every time the data of their dependencies change (through an insert/update/drop statement).  

Currently only the `VIRTUAL` kind is supported, and it is also the default option if the last field is left blank.

```sql
-- The simplest syntax for a generated column. 
-- The type is derived from the expression, and the variant defaults to VIRTUAL
CREATE TABLE t1(x FLOAT, two_x AS (2 * x))

-- Fully specifying the same generated column for completeness
CREATE TABLE t1(x FLOAT, two_x FLOAT GENERATED ALWAYS AS (2 * x) VIRTUAL)
```

### Syntax

<div id="rrdiagram"></div>
