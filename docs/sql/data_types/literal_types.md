---
layout: docu
title: Literal Types
---

DuckDB has special literal types for representing `NULL`, integer and string literals in queries. These have their own binding and conversion rules.

> Prior to version 0.10.0, integer and string literals behaved identically to the `INTEGER` and `VARCHAR` types.

## Null Literals

The `NULL` literal can be implicitly converted to any other type.

## Integer Literals

`INTEGER_LITERAL` types can be implicitly converted to any [integer type](numeric#integer-types) in which the value fits. For example, the integer literal `42` can be implicitly converted to a `TINYINT`, but the integer literal `1000` cannot be.

## String Literals

`STRING_LITERAL` instances can be implicitly converted to _any_ other type.

For example, we can compare string literals with dates.

```sql
SELECT d > '1992-01-01' AS result FROM (VALUES (DATE '1992-01-01')) t(d);
```

```text
┌─────────┐
│ result  │
│ boolean │
├─────────┤
│ false   │
└─────────┘
```

However, we cannot compare `VARCHAR` values with dates.

```sql
SELECT d > '1992-01-01'::VARCHAR FROM (VALUES (DATE '1992-01-01')) t(d);
```

```text
-- Binder Error: Cannot compare values of type DATE and type VARCHAR –
-- an explicit cast is required
```
