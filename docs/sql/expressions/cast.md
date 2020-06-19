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
-- integers [1, 2, 3]
SELECT CAST(i AS VARCHAR), i::DOUBLE;
-- "1", "2", "3"
-- 1.0, 2.0, 3.0
```

The exact behavior of the cast depends on the source and destination types. For example, when casting from `VARCHAR` to any other type, the string will be attempted to be converted.

Not all casts are possible. For example, it is not possible to convert an `INTEGER` to a `DATE`. Casts may also throw errors when the cast could not be successfully performed. For example, trying trying to cast the string `'hello'` to an `INTEGER` will result in an error being thrown.

## Implicit Casting
In many situations, the system will add casts by itself. This is called *implicit* casting. This happens for example when a function is called with an argument that does not match the type of the function, but can be casted to the desired type.

Consider the function `SIN(DOUBLE)`. This function takes as input argument a column of type `DOUBLE`, however, it can be called with an integer as well: `SIN(1)`. If we look at the `EXPLAIN` output, we will see that the integer is converted into a double before being passed to the `SIN` function:

```sql
explain SELECT SIN(1);
-- logical_plan|PROJECTION[sin(CAST[DOUBLE](1))]
```

Generally, implicit casts only cast upwards. That is to say, we can implicitly cast an `INTEGER` to a `BIGINT`, but not the other way around.
