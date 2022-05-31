---
layout: docu
title: IN Operator
selected: Documentation/Expressions/In
expanded: Expressions
railroad: expressions/in.js
---

## In Operator
<div id="rrdiagram"></div>

The `IN` operator checks containment of the left expression inside the set of expressions on the right hand side (RHS). The `IN` operator returns true if the expression is present in the RHS, false if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values.

```sql
SELECT 'Math' IN ('CS', 'Math');
-- true
SELECT 'English' IN ('CS', 'Math');
-- false

SELECT 'Math' IN ('CS', 'Math', NULL);
-- true
SELECT 'English' IN ('CS', 'Math', NULL);
-- NULL
```

`NOT IN` can be used to check if an element is not present in the set. `X NOT IN Y` is equivalent to `NOT(X IN Y)`.

The `IN` operator can also be used with a subquery that returns a single column. See the [subqueries page for more information](/docs/sql/expressions/subqueries).
