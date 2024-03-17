---
layout: docu
title: Functions
railroad: expressions/function.js
---

## Function Syntax

<div id="rrdiagram"></div>

## Query Functions

The `duckdb_functions()` table function shows the list of functions currently built into the system.

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

| function_name | function_type | return_type |       parameters       |         parameter_types          |                                                               description                                                                |
|---------------|---------------|-------------|------------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| bar           | scalar        | VARCHAR     | [x, min, max, width]   | [DOUBLE, DOUBLE, DOUBLE, DOUBLE] | Draws a band whose width is proportional to (x - min) and equal to width characters when x = max. width defaults to 80                   |
| base64        | scalar        | VARCHAR     | [blob]                 | [BLOB]                           | Convert a blob to a base64 encoded string                                                                                                |
| bin           | scalar        | VARCHAR     | [value]                | [VARCHAR]                        | Converts the value to binary representation                                                                                              |
| bit_count     | scalar        | TINYINT     | [x]                    | [TINYINT]                        | Returns the number of bits that are set                                                                                                  |
| bit_length    | scalar        | BIGINT      | [col0]                 | [VARCHAR]                        | NULL                                                                                                                                     |
| bit_position  | scalar        | INTEGER     | [substring, bitstring] | [BIT, BIT]                       | Returns first starting index of the specified substring within bits, or zero if it is not present. The first (leftmost) bit is indexed 1 |
| bitstring     | scalar        | BIT         | [bitstring, length]    | [VARCHAR, INTEGER]               | Pads the bitstring until the specified length                                                                                            |

> Currently, the description and parameter names of functions are not available in the `duckdb_functions()` function.
