---
layout: docu
redirect_from:
- /docs/sql/functions/union
title: Union Functions
---

<!-- markdownlint-disable MD001 -->

| Name | Description |
|:--|:-------|
| [`union.tag`](#uniontag) | Dot notation serves as an alias for `union_extract`. |
| [`union_extract(union, 'tag')`](#union_extractunion-tag) | Extract the value with the named tags from the union. `NULL` if the tag is not currently selected. |
| [`union_value(tag := any)`](#union_valuetag--any) | Create a single member `UNION` containing the argument value. The tag of the value will be the bound variable name. |
| [`union_tag(union)`](#union_tagunion) | Retrieve the currently selected tag of the union as an [Enum]({% link docs/stable/sql/data_types/enum.md %}). |

#### `union.tag`

<div class="nostroke_table"></div>

| **Description** | Dot notation serves as an alias for `union_extract`. |
| **Example** | `(union_value(k := 'hello')).k` |
| **Result** | `string` |

#### `union_extract(union, 'tag')`

<div class="nostroke_table"></div>

| **Description** | Extract the value with the named tags from the union. `NULL` if the tag is not currently selected. |
| **Example** | `union_extract(s, 'k')` |
| **Result** | `hello` |

#### `union_value(tag := any)`

<div class="nostroke_table"></div>

| **Description** | Create a single member `UNION` containing the argument value. The tag of the value will be the bound variable name. |
| **Example** | `union_value(k := 'hello')` |
| **Result** | `'hello'::UNION(k VARCHAR)` |

#### `union_tag(union)`

<div class="nostroke_table"></div>

| **Description** | Retrieve the currently selected tag of the union as an [Enum]({% link docs/stable/sql/data_types/enum.md %}). |
| **Example** | `union_tag(union_value(k := 'foo'))` |
| **Result** | `'k'` |
