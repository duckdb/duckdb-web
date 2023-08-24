---
layout: docu
title: Functions
railroad: expressions/function.js
---
Functions are ...
<div id="rrdiagram"></div>

### Query Functions

`duckdb_functions` table function shows the list of functions currently built into the system.

```sql
SELECT DISTINCT ON(function_name) function_name, function_type, return_type, parameters, parameter_types
FROM duckdb_functions()
WHERE function_type='scalar'
LIMIT 10;
```
```text
┌────────────────┬───────────────┬─────────────┬──────────────────────────┬──────────────────────────────────────┐
│ function_name  │ function_type │ return_type │        parameters        │           parameter_types            │
├────────────────┼───────────────┼─────────────┼──────────────────────────┼──────────────────────────────────────┤
│ log10          │ scalar        │ DOUBLE      │ [col0]                   │ [DOUBLE]                             │
│ mod            │ scalar        │ TINYINT     │ [col0, col1]             │ [TINYINT, TINYINT]                   │
│ date_diff      │ scalar        │ BIGINT      │ [col0, col1, col2]       │ [VARCHAR, DATE, DATE]                │
│ writefile      │ scalar        │ VARCHAR     │ []                       │ []                                   │
│ regexp_replace │ scalar        │ VARCHAR     │ [col0, col1, col2, col3] │ [VARCHAR, VARCHAR, VARCHAR, VARCHAR] │
│ age            │ scalar        │ INTERVAL    │ [col0]                   │ [TIMESTAMP]                          │
│ age            │ scalar        │ INTERVAL    │ [col0, col1]             │ [TIMESTAMP, TIMESTAMP]               │
│ datediff       │ scalar        │ BIGINT      │ [col0, col1, col2]       │ [VARCHAR, DATE, DATE]                │
│ map            │ scalar        │ MAP         │ []                       │ []                                   │
│ year           │ scalar        │ BIGINT      │ [col0]                   │ [TIMESTAMP WITH TIME ZONE]           │
└────────────────┴───────────────┴─────────────┴──────────────────────────┴──────────────────────────────────────┘
```

Currently the description and parameter names of functions are still missing.

### More
