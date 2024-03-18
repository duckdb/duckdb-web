| Function | Description | Example | Result |
|:--|:---|:---|:-|
| `cardinality(`*`map`*`)` | Return the size of the map (or the number of entries in the map). | `cardinality(map([4, 2], ['a', 'b']))` | `2` |
| `element_at(`*`map, key`*`)` | Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `element_at(map([100, 5], [42, 43]), 100)` | `[42]` |
| `map_entries(`*`map`*`)` | Return a list of struct(k, v) for each key-value pair in the map. | `map_entries(map([100, 5], [42, 43]))` | `[{'key': 100, 'value': 42}, {'key': 5, 'value': 43}]` |
| `map_extract(`*`map, key`*`)` | Alias of `element_at`. Return a list containing the value for a given key or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys else an error is returned. | `map_extract(map([100, 5], [42, 43]), 100)` | `[42]` |
| `map_from_entries(`*`STRUCT(k, v)[]`*`)` | Returns a map created from the entries of the array | `map_from_entries([{k: 5, v: 'val1'}, {k: 3, v: 'val2'}])` | `{5=val1, 3=val2}` |
| `map_keys(`*`map`*`)` | Return a list of all keys in the map. | `map_keys(map([100, 5], [42,43]))` | `[100, 5]` |
| `map_values(`*`map`*`)` | Return a list of all values in the map. | `map_values(map([100, 5], [42, 43]))` | `[42, 43]` |
| `map()` | Returns an empty map. | `map()` | `{}` |
| `map[`*`entry`*`]` | Alias for `element_at` | `map([100, 5], ['a', 'b'])[100]` | `[a]` |
