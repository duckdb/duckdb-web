---
layout: docu
title: Reclaiming Space
---

DuckDB uses a single-file format, which has some inherent limitations w.r.t. reclaiming disk space.

## `CHECKPOINT`

To reclaim space after deleting rows, use the [`CHECKPOINT` statement]({% link docs/preview/sql/statements/checkpoint.md %}).

## `VACUUM`

The [`VACUUM` statement]({% link docs/preview/sql/statements/vacuum.md %}) does _not_ trigger vacuuming deletes and hence does not reclaim space.

## Compacting a Database by Copying

To compact the database, you can create a fresh copy of the database using the [`COPY FROM DATABASE` statement]({% link docs/preview/sql/statements/copy.md %}#copy-from-database--to). In the following example, we first connect to the original database `db1`, then the new (empty) database `db2`. Then, we copy the content of `db1` to `db2`.

```sql
ATTACH 'db1.db' AS db1;
ATTACH 'db2.db' AS db2;
COPY FROM DATABASE db1 TO db2;
```
