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
| [`list_transform(`*`list`*`, `*`lambda`*`)`](#transform) | `array_transform`, `apply`, `list_apply`, `array_apply` | Returns a list that is the result of applying the lambda function to each element of the input list.         | `list_transform([4, 5, 6], x -> x + 1)`   | `[5, 6, 7]` |
| [`list_filter(`*`list`*`, `*`lambda`*`)`](#filter)      | `array_filter`, `filter`                                | Constructs a list from those elements of the input list for which the lambda function returns true.          | `list_filter([4, 5, 6], x -> x > 4)`      | `[5, 6]`    |
| [`list_reduce(`*`list`*`, `*`lambda`*`)`](#reduce)      | `array_reduce`, `reduce`                                | Returns a single value that is the result of applying the lambda function to each element of the input list. | `list_reduce([4, 5, 6], (x, y) -> x + y)` | `15`        |

### Nesting

All scalar functions can be arbitrarily nested.

```sql
-- nested lambda functions to get all squares of even list elements
SELECT list_transform(list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0), y -> y * y);
----
[0, 4, 16]
```
```sql
-- nested lambda function to add each element of the first list to the sum
-- of the second list
SELECT list_transform([1, 2, 3], x -> list_reduce([4, 5, 6], (a, b) -> a + b + x));
----
[17, 19, 21]
```

### Indexes as Parameters
All lambda functions accept an optional extra parameter that represents the index of the current element.
This is always the last parameter of the lambda function, and is 1-based (i.e., the first element has index 1).

```sql
-- get all elements that are larger than their index
SELECT list_filter([1, 3, 1, 5], (x, i) -> x > i);
----
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
 
**Number of parameters (excluding indexes):** 1

**Return type:** Defined by the Return type of the lambda function

**Examples:**  
```sql
-- incrementing each list element by one
SELECT list_transform([1, 2, NULL, 3], x -> x + 1);
----
[2, 3, NULL, 4]
```
```sql
-- transforming strings
SELECT list_transform(['duck', 'a', 'b'], s -> concat(s, 'DB'));
----
[duckDB, aDB, bDB]
```
```sql
-- combining lambda functions with other functions
SELECT list_transform([5, NULL, 6], x -> coalesce(x, 0) + 1);
----
[6, 1, 7]
```

## Filter

**Signature:** `list_filter(list, lambda)`

**Description:**  
Constructs a list from those elements of the input list for which the lambda function returns true.
The lambda function must have the Return type of `BOOLEAN`.

**Aliases:**  
- `array_filter`
- `filter`

**Number of parameters (excluding indexes):** 1

**Return type:** The same type as the input list

**Examples:**  
```sql
-- filter out negative values
SELECT list_filter([5, -6, NULL, 7], x -> x > 0);
----
[5, 7]
```
```sql
-- divisible by 2 and 5
SELECT list_filter(list_filter([2, 4, 3, 1, 20, 10, 3, 30], x -> x % 2 == 0), y -> y % 5 == 0);
----
[20, 10, 30]
```
```sql
-- in combination with range(...) to construct lists
SELECT list_filter([1, 2, 3, 4], x -> x > #1) FROM range(4);
----
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

**Number of parameters (excluding indexes):** 2

**Return type:** The underlying list type

**Examples:**  
```sql
--- sum of all list elements
SELECT list_reduce([1, 2, 3, 4], (x, y) -> x + y);
----
10
```
```sql
--- only add up list elements if they are greater than 2
SELECT list_reduce(list_filter([1, 2, 3, 4], x -> x > 2), (x, y) -> x + y);
----
7
```
```sql
--- concat all list elements
SELECT list_reduce(['DuckDB', 'is', 'awesome'], (x, y) -> concat(x, ' ', y));
----
DuckDB is awesome
```
