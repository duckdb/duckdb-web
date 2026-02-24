---
layout: docu
title: Literal Types
---

DuckDB has special literal types for representing `NULL`, integer and string literals in queries. These have their own binding and conversion rules.

> Prior to DuckDB version 0.10.0, integer and string literals behaved identically to the `INTEGER` and `VARCHAR` types.

## Null Literals

The `NULL` literal is denoted with the keyword `NULL`. The `NULL` literal can be implicitly converted to any other type.

## Integer Literals

Integer literals are denoted as a sequence of one or more decimal digits. At runtime, these result in values of the `INTEGER_LITERAL` type. `INTEGER_LITERAL` types can be implicitly converted to any [integer type]({% link docs/preview/sql/data_types/numeric.md %}#integer-types) in which the value fits. For example, the integer literal `42` can be implicitly converted to a `TINYINT`, but the integer literal `1000` cannot be.

> DuckDB does not support hexadecimal or binary literals directly. However, strings or string literals in hexadecimal or binary notation with `0x` or `0b` prefixes respectively, can be cast to integer types, e.g., `'0xFF'::INT = 255` or `0b101::INT = 5`.

## Other Numeric Literals

Non-integer numeric literals can be denoted with decimal notation, using the period character (`.`) to separate the integer part and the decimal part of the number.
Either the integer part or the decimal part may be omitted:

```sql
SELECT 1.5;          -- 1.5
SELECT .50;          -- 0.5
SELECT 2.;           -- 2.0
```

Non-integer numeric literals can also be denoted using [_E notation_](https://en.wikipedia.org/wiki/Scientific_notation#E_notation). In E notation, an integer or decimal literal is followed by an exponential part, which is denoted by `e` or `E`, followed by a literal integer indicating the exponent.
The exponential part indicates that the preceding value should be multiplied by 10 raised to the power of the exponent:

```sql
SELECT 1e2;           -- 100
SELECT 6.02214e23;    -- Avogadro's constant
SELECT 1e-10;         -- 1 ångström
```

## Underscores in Numeric Literals

DuckDB's SQL dialect allows using the underscore character `_` in numeric literals as an optional separator. The rules for using underscores are as follows:

* Underscores are allowed in integer, decimal, hexadecimal and binary notation.
* Underscores cannot be the first or last character in a literal.
* Underscores have to have an integer/numeric part on either side of them, i.e., there cannot be multiple underscores in a row and underscores cannot appear immediately before or after a decimal or exponent.

Examples:

```sql
SELECT 100_000_000;          -- 100000000
SELECT '0xFF_FF'::INTEGER;   -- 65535
SELECT 1_2.1_2E0_1;          -- 121.2
SELECT '0b0_1_0_1'::INTEGER; -- 5
```

## String Literals

String literals are delimited using single quotes (`'`, apostrophe) and result in `STRING_LITERAL` values.
Note that double quotes (`"`) cannot be used as string delimiter character: instead, double quotes are used to delimit [quoted identifiers]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#identifiers).

### Implicit String Literal Concatenation

Consecutive single-quoted string literals separated only by whitespace that contains at least one newline are implicitly concatenated:

```sql
SELECT 'Hello'
    ' '
    'World' AS greeting;
```

is equivalent to:

```sql
SELECT 'Hello'
    || ' '
    || 'World' AS greeting;
```

They both return the following result:

|  greeting   |
|-------------|
| Hello World |

Note that implicit concatenation only works if there is at least one newline between the literals. Using adjacent string literals separated by whitespace without a newline results in a syntax error:

```sql
SELECT 'Hello' ' ' 'World' AS greeting;
```

```console
Parser Error:
syntax error at or near "' '"

LINE 1: SELECT 'Hello' ' ' 'World' AS greeting;
                       ^
```

Also note that implicit concatenation only works with single-quoted string literals, and does not work with other kinds of string values.

### Implicit String Conversion

`STRING_LITERAL` instances can be implicitly converted to _any_ other type.

For example, we can compare string literals with dates:

```sql
SELECT d > '1992-01-01' AS result
FROM (VALUES (DATE '1992-01-01')) t(d);
```

| result |
|:-------|
| false  |

However, we cannot compare `VARCHAR` values with dates.

```sql
SELECT d > '1992-01-01'::VARCHAR
FROM (VALUES (DATE '1992-01-01')) t(d);
```

```console
Binder Error:
Cannot compare values of type DATE and type VARCHAR - an explicit cast is required
```

### Escape String Literals

To escape a single quote (apostrophe) character in a string literal, use `''`. For example, `SELECT '''' AS s` returns `'`.

To enable some common escape sequences, such as `\n` for the newline character, prefix a string literal with `e` (or `E`).

```sql
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

Even more, you can insert alphanumeric tags in the double-dollar symbols to allow for the use of regular double-dollar symbols *within* the string literal:

```sql
SELECT $tag$ this string can contain newlines,
'single quotes',
"double quotes",
and $$dollar quotes$$ $tag$ AS msg;
```

<!-- This output intentionally uses the duckbox formatter -->

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              msg                                               │
│                                            varchar                                             │
├────────────────────────────────────────────────────────────────────────────────────────────────┤
│  this string can contain newlines,\n'single quotes',\n"double quotes",\nand $$dollar quotes$$  │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

[Implicit concatenation](#implicit-string-literal-concatenation) only works for single-quoted string literals, not with dollar-quoted ones.
