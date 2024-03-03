---
layout: docu
railroad: statements/vacuum.js
redirect_from:
- docs/archive/0.9.2/sql/statements/vacuum
- docs/archive/0.9.1/sql/statements/vacuum
- docs/archive/0.9.0/sql/statements/vacuum
title: Vacuum
---

The `VACUUM` statement alone does nothing and is at present provided for PostgreSQL-compatibility.
The `VACUUM ANALYZE` statement recomputes table statistics if they have become stale due to table updates or deletions.

## Examples

```sql
-- No-op
VACUUM;
-- Rebuild database statistics
VACUUM ANALYZE;
-- Rebuild statistics for the table & column
VACUUM ANALYZE memory.main.my_table(my_column);
-- Not supported
VACUUM FULL; -- error
```

## Syntax

<div id="rrdiagram1"></div>