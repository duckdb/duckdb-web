---
layout: docu
title: QUALIFY Clause
railroad: query_syntax/qualify.js
blurb: The QUALIFY clause is used to filter the results of WINDOW functions.
---

The `QUALIFY` clause is used to filter the results of [`WINDOW` functions]({% link docs/sql/window_functions.md %}). This filtering of results is similar to how a [`HAVING` clause]({% link docs/sql/query_syntax/having.md %}) filters the results of aggregate functions applied based on the [`GROUP BY` clause]({% link docs/sql/query_syntax/groupby.md %}).

The `QUALIFY` clause avoids the need for a subquery or [`WITH` clause]({% link docs/sql/query_syntax/with.md %}) to perform this filtering (much like `HAVING` avoids a subquery). An example using a `WITH` clause instead of `QUALIFY` is included below the `QUALIFY` examples.

Note that this is filtering based on [`WINDOW` functions]({% link docs/sql/window_functions.md %}), not necessarily based on the [`WINDOW` clause]({% link docs/sql/query_syntax/window.md %}). The `WINDOW` clause is optional and can be used to simplify the creation of multiple `WINDOW` function expressions.

The position of where to specify a `QUALIFY` clause is following the [`WINDOW` clause]({% link docs/sql/query_syntax/window.md %}) in a `SELECT` statement (`WINDOW` does not need to be specified), and before the [`ORDER BY`]({% link docs/sql/query_syntax/orderby.md %}).

## Examples

Each of the following examples produce the same output, located below.

Filter based on a window function defined in the `QUALIFY` clause:

```sql
SELECT
    schema_name,
    function_name,
    -- In this example the function_rank column in the select clause is for reference
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) < 3;
```

Filter based on a window function defined in the `SELECT` clause:

```sql
SELECT
    schema_name,
    function_name,
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY
    function_rank < 3;
```

Filter based on a window function defined in the `QUALIFY` clause, but using the `WINDOW` clause:

```sql
SELECT
    schema_name,
    function_name,
    -- In this example the function_rank column in the select clause is for reference
    row_number() OVER my_window AS function_rank
FROM duckdb_functions()
WINDOW
    my_window AS (PARTITION BY schema_name ORDER BY function_name)
QUALIFY
    row_number() OVER my_window < 3;
```

Filter based on a window function defined in the `SELECT` clause, but using the `WINDOW` clause:

```sql
SELECT
    schema_name,
    function_name,
    row_number() OVER my_window AS function_rank
FROM duckdb_functions()
WINDOW
    my_window AS (PARTITION BY schema_name ORDER BY function_name)
QUALIFY
    function_rank < 3;
```

Equivalent query based on a `WITH` clause (without a `QUALIFY` clause):

```sql
WITH ranked_functions AS (
    SELECT
        schema_name,
        function_name,
        row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
    FROM duckdb_functions()
)
SELECT
    *
FROM ranked_functions
WHERE
    function_rank < 3;
```

<div class="narrow_table"></div>

| schema_name |  function_name  | function_rank |
|:---|:---|:---|
| main        | !__postfix      | 1             |
| main        | !~~             | 2             |
| pg_catalog  | col_description | 1             |
| pg_catalog  | format_pg_type  | 2             |

## Syntax

<div id="rrdiagram"></div>
