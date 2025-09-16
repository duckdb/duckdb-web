---
layout: docu
railroad: expressions/in.js
redirect_from:
- /docs/sql/expressions/in
title: IN Operator
---

The `IN` operator checks containment of the left expression inside the _collection_ on the right hand side (RHS).
Supported collections on the RHS are tuples, lists, maps and subqueries that return a single column.

<div id="rrdiagram"></div>

## `IN (val1, val2, ...)` (Tuple)

The `IN` operator on a tuple `(val1, val2, ...)` returns `true` if the expression is present in the RHS, `false` if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values.

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

## `IN [val1, val2, ...]` (List)

The `IN` operator works on lists according to the semantics used in Python.
Unlike for the [`IN tuple` operator](#in-val1-val2--tuple), the presence of `NULL` values on the right hand side of the expression does not make a difference in the result:

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

## `IN` Map

The `IN` operator works on [maps]({% link docs/stable/sql/data_types/map.md %}) according to the semantics used in Python, i.e., it checks for the presence of keys (not values):

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

## `IN` Subquery

The `IN` operator works with [subqueries]({% link docs/stable/sql/expressions/subqueries.md %}) that return a single column.
For example:

```sql
SELECT 42 IN (SELECT unnest([32, 42, 52]) AS x);
```

```text
true
```

If the subquery returns more than one column, a Binder Error is thrown:

```sql
SELECT 42 IN (SELECT unnest([32, 42, 52]) AS x, 'a' AS y);
```

```console
Binder Error:
Subquery returns 2 columns - expected 1
```

## `IN` String

The `IN` operator can be used as a shorthand for the [`contains` string function]({% link docs/stable/sql/functions/text.md %}#containsstring-search_string).
For example:

```sql
SELECT 'Hello' IN 'Hello World';
```

```text
true
```

## `NOT IN`

`NOT IN` can be used to check if an element is not present in the set.
`x NOT IN y` is equivalent to `NOT (x IN y)`.
