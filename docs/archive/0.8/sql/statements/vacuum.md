---
layout: docu
title: Vacuum
selected: Documentation/SQL/Vacuum
expanded: SQL
railroad: statements/vacuum.js
---

The `VACUUM` statement is primarily in place for PostgreSQL compatibility.

### Examples
```sql
-- No-op.
VACUUM;
-- Rebuild database statistics.
VACUUM ANALYZE;
-- Rebuild statistics for the table & column.
VACUUM ANALYZE memory.main.my_table(my_column);
```

### Syntax
<div id="rrdiagram1"></div>

The `VACUUM` statement alone does nothing. `VACUUM ANALYZE` will recompute table statistics if they
have become stale due to table updates or deletions.
