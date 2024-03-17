| Function | Description | Example | Result |
|:--|:--|:---|:-|
| `enum_code(`*`enum_value`*`)` | Returns the numeric value backing the given enum value | `enum_code('happy'::mood)` | `2` |
| `enum_first(`*`enum`*`)` | Returns the first value of the input enum type. | `enum_first(null::mood)` | `sad` |
| `enum_last(`*`enum`*`)` | Returns the last value of the input enum type. | `enum_last(null::mood)` | `anxious` |
| `enum_range(`*`enum`*`)` | Returns all values of the input enum type as an array. | `enum_range(null::mood)` | `[sad, ok, happy, anxious]` |
| `enum_range_boundary(`*`enum`*`, `*`enum`*`)` | Returns the range between the two given enum values as an array. The values must be of the same enum type. When the first parameter is `NULL`, the result starts with the first value of the enum type. When the second parameter is `NULL`, the result ends with the last value of the enum type. | `enum_range_boundary(NULL, 'happy'::mood)` | `[sad, ok, happy]` |
