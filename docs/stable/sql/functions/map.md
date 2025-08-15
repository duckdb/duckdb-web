---
layout: docu
redirect_from:
- /docs/sql/functions/map
title: Map Functions
---

<!-- markdownlint-disable MD001 -->

| Name | Description |
|:--|:-------|
| [`cardinality(map)`](#cardinalitymap) | Return the size of the map (or the number of entries in the map). |
| [`element_at(map, key)`](#element_atmap-key) | Return the value for a given `key` as a list, or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| [`map_concat(maps...)`](#map_concatmaps) | Returns a map created from merging the input `maps`. On key collision the value is taken from the last map with that key. |
| [`map_contains(map, key)`](#map_containsmap-key) | Checks if a map contains a given key. |
| [`map_contains_entry(map, key, value)`](#map_contains_entrymap-key-value) | Check if a map contains a given key-value pair. |
| [`map_contains_value(map, value)`](#map_contains_valuemap-value) | Checks if a map contains a given value. |
| [`map_entries(map)`](#map_entriesmap) | Return a list of struct(k, v) for each key-value pair in the map. |
| [`map_extract(map, key)`](#map_extractmap-key) | Return the value for a given `key` as a list, or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| [`map_extract_value(map, key)`](#map_extract_valuemap-key) | Returns the value for a given `key` or `NULL` if the `key` is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| [`map_from_entries(STRUCT(k, v)[])`](#map_from_entriesstructk-v) | Returns a map created from the entries of the array. |
| [`map_keys(map)`](#map_keysmap) | Return a list of all keys in the map. |
| [`map_values(map)`](#map_valuesmap) | Return a list of all values in the map. |
| [`map()`](#map) | Returns an empty map. |
| [`map[entry]`](#mapentry) | Returns the value for a given `key` or `NULL` if the `key` is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |

#### `cardinality(map)`

<div class="nostroke_table"></div>

| **Description** | Return the size of the map (or the number of entries in the map). |
| **Example** | `cardinality(map([4, 2], ['a', 'b']))` |
| **Result** | `2` |

#### `element_at(map, key)`

<div class="nostroke_table"></div>

| **Description** | Return the value for a given `key` as a list, or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| **Example** | `element_at(map([100, 5], [42, 43]), 100)` |
| **Result** | `[42]` |
| **Aliases** | `map_extract(map, key)` |

#### `map_concat(maps...)`

<div class="nostroke_table"></div>

| **Description** | Returns a map created from merging the input `maps`. On key collision the value is taken from the last map with that key. |
| **Example** | `map_concat(MAP {'key1': 10, 'key2': 20}, MAP {'key3': 30}, MAP {'key2': 5})` |
| **Result** | `{key1=10, key2=5, key3=30}` |

#### `map_contains(map, key)`

<div class="nostroke_table"></div>

| **Description** | Checks if a map contains a given key. |
| **Example** | `map_contains(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 'key2')` |
| **Result** | `true` |

#### `map_contains_entry(map, key, value)`

<div class="nostroke_table"></div>

| **Description** | Check if a map contains a given key-value pair. |
| **Example** | `map_contains_entry(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 'key2', 20)` |
| **Result** | `true` |

#### `map_contains_value(map, value)`

<div class="nostroke_table"></div>

| **Description** | Checks if a map contains a given value. |
| **Example** | `map_contains_value(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 20)` |
| **Result** | `true` |

#### `map_entries(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of struct(k, v) for each key-value pair in the map. |
| **Example** | `map_entries(map([100, 5], [42, 43]))` |
| **Result** | `[{'key': 100, 'value': 42}, {'key': 5, 'value': 43}]` |

#### `map_extract(map, key)`

<div class="nostroke_table"></div>

| **Description** | Return the value for a given `key` as a list, or `NULL` if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. |
| **Example** | `map_extract(map([100, 5], [42, 43]), 100)` |
| **Result** | `[42]` |
| **Aliases** | `element_at(map, key)` |

#### `map_extract_value(map, key)`

<div class="nostroke_table"></div>

| **Description** | Returns the value for a given `key` or `NULL` if the `key` is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| **Example** | `map_extract_value(map([100, 5], [42, 43]), 100);` |
| **Result** | `42` |
| **Aliases** | `map[key]` |

#### `map_from_entries(STRUCT(k, v)[])`

<div class="nostroke_table"></div>

| **Description** | Returns a map created from the entries of the array. |
| **Example** | `map_from_entries([{k: 5, v: 'val1'}, {k: 3, v: 'val2'}])` |
| **Result** | `{5=val1, 3=val2}` |

#### `map_keys(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of all keys in the map. |
| **Example** | `map_keys(map([100, 5], [42,43]))` |
| **Result** | `[100, 5]` |

#### `map_values(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of all values in the map. |
| **Example** | `map_values(map([100, 5], [42, 43]))` |
| **Result** | `[42, 43]` |

#### `map()`

<div class="nostroke_table"></div>

| **Description** | Returns an empty map. |
| **Example** | `map()` |
| **Result** | `{}` |

#### `map[entry]`

<div class="nostroke_table"></div>

| **Description** | Returns the value for a given `key` or `NULL` if the `key` is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. |
| **Example** | `map([100, 5], ['a', 'b'])[100]` |
| **Result** | `a` |
| **Aliases** | `map_extract_value(map, key)` |
