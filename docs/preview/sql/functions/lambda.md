---
layout: docu
title: Lambda Functions
---

Lambda functions enable the use of more complex and flexible expressions in queries.
DuckDB supports several scalar functions that operate on [`LIST`s]({% link docs/preview/sql/data_types/list.md %}) and
accept lambda functions as parameters
in the form `(parameter1, parameter2, ...) -> expression`.
If the lambda function has only one parameter, then the parentheses can be omitted.
The parameters can have any names.
For example, the following are all valid lambda functions:

* `param -> param > 1`
* `s -> contains(concat(s, 'DB'), 'duck')`
* `(acc, x) -> acc + x`

## Scalar Functions That Accept Lambda Functions

| Name | Description |
|:--|:-------|
| [`list_transform(list, lambda(x))`](#list_transformlist-lambda) | Returns a list that is the result of applying the lambda function to each element of the input list. The return type is defined by the return type of the lambda function. See [`list_transform` examples](#list_transform-examples). |
| [`list_filter(list, lambda(x))`](#list_filterlist-lambda) | Constructs a list from those elements of the input list for which the lambda function returns `true`. DuckDB must be able to cast the lambda function's return type to `BOOL`. The return type of `list_filter` is the same as the input list's. See [`list_filter` examples](#list_filter-examples). |
| [`list_reduce(list, lambda(x, y)`](#list_reducelist-lambda) | Reduces all elements of the input list into a single scalar value by executing the lambda function on a running result and the next list element. The list must have at least one element – the use of an initial accumulator value is currently not supported. See [`list_reduce` examples](#list_reduce-examples). |

### `list_transform(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Returns a list that is the result of applying the lambda function to each element of the input list. The return type is defined by the return type of the lambda function. See [`list_transform` examples](#list_transform-examples). |
| **Example** | `list_transform([4, 5, 6], x -> x + 1)` |
| **Result** | `[5, 6, 7]` |
| **Aliases** | `array_transform`, `apply`, `list_apply`, `array_apply` |

### `list_filter(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Constructs a list from those elements of the input list for which the lambda function returns `true`. DuckDB must be able to cast the lambda function's return type to `BOOL`. The return type of `list_filter` is the same as the input list's. See [`list_filter` examples](#list_filter-examples). |
| **Example** | `list_filter([4, 5, 6], x -> x > 4)` |
| **Result** | `[5, 6]` |
| **Aliases** | `array_filter`, `filter` |

### `list_reduce(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Reduces all elements of the input list into a single scalar value by executing the lambda function on a running result and the next list element. The list must have at least one element – the use of an initial accumulator value is currently not supported. See [`list_reduce` examples](#list_reduce-examples). |
| **Example** | `list_reduce([4, 5, 6], (acc, x) -> acc + x)` |
| **Result** | `15` |
| **Aliases** | `array_reduce`, `reduce` |

## Nesting Lambda Functions

All scalar functions can be arbitrarily nested. For example, nested lambda functions to get all squares of even list elements:

```sql
SELECT list_transform(
        list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0),
        y -> y * y
    );
```

```text
[0, 4, 16]
```

Nested lambda function to add each element of the first list to the sum of the second list:

```sql
SELECT list_transform(
        [1, 2, 3],
        x -> list_reduce([4, 5, 6], (a, b) -> a + b) + x
    );
```

```text
[16, 17, 18]
```

## Scoping

Lambda functions confirm to scoping rules in the following order:

* inner lambda parameters
* outer lambda parameters
* column names
* macro parameters

```sql
CREATE TABLE tbl (x INTEGER);
INSERT INTO tbl VALUES (10);
SELECT apply([1, 2], x -> apply([4], x -> x + tbl.x)[1] + x) FROM tbl;
```

```text
[15, 16]
```

## Indexes as Parameters

All lambda functions accept an optional extra parameter that represents the index of the current element.
This is always the last parameter of the lambda function (e.g., `i` in `(x, i)`), and is 1-based (i.e., the first element has index 1).

Get all elements that are larger than their index:

```sql
SELECT list_filter([1, 3, 1, 5], (x, i) -> x > i);
```

```text
[3, 5]
```

## Examples

### `list_transform` Examples

Incrementing each list element by one:

```sql
SELECT list_transform([1, 2, NULL, 3], x -> x + 1);
```

```text
[2, 3, NULL, 4]
```

Transforming strings:

```sql
SELECT list_transform(['Duck', 'Goose', 'Sparrow'], s -> concat(s, 'DB'));
```

```text
[DuckDB, GooseDB, SparrowDB]
```

Combining lambda functions with other functions:

```sql
SELECT list_transform([5, NULL, 6], x -> coalesce(x, 0) + 1);
```

```text
[6, 1, 7]
```

### `list_filter` Examples

Filter out negative values:

```sql
SELECT list_filter([5, -6, NULL, 7], x -> x > 0);
```

```text
[5, 7]
```

Divisible by 2 and 5:

```sql
SELECT list_filter(
        list_filter([2, 4, 3, 1, 20, 10, 3, 30], x -> x % 2 = 0),
        y -> y % 5 = 0
    );
```

```text
[20, 10, 30]
```

In combination with `range(...)` to construct lists:

```sql
SELECT list_filter([1, 2, 3, 4], x -> x > #1) FROM range(4);
```

```text
[1, 2, 3, 4]
[2, 3, 4]
[3, 4]
[4]
[]
```

### `list_reduce` Examples

Sum of all list elements:

```sql
SELECT list_reduce([1, 2, 3, 4], (acc, x) -> acc + x);
```

```text
10
```

Only add up list elements if they are greater than 2:

```sql
SELECT list_reduce(list_filter([1, 2, 3, 4], x -> x > 2), (acc, x) -> acc + x);
```

```text
7
```

Concat all list elements:

```sql
SELECT list_reduce(['DuckDB', 'is', 'awesome'], (acc, x) -> concat(acc, ' ', x));
```

```text
DuckDB is awesome
```

## Limitations

Subqueries in lambda expressions are not supported. For example:

```sql
SELECT list_apply([1, 2, 3], x -> (SELECT 42) + x);
```

```console
Binder Error:
subqueries in lambda expressions are not supported
```
