---
layout: docu
title: VACUUM Statement
railroad: statements/vacuum.js
---

The `VACUUM` statement alone does nothing and is at present provided for PostgreSQL-compatibility.
The `VACUUM ANALYZE` statement recomputes table statistics if they have become stale due to table updates or deletions.

## Examples

No-op:

```sql
VACUUM;
```

Rebuild database statistics:

```sql
VACUUM ANALYZE;
```

Rebuild statistics for the table and column:

```sql
VACUUM ANALYZE memory.main.my_table(my_column);
```

Not supported:

```sql
VACUUM FULL; -- error
```

## Reclaiming Space

To reclaim space after deleting rows, use the [`CHECKPOINT` statement]({% link docs/sql/statements/checkpoint.md %}).

## Syntax

<div id="rrdiagram1"></div>
