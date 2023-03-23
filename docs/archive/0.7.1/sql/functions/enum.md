---
layout: docu
title: Enum Functions
selected: Documentation/Functions/Enum Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating `ENUM` values.
The examples assume an enum type created as:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious');
```

These functions can take `NULL` or a specific value of the type as argument(s).
With the exception of `enum_range_boundary`, the result depends only on the type of the argument and not on its value.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `enum_first(`*`enum`*`)` | Returns the first value of the input enum type. | `enum_first(null::mood)` | `sad` |
| `enum_last(`*`enum`*`)` | Returns the last value of the input enum type. | `enum_last(null::mood)` | `anxious` |
| `enum_range(`*`enum`*`)` | Returns all values of the input enum type as an array. | `enum_range(null::mood)` | `[sad, ok, happy, anxious]` |
| `enum_range_boundary(`*`enum`*`, `*`enum`*`)` | Returns the range between the two given enum values as an array. The values must be of the same enum type. When the first parameter is `NULL`, the result starts with the first value of the enum type. When the second parameter is `NULL`, the result ends with the last value of the enum type. | `enum_range_boundary(NULL, 'happy'::mood)` | `[sad, ok, happy]` |
| `enum_code(`*`enum_value`*`)`                 | Returns the numeric value backing the given enum value                                                                                                                                                                                                                                             | `enum_code('happy'::mood)`                 | `2`                |
