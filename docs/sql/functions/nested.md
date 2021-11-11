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
| *`list`*`[`*`begin`*`:`*`end`*`]` | Alias for `array_slice`. Missing arguments are interprete as `NULL`s. | `l[1:2]` | `[5, 6]` |
| `array_length(`*`list`*`)` | Return the length of the list. |  `array_length([1, 2, 3])` | `3` |
| `len(`*`list`*`)` | Alias for `array_length`. | `len([1, 2, 3])` | `3` |
| `unnest(`*`list`*`)` | Unnests a list by one level. Note that this is a special function that alters the cardinality of the result. See the [UNNEST page](/docs/sql/query_syntax/unnest) for more details.  | `unnest([1, 2, 3])` | `1`, `2`, `3` |
| `list_concat(`*`list1`*`, `*`list2`*`)` | Concatenates two lists. | `list_concat([2, 3], [4, 5, 6])` | `[2, 3, 4, 5, 6]` |
| `list_cat(`*`list1`*`, `*`list2`*`)` | Alias for `list_concat`. | `list_cat([2, 3], [4, 5, 6])` | `[2, 3, 4, 5, 6`] |
| `array_concat(`*`list1`*`, `*`list2`*`)` | Alias for `list_concat`. | `array_concat([2, 3], [4, 5, 6])` | `[2, 3, 4, 5, 6`] |
| `array_cat(`*`list1`*`, `*`list2`*`)` | Alias for `list_concat`. | `array_cat([2, 3], [4, 5, 6])` | `[2, 3, 4, 5, 6`] |
| `list_append(`*`list`*`, `*`element`*`)` | Appends `element` to `list`. | `list_append([2, 3], 4)` | `[2, 3, 4`] |
| `list_prepend(`*`list`*`, `*`element`*`)` | Prepends `element` to `list`. | `list_prepend(3, [4, 5, 6])` | `[3, 4, 5, 6`] |

## Struct Functions

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`struct`*`[`*`entry`*`]` | Alias for `struct_extract`. | `struct_extract(s, 'i')` | `4` |
| `row(`*`any`*`, ...)` | Create a `STRUCT` containing the argument values. If the values are column references, the entry name will be the column name; otherwise it will be the string `'vN'` where `N` is the (1-based) position of the argument. | `row(i, i % 4, i / 4)` | `{'i': 3, 'v2': 3, 'v3': 0}`|
| `struct_extract(`*`struct`*`, `*`'entry'`*`)` | Extract the named entry from the struct. | `struct_extract(s, 'i')` | `4` |
| `struct_pack(`*`name := any`*`, ...)` | Create a `STRUCT` containing the argument values. The entry name will be the bound variable name. | `struct_pack(i := 4, s := 'string')` | `{'i': 3, 's': 'string'}`|

## Range Functions

The functions *`range`* and *`generate_series`* create a list of values in the range between `start` and `stop`.
The `start` parameter is inclusive.
For the `range` function, the `stop` parameter is exclusive, while for `generate_series`, it is inclusive.

Based on the number of arguments, the following variants exist:

* `range(`*`start`*`, `*`stop`*`, `*`step`*`)`
* `range(`*`start`*`, `*`stop`*`)`
* `range(`*`stop`*`)`
* `generate_series(`*`start`*`, `*`stop`*`, `*`step`*`)`
* `generate_series(`*`start`*`, `*`stop`*`)`
* `generate_series(`*`stop`*`)`

The default value of `start` is 0 and the default value of `step` is 1.

```sql
SELECT range(5);
-- [0, 1, 2, 3, 4]

SELECT range(2, 5);
-- [2, 3, 4]

SELECT range(2, 5, 3);
-- [2]

SELECT generate_series(5);
-- [0, 1, 2, 3, 4, 5]

SELECT generate_series(2, 5);
-- [2, 3, 4, 5]

SELECT generate_series(2, 5, 3);
-- [2, 5]
```

Date ranges are also supported:

```
SELECT * FROM range(date '1992-01-01', date '1992-03-01', interval '1' month);

┌─────────────────────┐
│        range        │
├─────────────────────┤
│ 1992-01-01 00:00:00 │
│ 1992-02-01 00:00:00 │
└─────────────────────┘
```

## Related Functions

There are also [aggregate functions](../aggregates) `list` and `histogram` that produces lists and lists of structs.
