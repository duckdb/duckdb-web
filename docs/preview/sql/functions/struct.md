---
layout: docu
redirect_from:
- /docs/sql/functions/struct
title: Struct Functions
---

<!-- markdownlint-disable MD001 -->

| Name | Description |
|:--|:-------|
| [`struct.entry`](#structentry) | Dot notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| [`struct[entry]`](#structentry) | Bracket notation that serves as an alias for `struct_extract` from named `STRUCT`s. |
| [`struct[idx]`](#structidx) | Bracket notation that serves as an alias for `struct_extract` from unnamed `STRUCT`s (tuples), using an index (1-based). |
| [`row(any, ...)`](#rowany-) | Create an unnamed `STRUCT` (tuple) containing the argument values. |
| [`struct_concat(structs...)`](#struct_concatstructs) | Merge the multiple `structs` into a single `STRUCT`. |
| [`struct_extract(struct, 'entry')`](#struct_extractstruct-entry) | Extract the named entry from the `STRUCT`. |
| [`struct_extract(struct, idx)`](#struct_extractstruct-idx) | Extract the entry from an unnamed `STRUCT` (tuple) using an index (1-based). |
| [`struct_extract_at(struct, idx)`](#struct_extract_atstruct-idx) | Extract the entry from a `STRUCT` (tuple) using an index (1-based). |
| [`struct_insert(struct, name := any, ...)`](#struct_insertstruct-name--any-) | Add field(s) to an existing `STRUCT`. |
| [`struct_pack(name := any, ...)`](#struct_packname--any-) | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. |
| [`struct_update(struct, name := any, ...)`](#struct_updatestruct-name--any-) | Add or update field(s) of an existing `STRUCT`. |

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

| **Description** | Bracket notation that serves as an alias for `struct_extract` from unnamed `STRUCT`s (tuples), using an index (1-based). |
| **Example** | `(row(42, 84))[1]` |
| **Result** | `42` |

#### `row(any, ...)`

<div class="nostroke_table"></div>

| **Description** | Create an unnamed `STRUCT` (tuple) containing the argument values. |
| **Example** | `row(i, i % 4, i / 4)` |
| **Result** | `(10, 2, 2.5)` |

#### `struct_concat(structs...)`

<div class="nostroke_table"></div>

| **Description** | Merge the multiple `structs` into a single `STRUCT`. |
| **Example** | `struct_concat(struct_pack(i := 4), struct_pack(s := 'string'))` |
| **Result** | `{'i': 4, 's': string}` |

#### `struct_extract(struct, 'entry')`

<div class="nostroke_table"></div>

| **Description** | Extract the named entry from the `STRUCT`. |
| **Example** | `struct_extract({'i': 3, 'v2': 3, 'v3': 0}, 'i')` |
| **Result** | `3` |

#### `struct_extract(struct, idx)`

<div class="nostroke_table"></div>

| **Description** | Extract the entry from an unnamed `STRUCT` (tuple) using an index (1-based). |
| **Example** | `struct_extract(row(42, 84), 1)` |
| **Result** | `42` |

#### `struct_extract_at(struct, idx)`

<div class="nostroke_table"></div>

| **Description** | Extract the entry from a `STRUCT` (tuple) using an index (1-based). |
| **Example** | `struct_extract_at({'v1': 10, 'v2': 20, 'v3': 3}, 20)` |
| **Result** | `20` |

#### `struct_insert(struct, name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Add field(s) to an existing `STRUCT`. |
| **Example** | `struct_insert({'a': 1}, b := 2)` |
| **Result** | `{'a': 1, 'b': 2}` |

#### `struct_pack(name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. |
| **Example** | `struct_pack(i := 4, s := 'string')` |
| **Result** | `{'i': 4, 's': string}` |

#### `struct_update(struct, name := any, ...)`

<div class="nostroke_table"></div>

| **Description** | Add or update field(s) of an existing `STRUCT`. |
| **Example** | `struct_insert({'a': 1, 'b': 2}, b := 3, c := 4)` |
| **Result** | `{'a': 1, 'b': 3, 'c': 4}` |
