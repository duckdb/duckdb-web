---
layout: docu
railroad: expressions/in.js
redirect_from:
- /docs/sql/expressions/in
title: IN Operator
---

<div id="rrdiagram"></div>

## `IN ⟨collection⟩`

The `IN` operator checks containment of the left expression inside the _collection_ on the right hand side (RHS). The `IN` operator returns `true` if the expression is present in the RHS, `false` if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values. Supported collections on the RHS are tuples, lists, maps and subqueries that return a single column (see the [subqueries page]({% link docs/stable/sql/expressions/subqueries.md %})). For maps, the `IN` operator checks for containment in the keys, not in the values.

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

## `IN ⟨list⟩`

The `IN` operator works on lists according to the semantics used in Python.
Unlike for the [`IN ⟨collection⟩` operator](#in-collection), the presence of `NULL` values on the right hand side of the expression does not make a difference in the result:

```sql
SELECT 'Math' IN ['CS', 'Math', NULL];
```

```text
true
```

```sql
SELECT 'English' IN ['CS', 'Math', NULL];
```

```text
false
```

## `IN ⟨map⟩`

The `IN` operator works on maps according to the semantics used in Python, i.e., the it checks for the presence of keys:

```sql
SELECT 'key1' IN MAP {'key1': 50, 'key2': 75};
```

```text
true
```

```sql
SELECT 'key3' IN MAP {'key1': 50, 'key2': 75};
```

```text
false
```

## `NOT IN`

`NOT IN` can be used to check if an element is not present in the set.
`x NOT IN y` is equivalent to `NOT (x IN y)`.
