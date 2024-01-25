---
layout: docu
title: Nested Functions
---

This section describes functions and operators for examining and manipulating nested values. There are five nested data types: `ARRAY`, `LIST`, `MAP`, `STRUCT`, and `UNION`.

## List Functions

In the descriptions, `l` is the three element list `[4, 5, 6]`.

<!-- This follows the order of shorthand, core/main function (list_), other list_ aliases, array_ aliases -->

| Function | Aliases | Description | Example | Result |
|--|--|---|--|-|
| *`list`*`[`*`index`*`]`                                      |                                                           | Bracket notation serves as an alias for `list_extract`.                                                                                                                                          | `l[3]`                                                     | `6`                                                                                  |
| *`list`*`[`*`begin`*`:`*`end`*`]`                            |                                                           | Bracket notation with colon is an alias for `list_slice`.                                                                                                                                        | `l[2:3]`                                                   | `[5, 6]`                                                                             |
| *`list`*`[`*`begin`*`:`*`end`*`: `*`step`*`]`                |                                                           | `list_slice` in bracket notation with an added `step` feature.                                                                                                                                   | `l[:-:2]`                                                  | `[4, 6]`                                                                             |
| `array_pop_back(`*`list`*`)`                                 |                                                           | Returns the list without the last element.                                                                                                                                                       | `array_pop_back(l)`                                        | `[4, 5]`                                                                             |
| `array_pop_front(`*`list`*`)`                                |                                                           | Returns the list without the first element.                                                                                                                                                      | `array_pop_front(l)`                                       | `[5, 6]`                                                                             |
| `flatten(`*`list_of_lists`*`)`                               |                                                           | Concatenate a list of lists into a single list. This only flattens one level of the list (see [examples](nested#flatten)).                                                                       | `flatten([[1, 2], [3, 4]])`                                | `[1, 2, 3, 4]`                                                                       |
| `len(`*`list`*`)`                                            | `array_length`                                            | Return the length of the list.                                                                                                                                                                   | `len([1, 2, 3])`                                           | `3`                                                                                  |
| `list_aggregate(`*`list`*`, `*`name`*`)`                     | `list_aggr`, `aggregate`, `array_aggregate`, `array_aggr` | Executes the aggregate function `name` on the elements of `list`. See the [List Aggregates](nested#list-aggregates) section for more details.                                                    | `list_aggregate([1, 2, NULL], 'min')`                      | `1`                                                                                  |
| `list_any_value(`*`list`*`)`                                 |                                                           | Returns the first non-null value in the list                                                                                                                                                     | `list_any_value([NULL, -3])`                               | `-3`                                                                                 |
| `list_append(`*`list`*`, `*`element`*`)`                     | `array_append`, `array_push_back`                         | Appends `element` to `list`.                                                                                                                                                                     | `list_append([2, 3], 4)`                                   | `[2, 3, 4]`                                                                          |
| `list_concat(`*`list1`*`, `*`list2`*`)`                      | `list_cat`, `array_concat`, `array_cat`                   | Concatenates two lists.                                                                                                                                                                          | `list_concat([2, 3], [4, 5, 6])`                           | `[2, 3, 4, 5, 6]`                                                                    |
| `list_contains(`*`list`*`, `*`element`*`)`                   | `list_has`, `array_contains`, `array_has`                 | Returns true if the list contains the element.                                                                                                                                                   | `list_contains([1, 2, NULL], 1)`                           | `true`                                                                               |
| `list_cosine_similarity(`*`list1`*`, `*`list2`*`)`           |                                                           | Compute the cosine similarity between two lists                                                                                                                                                  | `list_cosine_similarity([1, 2, 3], [1, 2, 5])`             | `0.9759000729485332`                                                                 |
| `list_distance(`*`list1`*`, `*`list2`*`)`                    |                                                           | Calculates the Euclidean distance between two points with coordinates given in two inputs lists of equal length.                                                                                 | `list_distance([1, 2, 3], [1, 2, 5])`                      | `2.0`                                                                                |
| `list_distinct(`*`list`*`)`                                  | `array_distinct`                                          | Removes all duplicates and NULLs from a list. Does not preserve the original order.                                                                                                              | `list_distinct([1, 1, NULL, -3, 1, 5])`                    | `[1, 5, -3]`                                                                         |
| `list_dot_product(`*`list1`*`, `*`list2`*`)`                 | `list_inner_product`                                      | Computes the dot product of two same-sized lists of numbers.                                                                                                                                     | `list_dot_product([1, 2, 3], [1, 2, 5])`                   | `20.0`                                                                               |
| `list_extract(`*`list`*`, `*`index`*`)`                      | `list_element`, `array_extract`                           | Extract the `index`th (1-based) value from the list.                                                                                                                                             | `list_extract(l, 3)`                                       | `6`                                                                                  |
| `list_filter(`*`list`*`, `*`lambda`*`)`                      | `array_filter`, `filter`                                  | Constructs a list from those elements of the input list for which the lambda function returns true. See the [Lambda Functions](lambda#filter) page for more details.                        | `list_filter(l, x -> x > 4)`                               | `[5, 6]`                                                                             |
| `list_grade_up(`*`list`*`)`                                  | `array_grade_up`                                          | Works like sort, but the results are the indexes that correspond to the position in the original `list` instead of the actual values.                                                            | `list_grade_up([30, 10, 40, 20])`                          | `[2, 4, 1, 3]`                                                                       |
| `list_has_all(`*`list`*`, `*`sub-list`*`)`                   | `array_has_all`                                           | Returns true if all elements of sub-list exist in list.                                                                                                                                          | `list_has_all(l, [4, 6])`                                  | `true`                                                                               |
| `list_has_any(`*`list1`*`, `*`list2`*`)`                     | `array_has_any`                                           | Returns true if any elements exist is both lists.                                                                                                                                                | `list_has_any([1, 2, 3], [2, 3, 4])`                       | `true`                                                                               |
| `list_intersect(`*`list1`*`, `*`list2`*`)`                   | `array_intersect`                                         | Returns a list of all the elements that exist in both l1 and l2, without duplicates.                                                                                                             | `list_intersect([1, 2, 3], [2, 3, 4])`                     | `[2, 3]`                                                                             |
| `list_position(`*`list`*`, `*`element`*`)`                   | `list_indexof`, `array_position`, `array_indexof`         | Returns the index of the element if the list contains the element.                                                                                                                               | `list_contains([1, 2, NULL], 2)`                           | `2`                                                                                  |
| `list_prepend(`*`element`*`, `*`list`*`)`                    | `array_prepend`, `array_push_front`                       | Prepends `element` to `list`.                                                                                                                                                                    | `list_prepend(3, [4, 5, 6])`                               | `[3, 4, 5, 6]`                                                                       |
| `list_reduce(`*`list`*`, `*`lambda`*`)`                      | `array_reduce`, `reduce`                                  | Returns a single value that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions](lambda#reduce) page for more details.               | `list_reduce(l, (x, y) -> x + y)`                          | `15`                                                                                 |
| `list_resize(`*`list`*`, `*`size`*`[, `*`value`*`])`         | `array_resize`                                            | Resizes the list to contain `size` elements. Initializes new elements with `value` or `NULL` if `value` is not set.                                                                              | `list_resize([1, 2, 3], 5, 0)`                             | `[1, 2, 3, 0, 0]`                                                                    |
| `list_reverse_sort(`*`list`*`)`                              | `array_reverse_sort`                                      | Sorts the elements of the list in reverse order. See the [Sorting Lists](nested#sorting-lists) section for more details about the null sorting order.                                            | `list_reverse_sort([3, 6, 1, 2])`                          | `[6, 3, 2, 1]`                                                                       |
| `list_reverse(`*`list`*`)`                                   | `array_reverse`                                           | Reverses the list.                                                                                                                                                                               | `list_reverse(l)`                                          | `[6, 5, 4]`                                                                          |
| `list_select(`*`value_list`*`, `*`index_list`*`)`            | `array_select`                                            | Returns a list based on the elements selected by the `index_list`.                                                                                                                               | `list_select([10, 20, 30, 40], [1, 4])`                    | `[10, 40]`                                                                           |
| `list_slice(`*`list`*`, `*`begin`*`, `*`end`*`, `*`step`*`)` | `array_slice`                                             | `list_slice` with added `step` feature.                                                                                                                                                          | `list_slice(l, 1, 3, 2)`                                   | `[4, 6]`                                                                             |
| `list_slice(`*`list`*`, `*`begin`*`, `*`end`*`)`             | `array_slice`                                             | Extract a sublist using slice conventions. Negative values are accepted. See [slicing](nested#slicing).                                                                                          | `list_slice(l, 2, 3)`                                      | `[5, 6]`                                                                             |
| `list_sort(`*`list`*`)`                                      | `array_sort`                                              | Sorts the elements of the list. See the [Sorting Lists](nested#sorting-lists) section for more details about the sorting order and the null sorting order.                                       | `list_sort([3, 6, 1, 2])`                                  | `[1, 2, 3, 6]`                                                                       |
| `list_transform(`*`list`*`, `*`lambda`*`)`                   | `array_transform`, `apply`, `list_apply`, `array_apply`   | Returns a list that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions](lambda#transform) page for more details.                    | `list_transform(l, x -> x + 1)`                            | `[5, 6, 7]`                                                                          |
| `list_unique(`*`list`*`)`                                    | `array_unique`                                            | Counts the unique elements of a list.                                                                                                                                                            | `list_unique([1, 1, NULL, -3, 1, 5])`                      | `3`                                                                                  |
| `list_value(`*`any`*`, ...)`                                 | `list_pack`                                               | Create a `LIST` containing the argument values.                                                                                                                                                  | `list_value(4, 5, 6)`                                      | `[4, 5, 6]`                                                                          |
| `list_where(`*`value_list`*`, `*`mask_list`*`)`              | `array_where`                                             | Returns a list with the `BOOLEAN`s in `mask_list` applied as a mask to the `value_list`.                                                                                                         | `list_where([10, 20, 30, 40], [true, false, false, true])` | `[10, 40]`                                                                           |
| `list_zip(`*`list1`*`, `*`list2`*`, ...)`                    | `array_zip`                                               | Zips _k_ `LIST`s to a new `LIST` whose length will be that of the longest list. Its elements are structs of _k_ elements `list_1`, ..., `list_k`. Elements missing will be replaced with `NULL`. | `list_zip([1, 2], [3, 4], [5, 6])`                         | `[{'list_1': 1, 'list_2': 3, 'list_3': 5}, {'list_1': 2, 'list_2': 4, 'list_3': 6}]` |
| `unnest(`*`list`*`)`                                         |                                                           | Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the [`unnest` page](../query_syntax/unnest) for more details.                   | `unnest([1, 2, 3])`                                        | `1`, `2`, `3`                                                                        |

## List Operators

The following operators are supported for lists:

| Operator | Description | Example | Result |
|-|--|---|-|
| `&&`  | Alias for `list_intersect`                                                                | `[1, 2, 3, 4, 5] && [2, 5, 5, 6]` | `[2, 5]`             |
| `@>`  | Alias for `list_has_all`, where the list on the **right** of the operator is the sublist. | `[1, 2, 3, 4] @> [3, 4, 3]`       | `true`               |
| `<@`  | Alias for `list_has_all`, where the list on the **left** of the operator is the sublist.  | `[1, 4] <@ [1, 2, 3, 4]`          | `true`               |
| `||`  | Alias for `list_concat`                                                                   | `[1, 2, 3] || [4, 5, 6]`          | `[1, 2, 3, 4, 5, 6]` |
| `<=>` | Alias for `list_cosine_similarity`                                                        | `[1, 2, 3] <=> [1, 2, 5]`         | `0.9759000729485332` |
| `<->` | Alias for `list_distance`                                                                 | `[1, 2, 3] <-> [1, 2, 5]`         | `2.0`                |

## List Comprehension

Python-style list comprehension can be used to compute expressions over elements in a list. For example:

```sql
SELECT [lower(x) for x in strings] FROM (VALUES (['Hello', '', 'World'])) t(strings);
-- ['hello', '', 'world']
SELECT [upper(x) for x in strings if len(x) > 0] FROM (VALUES (['Hello', '', 'World'])) t(strings);
-- [HELLO, WORLD]
```

## Struct Functions

| Function | Description | Example | Result |
|:--|:---|:---|:--|
| *`struct`*`.`*`entry`* | Dot notation serves as an alias for `struct_extract`. | `({'i': 3, 's': 'string'}).s` | `string` |
| *`struct`*`[`*`entry`*`]` | Bracket notation serves as an alias for `struct_extract`. | `({'i': 3, 's': 'string'})['s']` | `string` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct. | `struct_extract({'i': 3, 'v2': 3, 'v3': 0}, 'i')` | `3` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 4, 's': string}` |
| `struct_insert(`*`struct`*`, `*`name := any`*`, ...)` | Add field(s)/value(s) to an existing `STRUCT` with the argument values. The entry name(s) will be the bound variable name(s). | `struct_insert({'a': 1}, b := 2)` | `{'a': 1, 'b': 2}` |

## Map Functions

| Function | Description | Example | Result |
|:--|:---|:---|:-|
| `map[`*`entry`*`]` | Alias for `element_at` | `map([100, 5], ['a', 'b'])[100]` | `[a]` |
| `element_at(`*`map, key`*`)` | Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `element_at(map([100, 5], [42, 43]), 100)` | `[42]` |
| `map_extract(`*`map, key`*`)` | Alias of `element_at`. Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `map_extract(map([100, 5], [42, 43]), 100)` | `[42]` |
| `cardinality(`*`map`*`)` | Return the size of the map (or the number of entries in the map). | `cardinality(map([4, 2], ['a', 'b']))` | `2` |
| `map_from_entries(`*`STRUCT(k, v)[]`*`)` | Returns a map created from the entries of the array | `map_from_entries([{k: 5, v: 'val1'}, {k: 3, v: 'val2'}])` | `{5=val1, 3=val2}` |
| `map()` | Returns an empty map. | `map()` | `{}` |
| `map_keys(`*`map`*`)` | Return a list of all keys in the map. | `map_keys(map([100, 5], [42, 43]))` | `[100, 5]` |
| `map_values(`*`map`*`)` | Return a list of all values in the map. | `map_values(map([100, 5], [42, 43]))` | `[42, 43]` |
| `map_entries(`*`map`*`)` | Return a list of struct(k, v) for each key-value pair in the map. | `map_entries(map([100, 5], [42, 43]))` | `[{'key': 100, 'value': 42}, {'key': 5, 'value': 43}]` |

## Union Functions

| Function | Description | Example | Result |
|:--|:---|:---|:-|
| *`union`*`.`*`tag`* | Dot notation serves as an alias for `union_extract`.| `(union_value(k := 'hello')).k` | `string` |
| `union_extract(`*`union`*`, `*`'tag'`*`)` | Extract the value with the named tags from the union. `NULL` if the tag is not currently selected | `union_extract(s, 'k')` | `hello` |
| `union_value(`*`tag := any`*`)` | Create a single member `UNION` containing the argument value. The tag of the value will be the bound variable name. | `union_value(k := 'hello')` | `'hello'::UNION(k VARCHAR)`| 
| `union_tag(`*`union`*`)` | Retrieve the currently selected tag of the union as an [Enum](../../sql/data_types/enum). | `union_tag(union_value(k := 'foo'))`  | `'k'` |

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

```sql
SELECT * FROM range(date '1992-01-01', date '1992-03-01', interval '1' month);
```

```text
┌─────────────────────┐
│        range        │
├─────────────────────┤
│ 1992-01-01 00:00:00 │
│ 1992-02-01 00:00:00 │
└─────────────────────┘
```

## Slicing

The function `list_slice` can be used to extract a sublist from a list.  The following variants exist:
* `list_slice(`*`list`*`, `*`begin`*`, `*`end`*`)`
* `list_slice(`*`list`*`, `*`begin`*`, `*`end`*`)`
* `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`, `*`step`*`)`
* `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`, `*`step`*`)`
* `list[`*`begin`*`:`*`end`*`]`
* `list[`*`begin`*`:`*`end`*`:`*`step`*`]`

**`list`**
* Is the list to be sliced

**`begin`**
* Is the index of the first element to be included in the slice
* When `begin < 0` the index is counted from the end of the list
* When `begin < 0` and `-begin > length`, `begin` is clamped to the beginning of the list
* When `begin > length`, the result is an empty list
* **Bracket Notation:** When `begin` is omitted, it defaults to the beginning of the list

**`end`**
* Is the index of the last element to be included in the slice
* When `end < 0` the index is counted from the end of the list
* When `end > length`, end is clamped to `length`
* When `end < begin`, the result is an empty list
* **Bracket Notation:** When `end` is omitted, it defaults to the end of the list. When `end` is omitted and a `step` is provided, `end` must be replaced with a `-`

**`step`** *(optional)*
* Is the step size between elements in the slice
* When `step < 0` the slice is reversed, and `begin` and `end` are swapped
* Must be non-zero

```sql
SELECT list_slice([1, 2, 3, 4, 5], 2, 4);
-- [2, 3, 4]

SELECT ([1, 2, 3, 4, 5])[2:4:2];
-- [2, 4]

SELECT([1, 2, 3, 4, 5])[4:2:-2];
-- [4, 2]

SELECT ([1, 2, 3, 4, 5])[:];
-- [1, 2, 3, 4, 5]

SELECT ([1, 2, 3, 4, 5])[:-:2];
-- [1, 3, 5]

SELECT ([1, 2, 3, 4, 5])[:-:-2];
-- [5, 3, 1]
```

## List Aggregates

The function `list_aggregate` allows the execution of arbitrary existing aggregate functions on the elements of a list. Its first argument is the list (column), its second argument is the aggregate function name, e.g., `min`, `histogram` or `sum`.

`list_aggregate` accepts additional arguments after the aggregate function name. These extra arguments are passed directly to the aggregate function, which serves as the second argument of `list_aggregate`.

```sql
SELECT list_aggregate([1, 2, -4, NULL], 'min');
-- -4

SELECT list_aggregate([2, 4, 8, 42], 'sum');
-- 56

SELECT list_aggregate([[1, 2], [NULL], [2, 10, 3]], 'last');
-- [2, 10, 3]

SELECT list_aggregate([2, 4, 8, 42], 'string_agg', '|');
-- 2|4|8|42
```

The following is a list of existing rewrites. Rewrites simplify the use of the list aggregate function by only taking the list (column) as their argument. `list_avg`, `list_var_samp`, `list_var_pop`, `list_stddev_pop`, `list_stddev_samp`, `list_sem`, `list_approx_count_distinct`, `list_bit_xor`, `list_bit_or`, `list_bit_and`, `list_bool_and`, `list_bool_or`, `list_count`, `list_entropy`, `list_last`, `list_first`, `list_kurtosis`, `list_kurtosis_pop`, `list_min`, `list_max`, `list_product`, `list_skewness`, `list_sum`, `list_string_agg`, `list_mode`, `list_median`, `list_mad` and `list_histogram`.

```sql
SELECT list_min([1, 2, -4, NULL]);
-- -4

SELECT list_sum([2, 4, 8, 42]);
-- 56

SELECT list_last([[1, 2], [NULL], [2, 10, 3]]);
-- [2, 10, 3]
```

### array_to_string

Concatenates list/array elements using an optional delimiter.

```sql
SELECT array_to_string([1, 2, 3], '-') AS str;
-- 1-2-3

-- this is equivalent to the following SQL
SELECT list_aggr([1, 2, 3], 'string_agg', '-') AS str;
-- 1-2-3
```

## Sorting Lists

The function `list_sort` sorts the elements of a list either in ascending or descending order. In addition, it allows to provide whether NULL values should be moved to the beginning or to the end of the list.

By default if no modifiers are provided, DuckDB sorts ASC NULLS FIRST, i.e., the values are sorted in ascending order and NULL values are placed first. This is identical to the default sort order of SQLite. The default sort order can be changed using [these](../query_syntax/orderby) PRAGMA statements.

`list_sort` leaves it open to the user whether they want to use the default sort order or a custom order. `list_sort` takes up to two additional optional parameters. The second parameter provides the sort order and can be either `ASC` or `DESC`. The third parameter provides the NULL sort order and can be either `NULLS FIRST` or `NULLS LAST`.

```sql
-- default sort order and default NULL sort order
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
----
[NULL, NULL, -5, 1, 3, 5]

-- only providing the sort order
SELECT list_sort([1, 3, NULL, 2], 'ASC');
----
[NULL, 1, 2, 3]

-- providing the sort order and the NULL sort order
SELECT list_sort([1, 3, NULL, 2], 'DESC', 'NULLS FIRST');
----
[NULL, 3, 2, 1]
```

`list_reverse_sort` has an optional second parameter providing the NULL sort order. It can be either `NULLS FIRST` or `NULLS LAST`.

```sql
-- default NULL sort order
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
----
[NULL, NULL, -5, 1, 3, 5]

-- providing the NULL sort order
SELECT list_reverse_sort([1, 3, NULL, 2], 'NULLS LAST');
----
[3, 2, 1, NULL]
```

## Lambda Functions

DuckDB supports lambda functions in the form `(parameter1, parameter2, ...) -> expression`.
For details, see the [lambda functions page](lambda).

## Flatten

The flatten function is a scalar function that converts a list of lists into a single list by concatenating each sub-list together.
Note that this only flattens one level at a time, not all levels of sub-lists. 
```sql
-- Convert a list of lists into a single list
SELECT 
    flatten([
        [1, 2],
        [3, 4]
    ]);
----
[1, 2, 3, 4]

-- If the list has multiple levels of lists, 
-- only the first level of sub-lists is concatenated into a single list
SELECT 
    flatten([
        [
            [1, 2],
            [3, 4],
        ],
        [
            [5, 6],
            [7, 8],
        ]
    ]);
----
[[1, 2], [3, 4], [5, 6], [7, 8]] 
```

In general, the input to the flatten function should be a list of lists (not a single level list). 
However, the behavior of the flatten function has specific behavior when handling empty lists and `NULL` values.
```sql
-- If the input list is empty, return an empty list
SELECT flatten([]);
----
[]

-- If the entire input to flatten is NULL, return NULL
SELECT flatten(NULL);
----
NULL

-- If a list whose only entry is NULL is flattened, return an empty list
SELECT flatten([NULL]);
----
[]

-- If the sub-list in a list of lists only contains NULL, 
-- do not modify the sub-list
-- (Note the extra set of parentheses vs. the prior example)
SELECT flatten([[NULL]]);
----
[NULL]

-- Even if the only contents of each sub-list is NULL,
-- still concatenate them together
-- Note that no de-duplication occurs when flattening. 
-- See list_distinct function for de-duplication.
SELECT flatten([[NULL],[NULL]]);
----
[NULL, NULL]
```

## `generate_subscripts`

The `generate_subscript(`*`arr`*`, `*`dim`*`)` function generates indexes along the `dim`th dimension of array `arr`.

```sql
SELECT generate_subscripts([4, 5, 6], 1) AS i;
```

```text
┌───┐
│ i │
├───┤
│ 1 │
│ 2 │
│ 3 │
└───┘
```

## Related Functions

There are also [aggregate functions](../aggregates) `list` and `histogram` that produces lists and lists of structs.
The [`unnest`](../query_syntax/unnest) function is used to unnest a list by one level.
