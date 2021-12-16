---
layout: docu
title: Nested Types Overview
selected: Documentation/Data Types/Nested/Overview
expanded: Nested
---

This section describes functions and operators for examining and manipulating nested values. DuckDB supports three nested data types: lists, structs, and maps.

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:---|:---|:---|:---|:---|
| [LIST](/docs/sql/data_types/nested/list) | An ordered sequence of data values of the same type. | Each row must have the same data type within each LIST, but can have any number of elements. | [1, 2, 3] | INT[ ] |
| [STRUCT](/docs/sql/data_types/nested/struct) | A dictionary of multiple named values, where each key is a string, but the value can be a different type for each key. | Each row must have the same keys. | {'i': 42, 'j': 'a'} | STRUCT<i: INT, j: VARCHAR> |
| [MAP](/docs/sql/data_types/nested/map) | A dictionary of multiple named values, each key having the same type and each value having the same type. Keys and values can be any type and can be different types from one another. | Rows may have different keys. | map([1,2],['a','b']) | MAP<INT, VARCHAR> |

## Details
For details, please see the documentation pages for each nested data type:
1. [LIST Documentation](/docs/sql/data_types/nested/list)
2. [STRUCT Documentation](/docs/sql/data_types/nested/struct)
3. [MAP Documentation](/docs/sql/data_types/nested/map) 

## Functions
See [Nested Functions](/docs/sql/functions/nested).
