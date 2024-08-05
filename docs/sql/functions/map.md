---
layout: docu
title: Map Functions
---

| Name | Description |
|:--|:-------|
| [`cardinality(map)`](#cardinalitymap) | Return the size of the map (or the number of entries in the map). |
| [`element_at(map, key)`](#element_atmap-key) | Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. |
| [`map_entries(map)`](#map_entriesmap) | Return a list of struct(k, v) for each key-value pair in the map. |
| [`map_extract(map, key)`](#map_extractmap-key) | Alias of `element_at`. Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. |
| [`map_from_entries(STRUCT(k, v)[])`](#map_from_entriesstructk-v) | Returns a map created from the entries of the array. |
| [`map_keys(map)`](#map_keysmap) | Return a list of all keys in the map. |
| [`map_values(map)`](#map_valuesmap) | Return a list of all values in the map. |
| [`map()`](#map) | Returns an empty map. |
| [`map[entry]`](#mapentry) | Alias for `element_at`. |

### `cardinality(map)`

<div class="nostroke_table"></div>

| **Description** | Return the size of the map (or the number of entries in the map). |
| **Example** | `cardinality(map([4, 2], ['a', 'b']))` |
| **Result** | `2` |

### `element_at(map, key)`

<div class="nostroke_table"></div>

| **Description** | Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. |
| **Example** | `element_at(map([100, 5], [42, 43]), 100)` |
| **Result** | `[42]` |

### `map_entries(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of struct(k, v) for each key-value pair in the map. |
| **Example** | `map_entries(map([100, 5], [42, 43]))` |
| **Result** | `[{'key': 100, 'value': 42}, {'key': 5, 'value': 43}]` |

### `map_extract(map, key)`

<div class="nostroke_table"></div>

| **Description** | Alias of `element_at`. Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. |
| **Example** | `map_extract(map([100, 5], [42, 43]), 100)` |
| **Result** | `[42]` |

### `map_from_entries(STRUCT(k, v)[])`

<div class="nostroke_table"></div>

| **Description** | Returns a map created from the entries of the array. |
| **Example** | `map_from_entries([{k: 5, v: 'val1'}, {k: 3, v: 'val2'}])` |
| **Result** | `{5=val1, 3=val2}` |

### `map_keys(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of all keys in the map. |
| **Example** | `map_keys(map([100, 5], [42,43]))` |
| **Result** | `[100, 5]` |

### `map_values(map)`

<div class="nostroke_table"></div>

| **Description** | Return a list of all values in the map. |
| **Example** | `map_values(map([100, 5], [42, 43]))` |
| **Result** | `[42, 43]` |

### `map()`

<div class="nostroke_table"></div>

| **Description** | Returns an empty map. |
| **Example** | `map()` |
| **Result** | `{}` |

### `map[entry]`

<div class="nostroke_table"></div>

| **Description** | Alias for `element_at`. |
| **Example** | `map([100, 5], ['a', 'b'])[100]` |
| **Result** | `[a]` |
