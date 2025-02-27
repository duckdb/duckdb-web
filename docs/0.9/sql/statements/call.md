---
layout: docu
railroad: statements/call.js
redirect_from:
- docs/archive/0.9.2/sql/statements/call
- docs/archive/0.9.1/sql/statements/call
- docs/archive/0.9.0/sql/statements/call
title: Call
---

The `CALL` statement invokes the given table function and returns the results.

## Examples

```sql
-- Invoke the 'duckdb_functions' table function.
CALL duckdb_functions();
-- Invoke the 'pragma_table_info' table function. 
CALL pragma_table_info('pg_am');
```

## Syntax

<div id="rrdiagram1"></div>