---
layout: docu
title: Functions
railroad: expressions/function.js
---

## Function Syntax

<div id="rrdiagram"></div>

## Query Functions

`duckdb_functions` table function shows the list of functions currently built into the system.

```sql
SELECT DISTINCT ON(function_name)
    function_name,
    function_type,
    return_type,
    parameters,
    parameter_types,
    description
FROM duckdb_functions()
WHERE function_type = 'scalar' AND function_name LIKE 'b%'
ORDER BY function_name;
```
```text
┌───────────────┬───────────────┬─────────────┬──────────────────────┬──────────────────────┬──────────────────────────────────────────┐
│ function_name │ function_type │ return_type │      parameters      │   parameter_types    │               description                │
│    varchar    │    varchar    │   varchar   │      varchar[]       │      varchar[]       │                 varchar                  │
├───────────────┼───────────────┼─────────────┼──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ bar           │ scalar        │ VARCHAR     │ [x, min, max, width] │ [DOUBLE, DOUBLE, D…  │ Draws a band whose width is proportion…  │
│ base64        │ scalar        │ VARCHAR     │ [blob]               │ [BLOB]               │ Converts a blob to a base64 encoded st…  │
│ bin           │ scalar        │ VARCHAR     │ [value]              │ [VARCHAR]            │ Converts the value to binary represent…  │
│ bit_count     │ scalar        │ TINYINT     │ [x]                  │ [TINYINT]            │ Returns the number of bits that are set  │
│ bit_length    │ scalar        │ BIGINT      │ [col0]               │ [VARCHAR]            │                                          │
│ bit_position  │ scalar        │ INTEGER     │ [substring, bitstr…  │ [BIT, BIT]           │ Returns first starting index of the sp…  │
│ bitstring     │ scalar        │ BIT         │ [bitstring, length]  │ [VARCHAR, INTEGER]   │ Pads the bitstring until the specified…  │
└───────────────┴───────────────┴─────────────┴──────────────────────┴──────────────────────┴──────────────────────────────────────────┘
```

Currently the description and parameter names of functions are still missing.
