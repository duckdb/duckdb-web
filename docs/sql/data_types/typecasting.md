---
layout: docu
title: Typecasting
---

Typecasting is an operation that converts a value in one particular data type to the closest corresponding value in another data type.
Like other SQL engines, DuckDB supports both [implicit](../expressions/cast#implicit-casting) and [explicit typecasting](../expressions/cast#explicit-casting).

The following matrix describes which conversions are supported.
When implicit casting is allowed, it implies that explicit casting is also possible.

![Typecasting matrix](/images/typecasting-matrix.png)

Even though a casting operation is supported based on the source and target data type, it does not necessarily mean the cast operation will succeeed at runtime.

Casting operations that result in loss of precision are typically allowed. For example, it is possible to cast a numeric type with fractional digits like `DECIMAL`, `FLOAT` or `DOUBLE` to an integral type like `INTEGER`:

```sql
SELECT cast(pi() AS INTEGER);
```

Casting operations that would result in a value overflow are typically not allowed. For example, the value `999` is too large to be represented by the `TINYINT` data type. Therefore, an attempt to cast that value to that type results in a runtime error:

```sql
SELECT CAST(999 AS TINYINT);
```

So even though the cast operation from `INTEGER` to `TINYINT` is supported, it is not possible for this particular value. 
  
The [`VARCHAR`](text) type (also available under the aliases `TEXT` and `STRING`) acts like an univeral target: any arbitrary value of any arbitrary type can always be cast to the `VARCHAR` type.
Casting from `VARCHAR` to another data type is generally supported, but may fail at runtime if DuckDB cannot figure out how to parse and convert the provided value to the target data type.
