---
layout: docu
title: Indexes
selected: Documentation/Indexes
railroad: statements/indexes.js
---
## Index types

DuckDB currently uses two index types:

* A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) is automatically created for columns of all [general-purpose data types](../sql/data_types/overview).
* An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. Such an index is automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint and can be defined using `CREATE INDEX`.

Joins on columns with an ART index can make use of the [index join algorithm](https://en.wikipedia.org/wiki/Nested_loop_join#Index_join_variation). Forcing index joins is possible using [pragmas](../sql/pragmas).

> ART indexes must currently be able to fit in-memory. Avoid creating ART indexes if the index does not fit in memory.

## Persistence

* Min-max indexes are persisted.
* ART indexes are persisted.

## Create Index

<div id="rrdiagram1"></div>

`CREATE INDEX` constructs an index on the specified column(s) of the specified table. Compound indexes on multiple columns/expressions are supported. Currently unidimensional indexes are supported, [multidimensional indexes are not supported](https://github.com/duckdb/duckdb/issues/63).

### Parameters

| Name | Description |
|:---|:---|
|`UNIQUE`|Causes the system to check for duplicate values in the table when the index is created (if data already exist) and each time data is added. Attempts to insert or update data that would result in duplicate entries will generate an error.|
|`name`|The name of the index to be created.|
|`table`|The name of the table to be indexed.|
|`column`|The name of the column to be indexed.|
|`expression`|An expression based on one or more columns of the table. The expression usually must be written with surrounding parentheses, as shown in the syntax. However, the parentheses can be omitted if the expression has the form of a function call.|


### Examples

```sql
-- Create a unique index 'films_id_idx' on the column id of table films.
CREATE UNIQUE INDEX films_id_idx ON films (id);
-- Create index 's_idx' that allows for duplicate values on column revenue of table films.
CREATE INDEX s_idx ON films (revenue);
-- Create compound index 'gy_idx' on genre and year columns.
CREATE INDEX gy_idx ON films (genre, year);
-- Create index 'i_index' on the expression of the sum of columns j and k from table integers.
CREATE INDEX i_index ON integers ((j+k));
```

## Drop Index

<div id="rrdiagram2"></div>

`DROP INDEX` drops an existing index from the database system.


### Parameters

| Name | Description |
|:---|:---|
|`IF EXISTS`|Do not throw an error if the index does not exist.|
|`name`|The name of an index to remove.|

### Examples

```sql
-- Remove the index title_idx.
DROP INDEX title_idx;
```

## Index Limitations

ART indexes create a secondary copy of the data in a second location - this complicates processing, particularly when combined with transactions. Certain limitations apply when it comes to modifying data that is also stored in secondary indexes.

##### Updates become Deletes and Inserts

When an update statement is executed on a column that is present in an index - the statement is transformed into a *delete* of the original row followed by an *insert*. This has certain performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.

##### Over-Eager Unique Constraint Checking

Due to the presence of transactions, data can only be removed from the index after (1) the transaction that performed the delete is committed, and (2) no further transactions exist that refer to the old entry still present in the index. As a result of this - transactions that perform *deletions followed by insertions* may trigger unexpected unique constraint violations, as the deleted tuple has not actually been removed from the index yet. For example:

```sql
CREATE TABLE students(id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
BEGIN;
DELETE FROM students WHERE id=1;
INSERT INTO students VALUES (1, 'Student 2');
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
```

This, combined with the fact that updates are turned into deletions and insertions within the same transaction, means that updating rows in the presence of unique or primary key constraints can often lead to unexpected unique constraint violations.

```sql
CREATE TABLE students(id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
UPDATE students SET name='Student 2', id=1 WHERE id=1;
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
```

Currently this is an expected limitation of the system - although we aim to resolve this in the future.
