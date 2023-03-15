---
layout: docu
title: Pivot Statement
selected: Documentation/SQL/Pivot
expanded: SQL
railroad: statements/pivot.js
blurb: The PIVOT statement allows values within a column to be separated into their own columns.
---
<!-- 
TODO: 
    Add to menu 
    Build RR diagram
    Document Pivot
        Short form syntax
        Long form syntax
    Document UnPivot
        Separate document?
        Short
        Long
-->

The `PIVOT` statement allows distinct values within a column to be separated into their own columns.
The values within those new columns are calculated using an aggregate function on the subset of rows that match each distinct value.

DuckDB implements both the SQL Standard `PIVOT` syntax and a simplified `PIVOT` syntax that automatically detects the columns to create while pivoting. 
`PIVOT_WIDER` may also be used in place of the `PIVOT` keyword.

## Simplified Pivot Syntax

The full syntax diagram is below, but the simplified `PIVOT` syntax can be summarized as:
```sql
PIVOT [dataset] 
ON [pivot_column(s)] 
USING [aggregate_expression(s)] 
GROUP BY [group_by_expression(s)]
```
The `ON`, `USING`, and `GROUP BY` clauses are each optional, but they may not all be omitted.


## Simplified Pivot Full Syntax Diagram
Below is the full syntax diagram of the `PIVOT` statement. 

<div id="rrdiagram"></div>


## SQL Standard Pivot Syntax
The full syntax diagram is below, but the SQL Standard `PIVOT` syntax can be summarized as:
```sql
FROM [dataset] 
PIVOT (
    [aggregate_expression(s)]
    FOR 
        [pivot_column_1] IN ([in-list])
        [pivot_column_2] IN ([in-list])
        ...
    GROUP BY [group_by_expression(s)]
)
```