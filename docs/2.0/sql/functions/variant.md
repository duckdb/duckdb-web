---
layout: docu
redirect_from:
- /docs/current/sql/functions/variant
- /docs/lts/sql/functions/variant
- /docs/preview/sql/functions/variant
- /docs/stable/sql/functions/variant
title: Variant Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions that operate on the [`VARIANT` type]({% link docs/2.0/sql/data_types/variant.md %}).

> New Most `variant_*` functions were introduced in DuckDB 2.0. The `variant_extract`, `variant_normalize`, and `variant_typeof` functions were already available in DuckDB 1.5. The `variant_value` function was introduced in DuckDB 2.1 and is currently available in nightly builds.

| Name | Description |
|:--|:-------|
| [`variant_typeof(v)`](#variant_typeofv) | Returns the detailed type of a `VARIANT` value, including object keys and array lengths. |
| [`variant_type(v[, path])`](#variant_typev-path) | Returns the top-level type category of a `VARIANT` value or of the value at `path`. |
| [`variant_keys(v[, path])`](#variant_keysv-path) | Returns the keys of a `VARIANT` object, or of the object at `path`, as a list. |
| [`variant_extract(v, field)`](#variant_extractv-field) | Returns the value of an object field or a list element as a `VARIANT`. |
| [`variant_extract_string(v, path)`](#variant_extract_stringv-path) | Returns the value at `path` as a `VARCHAR`; objects and arrays are rendered as JSON text. |
| [`variant_value(v, path)`](#variant_valuev-path) | Returns the scalar value at `path`, or at an array index, as a `VARIANT`. |
| [`variant_array_length(v[, path])`](#variant_array_lengthv-path) | Returns the number of elements of a `VARIANT` array, or of the array at `path`. |
| [`variant_exists(v, path)`](#variant_existsv-path) | Returns whether `path` exists in a `VARIANT` value. |
| [`variant_contains(haystack, needle)`](#variant_containshaystack-needle) | Returns whether `needle` is contained in `haystack`, at any depth and regardless of key or element order. |
| [`variant_comparator(v)`](#variant_comparatorv) | Returns a sort key that is equal for `VARIANT` values with equal logical values. |
| [`variant_normalize(v)`](#variant_normalizev) | Returns a normalized representation of a `VARIANT` value. |
| [`variant_group_object(key, value)`](#variant_group_objectkey-value) | Aggregate. Returns a `VARIANT` object with one field per `key`, `value` pair in the group. |
| [`variant_group_array(x)`](#variant_group_arrayx) | Aggregate. Collects all values of `x` into a `VARIANT` array. |

The functions `variant_type`, `variant_keys`, `variant_extract_string`, `variant_value`, `variant_array_length` and `variant_exists` take a `path` argument that refers to a field inside the `VARIANT` value. A path is the name of a field; the empty string `''` refers to the value itself. Instead of a single path, a list of paths can be passed. In that case, the result is a list with one result per path. If a path does not exist, the result for that path is `NULL`, except for `variant_exists`, which returns `false`. A `NULL` path returns `NULL`, while a list of paths that contains `NULL` raises an error.

#### `variant_typeof(v)`

<div class="nostroke_table"></div>

| **Description** | Returns the detailed type of a `VARIANT` value. For objects, the result lists the keys in sorted order, e.g., `OBJECT(a, b, c)`. For arrays, it includes the number of elements, e.g., `ARRAY(3)`. For primitive values, it names the stored type, e.g., `INT32` or `DECIMAL(18, 6)`. A `NULL` field inside a `VARIANT` is reported as `VARIANT_NULL`. This is useful for inspecting the structure of semi-structured data. |
| **Example 1** | `variant_typeof({'c': [1], 'b': 2, 'a': 3}::VARIANT)` |
| **Result** | `OBJECT(a, b, c)` |
| **Example 2** | `variant_typeof([1, 2, 3]::VARIANT)` |
| **Result** | `ARRAY(3)` |

#### `variant_type(v[, path])`

<div class="nostroke_table"></div>

| **Description** | Returns the top-level type category of a `VARIANT` value, such as `OBJECT`, `ARRAY`, `VARCHAR` or `INT32`. Unlike `variant_typeof`, the result does not describe nested structure. With `path`, the type of the value at that path is returned; a field that holds `NULL` returns `VARIANT_NULL`, while a path that does not exist returns `NULL`. |
| **Example 1** | `variant_type({'a': 1, 'b': ['duck', 'goose']}::VARIANT, 'b')` |
| **Result** | `ARRAY` |
| **Example 2** | `variant_type({'a': 1, 'b': NULL}::VARIANT, ['a', 'b', 'q'])` |
| **Result** | `[INT32, VARIANT_NULL, NULL]` |

#### `variant_keys(v[, path])`

<div class="nostroke_table"></div>

| **Description** | Returns the keys of a `VARIANT` object as a list, in sorted order. Arrays and primitive values have no keys and return an empty list. With `path`, the keys of the object at that path are returned. |
| **Example 1** | `variant_keys({'b': 2, 'a': {'x': 1}}::VARIANT)` |
| **Result** | `[a, b]` |
| **Example 2** | `variant_keys({'a': {'x': 1, 'y': 2}, 'b': 42}::VARIANT, ['a', 'b', 'q'])` |
| **Result** | `[[x, y], [], NULL]` |

#### `variant_extract(v, field)`

<div class="nostroke_table"></div>

| **Description** | Returns the value of an object field or a list element as a `VARIANT`. `field` is either a field name or a list index. List indexes are 1-based; index `0` raises an error. Because the result is a `VARIANT`, calls can be chained, also in method syntax: `v.variant_extract('a').variant_extract(1)`. |
| **Example 1** | `variant_extract({'name': 'Fry', 'age': 25}::VARIANT, 'name')` |
| **Result** | `Fry` |
| **Example 2** | `variant_extract(['A', 'B']::VARIANT, 1)` |
| **Result** | `A` |

#### `variant_extract_string(v, path)`

<div class="nostroke_table"></div>

| **Description** | Returns the value at `path` as a `VARCHAR`. Objects and arrays are rendered as JSON text. Unlike `variant_extract`, which returns a `VARIANT`, the result can be used directly where a string is expected. A field that holds `NULL` returns `NULL`. |
| **Example 1** | `variant_extract_string({'a': 1, 'b': {'c': 12}}::VARIANT, 'b')` |
| **Result** | `{"c":12}` |
| **Example 2** | `variant_extract_string(['duck', 'goose']::VARIANT, '')` |
| **Result** | `["duck","goose"]` |

#### `variant_value(v, path)`

<div class="nostroke_table"></div>

| **Description** | Returns the scalar value at `path` as a `VARIANT`, keeping the type of the selected value. This is the `VARIANT` counterpart of [`json_value`]({% link docs/2.0/data/json/json_functions.md %}#json-extraction-functions). `path` is a `VARCHAR` object key. A `VARCHAR[]` list of keys returns a `VARIANT[]` with one value per key. A `BIGINT` index selects an array element instead. Indexes are 0-based, and a negative index counts from the end. The result is `NULL` when the selected value is an object, an array, or a `VARIANT` null (`VARIANT_NULL`), when the key is missing or the index is out of range, and when a key is used on a non-object or an index on a non-array. A path is a single object key. The empty string `''` selects the value itself, and JSONPath is not supported. The path or index must be a constant expression. A `NULL` path or index returns `NULL`. A list of paths that contains `NULL` raises a binder error. Only a `VARIANT` value is accepted: a `VARCHAR` or `JSON` value is not implicitly cast. A string literal is cast to a `VARCHAR` `VARIANT` and is not parsed as JSON. |
| **Example 1** | `variant_value({'a': 42, 'b': [1, 2]}::VARIANT, 'a')` |
| **Result** | `42` |
| **Example 2** | `variant_value({'a': 42, 'b': [1, 2]}::VARIANT, 'b')` |
| **Result** | `NULL` |
| **Example 3** | `variant_value({'a': 42, 'b': 'duck'}::VARIANT, ['b', 'a'])` |
| **Result** | `[duck, 42]` |
| **Example 4** | `variant_value([10, 20, 30]::VARIANT, -1)` |
| **Result** | `30` |

> New The `variant_value` function was introduced in DuckDB 2.1 and is currently available in nightly builds.

#### `variant_array_length(v[, path])`

<div class="nostroke_table"></div>

| **Description** | Returns the number of elements of a `VARIANT` array. An object returns `0`. With `path`, the length of the array at that path is returned. |
| **Example 1** | `variant_array_length([1, 2, 3]::VARIANT)` |
| **Result** | `3` |
| **Example 2** | `variant_array_length({'a': [1, 2], 'c': {'d': 1}}::VARIANT, ['a', 'c', 'q'])` |
| **Result** | `[2, 0, NULL]` |

#### `variant_exists(v, path)`

<div class="nostroke_table"></div>

| **Description** | Returns whether `path` exists in a `VARIANT` value. This is useful for selecting rows of semi-structured data by the presence of a field. |
| **Example 1** | `variant_exists({'a': 1, 'b': 2}::VARIANT, 'a')` |
| **Result** | `true` |
| **Example 2** | `variant_exists({'a': 1, 'b': 2}::VARIANT, ['a', 'c'])` |
| **Result** | `[true, false]` |

#### `variant_contains(haystack, needle)`

<div class="nostroke_table"></div>

| **Description** | Returns whether `needle` is contained in `haystack`. For objects, containment is subset matching: every field of `needle` must occur in `haystack`, regardless of key order. For arrays, every element of `needle` must occur in `haystack`, regardless of element order. `needle` can match a value at any depth of `haystack`; object keys are not values and do not match. Numbers compare by value across integer and decimal types, but integer and floating-point values do not match each other. This is useful for filtering semi-structured data on a partial structure. |
| **Example 1** | `variant_contains('{"a": 1, "b": 2}'::JSON::VARIANT, '{"a": 1}'::JSON::VARIANT)` |
| **Result** | `true` |
| **Example 2** | `variant_contains('{"a": {"b": [1, 2, 3]}}'::JSON::VARIANT, 2::VARIANT)` |
| **Result** | `true` |
| **Example 3** | `variant_contains('[1, 2, 3]'::JSON::VARIANT, '[3, 1]'::JSON::VARIANT)` |
| **Result** | `true` |

#### `variant_comparator(v)`

<div class="nostroke_table"></div>

| **Description** | Returns a sort key for a `VARIANT` value. Values with equal logical values produce equal keys: object key order does not matter, integer and decimal values of equal value are equal, and so are `FLOAT` and `DOUBLE` values of equal value. Integer and floating-point values remain distinct. `NULL` returns `NULL`. This is useful for comparing `VARIANT` values by content, e.g., `variant_comparator(a) = variant_comparator(b)`. |
| **Example 1** | `variant_comparator({'b': 10, 'a': 1}::VARIANT) = variant_comparator({'a': 1, 'b': 10}::VARIANT)` |
| **Result** | `true` |
| **Example 2** | `variant_comparator(5::INTEGER::VARIANT) = variant_comparator(5.00::DECIMAL(5, 2)::VARIANT)` |
| **Result** | `true` |

`VARIANT` values sort by their logical value, also across integer and decimal types, so that sorting a `VARIANT` column matches the order of the underlying values:

```sql
SELECT i
FROM range(-2, 2) t(i)
ORDER BY i::VARIANT;
```

| i |
|--:|
| -2 |
| -1 |
| 0 |
| 1 |

#### `variant_normalize(v)`

<div class="nostroke_table"></div>

| **Description** | Returns a normalized representation of a `VARIANT` value. The normalized value compares equal to the original value, including for less common types such as `TIME_NS`, `TIMESTAMPTZ_NS` and `BIGNUM`. |
| **Example** | `variant_normalize('123456789012345678901234567890'::BIGNUM::VARIANT) = '123456789012345678901234567890'::BIGNUM::VARIANT` |
| **Result** | `true` |

#### `variant_group_object(key, value)`

<div class="nostroke_table"></div>

| **Description** | Aggregate function. Returns a `VARIANT` object with one field per row of the group, using `key` (a `VARCHAR`) as the field name and `value` as its value. This is useful for turning key-value rows into a single object. A `NULL` key or a duplicate key raises an error; with `DISTINCT`, identical key-value pairs are removed before duplicate keys are checked. A `NULL` value becomes a `NULL` field. An empty group returns `NULL`. |

```sql
SELECT variant_group_object(k, v)
FROM (VALUES ('duck', 'goose'::VARIANT), ('pond', 26::VARIANT)) t(k, v);
```

| variant_group_object(k, v) |
|:--|
| {'duck': goose, 'pond': 26} |

> New The `variant_group_object` aggregate was added in DuckDB 2.0.

#### `variant_group_array(x)`

<div class="nostroke_table"></div>

| **Description** | Aggregate function. Collects all values of `x` into a `VARIANT` array. Values of different types keep their own types, and `NULL` values are kept as `NULL` elements. An empty group returns `NULL`. `variant_group_array` can also be used as a window function. |

```sql
SELECT i % 2 AS g, variant_group_array(i)
FROM range(4) t(i)
GROUP BY g
ORDER BY g;
```

| g | variant_group_array(i) |
|--:|:--|
| 0 | [0, 2] |
| 1 | [1, 3] |

> New The `variant_group_array` function was added in DuckDB 2.0.

## Example

The `variant_*` functions are useful for inspecting and filtering semi-structured data stored in a `VARIANT` column:

```sql
CREATE TABLE events (payload VARIANT);
INSERT INTO events
VALUES ('{"user": {"id": 42, "tags": ["a", "b"]}}'::JSON::VARIANT);

SELECT variant_type(payload), variant_keys(payload)
FROM events;

SELECT *
FROM events
WHERE variant_contains(payload, {'user': {'id': 42}}::VARIANT);
```
