---
layout: docu
title: Nested Functions
selected: Documentation/Functions/Nested Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating nested values. There are two nested data types: lists and structs.

## List Functions

In the descriptions, `l` is the three element list `[4, 5, 6]`.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `array_extract(`*`list`*`, `*`index`*`)` | Alias for `list_extract`. | `array_extract(l, 2)` | `6` |
| `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`)` | Extract a sublist using slice conventions. `NULL`s are interpreted as the bounds of the `LIST`. Negative values are accepted. | `array_slice(l, 1, NULL)` | `[5,6]` |
| `list_element(`*`list`*`, `*`index`*`)` | Alias for `list_extract`. | `list_element(l, 2)` | `6` |
| `list_extract(`*`list`*`, `*`index`*`)` | Extract the `index`th (0-based) value from the list. | `list_extract(l, 2)` | `6` |
| `list_pack(`*`any`*`, ...)` | Alias for `list_value`. | `list_pack(4, 5, 6)` | `[4, 5, 6]` |
| `list_value(`*`any`*`, ...)` | Create a `LIST` containing the argument values. | `list_value(4, 5, 6)` | `[4, 5, 6]` |
| *`list`*`[`*`index`*`]` | Alias for `list_extract`. | `l[2]` | `6` |
| *`list`*`[`*`begin`*`:`*`end`*`]` | Alias for `array_slice`. Missing arguments are interprete as `NULL`s | `l[1:2]` | `[5,6]` |

## Struct Functions

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`struct`*`[`*`entry`*`]` | Alias for `struct_extract`. | `struct_extract(s, 'i')` | `4` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct. | `struct_extract(s, 'i')` | `4` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 3, 's': 'string'}`|

## Related Functions

There are also [aggregate functions](../aggregates) `list` and `histogram` that produces lists and lists of structs.
