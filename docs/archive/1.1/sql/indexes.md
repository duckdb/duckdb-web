---
layout: docu
railroad: statements/indexes.js
title: Indexes
---

## Index Types

DuckDB has two built-in index types. Indexes can also be defined via [extensions]({% link docs/archive/1.1/extensions/overview.md %}).

### Min-Max Index (Zonemap)

A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as zonemap and block range index) is automatically created for columns of all [general-purpose data types]({% link docs/archive/1.1/sql/data_types/overview.md %}).

### Adaptive Radix Tree (ART)

An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. ART indexes are automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint and can be defined using `CREATE INDEX`.

> Warning ART indexes must currently be able to fit in-memory. Avoid creating ART indexes if the index does not fit in memory.

### Indexes Defined by Extensions

[Starting with version 1.1.0]({% post_url 2024-09-09-announcing-duckdb-110 %}#r-tree), DuckDB supports [R-trees for spatial indexing]({% link docs/archive/1.1/extensions/spatial/r-tree_indexes.md %}) via the `spatial` extension.

## Persistence

Both min-max indexes and ART indexes are persisted on disk.

## `CREATE INDEX` and `DROP INDEX`

To create an index, use the [`CREATE INDEX` statement]({% link docs/archive/1.1/sql/statements/create_index.md %}#create-index).
To drop an index, use the [`DROP INDEX` statement]({% link docs/archive/1.1/sql/statements/create_index.md %}#drop-index).

## Limitations of ART Indexes

ART indexes create a secondary copy of the data in a second location – this complicates processing, particularly when combined with transactions. Certain limitations apply when it comes to modifying data that is also stored in secondary indexes.

> As expected, indexes have a strong effect on performance, slowing down loading and updates, but speeding up certain queries. Please consult the [Performance Guide]({% link docs/archive/1.1/guides/performance/indexing.md %}) for details.

### Updates Become Deletes and Inserts

When an update statement is executed on a column that is present in an index, the statement is transformed into a *delete* of the original row followed by an *insert*.
This has certain performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.

### Over-Eager Unique Constraint Checking

Due to the presence of transactions, data can only be removed from the index after (1) the transaction that performed the delete is committed, and (2) no further transactions exist that refer to the old entry still present in the index. As a result of this – transactions that perform *deletions followed by insertions* may trigger unexpected unique constraint violations, as the deleted tuple has not actually been removed from the index yet. For example:

```sql
CREATE TABLE students (id INTEGER, name VARCHAR);
INSERT INTO students VALUES (1, 'John Doe');
CREATE UNIQUE INDEX students_id ON students (id);

BEGIN; -- start transaction
DELETE FROM students WHERE id = 1;
INSERT INTO students VALUES (1, 'Jane Doe');
```

The last statement fails with the following error:

```console
Constraint Error: Duplicate key "id: 1" violates unique constraint. If this is an unexpected constraint violation please double check with the known index limitations section in our documentation (https://duckdb.org/docs/sql/indexes).
```

This, combined with the fact that updates are turned into deletions and insertions within the same transaction, means that updating rows in the presence of unique or primary key constraints can often lead to unexpected unique constraint violations. For example, in the following query, `SET id = 1` causes a `Constraint Error` to occur.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'John Doe');

UPDATE students SET id = 1 WHERE id = 1;
```

```console
Constraint Error: Duplicate key "id: 1" violates primary key constraint.
If this is an unexpected constraint violation please double check with the known index limitations section in our documentation (https://duckdb.org/docs/sql/indexes).
```

Currently, this is an expected limitation of DuckDB – although we aim to resolve this in the future.