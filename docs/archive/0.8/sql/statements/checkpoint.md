---
layout: docu
title: Checkpoint
selected: Documentation/SQL/Checkpoint
expanded: SQL
railroad: statements/checkpoint.js
---

The `CHECKPOINT` statement synchronizes data in the write-ahead log (WAL) to the database data file. For in-memory
databases this statement will succeed with no effect.

### Examples
```sql
-- Synchronize data in the default database
CHECKPOINT;
-- Synchronize data in the specified database
CHECKPOINT file_db;
-- Abort any in-progress transactions to synchronize the data
FORCE CHECKPOINT;
```

### Syntax
<div id="rrdiagram1"></div>

Checkpoint operations happen automatically based on the WAL size (see [Configuration](../configuration)). This
statement is for manual checkpoint actions.

### Behavior
The default `CHECKPOINT` command will fail if there are any running transactions. Including `FORCE` will abort any
transactions and execute the checkpoint operation.

Also see the related [pragma](../pragmas#force_checkpoint) for further behavior modification.
