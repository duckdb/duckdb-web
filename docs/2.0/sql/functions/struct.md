---
layout: docu
redirect_from:
- /docs/sql/functions/struct
- /docs/stable/sql/functions/struct
- /docs/current/sql/functions/struct
- /docs/lts/sql/functions/struct
- /docs/preview/sql/functions/struct
title: Struct Functions
---

<!-- markdownlint-disable MD001 -->

The functions on this page work on [`STRUCT` values]({% link docs/2.0/sql/data_types/struct.md %}). Functions that access entries by position, such as `struct[idx]`, `struct_extract_at`, `struct_contains`, `struct_position` and `struct_values`, also accept [`TUPLE` values]({% link docs/2.0/sql/data_types/struct.md %}#tuples), i.e., structs with unnamed entries. `struct_concat` accepts either only `STRUCT`s or only `TUPLE`s. Functions that work with entry names, i.e., `struct_insert`, `struct_keys`, `struct_update` and `remap_struct`, require a `STRUCT`.

| Name | Description |
|:--|:-------|
| [`struct.entry`](#structentry) | Dot notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| [`struct[entry]`](#structentry) | Bracket notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| [`struct[idx]`](#structidx) | Bracket notation that serves as an alias for `struct_extract` from `TUPLE`s, using an index (1-based). |
| [`remap_struct(input, target_type, mapping, defaults)`](#remap_structinput-target_type-mapping-defaults) | Remap a `STRUCT`, `LIST`, or `MAP` value into the shape given by the type of `target_type`, renaming and reordering fields, descending into nested types, and filling missing fields from `defaults`. |
| [`row(any, ...)`](#rowany-) | Create a `TUPLE` containing the argument values. |
| [`struct_concat(structs...)`](#struct_concatstructs) | Merge the multiple `structs` into a single `STRUCT`. |
| [`struct_contains(struct, entry)`](#struct_containsstruct-entry) | Check if the `STRUCT` contains the specified entry. |
| [`struct_extract(struct, 'entry')`](#struct_extractstruct-entry) | Extract the named entry from the `STRUCT`. |
| [`struct_extract(struct, idx)`](#struct_extractstruct-idx) | Extract the entry from a `TUPLE` using an index (1-based). |
| [`struct_extract_at(struct, idx)`](#struct_extract_atstruct-idx) | Extract the entry from a `STRUCT` or `TUPLE` using an index (1-based). |
| [`struct_insert(struct, name := any, ...)`](#struct_insertstruct-name--any-) | Add field(s) to an existing `STRUCT`. |
| [`struct_keys(struct)`](#struct_keysstruct) | Return the names of the entries of a `STRUCT` as a list. |
| [`struct_pack(name := any, ...)`](#struct_packname--any-) | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. |
| [`struct_position(struct, entry)`](#struct_positionstruct-entry) | Return the index of the entry within the `STRUCT` (1-based), or `NULL` if not found. |
| [`struct_update(struct, name := any, ...)`](#struct_updatestruct-name--any-) | Add or update field(s) of an existing `STRUCT`. |
| [`struct_values(struct)`](#struct_valuesstruct) | Return the values of a `STRUCT` as a `TUPLE`. |

#### `struct.entry`

<div class="nostroke_table"></div>

| **Description** | Dot notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| **Example** | `({'i': 3, 's': 'string'}).i` |
| **Result** | `3` |

#### `struct[entry]`

<div class="nostroke_table"></div>

| **Description** | Bracket notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| **Example** | `({'i': 3, 's': 'string'})['i']` |
| **Result** | `3` |

#### `struct[idx]`

<div class="nostroke_table"></div>

| **Description** | Bracket notation that serves as an alias for `struct_extract` from `TUPLE`s, using an index (1-based). |
| **Example** | `(row(42, 84))[1]` |
| **Result** | `42` |

#### `remap_struct(input, target_type, mapping, defaults)`

<div class="nostroke_table"></div>

| **Description** | Remap an `input` value of type `STRUCT`, `LIST`, or `MAP` into the shape declared by the type of `target_type`, renaming and reordering fields, descending into nested types, and filling target fields that have no source counterpart from `defaults`. Only the type of `target_type` is used, not its value, so any value of the desired type works; a typed `NULL` literal (e.g. `NULL::STRUCT(v1 INT, v2 INT)`) is a convenient way to declare the target shape when no suitable value is at hand. `mapping` is a `STRUCT` keyed by target field name whose values name the source field to read from; `defaults` is a `STRUCT` of constant values for the remaining target fields. Every target field must be covered by either `mapping` or `defaults`. |
| **Example** | `remap_struct({'i': 1, 'j': 2}, NULL::STRUCT(v1 INT, v2 INT, v3 INT), {'v1': 'j', 'v3': 'i'}, {'v2': NULL::INTEGER})` |
| **Result** | `{'v1': 2, 'v2': NULL, 'v3': 1}` |

To remap a target field that is itself a `STRUCT`, give its mapping value as `ROW(source_field, {inner_mapping})`, and nest its defaults the same way. A `LIST`'s single child is addressed by the mapping key `'list'`, and a `MAP`'s children by the keys `'key'` and `'value'`.

#### `row(any, ...)`

<div class="nostroke_table"></div>

| **Description** | Create a `TUPLE` containing the argument values. |
| **Example** | `row(i, i % 4, i / 4)` |
| **Result** | `(10, 2, 2.5)` |

#### `struct_concat(structs...)`

<div class="nostroke_table"></div>

| **Description** | Merge the multiple `structs` into a single `STRUCT`. |
| **Example** | `struct_concat(struct_pack(i := 4), struct_pack(s := 'string'))` |
| **Result** | `{'i': 4, 's': string}` |

#### `struct_contains(struct, entry)`

<div class="nostroke_table"></div>

| **Description** | Check if the `STRUCT` contains the specified entry. |
| **Example** | `struct_contains(row(1, 2, 3), 2)` |
| **Result** | `true` |
| **Alias** | `struct_has` |

#### `struct_extract(struct, 'entry')`

<div class="nostroke_table"></div>

| **Description** | Extract the named entry from the `STRUCT`. |
| **Example** | `struct_extract({'i': 3, 'v2': 3, 'v3': 0}, 'i')` |
| **Result** | `3` |

#### `struct_extract(struct, idx)`

<div class="nostroke_table"></div>

| **Description** | Extract the entry from a `TUPLE` using an index (1-based). |
| **Example** | `struct_extract(row(42, 84), 1)` |
| **Result** | `42` |

#### `struct_extract_at(struct, idx)`

<div class="nostroke_table"></div>

| **Description** | Extract the entry from a `STRUCT` or `TUPLE` using an index (1-based). |
| **Example** | `struct_extract_at({'v1': 10, 'v2': 20, 'v3': 3}, 2)` |
| **Result** | `20` |

#### `struct_insert(struct, name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Add field(s) to an existing `STRUCT`. |
| **Example** | `struct_insert({'a': 1}, b := 2)` |
| **Result** | `{'a': 1, 'b': 2}` |

#### `struct_keys(struct)`

<div class="nostroke_table"></div>

| **Description** | Return the names of the entries of a `STRUCT` as a list. |
| **Example** | `struct_keys({'a': 1, 'b': 2})` |
| **Result** | `[a, b]` |

#### `struct_pack(name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. |
| **Example** | `struct_pack(i := 4, s := 'string')` |
| **Result** | `{'i': 4, 's': string}` |

#### `struct_position(struct, entry)`

<div class="nostroke_table"></div>

| **Description** | Return the index of the entry within the `STRUCT` (1-based), or `NULL` if not found. |
| **Example** | `struct_position(row(1, 2, 3), 2)` |
| **Result** | `2` |
| **Alias** | `struct_indexof` |

#### `struct_update(struct, name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Add or update field(s) of an existing `STRUCT`. |
| **Example** | `struct_update({'a': 1, 'b': 2}, b := 3, c := 4)` |
| **Result** | `{'a': 1, 'b': 3, 'c': 4}` |

#### `struct_values(struct)`

<div class="nostroke_table"></div>

| **Description** | Return the values of a `STRUCT` as a `TUPLE`. |
| **Example** | `struct_values({'a': 1, 'b': 2, 'c': 3})` |
| **Result** | `(1, 2, 3)` |
