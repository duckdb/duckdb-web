---
layout: docu
railroad: statements/checkpoint.js
redirect_from:
- /docs/sql/statements/checkpoint
title: CHECKPOINT Statement
---

The `CHECKPOINT` statement synchronizes data in the write-ahead log (WAL) to the database data file.

## Examples

Synchronize data in the default database:

```sql
CHECKPOINT;
```

Synchronize data in the specified database:

```sql
CHECKPOINT file_db;
```

Abort any in-progress transactions to synchronize the data:

```sql
FORCE CHECKPOINT;
```

## Checkpointing In-Memory Tables

Starting with v1.4.0, in-memory tables support checkpointing. This has two key benefits:

* In-memory tables also support compression. This is disabled by default – you can turn it on using:

  ```sql
  ATTACH ':memory:' AS memory_compressed (COMPRESS);
  USE memory_compressed;
  ```

* Checkpointing triggers vacuuming deleted rows, allowing space to be reclaimed after deletes/truncation.

## Syntax

<div id="rrdiagram1"></div>

Checkpoint operations happen automatically based on the WAL size (see [Configuration]({% link docs/stable/configuration/overview.md %})). This
statement is for manual checkpoint actions.

## Behavior

The default `CHECKPOINT` command will fail if there are any running transactions. Including `FORCE` will abort any
transactions and execute the checkpoint operation.

Also see the related [`PRAGMA` option]({% link docs/stable/configuration/pragmas.md %}#force-checkpoint) for further behavior modification.

### Reclaiming Space

When performing a checkpoint (automatic or otherwise), the space occupied by deleted rows is partially reclaimed. Note that this does not remove all deleted rows, but rather merges row groups that have a significant amount of deletes together. In the current implementation this requires ~25% of rows to be deleted in adjacent row groups.

When running in in-memory mode, checkpointing has no effect, hence it does not reclaim space after deletes in in-memory databases.

> Warning The [`VACUUM` statement]({% link docs/stable/sql/statements/vacuum.md %}) does _not_ trigger vacuuming deletes and hence does not reclaim space.
