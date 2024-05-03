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

| result |
|:-------|
| false  |

However, we cannot compare `VARCHAR` values with dates.

```sql
SELECT d > '1992-01-01'::VARCHAR FROM (VALUES (DATE '1992-01-01')) t(d);
```

```console
Binder Error: Cannot compare values of type DATE and type VARCHAR - an explicit cast is required
LINE 1: SELECT d > '1992-01-01'::VARCHAR FROM (VALUES (D...
                 ^
```

### Escape String Literals

To include special characters such as newline, use `E` escape the string. Both the uppercase (`E'...'`) and lowercase variants (`e'...'`) work.

```sql
SELECT E'Hello\nworld' AS msg;
-- or
SELECT e'Hello\nworld' AS msg;
```

<!-- This output intentionally uses the duckbox formatter -->

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

The following backslash escape sequences are supported:

| Escape sequence | Name | ASCII code |
|:--|:--|--:|
| `\b` | backspace | 8 |
| `\f` | form feed | 12 |
| `\n` | newline | 10 |
| `\r` | carriage return |  13 |
| `\t` | tab | 9 |

### Dollar-Quoted String Literals

DuckDB supports dollar-quoted string literals, which are surrounded by double-dollar symbols (`$$`):

```sql
SELECT $$Hello
world$$ AS msg;
```

<!-- This output intentionally uses the duckbox formatter -->

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

```sql
SELECT $$The price is $9.95$$ AS msg;
```

|        msg         |
|--------------------|
| The price is $9.95 |
