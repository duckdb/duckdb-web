---
layout: docu
railroad: statements/indexes.js
redirect_from:
  - /docs/sql/indexes
title: Indexes
---

## Index Types

DuckDB has two built-in index types. Indexes can also be defined via [extensions]({% link docs/stable/extensions/overview.md %}).

### Min-Max Index (Zonemap)

A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as zonemap or block range index) is _automatically created_ for columns of all [general-purpose data types]({% link docs/stable/sql/data_types/overview.md %}).

### Adaptive Radix Tree (ART)

An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. ART indexes can be created manually using `CREATE INDEX` clause and they are automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint.

> Warning ART indexes must currently be able to fit in memory during index creation. Avoid creating ART indexes if the index does not fit in memory during index creation.

### Indexes Defined by Extensions

DuckDB supports [R-trees for spatial indexing]({% link docs/stable/core_extensions/spatial/r-tree_indexes.md %}) via the `spatial` extension.

## Persistence

Both min-max indexes and ART indexes are persisted on disk.

## `CREATE INDEX` and `DROP INDEX` Statements

To create an [ART index](#adaptive-radix-tree-art), use the [`CREATE INDEX` statement]({% link docs/stable/sql/statements/create_index.md %}#create-index).
To drop an [ART index](#adaptive-radix-tree-art), use the [`DROP INDEX` statement]({% link docs/stable/sql/statements/create_index.md %}#drop-index).

## Limitations of ART Indexes

ART indexes create a secondary copy of the data in a second location.
Maintaining that second copy complicates processing, particularly when combined with transactions. 
Thus, certain limitations currently apply when it comes to modifying data that is also stored in secondary indexes.

> As expected, indexes have a strong effect on performance, slowing down loading and updates, but speeding up certain queries. Please consult the [Performance Guide]({% link docs/stable/guides/performance/indexing.md %}) for details.

### Constraint Checking in `UPDATE` Statements

`UPDATE` statements on indexed columns and columns that cannot be updated in place are transformed into a `DELETE` of the original row followed by an `INSERT` of the updated row.
This rewrite has performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.

Additionally, it causes the following constraint-checking limitation of `UPDATE` statements.
The same limitation exists in other DBMSs, like PostgreSQL.

In the example below, note how the number of rows exceeds DuckDB's standard vector size, which is 2048 by default.
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

```console
Constraint Error:
Duplicate key "i: 2048" violates primary key constraint.
```

A workaround is to split the `UPDATE` into a `DELETE ... RETURNING ...` followed by an `INSERT`,
with some additional logic to (temporarily) store the result of the `DELETE`.
All statements should be run inside a transaction via `BEGIN`, and eventually `COMMIT`.

Here's an example of how that could look like in the command line client.

```sql
CREATE TABLE my_table (i INTEGER PRIMARY KEY);
INSERT INTO my_table SELECT range FROM range(3_000);

BEGIN;
CREATE TEMP TABLE tmp AS SELECT i FROM my_table;
DELETE FROM my_table;
INSERT INTO my_table SELECT i FROM tmp;
DROP TABLE tmp;
COMMIT;
```

In other clients, you might be able to fetch the result of `DELETE ... RETURNING ...`.
Then, you can use that result in a subsequent `INSERT ...` statement, or potentially make use of DuckDB's `Appender` (if available in the client).

### Over-Eager Constraint Checking in Foreign Keys

This limitation occurs if you meet the following conditions:

* A table has a `FOREIGN KEY` constraint.
* There is an `UPDATE` on the corresponding `PRIMARY KEY` table, which DuckDB rewrites into a `DELETE` followed by an `INSERT`.
* The to-be-deleted row exists in the foreign key table.

If these hold, you'll encounter an unexpected constraint violation:

```sql
CREATE TABLE pk_table (id INTEGER PRIMARY KEY, payload VARCHAR[]);
INSERT INTO pk_table VALUES (1, ['hello']);
CREATE TABLE fk_table (id INTEGER REFERENCES pk_table(id));
INSERT INTO fk_table VALUES (1);
UPDATE pk_table SET payload = ['world'] WHERE id = 1;
```

```console
Constraint Error:
Violates foreign key constraint because key "id: 1" is still referenced by a foreign key in a different table. If this is an unexpected constraint violation, please refer to our foreign key limitations in the documentation
```

The reason for this is that DuckDB does not yet support “looking ahead”.
During the `INSERT`, it is unaware it will reinsert the foreign key value as part of the `UPDATE` rewrite.

### Constraint Checking after Delete with Concurrent Transactions

To better understand the limitations of indexes, we'll first provide a brief overview of index storage in DuckDB.
DuckDB creates a physical secondary copy of the key column expressions and their row IDs when defining index-based constraints, or when using the `CREATE [UNIQUE] INDEX` statement.
That secondary structure lives in the physical storage of the table to which it belongs.
Note that constraint violations are only relevant for primary key, foreign key, and `UNIQUE` indexes.

When running transactions, DuckDB can only change or delete a value after there are no more dependencies to it from older transactions.
I.e., after all older transactions that still need to see the old value have finished.
DuckDB uses MVCC to ensure that transactionality.
For the table storage, each transaction knows if it still has visibility on a value or not.
A transaction has visibility on a value, if it started before the `COMMIT` of the change/delete.
Similarly, it has no more visibility on the value, if it started afterward.

**Indexes do not yet have such functionality.**
Let's say that a `value-row_id` pair exists in the global index and there is a `COMMIT` changing/deleting that value.
In that case, it **also** stays visible to newer transactions until all **older**, dependent transactions have finished.
That behavior causes two main limitations, which are listed in more detail below.

Please also note that the limitation extends to concurrent access to multiple tables.
Older read transactions on table X can cause write-write conflicts on consecutive changes to table Y, if both tables are in the same schema.

The long-term solution to these limitations is to enable transaction-timestamp tracking in indexes.
However, as-of now, DuckDB does not fully support MVCC for its indexes.

#### Workarounds

As this is a limitation in DuckDB, there is currently no pure-SQL workaround.
If you have concurrent reads and writes on a table with indexes, then you need to add application-side locks.
I.e., if you have multiple writes happening while a concurrent read is running, then these have to wait for the read(s) to finish.

You might also consider not using indexes altogether. 
Instead, DuckDB's `MERGE INTO` statement might suit your needs better.

#### Over-Eager Unique Constraint Checking

For uniqueness constraints, inserts can fail when they should succeed:

```cpp
// Assume "someTable" is a table with an index enforcing uniqueness.
tx1 = duckdbTxStart()
someRecord = duckdb(tx1, "SELECT * FROM someTable USING SAMPLE 1 ROWS")

tx2 = duckdbTxStart()
duckdbDelete(tx2, someRecord)
duckdbTxCommit(tx2)

// At this point someRecord is deleted, but tx1 still needs visibility on that record.
// Thus, the ART index is not updated, so the following query fails with a constraint error:
tx3 = duckdbTxStart()
duckdbInsert(tx3, someRecord)
duckdbTxCommit(tx3)

// Following this, the above insert succeeds because the ART index was allowed to update.
duckdbTxCommit(tx1)
```

Note that in older versions of DuckDB some variations of this might've **seemed** to work (no constraint exception).
That is especially the case for `UPSERT` statements.
However, these variations caused incorrect states, as constraint checking was incorrectly based on an already-deleted value.

For more details, here's a reproducer using our SQLLogic test framework.

```sql
statement ok
CREATE SCHEMA IF NOT EXISTS schema__test

concurrentloop threadid 0 3

statement ok
CREATE TABLE IF NOT EXISTS schema__test.test_table${threadid} (
                    id VARCHAR PRIMARY KEY,
                    available_actions VARCHAR[],
                    subscriber_ids VARCHAR[]
                )

loop i 0 5

statement ok
INSERT OR REPLACE INTO schema__test.test_table${threadid} VALUES ('test:scope/test-worker-${threadid}:test-id-0', ['read', 'write', 'delete'], ['sub-{threadid}', 'sub-{threadid}+1'])

endloop

endloop
```

#### Under-Eager Foreign Key Constraint Checking

For foreign key constraints, inserts can succeed when they should fail:

```cpp
// Setup: Create a primary table with a UUID primary key and a secondary table with a foreign key reference.
primaryId = generateNewGUID()
conn = duckdbConnectInMemory()

// Create tables and insert the initial record in the primary table.
duckdb(conn, "CREATE TABLE primary_table (id UUID PRIMARY KEY)")
duckdb(conn, "CREATE TABLE secondary_table (primary_id UUID, FOREIGN KEY (primary_id) REFERENCES primary_table(id))")
duckdbInsert(conn, "primary_table", {id: primaryId})

// Start a transaction tx1, which reads from primary_table.
tx1 = duckdbTxStart(conn)
readRecord = duckdb(tx1, "SELECT id FROM primary_table LIMIT 1")

// Note: tx1 remains open, holding locks/resources.
// Outside of tx1, delete the record from primary_table.
duckdbDelete(conn, "primary_table", {id: primaryId})

// Try to insert into secondary_table, which has a foreign key reference to the now-deleted primary record.
// This succeeds because tx1 is still open and the constraint isn't fully enforced yet.
duckdbInsert(conn, "secondary_table", {primary_id: primaryId})

// Commit tx1, releasing any locks/resources.
duckdbTxCommit(tx1)

// Verify the primary record is indeed deleted.
count = duckdb(conn, "SELECT count() FROM primary_table WHERE id = $primaryId", {primaryId: primaryId})
assert(count == 0, "Record should be deleted")

// Verify the secondary record with the foreign key reference exists, an inconsistent state!
count = duckdb(conn, "SELECT count() FROM secondary_table WHERE primary_id = $primaryId", {primaryId: primaryId})
assert(count == 1, "Foreign key reference should exist")
```
