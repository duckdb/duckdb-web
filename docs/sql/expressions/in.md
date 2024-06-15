---
layout: docu
title: IN Operator
railroad: expressions/in.js
---

<div id="rrdiagram"></div>

## `IN`

The `IN` operator checks containment of the left expression inside the set of expressions on the right hand side (RHS). The `IN` operator returns true if the expression is present in the RHS, false if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values.

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

## Use with Subqueries

The `IN` operator can also be used with a subquery that returns a single column. See the [subqueries page for more information]({% link docs/sql/expressions/subqueries.md %}).
