---
layout: docu
title: Casting
selected: Documentation/Expressions/Casting
expanded: Expressions
railroad: expressions/cast.js
---
<div id="rrdiagram"></div>

Casting refers to the process of changing the type of a row from one type to another. The standard SQL syntax for this is `CAST(expr AS typename)`. DuckDB also supports the easier to type shorthand `expr::typename`, which is also present in PostgreSQL.

```sql
SELECT CAST(i AS VARCHAR) FROM generate_series(1, 3) tbl(i);
-- "1", "2", "3"
SELECT i::DOUBLE FROM generate_series(1, 3) tbl(i);
-- 1.0, 2.0, 3.0

SELECT CAST('hello' AS INTEGER);
-- Conversion Error: Could not convert string 'hello' to INT32
SELECT TRY_CAST('hello' AS INTEGER);
-- NULL
```

The exact behavior of the cast depends on the source and destination types. For example, when casting from `VARCHAR` to any other type, the string will be attempted to be converted.

Not all casts are possible. For example, it is not possible to convert an `INTEGER` to a `DATE`. Casts may also throw errors when the cast could not be successfully performed. For example, trying trying to cast the string `'hello'` to an `INTEGER` will result in an error being thrown.

`TRY_CAST` can be used when the preferred behavior is not to throw an error, but instead to return a `NULL` value. `TRY_CAST` will never throw an error, and will instead return `NULL` if a cast is not possible.

## Implicit Casting
In many situations, the system will add casts by itself. This is called *implicit* casting. This happens for example when a function is called with an argument that does not match the type of the function, but can be casted to the desired type.

Consider the function `SIN(DOUBLE)`. This function takes as input argument a column of type `DOUBLE`, however, it can be called with an integer as well: `SIN(1)`. The integer is converted into a double before being passed to the `SIN` function.

Generally, implicit casts only cast upwards. That is to say, we can implicitly cast an `INTEGER` to a `BIGINT`, but not the other way around.
