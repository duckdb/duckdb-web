---
layout: docu
title: Variant Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions that operate on the [`VARIANT` type]({% link docs/preview/sql/data_types/variant.md %}).

> New Support for the `variant_*` functions is introduced in DuckDB 2.0.

| Name | Description |
|:--|:-------|
| [`variant_typeof(v)`](#variant_typeofv) | Return the full type of a `VARIANT` value, including nested structure. |
| [`variant_type(v)`](#variant_typev) | Return the top-level type category of a `VARIANT` value. |
| [`variant_keys(v)`](#variant_keysv) | Return the keys of a `VARIANT` object as a list. |
| [`variant_extract(v, field)`](#variant_extractv-field) | Extract a nested value by object field name or list index. Returns a `VARIANT`. |
| [`variant_extract_string(v, field)`](#variant_extract_stringv-field) | Extract a nested value as a `VARCHAR`. |
| [`variant_array_length(v)`](#variant_array_lengthv) | Return the number of elements in a `VARIANT` array. |
| [`variant_exists(v, key)`](#variant_existsv-key) | Return whether the given key exists in a `VARIANT` object. |
| [`variant_contains(haystack, needle)`](#variant_containshaystack-needle) | Return whether the `needle` `VARIANT` is contained in the `haystack` `VARIANT`. |
| [`variant_comparator(v)`](#variant_comparatorv) | Return a binary sort key that orders a `VARIANT` value by the logical ordering of `VARIANT` values. |
| [`variant_normalize(v)`](#variant_normalizev) | Return a canonical representation of a `VARIANT` value, so that values representing the same data share the same form. |
| [`variant_group_object(key, value)`](#variant_group_objectkey-value) | Aggregate. Return a `VARIANT` object built from all `key`, `value` pairs in the group. |
| [`variant_group_array(x)`](#variant_group_arrayx) | Aggregate. Collect all values of `x` into a `VARIANT` array. |

#### `variant_typeof(v)`

<div class="nostroke_table"></div>

| **Description** | Return the full type of a `VARIANT` value, including nested structure. |
| **Example** | `variant_typeof('{"a": 1}'::JSON::VARIANT)` |
| **Result** | `OBJECT(a)` |

#### `variant_type(v)`

<div class="nostroke_table"></div>

| **Description** | Return the top-level type category of a `VARIANT` value. |
| **Example** | `variant_type('{"a": 1}'::JSON::VARIANT)` |
| **Result** | `OBJECT` |

#### `variant_keys(v)`

<div class="nostroke_table"></div>

| **Description** | Return the keys of a `VARIANT` object as a list. |
| **Example** | `variant_keys('{"a": 1, "b": 2}'::JSON::VARIANT)` |
| **Result** | `[a, b]` |

#### `variant_extract(v, field)`

<div class="nostroke_table"></div>

| **Description** | Extract a nested value by object field name or list index. Returns a `VARIANT`. |
| **Example** | `variant_extract('{"name": "Fry"}'::JSON::VARIANT, 'name')` |
| **Result** | `Fry` |

#### `variant_extract_string(v, field)`

<div class="nostroke_table"></div>

| **Description** | Extract a nested value as a `VARCHAR`. |
| **Example** | `variant_extract_string('{"name": "Fry"}'::JSON::VARIANT, 'name')` |
| **Result** | `Fry` |

#### `variant_array_length(v)`

<div class="nostroke_table"></div>

| **Description** | Return the number of elements in a `VARIANT` array. |
| **Example** | `variant_array_length('[1, 2, 3]'::JSON::VARIANT)` |
| **Result** | `3` |

#### `variant_exists(v, key)`

<div class="nostroke_table"></div>

| **Description** | Return whether the given key exists in a `VARIANT` object. |
| **Example** | `variant_exists('{"a": 1}'::JSON::VARIANT, 'a')` |
| **Result** | `true` |

#### `variant_contains(haystack, needle)`

<div class="nostroke_table"></div>

| **Description** | Return whether the `needle` `VARIANT` is contained in the `haystack` `VARIANT`. |
| **Example** | `variant_contains('{"user": {"id": 42}}'::JSON::VARIANT, '{"user": {"id": 42}}'::JSON::VARIANT)` |
| **Result** | `true` |

#### `variant_comparator(v)`

<div class="nostroke_table"></div>

| **Description** | Return a binary sort key (a `BLOB`) that orders a `VARIANT` value according to the logical ordering of `VARIANT` values. This is used internally so that `VARIANT`s compare and sort consistently with the corresponding native DuckDB types, rather than by their internal byte representation. |
| **Example** | `variant_comparator({'a': 1, 'b': 2}::VARIANT)` |
| **Result** | A `BLOB` sort key |

Values are ordered first by type bucket (for example, booleans before numbers, numbers before strings) and then by value within a bucket, so that sorting a `VARIANT` column matches the order of the underlying values:

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

| **Description** | Return a canonical representation of a `VARIANT` value. Two `VARIANT` values that represent the same data normalize to the same result, regardless of how they were constructed or physically stored. This is useful when comparing or storing `VARIANT` values. |
| **Example** | `variant_normalize({'b': [1, 2, 3], 'a': 42}::VARIANT)` |
| **Result** | A normalized `VARIANT` |

> New The `variant_normalize` function was added in DuckDB 2.0.

#### `variant_group_object(key, value)`

<div class="nostroke_table"></div>

| **Description** | Aggregate function. Returns a `VARIANT` object containing all `key`, `value` pairs in the group, where `key` is a `VARCHAR` and `value` is a `VARIANT`. A `NULL` key or a duplicate key raises an error. |
| **Example** | `variant_group_object('duck', 'goose'::VARIANT)` |
| **Result** | `{'duck': goose}` |

> New The `variant_group_object` aggregate was added in DuckDB 2.0.

#### `variant_group_array(x)`

<div class="nostroke_table"></div>

| **Description** | Collects all values of `x` into a `VARIANT` array, preserving order. Defined as a macro equivalent to `list(x)::VARIANT`, so it has aggregate semantics and also works as a window function. `NULL` values are kept as `VARIANT` nulls. |
| **Example** | `variant_group_array(i)` |
| **Result** | `[0, 1, 2, 3]` |

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
