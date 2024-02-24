---
layout: docu
title: CHECKPOINT Statement
railroad: statements/checkpoint.js
---

The `CHECKPOINT` statement synchronizes data in the write-ahead log (WAL) to the database data file. For in-memory
databases this statement will succeed with no effect.

## Examples

```sql
-- Synchronize data in the default database
CHECKPOINT;
-- Synchronize data in the specified database
CHECKPOINT file_db;
-- Abort any in-progress transactions to synchronize the data
FORCE CHECKPOINT;
```

## Syntax

<div id="rrdiagram1"></div>

Checkpoint operations happen automatically based on the WAL size (see [Configuration](../configuration)). This
statement is for manual checkpoint actions.

## Behavior

The default `CHECKPOINT` command will fail if there are any running transactions. Including `FORCE` will abort any
transactions and execute the checkpoint operation.

Also see the related [`PRAGMA` option](../pragmas#force-checkpoint) for further behavior modification.

### Reclaiming Space

When performing a checkpoint (automatic or otherwise), the space occupied by deleted rows is partially reclaimed. Note that this does not remove all deleted rows, but rather merges row groups that have a significant amount of deletes together. In the current implementation this requires ~25% of rows to be deleted in adjacent row groups.

When running in in-memory mode, checkpointing has no effect, hence it does not reclaim space after deletes in in-memory databases.

> Warning The [`VACUUM` statement](vacuum) does _not_ trigger vacuuming deletes and hence does not reclaim space.
