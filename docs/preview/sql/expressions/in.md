---
layout: docu
railroad: expressions/in.js
title: IN Operator
---

<div id="rrdiagram"></div>

## `IN`

The `IN` operator checks containment of the left expression inside the collection the right hand side (RHS). The `IN` operator returns `true` if the expression is present in the RHS, `false` if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values. Supported collections on the RHS are tuples, lists, maps and subqueries that return a single column (see the [subqueries page]({% link docs/preview/sql/expressions/subqueries.md %})). For maps, the `IN` operator checks for containment in the keys, not in the values.

```sql
SELECT 'Math' IN ('CS', 'Math');
```

```text
true
```

```sql
SELECT 'English' IN ('CS', 'Math');
```

```text
false
```

```sql
SELECT 'Math' IN ('CS', 'Math', NULL);
```

```text
true
```

```sql
SELECT 'English' IN ('CS', 'Math', NULL);
```

```text
NULL
```

## `NOT IN`

`NOT IN` can be used to check if an element is not present in the set. `x NOT IN y` is equivalent to `NOT (x IN y)`.
