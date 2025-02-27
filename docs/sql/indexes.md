---
layout: docu
title: Indexes
railroad: statements/indexes.js
---

## Index Types

DuckDB has two built-in index types. Indexes can also be defined via [extensions]({% link docs/extensions/overview.md %}).

### Min-Max Index (Zonemap)

A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as zonemap or block range index) is _automatically created_ for columns of all [general-purpose data types]({% link docs/sql/data_types/overview.md %}).

### Adaptive Radix Tree (ART)

An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. ART indexes can be created manually using `CREATE INDEX` clause and they are automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint.

> Warning ART indexes must currently be able to fit in memory during index creation. Avoid creating ART indexes if the index does not fit in memory during index creation.

### Indexes Defined by Extensions

DuckDB supports [R-trees for spatial indexing]({% link docs/extensions/spatial/r-tree_indexes.md %}) via the `spatial` extension.

## Persistence

Both min-max indexes and ART indexes are persisted on disk.

## `CREATE INDEX` and `DROP INDEX` Statements

To create an [ART index](#adaptive-radix-tree-art), use the [`CREATE INDEX` statement]({% link docs/sql/statements/create_index.md %}#create-index).
To drop an [ART index](#adaptive-radix-tree-art), use the [`DROP INDEX` statement]({% link docs/sql/statements/create_index.md %}#drop-index).

## Limitations of ART Indexes

ART indexes create a secondary copy of the data in a second location – this complicates processing, particularly when combined with transactions. Certain limitations apply when it comes to modifying data that is also stored in secondary indexes.

> As expected, indexes have a strong effect on performance, slowing down loading and updates, but speeding up certain queries. Please consult the [Performance Guide]({% link docs/guides/performance/indexing.md %}) for details.

### Constraint Checking in `UPDATE` Statements

`UPDATE` statements on indexed columns and columns that cannot be updated in place are transformed into a `DELETE` of the original row followed by an `INSERT` of the updated row.
This rewrite has performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.

Additionally, it causes the following constraint-checking limitation of `UPDATE` statements. The same limitation exists in other DBMSs, like PostgreSQL.

In the example below, note how the number of rows exceeds DuckDB's standard vector size, which is 2048.
The `UPDATE` statement is rewritten into a `DELETE`, followed by an `INSERT`.
This rewrite happens per chunk of data (2048 rows) moving through DuckDB's processing pipeline.
When updating `i = 2047` to `i = 2048`, we do not yet know that 2048 becomes 2049, and so forth.
That is because we have not yet seen that chunk.
Thus, we throw a constraint violation.

```sql
CREATE TABLE my_table (i INTEGER PRIMARY KEY);
INSERT INTO my_table SELECT range FROM range(3_000);
UPDATE my_table SET i = i + 1;
```

```sql
Constraint Error:
Duplicate key "i: 2048" violates primary key constraint.
```

A workaround is to split the `UPDATE` into a `DELETE ... RETURNING ...` followed by an `INSERT`.
Both statements should be run inside a transaction via `BEGIN`, and eventually `COMMIT`.

### Over-eager Constraint Checking in Foreign Keys

This limitation occurs if you meet the following conditions:
- A table has a `FOREIGN KEY` constraint.
- There is an `UPDATE` on the corresponding `PRIMARY KEY` table, which DuckDB rewrites into a `DELETE` followed by an `INSERT`.
  - The to-be-deleted row must exist in the foreign key table.

You'll encounter an unexpected constraint violation.
That is because DuckDB does not yet support 'looking ahead'.
During the `INSERT`, it is unaware it will reinsert the foreign key value as part of the `UPDATE` rewrite.

```sql
CREATE TABLE pk_table (id INT PRIMARY KEY, payload VARCHAR[]);
INSERT INTO pk_table VALUES (1, ['hello']);
CREATE TABLE fk_table (id INT REFERENCES pk_table(id));
INSERT INTO fk_table VALUES (1);
UPDATE pk_table SET payload = ['world'] WHERE id = 1;
```

```sql
Constraint Error:
Violates foreign key constraint because key "id: 1" is still referenced by a foreign key in a different table. If this is an unexpected constraint violation, please refer to our foreign key limitations in the documentation
```
