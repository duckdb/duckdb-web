---
layout: docu
title: Lambda Functions
---

Lambda functions enable the use of more complex and flexible expressions in queries.
DuckDB supports several scalar functions that accept lambda functions as parameters
in the form `(parameter1, parameter2, ...) -> expression`.
If the lambda function has only one parameter, then the parentheses can be omitted.
The parameters can have any names.
For example, the following are all valid lambda functions:

- `param -> param > 1`
- `s -> contains(concat(s, 'DB'), 'duck')`
- `(x, y) -> x + y`

### Scalar Functions That Accept Lambda Functions

| Function | Aliases | Description | Example | Result |
|--|--|---|--|-|
| [`list_transform(`*`list`*`, `*`lambda`*`)`](#transform) | `array_transform`, `apply`, `list_apply`, `array_apply` | Returns a list that is the result of applying the lambda function to each element of the input list.                                       | `list_transform([4, 5, 6], x -> x + 1)`   | `[5, 6, 7]` |
| [`list_filter(`*`list`*`, `*`lambda`*`)`](#filter)      | `array_filter`, `filter`                                | Constructs a list from those elements of the input list for which the lambda function returns `true`.                                      | `list_filter([4, 5, 6], x -> x > 4)`      | `[5, 6]`    |
| [`list_reduce(`*`list`*`, `*`lambda`*`)`](#reduce)      | `array_reduce`, `reduce`                                | Reduces all elements of the input list into a single value by executing the lambda function on a running result and the next list element. | `list_reduce([4, 5, 6], (x, y) -> x + y)` | `15`        |

### Nesting

All scalar functions can be arbitrarily nested.

_Nested lambda functions to get all squares of even list elements:_
```sql
SELECT list_transform(
        list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0),
        y -> y * y
    );
```
```text
[0, 4, 16]
```
_Nested lambda function to add each element of the first list to the sum of the second list:_
```sql
SELECT list_transform(
        [1, 2, 3],
        x -> list_reduce([4, 5, 6], (a, b) -> a + b) + x
    );
```
```text
[16, 17, 18]
```

### Scoping

Lambda functions confirm to scoping rules in the following order:
- inner lambda parameters
- outer lambda parameters
- column names
- macro parameters

```sql
CREATE TABLE tbl (x INT);
INSERT INTO tbl VALUES (10);
SELECT apply([1, 2], x -> apply([4], x -> x + tbl.x)[1] + x) FROM tbl;
```
```text
[15, 16]
```

### Indexes as Parameters
All lambda functions accept an optional extra parameter that represents the index of the current element.
This is always the last parameter of the lambda function, and is 1-based (i.e., the first element has index 1).

_Get all elements that are larger than their index:_
```sql
SELECT list_filter([1, 3, 1, 5], (x, i) -> x > i);
```
```text
[3, 5]
```

## Transform

**Signature:** `list_transform(list, lambda)`

**Description:**  
`list_transform` returns a list that is the result of applying the lambda function to each element of the input list.

**Aliases:**  
- `array_transform`
- `apply`
- `list_apply`
- `array_apply`
 
**Number of parameters excluding indexes:** 1

**Return type:** Defined by the return type of the lambda function

**Examples:**  
_Incrementing each list element by one:_
```sql
SELECT list_transform([1, 2, NULL, 3], x -> x + 1);
```
```sql
[2, 3, NULL, 4]
```
_Transforming strings:_
```sql
SELECT list_transform(['duck', 'a', 'b'], s -> concat(s, 'DB'));
```
```sql
[duckDB, aDB, bDB]
```
_Combining lambda functions with other functions:_
```sql
SELECT list_transform([5, NULL, 6], x -> coalesce(x, 0) + 1);
```
```sql
[6, 1, 7]
```

## Filter

**Signature:** `list_filter(list, lambda)`

**Description:**  
Constructs a list from those elements of the input list for which the lambda function returns `true`.
DuckDB must be able to cast the lambda function's return type to `BOOL`.

**Aliases:**  
- `array_filter`
- `filter`

**Number of parameters excluding indexes:** 1

**Return type:** The same type as the input list

**Examples:**  
_Filter out negative values:_
```sql
SELECT list_filter([5, -6, NULL, 7], x -> x > 0);
```
```sql
[5, 7]
```
_Divisible by 2 and 5:_
```sql
SELECT list_filter(list_filter([2, 4, 3, 1, 20, 10, 3, 30], x -> x % 2 == 0), y -> y % 5 == 0);
```
```sql
[20, 10, 30]
```
_In combination with `range(...)` to construct lists:_
```sql
SELECT list_filter([1, 2, 3, 4], x -> x > #1) FROM range(4);
```
```sql
[1, 2, 3, 4]
[2, 3, 4]
[3, 4]
[4]
[]
```

## Reduce

**Signature:** `list_reduce(list, lambda)`

**Description:**  
The scalar function returns a single value
that is the result of applying the lambda function to each element of the input list.
Starting with the first element
and then repeatedly applying the lambda function to the result of the previous application and the next element of the list.
The list must have at least one element.

**Aliases:**  
- `array_reduce`
- `reduce`

**Number of parameters excluding indexes:** 2

**Return type:** The type of the input list's elements

**Examples:**  
_Sum of all list elements:_
```sql
SELECT list_reduce([1, 2, 3, 4], (x, y) -> x + y);
```
```sql
10
```
_Only add up list elements if they are greater than 2:_
```sql
SELECT list_reduce(list_filter([1, 2, 3, 4], x -> x > 2), (x, y) -> x + y);
```
```sql
7
```
_Concat all list elements:_
```sql
SELECT list_reduce(['DuckDB', 'is', 'awesome'], (x, y) -> concat(x, ' ', y));
```
```sql
DuckDB is awesome
```
