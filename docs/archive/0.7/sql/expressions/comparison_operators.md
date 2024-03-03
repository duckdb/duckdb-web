---
layout: docu
title: Comparisons
selected: Documentation/Expressions/Comparisons
expanded: Expressions
railroad: expressions/comparison.js
---
## Comparison Operators
<div id="rrdiagram2"></div>

The table below shows the standard comparison operators.
Whenever either of the input arguments is `NULL`, the output of the comparison is `NULL`.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `<` | less than | `2 < 3` | `TRUE` |
| `>` | greater than | `2 > 3` | `FALSE` |
| `<=` | less than or equal to | `2 <= 3` | `TRUE` |
| `>=` | greater than or equal to | `4 >= NULL` | `NULL` |
| `=` | equal | `NULL = NULL` | `NULL` |
| `<>` or `!=` | not equal | `2 <> 2` | `FALSE` |

The table below shows the standard distinction operators.
These operators treat `NULL` values as equal.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `IS DISTINCT FROM` | equal, including `NULL` | `2 IS DISTINCT FROM NULL` | `TRUE` |
| `IS NOT DISTINCT FROM` | not equal, including `NULL` | `NULL IS NOT DISTINCT FROM NULL` | `TRUE` |

## BETWEEN and IS (NOT) NULL
<div id="rrdiagram1"></div>

Besides the standard comparison operators there are also the `BETWEEN` and `IS (NOT) NULL` operators. These behave much like operators, but have special syntax mandated by the SQL standard. They are shown in the table below.

| Predicate | Description |
|:---|:---|
| `a BETWEEN x AND y` | equivalent to `a >= x AND a <= y` |
| `a NOT BETWEEN x AND y` | equivalent to `a < x OR a > y` |
| `expression IS NULL` | `TRUE` if expression is `NULL`, `FALSE` otherwise |
| `expression ISNULL` | alias for `IS NULL` (non-standard) |
| `expression IS NOT NULL` | `FALSE` if expression is `NULL`, `TRUE` otherwise |
| `expression NOTNULL` | alias for `IS NOT NULL` (non-standard) |
