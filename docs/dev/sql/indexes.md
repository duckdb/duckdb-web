---
layout: docu
railroad: statements/indexes.js
redirect_from:
- /docs/sql/indexes
title: Indexes
---

## Index Types

DuckDB currently uses two index types:

* A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as zonemap and block range index) is automatically created for columns of all [general-purpose data types](../sql/data_types/overview).
* An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. Such an index is automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint and can be defined using `CREATE INDEX`.

> ART indexes must currently be able to fit in-memory. Avoid creating ART indexes if the index does not fit in memory.

## Persistence

Both min-max indexes and ART indexes are persisted on disk.

## `CREATE INDEX` and `DROP INDEX`

To create an index, use the [`CREATE INDEX` statement](statements/create_index#create-index).
To drop an index, use the [`DROP INDEX` statement](statements/create_index#drop-index).

## Index Limitations

ART indexes create a secondary copy of the data in a second location - this complicates processing, particularly when combined with transactions. Certain limitations apply when it comes to modifying data that is also stored in secondary indexes.

### Updates Become Deletes and Inserts

When an update statement is executed on a column that is present in an index - the statement is transformed into a *delete* of the original row followed by an *insert*. This has certain performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.

### Over-Eager Unique Constraint Checking

Due to the presence of transactions, data can only be removed from the index after (1) the transaction that performed the delete is committed, and (2) no further transactions exist that refer to the old entry still present in the index. As a result of this - transactions that perform *deletions followed by insertions* may trigger unexpected unique constraint violations, as the deleted tuple has not actually been removed from the index yet. For example:

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
BEGIN;
DELETE FROM students WHERE id = 1;
INSERT INTO students VALUES (1, 'Student 2');
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
```

This, combined with the fact that updates are turned into deletions and insertions within the same transaction, means that updating rows in the presence of unique or primary key constraints can often lead to unexpected unique constraint violations.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
UPDATE students SET name = 'Student 2', id = 1 WHERE id = 1;
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
```

Currently this is an expected limitation of the system - although we aim to resolve this in the future.
