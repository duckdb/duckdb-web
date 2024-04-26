---
layout: docu
title: CALL Statement
railroad: statements/call.js
---

The `CALL` statement invokes the given table function and returns the results.

## Examples

```sql
-- Invoke the 'duckdb_functions' table function.
CALL duckdb_functions();
-- Invoke the 'pragma_table_info' table function.
CALL pragma_table_info('pg_am');

-- Select only the functions where the name starts with 'ST_'.
SELECT function_name, parameters, parameter_types, return_type 
FROM duckdb_functions()
WHERE function_name LIKE 'ST_%';
```

## Syntax

<div id="rrdiagram1"></div>
