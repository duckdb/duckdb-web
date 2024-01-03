---
layout: docu
title: Lambda Functions
---

DuckDB supports lambda functions in the form `(parameter1, parameter2, ...) -> expression`. If the lambda function has only one parameter, then the brackets can be omitted. The parameters can have any names.  For example, the following are all valid lambda functions:
- `param -> param > 1`
- `duck -> contains(concat(duck, 'DB'), 'duck')`
- `(x, y) -> x + y`

### Functions That Accept Lambda Functions

| Function                                                | Aliases                                                 | Description                                                                                                  | Example                                   | Result      |
|---------------------------------------------------------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------|-------------|
| [`list_transform(`*`list`*`, `*`lambda`*`)`](#tranform) | `array_transform`, `apply`, `list_apply`, `array_apply` | Returns a list that is the result of applying the lambda function to each element of the input list.         | `list_transform([4, 5, 6], x -> x + 1)`   | `[5, 6, 7]` |
| [`list_filter(`*`list`*`, `*`lambda`*`)`](#filter)      | `array_filter`, `filter`                                | Constructs a list from those elements of the input list for which the lambda function returns true.          | `list_filter([4, 5, 6], x -> x > 4)`      | `[5, 6]`    |
| [`list_reduce(`*`list`*`, `*`lambda`*`)`](#reduce)      | `array_reduce`, `reduce`                                | Returns a single value that is the result of applying the lambda function to each element of the input list. | `list_reduce([4, 5, 6], (x, y) -> x + y)` | `15`        |


### Nesting Lambda Functions
All lambda functions can be arbitrarily nested.

```sql
-- nested lambda functions to get all squares of even list elements
SELECT list_transform(list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0), y -> y * y);
----
[0, 4, 16]

-- nested lambda function to add each element of the first list to the sum of the second list
SELECT list_transform([1, 2, 3], x -> list_reduce([4, 5, 6], (a, b) -> a + b + x));
----
[17, 19, 21]
```

### Indexes As Parameters
All lambda functions accept an optional extra parameter that represents the index of the current element.
This is always the last parameter of the lambda function, and is 1-based (i.e., the first element has index 1).

```sql
-- get all elements that are larger than their index
SELECT list_filter([1, 3, 1, 5], (x, i) -> x > i);
----
[3, 5]
```

## Transform

**Signature:**<br>
`list_transform(list, lambda)`

**Description:**<br>
`list_transform` returns a list that is the result of applying the lambda function to each element of the input list.

**Aliases:**<br>
- `array_transform`,
- `apply`
- `list_apply`
- `array_apply`
 
**Number of Parameters (excluding indexes):**<br>
1

**Return Type:**<br>
Defined by the return type of the lambda function

**Examples:**<br>
```sql
-- incrementing each list element by one
SELECT list_transform([1, 2, NULL, 3], x -> x + 1);
----
[2, 3, NULL, 4]

-- transforming strings
SELECT list_transform(['duck', 'a', 'b'], duck -> concat(duck, 'DB'));
----
[duckDB, aDB, bDB]

-- combining lambda functions with other functions
SELECT list_transform([5, NULL, 6], x -> coalesce(x, 0) + 1);
----
[6, 1, 7]
```

## Filter

**Signature:**<br>
`list_filter(list, lambda)`

**Description:**<br>
Constructs a list from those elements of the input list for which the lambda function returns true.
The lambda function must have the return type of `BOOLEAN`.

**Aliases:**<br>
- `array_filter`
- `filter`

**Number of Parameters (excluding indexes):**<br>
1

**Return Type:**<br>
The same type as the input list

#### Examples:
```sql
-- filter out negative values
SELECT list_filter([5, -6, NULL, 7], x -> x > 0);
----
[5, 7]

-- divisible by 2 and 5
SELECT list_filter(list_filter([2, 4, 3, 1, 20, 10, 3, 30], x -> x % 2 == 0), y -> y % 5 == 0);
----
[20, 10, 30]

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

**Signature:**<br>
`list_reduce(list, lambda)`

**Description:**<br>
The function returns a single value
that is the result of applying the lambda function to each element of the input list.
Starting with the first element
and then repeatedly applying the lambda function to the result of the previous application and the next element of the list.
The list must have at least one element.

**Aliases:**<br>
- `array_reduce`
- `reduce`

**Number of Parameters (excluding indexes):**<br>
2

**Return Type:**<br>
The underlying list type

**Examples:**<br>
```sql
--- sum of all list elements
SELECT list_reduce([1, 2, 3, 4], (x, y) -> x + y);
----
10

--- only add up list elements if they are greater than 2
SELECT list_reduce(list_filter([1, 2, 3, 4], x -> x > 2), (x, y) -> x + y);
----
7

--- concat all list elements
SELECT list_reduce(['DuckDB', 'is', 'awesome'], (x, y) -> concat(x, ' ', y));
----
DuckDB is awesome
```
