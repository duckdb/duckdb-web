---
layout: docu
railroad: statements/constraints.js
tested: true
title: Constraints
---

In SQL, constraints can be specified for tables. Constraints enforce certain properties over data that is inserted into a table. Constraints can be specified along with the schema of the table as part of the [`CREATE TABLE` statement]({% link docs/preview/sql/statements/create_table.md %}). In certain cases, constraints can also be added to a table using the [`ALTER TABLE` statement]({% link docs/preview/sql/statements/alter_table.md %}), but this is not currently supported for all constraints.

> Warning Constraints have a strong impact on performance: they slow down loading and updates but speed up certain queries. Please consult the [Performance Guide]({% link docs/preview/guides/performance/schema.md %}#constraints) for details.

## Syntax

<div id="rrdiagram"></div>

## Check Constraint

Check constraints allow you to specify an arbitrary Boolean expression. Any columns that *do not* satisfy this expression violate the constraint. For example, we could enforce that the `name` column does not contain spaces using the following `CHECK` constraint.

```sql
CREATE TABLE students (name VARCHAR CHECK (NOT contains(name, ' ')));
INSERT INTO students VALUES ('this name contains spaces');
```

```console
Constraint Error:
CHECK constraint failed on table students with expression CHECK((NOT contains("name", ' ')))
```

## Not Null Constraint

A not-null constraint specifies that the column cannot contain any `NULL` values. By default, all columns in tables are nullable. Adding `NOT NULL` to a column definition enforces that a column cannot contain `NULL` values.

```sql
CREATE TABLE students (name VARCHAR NOT NULL);
INSERT INTO students VALUES (NULL);
```

```console
Constraint Error:
NOT NULL constraint failed: students.name
```

## Primary Key and Unique Constraint

Primary key or unique constraints define a column, or set of columns, that are a unique identifier for a row in the table. The constraint enforces that the specified columns are *unique* within a table, i.e., that at most one row contains the given values for the set of columns.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO students VALUES (1, 'Student 2');
```

```console
Constraint Error:
Duplicate key "id: 1" violates primary key constraint
```

```sql
CREATE TABLE students (id INTEGER, name VARCHAR, PRIMARY KEY (id, name));
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO students VALUES (1, 'Student 2');
INSERT INTO students VALUES (1, 'Student 1');
```

```console
Constraint Error:
Duplicate key "id: 1, name: Student 1" violates primary key constraint
```

To enforce this property efficiently, an [ART index is automatically created]({% link docs/preview/sql/indexes.md %}) for every primary key or unique constraint that is defined in the table.

Primary key constraints and unique constraints are identical except for two points:

* A table can only have one primary key constraint defined, but many unique constraints
* A primary key constraint also enforces the keys to not be `NULL`.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR, email VARCHAR UNIQUE);
INSERT INTO students VALUES (1, 'Student 1', 'student1@uni.com');
INSERT INTO students VALUES (2, 'Student 2', 'student1@uni.com');
```

```console
Constraint Error:
Duplicate key "email: student1@uni.com" violates unique constraint.
```

```sql
INSERT INTO students (id, name) VALUES (3, 'Student 3');
INSERT INTO students (name, email) VALUES ('Student 3', 'student3@uni.com');
```

```console
Constraint Error:
NOT NULL constraint failed: students.id
```

> Warning Indexes have certain limitations that might result in constraints being evaluated too eagerly, leading to constraint errors such as `violates primary key constraint` and `violates unique constraint`. See the [Indexes page]({% link docs/preview/sql/indexes.md %}#limitations-of-art-indexes) for more details.

You can also define a uniqueness constraint on multiple columns:

```sql
CREATE TABLE integers (i INTEGER, j INTEGER, k INTEGER, UNIQUE (i, j));
INSERT INTO integers VALUES (1, 2, 3);
INSERT INTO integers VALUES (1, 4, 5);
INSERT INTO integers VALUES (1, 2, 5);
```

```console
Constraint Error:
Duplicate key "i: 1, j: 2" violates unique constraint.
```

### Deferred Constraints

> New As of DuckDB 2.0, primary key and unique constraints can be declared `DEFERRED` so that they are checked at `COMMIT` time instead of during each statement. This allows a transaction to transiently violate uniqueness as long as the violation is resolved before the transaction commits. The default (or an explicit `IMMEDIATE`) checks the constraint during statement execution.

Append `DEFERRED` (or `IMMEDIATE`) to the constraint, either on a column or at the table level:

```sql
CREATE TABLE t1 (i INTEGER PRIMARY KEY DEFERRED);
CREATE TABLE t2 (i INTEGER UNIQUE DEFERRED);
CREATE TABLE t3 (i INTEGER, j INTEGER, PRIMARY KEY (i) DEFERRED);
CREATE TABLE t4 (i INTEGER, UNIQUE (i) DEFERRED);
```

The timing can also be set when adding a constraint with [`ALTER TABLE`]({% link docs/preview/sql/statements/alter_table.md %}):

```sql
ALTER TABLE t5 ADD UNIQUE (i) DEFERRED;
```

If a deferred constraint is still violated at `COMMIT`, the commit fails. The following restrictions apply:

* DuckDB uses the bare `DEFERRED` and `IMMEDIATE` keywords; the PostgreSQL `INITIALLY DEFERRED` and `DEFERRABLE` spellings are not supported, and there is no `SET CONSTRAINTS` statement.
* A `NOT NULL` constraint on a deferred primary key is still checked eagerly.
* A foreign key cannot reference a deferred key.
* A deferred constraint cannot be used as an `ON CONFLICT` target.

The [`duckdb_constraints()`]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_constraints) function reports the timing in its `constraint_text` column (for example `UNIQUE(i) DEFERRED`) and exposes an `is_deferred` column.

## Foreign Keys

Foreign keys define a column, or set of columns, that refer to a primary key or unique constraint from *another* table. The constraint enforces that the key exists in the other table.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE subjects (id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE exams (
    exam_id INTEGER PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    student_id INTEGER REFERENCES students(id),
    grade INTEGER
);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO subjects VALUES (1, 'CS 101');
INSERT INTO exams VALUES (1, 1, 1, 10);
INSERT INTO exams VALUES (2, 1, 2, 10);
```

```console
Constraint Error:
Violates foreign key constraint because key "id: 2" does not exist in the referenced table
```

To enforce this property efficiently, an [ART index is automatically created]({% link docs/preview/sql/indexes.md %}) for every foreign key constraint that is defined in the table.

> Warning Indexes have certain limitations that might result in constraints being evaluated too eagerly, leading to constraint errors such as `violates primary key constraint` and `violates unique constraint`. See the [indexes section for more details]({% link docs/preview/sql/indexes.md %}#index-limitations).
