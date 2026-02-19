---
layout: docu
title: TRY expression
---

The `TRY` expression ensures that errors caused by the input rows in the child (scalar) expression result in `NULL` for those rows, instead of causing the query to throw an error.

> The `TRY` expression was inspired by the [`TRY_CAST` expression]({% link docs/preview/sql/expressions/cast.md %}#try_cast).

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

### Logarithm on Zero

#### Without `TRY`

```sql
SELECT ln(0);
```

```console
Out of Range Error:
cannot take logarithm of zero
```

#### With `TRY`

```sql
SELECT TRY(ln(0));
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

## Limitations

`TRY` cannot be used in combination with a volatile function or with a [scalar subquery]({% link docs/preview/sql/expressions/subqueries.md %}#scalar-subquery).
For example:

```sql
SELECT TRY(random())
```

```console
Binder Error:
TRY can not be used in combination with a volatile function
```
