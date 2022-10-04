---
layout: docu
title: Nested Functions
selected: Documentation/Functions/Nested Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating nested values. There are three nested data types: lists, structs, and maps.

## List Functions

In the descriptions, `l` is the three element list `[4, 5, 6]`.

<!-- This follows the order of shorthand, core/main function (list_), other list_ aliases, array_ aliases -->

| Function                                          | Description                                                                                                                                                                         | Example                                | Result       |
|:--------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------|:-------------|
| *`list`*`[`*`index`*`]`                           | Bracket notation serves as an alias for `list_extract`.                                                                                                                             | `l[3]`                                 | `6`          |
| `list_extract(`*`list`*`, `*`index`*`)`           | Extract the `index`th (1-based) value from the list.                                                                                                                                | `list_extract(l, 3)`                   | `6`          |
| `list_element(`*`list`*`, `*`index`*`)`           | Alias for `list_extract`.                                                                                                                                                           | `list_element(l, 3)`                   | `6`          |
| `array_extract(`*`list`*`, `*`index`*`)`          | Alias for `list_extract`.                                                                                                                                                           | `array_extract(l, 3)`                  | `6`          |
| *`list`*`[`*`begin`*`:`*`end`*`]`                 | Bracket notation with colon is an alias for `list_slice`. Missing arguments are interpreted as `NULL`s.                                                                             | `l[2:3]`                               | `[5, 6]`     |
| `list_slice(`*`list`*`, `*`begin`*`, `*`end`*`)`  | Extract a sublist using slice conventions. `NULL`s are interpreted as the bounds of the `LIST`. Negative values are accepted.                                                       | `list_slice(l, 2, NULL)`               | `[5, 6]`     |
| `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`)` | Alias for list_slice.                                                                                                                                                               | `array_slice(l, 2, NULL)`              | `[5, 6]`     |
| `array_pop_front(`*`list`*`)`                     | Returns the list without the first element.                                                                                                                                         | `array_pop_front(l)`                   | `[5, 6]`     |
| `array_pop_back(`*`list`*`)`                      | Returns the list without the last element.                                                                                                                                          | `array_pop_back(l)`                    | `[4, 5]`     |
| `list_value(`*`any`*`, ...)`                      | Create a `LIST` containing the argument values.                                                                                                                                     | `list_value(4, 5, 6)`                  | `[4, 5, 6]`  |
| `list_pack(`*`any`*`, ...)`                       | Alias for `list_value`.                                                                                                                                                             | `list_pack(4, 5, 6)`                   | `[4, 5, 6]`  |
| `len(`*`list`*`)`                                 | Return the length of the list.                                                                                                                                                      | `len([1, 2, 3])`                       | `3`          |
| `array_length(`*`list`*`)`                        | Alias for `len`.                                                                                                                                                                    | `array_length([1, 2, 3])`              | `3`          |
| `unnest(`*`list`*`)`                              | Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the [UNNEST page](/docs/sql/query_syntax/unnest) for more details. | `unnest([1, 2, 3])`                    | `1`, `2`, `3` |
| `list_concat(`*`list1`*`, `*`list2`*`)`           | Concatenates two lists.                                                                                                                                                             | `list_concat([2, 3], [4, 5, 6])`       | `[2, 3, 4, 5, 6]` |
| `list_cat(`*`list1`*`, `*`list2`*`)`              | Alias for `list_concat`.                                                                                                                                                            | `list_cat([2, 3], [4, 5, 6])`          | `[2, 3, 4, 5, 6`] |
| `array_concat(`*`list1`*`, `*`list2`*`)`          | Alias for `list_concat`.                                                                                                                                                            | `array_concat([2, 3], [4, 5, 6])`      | `[2, 3, 4, 5, 6`] |
| `array_cat(`*`list1`*`, `*`list2`*`)`             | Alias for `list_concat`.                                                                                                                                                            | `array_cat([2, 3], [4, 5, 6])`         | `[2, 3, 4, 5, 6`] |
| `list_prepend(`*`element`*`, `*`list`*`)`         | Prepends `element` to `list`.                                                                                                                                                       | `list_prepend(3, [4, 5, 6])`           | `[3, 4, 5, 6`] |
| `array_prepend(`*`element`*`, `*`list`*`)`        | Alias for `list_prepend`.                                                                                                                                                           | `array_prepend(3, [4, 5, 6])`          | `[3, 4, 5, 6`] |
| `array_push_front(`*`list`*`, `*`element`*`)`     | Alias for `list_prepend`.                                                                                                                                                           | `array_push_front(l, 3)`               | `[3, 4, 5,6]` |
| `list_append(`*`list`*`, `*`element`*`)`          | Appends `element` to `list`.                                                                                                                                                        | `list_append([2, 3], 4)`               | `[2, 3, 4`]  |
| `array_append(`*`list`*`, `*`element`*`)`         | Alias for `list_append`.                                                                                                                                                            | `array_append([2, 3], 4)`              | `[2, 3, 4`]  |
| `array_push_back(`*`list`*`, `*`element`*`)`      | Alias for `list_append`.                                                                                                                                                            | `array_push_back(l, 7)`                | `[4, 5, 6, 7]` |
| `list_contains(`*`list`*`, `*`element`*`)`        | Returns true if the list contains the element.                                                                                                                                      | `list_contains([1, 2, NULL], 1)`       | `true`       |
| `list_has(`*`list`*`, `*`element`*`)`             | Alias for `list_contains`.                                                                                                                                                          | `list_has([1, 2, NULL], 1)`            | `true`       |
| `array_contains(`*`list`*`, `*`element`*`)`       | Alias for `list_contains`.                                                                                                                                                          | `array_contains([1, 2, NULL], 1)`      | `true`       |
| `array_has(`*`list`*`, `*`element`*`)`            | Alias for `list_contains`.                                                                                                                                                          | `array_has([1, 2, NULL], 1)`           | `true`       |
| `list_position(`*`list`*`, `*`element`*`)`        | Returns the index of the element if the list contains the element.                                                                                                                  | `list_contains([1, 2, NULL], 2)`       | `2`          |
| `list_indexof(`*`list`*`, `*`element`*`)`         | Alias for `list_position`.                                                                                                                                                          | `list_indexof([1, 2, NULL], 2)`        | `2`          |
| `array_position(`*`list`*`, `*`element`*`)`       | Alias for `list_position`.                                                                                                                                                          | `array_position([1, 2, NULL], 2)`      | `2`          |
| `array_indexof(`*`list`*`, `*`element`*`)`        | Alias for `list_position`.                                                                                                                                                          | `array_indexof([1, 2, NULL], 2)`       | `2`          |
| `list_aggregate(`*`list`*`, `*`name`*`)`          | Executes the aggregate function `name` on the elements of `list`. See the [List Aggregates](nested#list-aggregates) section for more details.                                       | `list_aggregate([1, 2, NULL], 'min')`  | `1`          |
| `list_aggr(`*`list`*`, `*`name`*`)`               | Alias for `list_aggregate`.                                                                                                                                                         | `list_aggr([1, 2, NULL], 'min')`       | `1`          |
| `array_aggregate(`*`list`*`, `*`name`*`)`         | Alias for `list_aggregate`.                                                                                                                                                         | `array_aggregate([1, 2, NULL], 'min')` | `1`          |
| `array_aggr(`*`list`*`, `*`name`*`)`              | Alias for `list_aggregate`.                                                                                                                                                         | `array_aggr([1, 2, NULL], 'min')`      | `1`          |
| `list_sort(`*`list`*`)`                           | Sorts the elements of the list. See the [Sorting Lists](nested#sorting-lists) section for more details about the sorting order and the null sorting order.                          | `list_sort([3, 6, 1, 2])`              | `[1, 2, 3, 6]` |
| `array_sort(`*`list`*`)`                          | Alias for `list_sort`.                                                                                                                                                              | `array_sort([3, 6, 1, 2])`             | `[1, 2, 3, 6]` |
| `list_reverse_sort(`*`list`*`)`                   | Sorts the elements of the list in reverse order. See the [Sorting Lists](nested#sorting-lists) section for more details about the null sorting order.                               | `list_reverse_sort([3, 6, 1, 2])`      | `[6, 3, 2, 1]` |
| `array_reverse_sort(`*`list`*`)`                  | Alias for `list_reverse_sort`.                                                                                                                                                      | `array_reverse_sort([3, 6, 1, 2])`     | `[6, 3, 2, 1]` |
| `list_transform(`*`list`*`, `*`lambda`*`)`        | Returns a list that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions](nested#lambda-functions) section for more details.  | `list_transform(l, x -> x + 1)`        | `[5, 6, 7]`  |
| `array_transform(`*`list`*`, `*`lambda`*`)`       | Alias for `list_transform`.                                                                                                                                                         | `array_transform(l, x -> x + 1)`       | `[5, 6, 7]`  |
| `list_apply(`*`list`*`, `*`lambda`*`)`            | Alias for `list_transform`.                                                                                                                                                         | `list_apply(l, x -> x + 1)`            | `[5, 6, 7]`  |
| `array_apply(`*`list`*`, `*`lambda`*`)`           | Alias for `list_transform`.                                                                                                                                                         | `array_apply(l, x -> x + 1)`           | `[5, 6, 7]`  |
| `list_filter(`*`list`*`, `*`lambda`*`)`           | Constructs a list from those elements of the input list for which the lambda function returns true. See the [Lambda Functions](nested#lambda-functions) section for more details.   | `list_filter(l, x -> x > 4)`           | `[5, 6]`     |
| `array_filter(`*`list`*`, `*`lambda`*`)`          | Alias for `list_filter`.                                                                                                                                                            | `array_filter(l, x -> x > 4)`          | `[5, 6]`     |




## Struct Functions

| Function | Description                                                                                                                                                                                                                | Example | Result |
|:---|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---|:---|
| *`struct`*`.`*`entry`* | Dot notation serves as an alias for `struct_extract`.                                                                                                                                                                      | `({'i': 3, 's': 'string'}).s` | `string` |
| *`struct`*`[`*`entry`*`]` | Bracket notation serves as an alias for `struct_extract`.                                                                                                                                                                  | `({'i': 3, 's': 'string'})['s']` | `string` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct.                                                                                                                                                                                   | `struct_extract(s, 'i')` | `4` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name.                                                                                                                          | `struct_pack(i := 4, s := 'string')` | `{'i': 3, 's': 'string'}`|
| `struct_insert(`*`struct`*`, `*`name := any`*`, ...)` | Add field(s)/value(s) to an existing `STRUCT` with the argument values. The entry name(s) will be the bound variable name(s).                                                                                             | `struct_insert({'a': 1}, b := 2)`    | `{'a': 1, 'b': 2}`           |

## Map Functions

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `map[`*`entry`*`]` | Alias for `element_at` | `map([100, 5], ['a', 'b'])[100]` | `[a]` |
| `element_at(`*`map, key`*`)` | Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `element_at(map([100, 5], [42, 43]),100);` | `[42]` |
| `map_extract(`*`map, key`*`)` | Alias of `element_at`. Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `map_extract(map([100, 5], [42, 43]),100);` | `[42]` |
| `cardinality(`*`map`*`)` | Return the size of the map (or the number of entries in the map). | `cardinality( map([4, 2], ['a', 'b']) );` | `2` |
| `map()` | Returns an empty map. | `map()` | `{}` |

## Range Functions

The functions *`range`* and *`generate_series`* create a list of values in the range between `start` and `stop`.
The `start` parameter is inclusive.
For the `range` function, the `stop` parameter is exclusive, while for `generate_series`, it is inclusive.

Based on the number of arguments, the following variants exist:

* `range(`*`start`*`, `*`stop`*`, `*`step`*`)`
* `range(`*`start`*`, `*`stop`*`)`
* `range(`*`stop`*`)`
* `generate_series(`*`start`*`, `*`stop`*`, `*`step`*`)`
* `generate_series(`*`start`*`, `*`stop`*`)`
* `generate_series(`*`stop`*`)`

The default value of `start` is 0 and the default value of `step` is 1.

```sql
SELECT range(5);
-- [0, 1, 2, 3, 4]

SELECT range(2, 5);
-- [2, 3, 4]

SELECT range(2, 5, 3);
-- [2]

SELECT generate_series(5);
-- [0, 1, 2, 3, 4, 5]

SELECT generate_series(2, 5);
-- [2, 3, 4, 5]

SELECT generate_series(2, 5, 3);
-- [2, 5]
```

Date ranges are also supported:

```
SELECT * FROM range(date '1992-01-01', date '1992-03-01', interval '1' month);

┌─────────────────────┐
│        range        │
├─────────────────────┤
│ 1992-01-01 00:00:00 │
│ 1992-02-01 00:00:00 │
└─────────────────────┘
```

## List Aggregates

The function `list_aggregate` allows the execution of arbitrary existing aggregate functions on the elements of a list. Its first argument is the list (column), its second argument is the aggregate function name, e.g. `min`, `histogram` or `sum`.

```sql
SELECT list_aggregate([1, 2, -4, NULL], 'min');
-- -4

SELECT list_aggregate([2, 4, 8, 42], 'sum');
-- 56

SELECT list_aggregate([[1, 2], [NULL], [2, 10, 3]], 'last');
-- [2, 10, 3]
```

The following is a list of existing rewrites. Rewrites simplify the use of the list aggregate function by only taking the list (column) as their argument. `list_avg`, `list_var_samp`, `list_var_pop`, `list_stddev_pop`, `list_stddev_samp`, `list_sem`, `list_approx_count_distinct`, `list_bit_xor`, `list_bit_or`, `list_bit_and`, `list_bool_and`, `list_bool_or`, `list_count`, `list_entropy`, `list_last`, `list_first`, `list_kurtosis`, `list_min`, `list_max`, `list_product`, `list_skewness`, `list_sum`, `list_string_agg`, `list_mode`, `list_median`, `list_mad` and `list_histogram`.

```sql
SELECT list_min([1, 2, -4, NULL]);
-- -4

SELECT list_sum([2, 4, 8, 42]);
-- 56

SELECT list_last([[1, 2], [NULL], [2, 10, 3]]);
-- [2, 10, 3]
```

## Sorting Lists

The function `list_sort` sorts the elements of a list either in ascending or descending order. In addition, it allows to provide whether NULL values should be moved to the beginning or to the end of the list.

By default if no modifiers are provided, DuckDB sorts ASC NULLS FIRST, i.e. the values are sorted in ascending order and NULL values are placed first. This is identical to the default sort order of SQLite. The default sort order can be changed using [these](../query_syntax/orderby) PRAGMA statements.

`list_sort` leaves it open to the user whether they want to use the default sort order or a custom order. `list_sort` takes up to two additional optional parameters. The second parameter provides the sort order and can be either `ASC` or `DESC`. The third parameter provides the NULL sort order and can be either `NULLS FIRST` or `NULLS LAST`.

```sql
-- default sort order and default NULL sort order
SELECT list_sort([1, 3, NULL, 5, NULL, -5])
----
[NULL, NULL, -5, 1, 3, 5]

-- only providing the sort order
SELECT list_sort([1, 3, NULL, 2], 'ASC')
----
[NULL, 1, 2, 3]

-- providing the sort order and the NULL sort order
SELECT list_sort([1, 3, NULL, 2], 'DESC', 'NULLS FIRST')
----
[NULL, 3, 2, 1]
```

`list_reverse_sort` has an optional second parameter providing the NULL sort order. It can be either `NULLS FIRST` or `NULLS LAST`.

```sql
-- default NULL sort order
SELECT list_sort([1, 3, NULL, 5, NULL, -5])
----
[NULL, NULL, -5, 1, 3, 5]

-- providing the NULL sort order
SELECT list_reverse_sort([1, 3, NULL, 2], 'NULLS LAST')
----
[3, 2, 1, NULL]
```

## Lambda Functions

`(parameter1, parameter2, ...) -> expression`. If the lambda function has only one parameter, then the brackets can be omitted. The parameters can have any names.
```
param -> param > 1
duck -> CONTAINS(CONCAT(duck, 'DB'), 'duck')
(x, y) -> x + y
```

### Transform

`list_transform(list, lambda)`

Returns a list that is the result of applying the lambda function to each element of the input list. The lambda function must have exactly one left-hand side parameter. The return type of the lambda function defines the type of the list elements.

```sql
-- incrementing each list element by one
SELECT list_transform([1, 2, NULL, 3], x -> x + 1)
----
[2, 3, NULL, 4]

-- transforming strings
SELECT list_transform(['duck', 'a', 'b'], duck -> CONCAT(duck, 'DB'))
----
[duckDB, aDB, bDB]

-- combining lambda functions with other functions
SELECT list_transform([5, NULL, 6], x -> COALESCE(x, 0) + 1)
----
[6, 1, 7]
```

### Filter

`list_filter(list, lambda)`

Constructs a list from those elements of the input list for which the lambda function returns true. The lambda function must have exactly one left-hand side parameter and its return type must be of type `BOOLEAN`.

```sql
-- filter out negative values
SELECT list_filter([5, -6, NULL, 7], x -> x > 0)
----
[5, 7]

-- divisible by 2 and 5
SELECT list_filter(list_filter([2, 4, 3, 1, 20, 10, 3, 30], x -> x % 2 == 0), y -> y % 5 == 0)
----
[20, 10, 30]

-- in combination with range(...) to construct lists
SELECT list_filter([1, 2, 3, 4], x -> x > #1) FROM range(4)
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
SELECT list_transform(list_filter([0, 1, 2, 3, 4, 5], x -> x % 2 = 0), y -> y * y)
----
[0, 4, 16]
```


## `generate_subscripts`

The `generate_subscript(`*`arr`*`, `*`dim`*`)` function generates indexes along the `dim`th dimension of array `arr`.

```
SELECT generate_subscripts([4,5,6], 1) AS i;
┌───┐
│ i │
├───┤
│ 1 │
│ 2 │
│ 3 │
└───┘
```

## Related Functions

There are also [aggregate functions](/docs/sql/aggregates) `list` and `histogram` that produces lists and lists of structs.
[UNNEST](/docs/sql/query_syntax/unnest) is used to unnest a list by one level.
