---
layout: docu
railroad: statements/vacuum.js
title: VACUUM Statement
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

The `VACUUM` statement does not reclaim space.
For instruction on reclaiming space, refer to the [“Reclaiming space” page]({% link docs/archive/1.1/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## Syntax

<div id="rrdiagram1"></div>