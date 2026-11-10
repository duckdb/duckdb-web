---
layout: docu
redirect_from:
- /docs/stable/sql/expressions/try
- /docs/current/sql/expressions/try
- /docs/lts/sql/expressions/try
- /docs/preview/sql/expressions/try
tested: true
title: TRY Expression
---

The `TRY` expression ensures that errors caused by the input rows in the child (scalar) expression result in `NULL` for those rows, instead of causing the query to throw an error.

> The `TRY` expression was inspired by the [`TRY_CAST` expression]({% link docs/2.0/sql/expressions/cast.md %}#try_cast).

## Examples

The following calls return errors when invoked without the `TRY` expression.
When they are wrapped into a `TRY` expression, they return `NULL`:

### Casting

#### Without `TRY`

```sql
SELECT 'abc'::INTEGER;
```

```console
Conversion Error:
Could not convert string 'abc' to INT32
```

#### With `TRY`

```sql
SELECT TRY('abc'::INTEGER);
```

```text
NULL
```

### Integer Division by Zero

#### Without `TRY`

```sql
SELECT 1 // 0;
```

```console
Invalid Input Error:
Division by zero in expression (1 // 0). Use TRY(...) to return NULL for this expression, or SET error_on_division_by_zero=false to return NULL for all divisions by zero.
```

#### With `TRY`

```sql
SELECT TRY(1 // 0);
```

```text
NULL
```

### Casting Multiple Rows

#### Without `TRY`

```sql
WITH cte AS (FROM (VALUES ('123'), ('test'), ('235')) t(a))
SELECT a::INTEGER AS x FROM cte;
```

```console
Conversion Error:
Could not convert string 'test' to INT32
```

#### With `TRY`

```sql
WITH cte AS (FROM (VALUES ('123'), ('test'), ('235')) t(a))
SELECT TRY(a::INTEGER) AS x FROM cte;
```

<div class="center_aligned_header_table"></div>

|  x   |
|-----:|
| 123  |
| NULL |
| 235  |

### Scalar Subqueries

`TRY` can wrap a [scalar subquery]({% link docs/2.0/sql/expressions/subqueries.md %}#scalar-subquery).
If an expression inside the subquery raises an execution error, the subquery result is `NULL` as a whole:

```sql
CREATE TABLE t AS SELECT * FROM (VALUES (1), (0), (2)) s(x);
SELECT TRY((SELECT max(1 // x) FROM t));
```

```text
NULL
```

For aggregate projections, DuckDB also probes inputs with `has_error` so a single failing row does not silently drop from the aggregate; empty-input aggregates keep their usual results.

## Limitations

`TRY` cannot be used in combination with a volatile function or an aggregate function used *outside* a scalar subquery rewrite.
For example:

```sql
SELECT TRY(random())
```

```console
Binder Error:
TRY can not be used in combination with a volatile function
```
