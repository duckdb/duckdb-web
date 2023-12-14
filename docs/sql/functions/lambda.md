---
layout: docu
title: Lambda Functions
---

DuckDB supports lambda functions in the form `(parameter1, parameter2, ...) -> expression`. If the lambda function has only one parameter, then the brackets can be omitted. The parameters can have any names.

```sql
param -> param > 1
duck -> contains(concat(duck, 'DB'), 'duck')
(x, y) -> x + y
```

## Transform

The `list_transform` function has the following signature:

```sql
list_transform(list, lambda)
```

It returns a list that is the result of applying the lambda function to each element of the input list. The lambda function must have exactly one left-hand side parameter. The return type of the lambda function defines the type of the list elements.

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

The `list_filter` function has the following signature:

```sql
list_filter(list, lambda)
```

It constructs a list from those elements of the input list for which the lambda function returns true. The lambda function must have exactly one left-hand side parameter and its return type must be of type `BOOLEAN`.

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

Lambda functions can be arbitrarily nested.

```sql
-- nested lambda functions to get all squares of even list elements
SELECT list_transform(list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0), y -> y * y);
----
[0, 4, 16]
```
