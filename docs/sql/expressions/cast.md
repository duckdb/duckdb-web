---
layout: docu
title: Casting
railroad: expressions/cast.js
---

<div id="rrdiagram"></div>

Casting refers to the operation of converting a value in a particular data type to the corresponding value in another data type.
Casting can occur either implicitly or explicitly. The syntax described here performs an explicit cast. More information on casting can be found on the [typecasting page]({% link docs/sql/data_types/typecasting.md %}).

## Explicit Casting

The standard SQL syntax for explicit casting is `CAST(expr AS TYPENAME)`, where `TYPENAME` is a name (or alias) of one of [DuckDB's data types]({% link docs/sql/data_types/overview.md %}). DuckDB also supports the shorthand `expr::TYPENAME`, which is also present in PostgreSQL.

```sql
SELECT CAST(i AS VARCHAR) AS i FROM generate_series(1, 3) tbl(i);
```

| i |
|---|
| 1 |
| 2 |
| 3 |

```sql
SELECT i::DOUBLE AS i FROM generate_series(1, 3) tbl(i);
```

|  i  |
|----:|
| 1.0 |
| 2.0 |
| 3.0 |

### Casting Rules

Not all casts are possible. For example, it is not possible to convert an `INTEGER` to a `DATE`. Casts may also throw errors when the cast could not be successfully performed. For example, trying to cast the string `'hello'` to an `INTEGER` will result in an error being thrown.

```sql
SELECT CAST('hello' AS INTEGER);
```

```console
Conversion Error: Could not convert string 'hello' to INT32
```

The exact behavior of the cast depends on the source and destination types. For example, when casting from `VARCHAR` to any other type, the string will be attempted to be converted.

### `TRY_CAST`

`TRY_CAST` can be used when the preferred behavior is not to throw an error, but instead to return a `NULL` value. `TRY_CAST` will never throw an error, and will instead return `NULL` if a cast is not possible.

```sql
SELECT TRY_CAST('hello' AS INTEGER) AS i;
```

|  i   |
|------|
| NULL |
