---
layout: docu
railroad: statements/checkpoint.js
redirect_from:
- docs/archive/0.9.2/sql/statements/checkpoint
- docs/archive/0.9.1/sql/statements/checkpoint
- docs/archive/0.9.0/sql/statements/checkpoint
title: Checkpoint
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

Also see the related [pragma](../pragmas#force_checkpoint) for further behavior modification.