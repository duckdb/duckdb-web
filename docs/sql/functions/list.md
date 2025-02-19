---
layout: docu
title: List Functions
---

<!-- markdownlint-disable MD001 MD056 -->

| Name | Description |
|:--|:-------|
| [`list[index]`](#listindex) | Bracket notation serves as an alias for `list_extract`. |
| [`list[begin:end]`](#listbeginend) | Bracket notation with colon is an alias for `list_slice`. |
| [`list[begin:end:step]`](#listbeginendstep) | `list_slice` in bracket notation with an added `step` feature. |
| [`array_pop_back(list)`](#array_pop_backlist) | Returns the list without the last element. |
| [`array_pop_front(list)`](#array_pop_frontlist) | Returns the list without the first element. |
| [`flatten(list_of_lists)`](#flattenlist_of_lists) | Concatenate a list of lists into a single list. This only flattens one level of the list (see [examples](#flattening)). |
| [`len(list)`](#lenlist) | Return the length of the list. |
| [`list_aggregate(list, name)`](#list_aggregatelist-name) | Executes the aggregate function `name` on the elements of `list`. See the [List Aggregates]({% link docs/sql/functions/list.md %}#list-aggregates) section for more details. |
| [`list_any_value(list)`](#list_any_valuelist) | Returns the first non-null value in the list. |
| [`list_append(list, element)`](#list_appendlist-element) | Appends `element` to `list`. |
| [`list_concat(list1, list2)`](#list_concatlist1-list2) | Concatenate two lists. NULL inputs are skipped. See also `||` |
| [`list_contains(list, element)`](#list_containslist-element) | Returns true if the list contains the element. |
| [`list_cosine_similarity(list1, list2)`](#list_cosine_similaritylist1-list2) | Compute the cosine similarity between two lists. |
| [`list_cosine_distance(list1, list2)`](#list_cosine_distancelist1-list2) | Compute the cosine distance between two lists. Equivalent to `1.0 - list_cosine_similarity`. |
| [`list_distance(list1, list2)`](#list_distancelist1-list2) | Calculates the Euclidean distance between two points with coordinates given in two inputs lists of equal length. |
| [`list_distinct(list)`](#list_distinctlist) | Removes all duplicates and `NULL` values from a list. Does not preserve the original order. |
| [`list_dot_product(list1, list2)`](#list_dot_productlist1-list2) | Computes the dot product of two same-sized lists of numbers. |
| [`list_negative_dot_product(list1, list2)`](#list_negative_dot_productlist1-list2) | Computes the negative dot product of two same-sized lists of numbers. Equivalent to `- list_dot_product`. |
| [`list_extract(list, index)`](#list_extractlist-index) | Extract the `index`th (1-based) value from the list. |
| [`list_filter(list, lambda)`](#list_filterlist-lambda) | Constructs a list from those elements of the input list for which the lambda function returns true. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#filter) page for more details. |
| [`list_grade_up(list)`](#list_grade_uplist) | Works like sort, but the results are the indexes that correspond to the position in the original `list` instead of the actual values. |
| [`list_has_all(list, sub-list)`](#list_has_alllist-sub-list) | Returns true if all elements of sub-list exist in list. |
| [`list_has_any(list1, list2)`](#list_has_anylist1-list2) | Returns true if any elements exist is both lists. |
| [`list_intersect(list1, list2)`](#list_intersectlist1-list2) | Returns a list of all the elements that exist in both `l1` and `l2`, without duplicates. |
| [`list_position(list, element)`](#list_positionlist-element) | Returns the index of the element if the list contains the element. If the element is not found, it returns `NULL`. |
| [`list_prepend(element, list)`](#list_prependelement-list) | Prepends `element` to `list`. |
| [`list_reduce(list, lambda)`](#list_reducelist-lambda) | Returns a single value that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#reduce) page for more details. |
| [`list_resize(list, size[, value])`](#list_resizelist-size-value) | Resizes the list to contain `size` elements. Initializes new elements with `value` or `NULL` if `value` is not set. |
| [`list_reverse_sort(list)`](#list_reverse_sortlist) | Sorts the elements of the list in reverse order. See the [Sorting Lists]({% link docs/sql/functions/list.md %}#sorting-lists) section for more details about the `NULL` sorting order. |
| [`list_reverse(list)`](#list_reverselist) | Reverses the list. |
| [`list_select(value_list, index_list)`](#list_selectvalue_list-index_list) | Returns a list based on the elements selected by the `index_list`. |
| [`list_slice(list, begin, end, step)`](#list_slicelist-begin-end-step) | `list_slice` with added `step` feature. |
| [`list_slice(list, begin, end)`](#list_slicelist-begin-end) | Extract a sublist using slice conventions. Negative values are accepted. See [slicing]({% link docs/sql/functions/list.md %}#slicing). |
| [`list_sort(list)`](#list_sortlist) | Sorts the elements of the list. See the [Sorting Lists]({% link docs/sql/functions/list.md %}#sorting-lists) section for more details about the sorting order and the `NULL` sorting order. |
| [`list_transform(list, lambda)`](#list_transformlist-lambda) | Returns a list that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#transform) page for more details. |
| [`list_unique(list)`](#list_uniquelist) | Counts the unique elements of a list. |
| [`list_value(any, ...)`](#list_valueany-) | Create a `LIST` containing the argument values. |
| [`list_where(value_list, mask_list)`](#list_wherevalue_list-mask_list) | Returns a list with the `BOOLEAN`s in `mask_list` applied as a mask to the `value_list`. |
| [`list_zip(list_1, list_2, ...[, truncate])`](#list_ziplist1-list2-) | Zips _k_ `LIST`s to a new `LIST` whose length will be that of the longest list. Its elements are structs of _k_ elements from each list `list_1`, ..., `list_k`, missing elements are replaced with `NULL`. If `truncate` is set, all lists are truncated to the smallest list length. |
| [`unnest(list)`](#unnestlist) | Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the [`unnest` page]({% link docs/sql/query_syntax/unnest.md %}) for more details. |

#### `list[index]`

<div class="nostroke_table"></div>

| **Description** | Bracket notation serves as an alias for `list_extract`. |
| **Example** | `[4, 5, 6][3]` |
| **Result** | `6` |
| **Alias** | `list_extract` |

#### `list[begin:end]`

<div class="nostroke_table"></div>

| **Description** | Bracket notation with colon is an alias for `list_slice`. |
| **Example** | `[4, 5, 6][2:3]` |
| **Result** | `[5, 6]` |
| **Alias** | `list_slice` |

#### `list[begin:end:step]`

<div class="nostroke_table"></div>

| **Description** | `list_slice` in bracket notation with an added `step` feature. |
| **Example** | `[4, 5, 6][:-:2]` |
| **Result** | `[4, 6]` |
| **Alias** | `list_slice` |

#### `array_pop_back(list)`

<div class="nostroke_table"></div>

| **Description** | Returns the list without the last element. |
| **Example** | `array_pop_back([4, 5, 6])` |
| **Result** | `[4, 5]` |

#### `array_pop_front(list)`

<div class="nostroke_table"></div>

| **Description** | Returns the list without the first element. |
| **Example** | `array_pop_front([4, 5, 6])` |
| **Result** | `[5, 6]` |

#### `flatten(list_of_lists)`

<div class="nostroke_table"></div>

| **Description** | Concatenate a list of lists into a single list. This only flattens one level of the list (see [examples](#flattening)). |
| **Example** | `flatten([[1, 2], [3, 4]])` |
| **Result** | `[1, 2, 3, 4]` |

#### `len(list)`

<div class="nostroke_table"></div>

| **Description** | Return the length of the list. |
| **Example** | `len([1, 2, 3])` |
| **Result** | `3` |
| **Alias** | `array_length` |

#### `list_aggregate(list, name)`

<div class="nostroke_table"></div>

| **Description** | Executes the aggregate function `name` on the elements of `list`. See the [List Aggregates]({% link docs/sql/functions/list.md %}#list-aggregates) section for more details. |
| **Example** | `list_aggregate([1, 2, NULL], 'min')` |
| **Result** | `1` |
| **Aliases** | `list_aggr`, `aggregate`, `array_aggregate`, `array_aggr` |

#### `list_any_value(list)`

<div class="nostroke_table"></div>

| **Description** | Returns the first non-null value in the list. |
| **Example** | `list_any_value([NULL, -3])` |
| **Result** | `-3` |

#### `list_append(list, element)`

<div class="nostroke_table"></div>

| **Description** | Appends `element` to `list`. |
| **Example** | `list_append([2, 3], 4)` |
| **Result** | `[2, 3, 4]` |
| **Aliases** | `array_append`, `array_push_back` |

#### `list_concat(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Concatenate two lists. `NULL` inputs are skipped. See also `||`  |
| **Example** | `list_concat([2, 3], [4, 5, 6])` |
| **Result** | `[2, 3, 4, 5, 6]` |
| **Aliases** | `list_cat`, `array_concat`, `array_cat` |

#### `list_contains(list, element)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the list contains the element. |
| **Example** | `list_contains([1, 2, NULL], 1)` |
| **Result** | `true` |
| **Aliases** | `list_has`, `array_contains`, `array_has` |

#### `list_cosine_similarity(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Compute the cosine similarity between two lists. |
| **Example** | `list_cosine_similarity([1, 2, 3], [1, 2, 5])` |
| **Result** | `0.9759000729485332` |

#### `list_cosine_distance(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Compute the cosine distance between two lists. Equivalent to `1.0 - list_cosine_similarity` |
| **Example** | `list_cosine_distance([1, 2, 3], [1, 2, 5])` |
| **Result** | `0.024099927051466796` |

#### `list_distance(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Calculates the Euclidean distance between two points with coordinates given in two inputs lists of equal length. |
| **Example** | `list_distance([1, 2, 3], [1, 2, 5])` |
| **Result** | `2.0` |

#### `list_distinct(list)`

<div class="nostroke_table"></div>

| **Description** | Removes all duplicates and `NULL` values from a list. Does not preserve the original order. |
| **Example** | `list_distinct([1, 1, NULL, -3, 1, 5])` |
| **Result** | `[1, 5, -3]` |
| **Alias** | `array_distinct` |

#### `list_dot_product(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Computes the dot product of two same-sized lists of numbers. |
| **Example** | `list_dot_product([1, 2, 3], [1, 2, 5])` |
| **Result** | `20.0` |
| **Alias** | `list_inner_product` |

#### `list_negative_dot_product(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Computes the negative dot product of two same-sized lists of numbers. Equivalent to `- list_dot_product` |
| **Example** | `list_negative_dot_product([1, 2, 3], [1, 2, 5])` |
| **Result** | `-20.0` |
| **Alias** | `list_negative_inner_product` |

#### `list_extract(list, index)`

<div class="nostroke_table"></div>

| **Description** | Extract the `index`th (1-based) value from the list. |
| **Example** | `list_extract([4, 5, 6], 3)` |
| **Result** | `6` |
| **Aliases** | `list_element`, `array_extract` |

#### `list_filter(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Constructs a list from those elements of the input list for which the lambda function returns true. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#filter) page for more details. |
| **Example** | `list_filter([4, 5, 6], x -> x > 4)` |
| **Result** | `[5, 6]` |
| **Aliases** | `array_filter`, `filter` |

#### `list_grade_up(list)`

<div class="nostroke_table"></div>

| **Description** | Works like sort, but the results are the indexes that correspond to the position in the original `list` instead of the actual values. |
| **Example** | `list_grade_up([30, 10, 40, 20])` |
| **Result** | `[2, 4, 1, 3]` |
| **Alias** | `array_grade_up` |

#### `list_has_all(list, sub-list)`

<div class="nostroke_table"></div>

| **Description** | Returns true if all elements of sub-list exist in list. |
| **Example** | `list_has_all([4, 5, 6], [4, 6])` |
| **Result** | `true` |
| **Alias** | `array_has_all` |

#### `list_has_any(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Returns true if any elements exist is both lists. |
| **Example** | `list_has_any([1, 2, 3], [2, 3, 4])` |
| **Result** | `true` |
| **Alias** | `array_has_any` |

#### `list_intersect(list1, list2)`

<div class="nostroke_table"></div>

| **Description** | Returns a list of all the elements that exist in both `l1` and `l2`, without duplicates. |
| **Example** | `list_intersect([1, 2, 3], [2, 3, 4])` |
| **Result** | `[2, 3]` |
| **Alias** | `array_intersect` |

#### `list_position(list, element)`

<div class="nostroke_table"></div>

| **Description** | Returns the index of the element if the list contains the element. If the element is not found, it returns `NULL`. |
| **Example** | `list_position([1, 2, NULL], 2)` |
| **Result** | `2` |
| **Aliases** | `list_indexof`, `array_position`, `array_indexof` |

#### `list_prepend(element, list)`

<div class="nostroke_table"></div>

| **Description** | Prepends `element` to `list`. |
| **Example** | `list_prepend(3, [4, 5, 6])` |
| **Result** | `[3, 4, 5, 6]` |
| **Aliases** | `array_prepend`, `array_push_front` |

#### `list_reduce(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Returns a single value that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#reduce) page for more details. |
| **Example** | `list_reduce([4, 5, 6], (acc, x) -> acc + x)` |
| **Result** | `15` |
| **Aliases** | `array_reduce`, `reduce` |

#### `list_resize(list, size[, value])`

<div class="nostroke_table"></div>

| **Description** | Resizes the list to contain `size` elements. Initializes new elements with `value` or `NULL` if `value` is not set. |
| **Example** | `list_resize([1, 2, 3], 5, 0)` |
| **Result** | `[1, 2, 3, 0, 0]` |
| **Alias** | `array_resize` |

#### `list_reverse_sort(list)`

<div class="nostroke_table"></div>

| **Description** | Sorts the elements of the list in reverse order. See the [Sorting Lists]({% link docs/sql/functions/list.md %}#sorting-lists) section for more details about the `NULL` sorting order. |
| **Example** | `list_reverse_sort([3, 6, 1, 2])` |
| **Result** | `[6, 3, 2, 1]` |
| **Alias** | `array_reverse_sort` |

#### `list_reverse(list)`

<div class="nostroke_table"></div>

| **Description** | Reverses the list. |
| **Example** | `list_reverse([3, 6, 1, 2])` |
| **Result** | `[2, 1, 6, 3]` |
| **Alias** | `array_reverse` |

#### `list_select(value_list, index_list)`

<div class="nostroke_table"></div>

| **Description** | Returns a list based on the elements selected by the `index_list`. |
| **Example** | `list_select([10, 20, 30, 40], [1, 4])` |
| **Result** | `[10, 40]` |
| **Alias** | `array_select` |

#### `list_slice(list, begin, end, step)`

<div class="nostroke_table"></div>

| **Description** | `list_slice` with added `step` feature. |
| **Example** | `list_slice([4, 5, 6], 1, 3, 2)` |
| **Result** | `[4, 6]` |
| **Alias** | `array_slice` |

#### `list_slice(list, begin, end)`

<div class="nostroke_table"></div>

| **Description** | Extract a sublist using slice conventions. Negative values are accepted. See [slicing]({% link docs/sql/functions/list.md %}#slicing). |
| **Example** | `list_slice([4, 5, 6], 2, 3)` |
| **Result** | `[5, 6]` |
| **Alias** | `array_slice` |

#### `list_sort(list)`

<div class="nostroke_table"></div>

| **Description** | Sorts the elements of the list. See the [Sorting Lists]({% link docs/sql/functions/list.md %}#sorting-lists) section for more details about the sorting order and the `NULL` sorting order. |
| **Example** | `list_sort([3, 6, 1, 2])` |
| **Result** | `[1, 2, 3, 6]` |
| **Alias** | `array_sort` |

#### `list_transform(list, lambda)`

<div class="nostroke_table"></div>

| **Description** | Returns a list that is the result of applying the lambda function to each element of the input list. See the [Lambda Functions]({% link docs/sql/functions/lambda.md %}#transform) page for more details. |
| **Example** | `list_transform([4, 5, 6], x -> x + 1)` |
| **Result** | `[5, 6, 7]` |
| **Aliases** | `array_transform`, `apply`, `list_apply`, `array_apply` |

#### `list_unique(list)`

<div class="nostroke_table"></div>

| **Description** | Counts the unique elements of a list. |
| **Example** | `list_unique([1, 1, NULL, -3, 1, 5])` |
| **Result** | `3` |
| **Alias** | `array_unique` |

#### `list_value(any, ...)`

<div class="nostroke_table"></div>

| **Description** | Create a `LIST` containing the argument values. |
| **Example** | `list_value(4, 5, 6)` |
| **Result** | `[4, 5, 6]` |
| **Alias** | `list_pack` |

#### `list_where(value_list, mask_list)`

<div class="nostroke_table"></div>

| **Description** | Returns a list with the `BOOLEAN`s in `mask_list` applied as a mask to the `value_list`. |
| **Example** | `list_where([10, 20, 30, 40], [true, false, false, true])` |
| **Result** | `[10, 40]` |
| **Alias** | `array_where` |

#### `list_zip(list1, list2, ...)`

<div class="nostroke_table"></div>

| **Description** | Zips _k_ `LIST`s to a new `LIST` whose length will be that of the longest list. Its elements are structs of _k_ elements from each list `list_1`, ..., `list_k`, missing elements are replaced with `NULL`. If `truncate` is set, all lists are truncated to the smallest list length. |
| **Example** | `list_zip([1, 2], [3, 4], [5, 6])` |
| **Result** | `[(1, 3, 5), (2, 4, 6)]` |
| **Alias** | `array_zip` |

#### `unnest(list)`

<div class="nostroke_table"></div>

| **Description** | Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the [`unnest` page]({% link docs/sql/query_syntax/unnest.md %}) for more details. |
| **Example** | `unnest([1, 2, 3])` |
| **Result** | `1`, `2`, `3` |

## List Operators

The following operators are supported for lists:

<!-- markdownlint-disable MD056 -->

| Operator | Description | Example | Result |
|-|--|---|-|
| `&&`  | Alias for [`list_has_any`](#list_has_anylist1-list2).                                                                   | `[1, 2, 3, 4, 5] && [2, 5, 5, 6]` | `true`               |
| `@>`  | Alias for [`list_has_all`](#list_has_alllist-sub-list), where the list on the **right** of the operator is the sublist. | `[1, 2, 3, 4] @> [3, 4, 3]`       | `true`               |
| `<@`  | Alias for [`list_has_all`](#list_has_alllist-sub-list), where the list on the **left** of the operator is the sublist.  | `[1, 4] <@ [1, 2, 3, 4]`          | `true`               |
| `||`  | Similar to [`list_concat`](#list_concatlist1-list2), except any `NULL` input results in `NULL`.                         | `[1, 2, 3] || [4, 5, 6]`          | `[1, 2, 3, 4, 5, 6]` |
| `<=>` | Alias for [`list_cosine_distance`](#list_cosine_distancelist1-list2).                                                   | `[1, 2, 3] <=> [1, 2, 5]`         | `0.007416606`        |
| `<->` | Alias for [`list_distance`](#list_distancelist1-list2).                                                                 | `[1, 2, 3] <-> [1, 2, 5]`         | `2.0`                |

<!-- markdownlint-enable MD056 -->

## List Comprehension

Python-style list comprehension can be used to compute expressions over elements in a list. For example:

```sql
SELECT [lower(x) FOR x IN strings] AS strings
FROM (VALUES (['Hello', '', 'World'])) t(strings);
```

<div class="monospace_table"></div>

|     strings      |
|------------------|
| [hello, , world] |

```sql
SELECT [upper(x) FOR x IN strings IF len(x) > 0] AS strings
FROM (VALUES (['Hello', '', 'World'])) t(strings);
```

<div class="monospace_table"></div>

|    strings     |
|----------------|
| [HELLO, WORLD] |

List comprehensions can also use the position of the list elements by adding a second variable.
In the following example, we use `x, i`, where `x` is the value and `i` is the position:

```sql
SELECT [4, 5, 6] AS l, [x FOR x, i IN l IF i != 2] AS filtered;
```

<div class="monospace_table"></div>

|     l     | filtered |
|-----------|----------|
| [4, 5, 6] | [4, 6]   |

Under the hood, `[f(x) FOR x IN y IF g(x)]` is translated to `list_transform(list_filter(y, x -> f(x)), x -> f(x))`.

## Range Functions

DuckDB offers two range functions, [`range(start, stop, step)`](#range) and [`generate_series(start, stop, step)`](#generate_series), and their variants with default arguments for `stop` and `step`. The two functions' behavior is different regarding their `stop` argument. This is documented below.

### `range`

The `range` function creates a list of values in the range between `start` and `stop`.
The `start` parameter is inclusive, while the `stop` parameter is exclusive.
The default value of `start` is 0 and the default value of `step` is 1.

Based on the number of arguments, the following variants of `range` exist.

#### `range(stop)`

```sql
SELECT range(5);
```

```text
[0, 1, 2, 3, 4]
```

#### `range(start, stop)`

```sql
SELECT range(2, 5);
```

```text
[2, 3, 4]
```

#### `range(start, stop, step)`

```sql
SELECT range(2, 5, 3);
```

```text
[2]
```

### `generate_series`

The `generate_series` function creates a list of values in the range between `start` and `stop`.
Both the `start` and the `stop` parameters are inclusive.
The default value of `start` is 0 and the default value of `step` is 1.
Based on the number of arguments, the following variants of `generate_series` exist.

#### `generate_series(stop)`

```sql
SELECT generate_series(5);
```

```text
[0, 1, 2, 3, 4, 5]
```

#### `generate_series(start, stop)`

```sql
SELECT generate_series(2, 5);
```

```text
[2, 3, 4, 5]
```

#### `generate_series(start, stop, step)`

```sql
SELECT generate_series(2, 5, 3);
```

```text
[2, 5]
```

#### `generate_subscripts(arr, dim)`

The `generate_subscripts(arr, dim)` function generates indexes along the `dim`th dimension of array `arr`.

```sql
SELECT generate_subscripts([4, 5, 6], 1) AS i;
```

| i |
|--:|
| 1 |
| 2 |
| 3 |

### Date Ranges

Date ranges are also supported for `TIMESTAMP` and `TIMESTAMP WITH TIME ZONE` values.
Note that for these types, the `stop` and `step` arguments have to be specified explicitly (a default value is not provided).

#### `range` for Date Ranges

```sql
SELECT *
FROM range(DATE '1992-01-01', DATE '1992-03-01', INTERVAL '1' MONTH);
```

|        range        |
|---------------------|
| 1992-01-01 00:00:00 |
| 1992-02-01 00:00:00 |

#### `generate_series` for Date Ranges

```sql
SELECT *
FROM generate_series(DATE '1992-01-01', DATE '1992-03-01', INTERVAL '1' MONTH);
```

|   generate_series   |
|---------------------|
| 1992-01-01 00:00:00 |
| 1992-02-01 00:00:00 |
| 1992-03-01 00:00:00 |

## Slicing

The function [`list_slice`](#list_slicelist-begin-end) can be used to extract a sublist from a list. The following variants exist:

* `list_slice(list, begin, end)`
* `list_slice(list, begin, end, step)`
* `array_slice(list, begin, end)`
* `array_slice(list, begin, end, step)`
* `list[begin:end]`
* `list[begin:end:step]`

The arguments are as follows:

* `list`
    * Is the list to be sliced
* `begin`
    * Is the index of the first element to be included in the slice
    * When `begin < 0` the index is counted from the end of the list
    * When `begin < 0` and `-begin > length`, `begin` is clamped to the beginning of the list
    * When `begin > length`, the result is an empty list
    * **Bracket Notation:** When `begin` is omitted, it defaults to the beginning of the list
* `end`
    * Is the index of the last element to be included in the slice
    * When `end < 0` the index is counted from the end of the list
    * When `end > length`, end is clamped to `length`
    * When `end < begin`, the result is an empty list
    * **Bracket Notation:** When `end` is omitted, it defaults to the end of the list. When `end` is omitted and a `step` is provided, `end` must be replaced with a `-`
* `step` *(optional)*
    * Is the step size between elements in the slice
    * When `step < 0` the slice is reversed, and `begin` and `end` are swapped
    * Must be non-zero

Examples:

```sql
SELECT list_slice([1, 2, 3, 4, 5], 2, 4);
```

```text
[2, 3, 4]
```

```sql
SELECT ([1, 2, 3, 4, 5])[2:4:2];
```

```text
[2, 4]
```

```sql
SELECT([1, 2, 3, 4, 5])[4:2:-2];
```

```text
[4, 2]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:];
```

```text
[1, 2, 3, 4, 5]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:-:2];
```

```text
[1, 3, 5]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:-:-2];
```

```text
[5, 3, 1]
```

## List Aggregates

The function [`list_aggregate`](#list_aggregatelist-name) allows the execution of arbitrary existing aggregate functions on the elements of a list. Its first argument is the list (column), its second argument is the aggregate function name, e.g., `min`, `histogram` or `sum`.

`list_aggregate` accepts additional arguments after the aggregate function name. These extra arguments are passed directly to the aggregate function, which serves as the second argument of `list_aggregate`.

```sql
SELECT list_aggregate([1, 2, -4, NULL], 'min');
```

```text
-4
```

```sql
SELECT list_aggregate([2, 4, 8, 42], 'sum');
```

```text
56
```

```sql
SELECT list_aggregate([[1, 2], [NULL], [2, 10, 3]], 'last');
```

```text
[2, 10, 3]
```

```sql
SELECT list_aggregate([2, 4, 8, 42], 'string_agg', '|');
```

```text
2|4|8|42
```

### `list_*` Rewrite Functions

The following is a list of existing rewrites. Rewrites simplify the use of the list aggregate function by only taking the list (column) as their argument. `list_avg`, `list_var_samp`, `list_var_pop`, `list_stddev_pop`, `list_stddev_samp`, `list_sem`, `list_approx_count_distinct`, `list_bit_xor`, `list_bit_or`, `list_bit_and`, `list_bool_and`, `list_bool_or`, `list_count`, `list_entropy`, `list_last`, `list_first`, `list_kurtosis`, `list_kurtosis_pop`, `list_min`, `list_max`, `list_product`, `list_skewness`, `list_sum`, `list_string_agg`, `list_mode`, `list_median`, `list_mad` and `list_histogram`.

```sql
SELECT list_min([1, 2, -4, NULL]);
```

```text
-4
```

```sql
SELECT list_sum([2, 4, 8, 42]);
```

```text
56
```

```sql
SELECT list_last([[1, 2], [NULL], [2, 10, 3]]);
```

```text
[2, 10, 3]
```

#### `array_to_string`

Concatenates list/array elements using an optional delimiter.

```sql
SELECT array_to_string([1, 2, 3], '-') AS str;
```

```text
1-2-3
```

This is equivalent to the following SQL:

```sql
SELECT list_aggr([1, 2, 3], 'string_agg', '-') AS str;
```

```text
1-2-3
```

## Sorting Lists

The function `list_sort` sorts the elements of a list either in ascending or descending order.
In addition, it allows to provide whether `NULL` values should be moved to the beginning or to the end of the list.
It has the same sorting behavior as DuckDB's `ORDER BY` clause.
Therefore, (nested) values compare the same in `list_sort` as in `ORDER BY`.

By default, if no modifiers are provided, DuckDB sorts `ASC NULLS FIRST`.
I.e., the values are sorted in ascending order and `NULL` values are placed first.
This is identical to the default sort order of SQLite.
The default sort order can be changed using [`PRAGMA` statements.](../query_syntax/orderby).

`list_sort` leaves it open to the user whether they want to use the default sort order or a custom order.
`list_sort` takes up to two additional optional parameters.
The second parameter provides the sort order and can be either `ASC` or `DESC`.
The third parameter provides the `NULL` order and can be either `NULLS FIRST` or `NULLS LAST`.

This query uses the default sort order and the default `NULL` order.

```sql
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
```

```sql
[NULL, NULL, -5, 1, 3, 5]
```

This query provides the sort order.
The `NULL` order uses the configurable default value.

```sql
SELECT list_sort([1, 3, NULL, 2], 'ASC');
```

```sql
[NULL, 1, 2, 3]
```

This query provides both the sort order and the `NULL` order.
```sql
SELECT list_sort([1, 3, NULL, 2], 'DESC', 'NULLS FIRST');
```

```sql
[NULL, 3, 2, 1]
```

`list_reverse_sort` has an optional second parameter providing the `NULL` sort order.
It can be either `NULLS FIRST` or `NULLS LAST`.

This query uses the default `NULL` sort order.

```sql
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
```

```sql
[NULL, NULL, -5, 1, 3, 5]
```

This query provides the `NULL` sort order.

```sql
SELECT list_reverse_sort([1, 3, NULL, 2], 'NULLS LAST');
```

```sql
[3, 2, 1, NULL]
```

## Flattening

The flatten function is a scalar function that converts a list of lists into a single list by concatenating each sub-list together.
Note that this only flattens one level at a time, not all levels of sub-lists.

Convert a list of lists into a single list:

```sql
SELECT
    flatten([
        [1, 2],
        [3, 4]
    ]);
```

```text
[1, 2, 3, 4]
```

If the list has multiple levels of lists, only the first level of sub-lists is concatenated into a single list:

```sql
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
```

```text
[[1, 2], [3, 4], [5, 6], [7, 8]]
```

In general, the input to the flatten function should be a list of lists (not a single level list).
However, the behavior of the flatten function has specific behavior when handling empty lists and `NULL` values.

If the input list is empty, return an empty list:

```sql
SELECT flatten([]);
```

```text
[]
```

If the entire input to flatten is `NULL`, return `NULL`:

```sql
SELECT flatten(NULL);
```

```text
NULL
```

If a list whose only entry is `NULL` is flattened, return an empty list:

```sql
SELECT flatten([NULL]);
```

```text
[]
```

If the sub-list in a list of lists only contains `NULL`, do not modify the sub-list:

```sql
-- (Note the extra set of parentheses vs. the prior example)
SELECT flatten([[NULL]]);
```

```text
[NULL]
```

Even if the only contents of each sub-list is `NULL`, still concatenate them together. Note that no de-duplication occurs when flattening. See `list_distinct` function for de-duplication:

```sql
SELECT flatten([[NULL],[NULL]]);
```

```text
[NULL, NULL]
```

## Lambda Functions

DuckDB supports lambda functions in the form `(parameter1, parameter2, ...) -> expression`.
For details, see the [lambda functions page]({% link docs/sql/functions/lambda.md %}).

## Related Functions

There are also [aggregate functions]({% link docs/sql/functions/aggregates.md %}) `list` and `histogram` that produces lists and lists of structs.
The [`unnest`]({% link docs/sql/query_syntax/unnest.md %}) function is used to unnest a list by one level.
