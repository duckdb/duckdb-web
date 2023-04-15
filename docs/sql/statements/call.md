---
layout: docu
title: Call
selected: Documentation/SQL/Call
expanded: SQL
railroad: statements/call.js
---

The `CALL` statement invokes the given table function and returns the results.

### Examples
```sql
-- Inoke the 'duckdb_functions' table function.
CALL duckdb_functions();
-- Invoke the 'pragma_table_info' table function. 
CALL pragma_table_info('pg_am');
```

### Syntax
<div id="rrdiagram1"></div>
