---
layout: docu
title: Enum Functions
---

This section describes functions and operators for examining and manipulating `ENUM` values.
The examples assume an enum type created as:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious');
```

These functions can take `NULL` or a specific value of the type as argument(s).
With the exception of `enum_range_boundary`, the result depends only on the type of the argument and not on its value.

| Name | Description |
|:--|:-------|
| [`enum_code(enum_value)`](#enum_codeenum_value) | Returns the numeric value backing the given enum value. |
| [`enum_first(enum)`](#enum_firstenum) | Returns the first value of the input enum type. |
| [`enum_last(enum)`](#enum_lastenum) | Returns the last value of the input enum type. |
| [`enum_range(enum)`](#enum_rangeenum) | Returns all values of the input enum type as an array. |
| [`enum_range_boundary(enum, enum)`](#enum_range_boundaryenum-enum) | Returns the range between the two given enum values as an array. |

### `enum_code(enum_value)`

<div class="nostroke_table"></div>

| **Description** | Returns the numeric value backing the given enum value. |
| **Example** | `enum_code('happy'::mood)` |
| **Result** | `2` |

### `enum_first(enum)`

<div class="nostroke_table"></div>

| **Description** | Returns the first value of the input enum type. |
| **Example** | `enum_first(NULL::mood)` |
| **Result** | `sad` |

### `enum_last(enum)`

<div class="nostroke_table"></div>

| **Description** | Returns the last value of the input enum type. |
| **Example** | `enum_last(NULL::mood)` |
| **Result** | `anxious` |

### `enum_range(enum)`

<div class="nostroke_table"></div>

| **Description** | Returns all values of the input enum type as an array. |
| **Example** | `enum_range(NULL::mood)` |
| **Result** | `[sad, ok, happy, anxious]` |

### `enum_range_boundary(enum, enum)`

<div class="nostroke_table"></div>

| **Description** | Returns the range between the two given enum values as an array. The values must be of the same enum type. When the first parameter is `NULL`, the result starts with the first value of the enum type. When the second parameter is `NULL`, the result ends with the last value of the enum type. |
| **Example** | `enum_range_boundary(NULL, 'happy'::mood)` |
| **Result** | `[sad, ok, happy]` |
