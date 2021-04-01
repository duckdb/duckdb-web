---
layout: docu
title: Nested Functions
selected: Documentation/Functions/Nested Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating nested values. There are two nested data types: lists and structs.

## List Functions

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`list`*`[`*`index`*`]` | Alias for `list_extract`. | `list_value(4, 5, 6)[2]` | `6` |
| `array_extract(`*`list`*`, `*`index`*`)` | Alias for `list_extract`. | `array_extract(l, 2)` | `6` |
| `list_element(`*`list`*`, `*`index`*`)` | Alias for `list_extract`. | `list_element(l, 2)` | `6` |
| `list_extract(`*`list`*`, `*`index`*`)` | Extract the `index`th (0-based) value from the list. | `list_extract(l, 2)` | `6` |
| `list_pack(`*`any`*`, ...)` | Alias for `list_value`. | `list_pack(4, 5, 6)` | `(4, 5, 6)` |
| `list_value(`*`any`*`, ...)` | Create a `LIST` containing the argument values. | `list_value(4, 5, 6)` | `(4, 5, 6)` |

There are also an [aggregate function](../aggregates) `list` that collects the aggregated values into a single list, and [text functions](./char) `string_split` and `string_split_regex` that create lists of strings by splitting a single string value at a delimiter.

## Struct Functions

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`struct`*`[`*`entry`*`]` | Alias for `struct_extract`. | `struct_extract(s, 'i')` | `4` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct. | `struct_extract(s, 'i')` | `4` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 3, 's': 'string'}`|

There are also an [aggregate function](../aggregates) `histogram` that returns a two-element struct with entries `bucket` and `count`.
