---
layout: docu
title: Nested Functions
selected: Documentation/Functions/Nested Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating nested values.

There are two types of nested data types: lists and structs. 
* A `LIST` is an ordered sequence of data values of the same type. A `LIST` column can have values with different lengths, but they must all have the same underlying type.
* A `STRUCT` is a dictionary of data values. The values are looked up in the dictionary using string entry names. A `STRUCT` column must have the same entry names and data types for each value.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `list_extract(`*`list`*`, `*`index`*`)` | Extract the `index`th (0-based) value from the list. | `list_extract(l, 2)` | `6` |
| `list_value(`*`any`*`, ...)` | Create a `LIST` containing the argument values. | `list_value(4, 5, 6)` | `(4, 5, 6)` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct. | `struct_extract(s, 'i')` | `4` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 3, 's': 'string'}`|
