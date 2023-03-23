---
layout: docu
title: Case Statement
selected: Documentation/Expressions/Case
expanded: Expressions
railroad: expressions/case.js
---
<div id="rrdiagram"></div>

The `CASE` statement performs a switch based on a condition. The basic form is identical to the ternary condition used in many programming languages (`CASE WHEN cond THEN a ELSE b END` is equivalent to `cond ? a : b`).
```sql
-- integers [1, 2, 3]
SELECT i, CASE WHEN i>2 THEN 1 ELSE 0 END FROM integers;
-- 1, 2, 3
-- 0, 0, 1
```

The `WHEN cond THEN expr` part of the `CASE` statement can be chained, whenever any of the conditions returns true for a single tuple, the corresponding expression is evaluated and returned.

```sql
-- integers [1, 2, 3]
SELECT i, CASE WHEN i=1 THEN 10 WHEN i=2 THEN 20 ELSE 0 END FROM integers;
-- 1, 2, 3
-- 10, 20, 0
```

The `ELSE` part of the `CASE` statement is optional. If no else statement is provided and none of the conditions match, the `CASE` statement will return `NULL`.

```sql
-- integers [1, 2, 3]
SELECT i, CASE WHEN i=1 THEN 10 END FROM integers;
-- 1, 2, 3
-- 10, NULL, NULL
```

After the `CASE` but before the `WHEN` an individual expression can also be provided. When this is done, the `CASE` statement is essentially transformed into a switch statement.

```sql
-- integers [1, 2, 3]
SELECT i, CASE i WHEN 1 THEN 10 WHEN 2 THEN 20 WHEN 3 THEN 30 END FROM integers;
-- 1, 2, 3
-- 10, 20, 30

-- this is equivalent to:
SELECT i, CASE WHEN i=1 THEN 10 WHEN i=2 THEN 20 WHEN i=3 THEN 30 END FROM integers;
```
