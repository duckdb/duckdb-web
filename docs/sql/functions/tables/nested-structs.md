| Function | Description | Example | Result |
|:--|:---|:---|:--|
| *`struct`*`.`*`entry`* | Dot notation that serves as an alias for `struct_extract` from named `STRUCT`s. | `({'i': 3, 's': 'string'}).i` | `3` |
| *`struct`*`[`*`entry`*`]` | Bracket notation that serves as an alias for `struct_extract` from named `STRUCT`s. | `({'i': 3, 's': 'string'})['i']` | `3` |
| *`struct`*`[`*`idx`*`]` | Bracket notation that serves as an alias for `struct_extract` from unnamed `STRUCT`s (tuples), using an index (1-based). | `(row(42, 84))[1]` | `42` |
| `row(`*`any`*`, ...)` | Create an unnamed `STRUCT` (tuple) containing the argument values. | `row(i, i % 4, i / 4)` | `(10, 2, 2.5)`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the `STRUCT`. | `struct_extract({'i': 3, 'v2': 3, 'v3': 0}, 'i')` | `3` |
| `struct_extract(`*`struct`*`, `*`idx`*`)` | Extract the entry from an unnamed `STRUCT` (tuple) using an index (1-based). | `struct_extract(row(42, 84), 1)` | `42` |
| `struct_insert(`*`struct`*`, `*`name := any`*`, ...)` | Add field(s)/value(s) to an existing `STRUCT` with the argument values. The entry name(s) will be the bound variable name(s). | `struct_insert({'a': 1}, b := 2)` | `{'a': 1, 'b': 2}` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 4, 's': string}` |
