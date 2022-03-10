---
layout: docu
title: QUALIFY Clause
selected: Documentation/SQL/Query Syntax/Qualify
expanded: SQL
railroad: query_syntax/qualify.js
blurb: The QUALIFY clause is used to filter the result of a WINDOW function.
---

The `QUALIFY` clause is used to filter the result of [`WINDOW` functions](/docs/sql/window_functions). This filtering of results is similar to how a [`HAVING` clause](/docs/sql/query_syntax/having) filters the results of aggregate functions applied based on the [`GROUP BY` clause](/docs/sql/query_syntax/groupby). 

The `QUALIFY` clause avoids the need for a subquery or [WITH clause](/docs/sql/query_syntax/with) to perform this filtering (much like `HAVING` avoids a subquery). An example using a `WITH` clause instead of `QUALIFY` is included below the `QUALIFY` examples.

Note that this is filtering based on [`WINDOW` functions](/docs/sql/window_functions), not necessarily based on the [`WINDOW` clause](/docs/sql/query_syntax/window). The `WINDOW` clause is optional and can be used to simplify the creation of multiple `WINDOW` function expressions. 

The position of where to specify a `QUALIFY` clause is following the [`WINDOW` clause](/docs/sql/query_syntax/window) in a `SELECT` statement (`WINDOW` does not need to be specified), and before the [`ORDER BY`](/docs/sql/query_syntax/orderby).

### Examples

Each of the following examples produce the same output, located below.

```sql
-- Filter based on a WINDOW function defined in the QUALIFY clause
SELECT 
    schema_name, 
    function_name, 
    -- In this example the function_rank column in the select clause is for reference 
    row_number() over (partition by schema_name order by function_name) as function_rank 
FROM duckdb_functions() 
QUALIFY 
    row_number() over (partition by schema_name order by function_name) < 3;

-- Filter based on a WINDOW function defined in the SELECT clause
SELECT 
    schema_name, 
    function_name, 
    row_number() over (partition by schema_name order by function_name) as function_rank 
FROM duckdb_functions() 
QUALIFY 
    function_rank < 3;

-- Filter based on a WINDOW function defined in the QUALIFY clause, but using the WINDOW clause
SELECT 
    schema_name, 
    function_name, 
    -- In this example the function_rank column in the select clause is for reference 
    row_number() over my_window as function_rank 
FROM duckdb_functions() 
WINDOW
    my_window as (partition by schema_name order by function_name)
QUALIFY 
    row_number() over my_window < 3;

-- Filter based on a WINDOW function defined in the SELECT clause, but using the WINDOW clause
SELECT 
    schema_name, 
    function_name, 
    row_number() over my_window as function_rank 
FROM duckdb_functions() 
WINDOW
    my_window as (partition by schema_name order by function_name)
QUALIFY 
    function_rank < 3;

-- Equivalent query based on a WITH clause (without QUALIFY clause)
WITH ranked_functions as (
    SELECT 
        schema_name, 
        function_name, 
        row_number() over (partition by schema_name order by function_name) as function_rank 
    FROM duckdb_functions() 
)
SELECT
    *
FROM ranked_functions
WHERE
    function_rank < 3;
```

| schema_name |  function_name  | function_rank |
|:---|:---|:---|
| main        | !__postfix      | 1             |
| main        | !~~             | 2             |
| pg_catalog  | col_description | 1             |
| pg_catalog  | format_pg_type  | 2             |

### Syntax
<div id="rrdiagram"></div>