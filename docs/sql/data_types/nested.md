---
layout: docu
title: Nested Types
selected: Documentation/Data Types/Nested
expanded: Data Types
---
| Name | Description |
|:---|:---|
| LIST | An ordered sequence of data values of the same type. |
| STRUCT | A dictionary of data values. |

A `LIST` column can have values with different lengths, but they must all have the same underlying type. `LIST`s are typically used to store arrays of numbers.

A `STRUCT` column must have the same entry names and data types for each value. The values are looked up in the `STRUCT` using string entry names. `STRUCT`s are typically used to nest rows into single columns.

## Operators
See [Nested Functions](../functions/nested).
