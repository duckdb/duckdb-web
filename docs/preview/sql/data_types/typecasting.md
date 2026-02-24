---
layout: docu
title: Typecasting
---

Typecasting is an operation that converts a value in one particular data type to the closest corresponding value in another data type.
Like other SQL engines, DuckDB supports both implicit and explicit typecasting.

## Explicit Casting

Explicit typecasting is performed by using a `CAST` expression. For example, `CAST(col AS VARCHAR)` or `col::VARCHAR` explicitly cast the column `col` to `VARCHAR`. See the [cast page]({% link docs/preview/sql/expressions/cast.md %}) for more information.

## Implicit Casting

In many situations, the system will add casts by itself. This is called *implicit* casting and happens, for example, when a function is called with an argument that does not match the type of the function but can be cast to the required type.

Implicit casts can only be added for a number of type combinations, and is generally only possible when the cast cannot fail. For example, an implicit cast can be added from `INTEGER` to `DOUBLE` – but not from `DOUBLE` to `INTEGER`.

Consider the function `sin(DOUBLE)`. This function takes as input argument a column of type `DOUBLE`, however, it can be called with an integer as well: `sin(1)`. The integer is converted into a double before being passed to the `sin` function.

> Tip To check whether a type can be implicitly cast to another type, use the [`can_cast_implicitly` function]({% link docs/preview/sql/functions/utility.md %}#can_cast_implicitlysource_value-target_value).

### Combination Casting

When values of different types need to be combined to an unspecified joint parent type, the system will perform implicit casts to an automatically selected parent type. For example, `list_value(1::INT64, 1::UINT64)` creates a list of type `INT128[]`. The implicit casts performed in this situation are sometimes more lenient than regular implicit casts. For example, a `BOOL` value may be cast to `INT` (with `true` mapping to `1` and `false` to `0`) even though this is not possible for regular implicit casts.

This *combination casting* occurs for comparisons (`=` / `<` / `>`), set operations (`UNION` / `EXCEPT` / `INTERSECT`), and nested type constructors (`list_value` / `[...]` / `MAP`).

## Casting Operations Matrix

Values of a particular data type cannot always be cast to any arbitrary target data type. The only exception is the `NULL` value – which can always be converted between types.
The following matrix describes which conversions are supported.
When implicit casting is allowed, it implies that explicit casting is also possible.

![Typecasting matrix](/images/typecasting-matrix.png)

Even though a casting operation is supported based on the source and target data type, it does not necessarily mean the cast operation will succeed at runtime.

> Deprecated Prior to version 0.10.0, DuckDB allowed any type to be implicitly cast to `VARCHAR` during function binding.
> Version 0.10.0 introduced a [breaking change which no longer allows implicit casts to `VARCHAR`]({% post_url 2024-02-13-announcing-duckdb-0100 %}#breaking-sql-changes).
> The [`old_implicit_casting` configuration option]({% link docs/preview/configuration/pragmas.md %}#implicit-casting-to-varchar) setting can be used to revert to the old behavior.
> However, please note that this flag will be deprecated in the future.

### Lossy Casts

Casting operations that result in loss of precision are allowed. For example, it is possible to explicitly cast a numeric type with fractional digits – such as `DECIMAL`, `FLOAT` or `DOUBLE` – to an integral type like `INTEGER` or `BIGINT`. The number will be rounded.

```sql
SELECT CAST(3.1 AS INTEGER);  -- 3
SELECT CAST(3.5 AS INTEGER);  -- 4
SELECT CAST(-1.7 AS INTEGER); -- -2
```

### Overflows

Casting operations that would result in a value overflow throw an error. For example, the value `999` is too large to be represented by the `TINYINT` data type. Therefore, an attempt to cast that value to that type results in a runtime error:

```sql
SELECT CAST(999 AS TINYINT);
```

```console
Conversion Error:
Type INT32 with value 999 can't be cast because the value is out of range for the destination type INT8
```

So even though the cast operation from `INTEGER` to `TINYINT` is supported, it is not possible for this particular value. [TRY_CAST]({% link docs/preview/sql/expressions/cast.md %}) can be used to convert the value into `NULL` instead of throwing an error.

### Varchar

The [`VARCHAR`]({% link docs/preview/sql/data_types/text.md %}) type acts as a universal target: any arbitrary value of any arbitrary type can always be cast to the `VARCHAR` type. This type is also used for displaying values in the shell.

```sql
SELECT CAST(42.5 AS VARCHAR);
```

Casting from `VARCHAR` to another data type is supported, but can raise an error at runtime if DuckDB cannot parse and convert the provided text to the target data type.

```sql
SELECT CAST('NotANumber' AS INTEGER);
```

In general, casting to `VARCHAR` is a lossless operation and any type can be cast back to the original type after being converted into text.

```sql
SELECT CAST(CAST([1, 2, 3] AS VARCHAR) AS INTEGER[]);
```

### Literal Types

Integer literals (such as `42`) and string literals (such as `'string'`) have special implicit casting rules. See the [literal types page]({% link docs/preview/sql/data_types/literal_types.md %}) for more information.

### Lists / Arrays

Lists can be explicitly cast to other lists using the same casting rules. The cast is applied to the children of the list. For example, if we convert an `INTEGER[]` list to a `VARCHAR[]` list, the child `INTEGER` elements are individually cast to `VARCHAR` and a new list is constructed.

```sql
SELECT CAST([1, 2, 3] AS VARCHAR[]);
```

### Arrays

Arrays follow the same casting rules as lists. In addition, arrays can be implicitly cast to lists of the same type. For example, an `INTEGER[3]` array can be implicitly cast to an `INTEGER[]` list.

### Structs

Structs can be cast to other structs as long as they share at least one field.

> The rationale behind this requirement is to help avoid unintended errors. If two structs do not have any fields in common, then the cast was likely not intended.

```sql
SELECT CAST({'a': 42} AS STRUCT(a VARCHAR));
```

Fields that exist in the target struct, but that do not exist in the source struct, default to `NULL`.

```sql
SELECT CAST({'a': 42} AS STRUCT(a VARCHAR, b VARCHAR));
```

Fields that only exist in the source struct are ignored.

```sql
SELECT CAST({'a': 42, 'b': 43} AS STRUCT(a VARCHAR));
```

The names of the struct can also be in a different order. The fields of the struct will be reshuffled based on the names of the structs.

```sql
SELECT CAST({'a': 42, 'b': 84} AS STRUCT(b VARCHAR, a VARCHAR));
```

For [combination casting]({% link docs/preview/sql/data_types/typecasting.md %}#combination-casting), the fields of the resulting struct are the superset of all fields of the input structs.
This logic also applies recursively to potentially nested structs.

```sql
SELECT {'outer1': {'inner1': 42, 'inner2': 42}} AS c
UNION
SELECT {'outer1': {'inner2': 'hello', 'inner3': 'world'}, 'outer2': '100'} AS c;
```

```sql
SELECT [{'a': 42}, {'b': 84}];
```

### Unions

Union casting rules can be found on the [`UNION type page`]({% link docs/preview/sql/data_types/union.md %}#casting-to-unions).
