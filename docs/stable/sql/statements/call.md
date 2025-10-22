---
layout: docu
railroad: statements/call.js
redirect_from:
- /docs/sql/statements/call
title: CALL Statement
---

The `CALL` statement invokes the given [table function]({% link docs/stable/sql/query_syntax/from.md %}#table-functions) and returns the results. 

> Thanks to the [`FROM`-first syntax]({% link docs/stable/sql/query_syntax/from.md %}#from-first-syntax) and the fact that procedures in DuckDB are implemented as table functions, you can use `FROM` instead of `CALL`.

## Examples

Invoke the 'duckdb_functions' table function:

```sql
CALL duckdb_functions();
```

Invoke the 'pragma_table_info' table function:

```sql
CALL pragma_table_info('pg_am');
```

Select only the functions where the name starts with `ST_`:

```sql
SELECT function_name, parameters, parameter_types, return_type
FROM duckdb_functions()
WHERE function_name LIKE 'ST_%';
```

## Syntax

<div id="rrdiagram1"></div>
