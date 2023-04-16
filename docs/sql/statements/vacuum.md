---
layout: docu
title: Vacuum
selected: Documentation/SQL/Vacuum
expanded: SQL
railroad: statements/vacuum.js
---

The `VACUUM` statement garbage collects DuckDB.

### Examples
```sql
-- Clean up all tables in all databases.
VACUUM;
-- Clean up everything, then run analyze.
VACUUM ANALYZE;
-- Garbage collect the given database and column.
VACUUM memory.main.my_table(my_column);
```

### Syntax
<div id="rrdiagram1"></div>

The `VACUUM` statement is modeled on the PostgreSQL [VACUUM](https://www.postgresql.org/docs/current/sql-vacuum.html) statement.
