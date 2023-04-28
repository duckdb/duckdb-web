---
layout: docu
title: Constraints
selected: Documentation/SQL/Constraints
expanded: SQL
railroad: statements/constraints.js
---

In SQL, constraints can be specified for tables. Constraints enforce certain properties over data that is inserted into a table. Constraints can be specified along with the schema of the table as part of the [create table statement](statements/create_table). In certain cases, constraints can also be added to a table using the [alter table statement](statements/alter_table), but this is not currently supported for all constraints.

### Syntax
<div id="rrdiagram"></div>

#### Check

Check constraints allow you to specify an arbitrary boolean expression. Any columns that *do not* satisfy this expression violate the constraint. For example, we could enforce that the `name` column does not contain spaces using the following `CHECK` constraint.

```sql
CREATE TABLE students(name VARCHAR CHECK(NOT CONTAINS(name, ' ')));
INSERT INTO students VALUES ('this name contains spaces');
-- Constraint Error: CHECK constraint failed: students
```

#### Not Null

A not-null constraint specifies that the column cannot contain any `NULL` values. By default, all columns in tables are nullable. Adding `NOT NULL` to a column definition enforces that a column cannot contain `NULL` values.
 
```sql
CREATE TABLE students(name VARCHAR NOT NULL);
INSERT INTO students VALUES (NULL);
-- Constraint Error: NOT NULL constraint failed: students.name
```

#### Primary Key/Unique

Primary key or unique constraints define a column, or set of columns, that are a unique identifier for a row in the table. The constraint enforces that the specified columns are *unique* within a table, i.e. that at most one row contains the given values for the set of columns.

```sql
CREATE TABLE students(id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO students VALUES (1, 'Student 2');
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
```

In order to enforce this property efficiently, an [ART index is automatically created](indexes) for every primary key or unique constraint that is defined in the table.

Primary key constraints and unique constraints are identical except for two points:

* A table can only have one primary key constraint defined, but many unique constraints
* A primary key constraint also enforces the keys to not be `NULL`. 

> Indexes have certain limitations that might result in constraints being evaluated too eagerly, see the [indexes section for more details](indexes#index-limitations)

#### Foreign Key

Foreign keys define a column, or set of columns, that refer to a primary key or unique constraint from *another* table. The constraint enforces that the key exists in the other table. 

```sql
CREATE TABLE students(id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE exams(exam_id INTEGER REFERENCES students(id), grade INTEGER);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO exams VALUES (1, 10);
INSERT INTO exams VALUES (2, 10);
-- Constraint Error: Violates foreign key constraint because key "id: 2" does not exist in the referenced table
```

In order to enforce this property efficiently, an [ART index is automatically created](indexes) for every foreign key constraint that is defined in the table.

> Indexes have certain limitations that might result in constraints being evaluated too eagerly, see the [indexes section for more details](indexes#index-limitations)
