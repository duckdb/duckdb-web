---
layout: docu
title: Numeric Types
selected: Documentation/Data Types/Numeric
expanded: Data Types
---
## Integer Types
The types `TINYINT`, `SMALLINT`, `INTEGER`, `BIGINT` AND `HUGEINT` store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.

| Name | Aliases | Min | Max |
|:---|:---|---:|---:|
| `TINYINT` |   | -127 | 127 |
| `SMALLINT` | `INT2` | -32767 | 32767 |
| `INTEGER` | `INT`, `INT4`, `SIGNED` | -2147483647 | 2147483647 |
| `BIGINT` | `INT8` | -9223372036854775808 | 9223372036854775808 |
| `HUGEINT` | | -170141183460469231731687303715884105727 | 170141183460469231731687303715884105727 |

The type integer is the common choice, as it offers the best balance between range, storage size, and performance. The `SMALLINT` type is generally only used if disk space is at a premium. The `BIGINT` and `HUGEINT` types are designed to be used when the range of the integer type is insufficient.

## Fixed-Point Decimals
The data type `decimal` represents an exact fixed-point decimal value. When creating a value of type `decimal`, the `width` and `scale` can be specified to define which size of decimal values can be held in the field. The `width` field determines how many digits can be held, and the `scale` determines the amount of digits after the decimal point. For example, the type `DECIMAL(3,2)` can fit the value `1.23`, but cannot fit the value `12.3` or the value `1.234`. The default `width` and `scale` is `DECIMAL(18,3)`, if none are specified.

Internally, decimals are represented as integers depending on their specified width.

| Width | Internal | Size (Bytes) |
|:---|:---|---:|
| 1-4 | `int16` | 2 |
| 5-9 | `int32` | 4 |
| 10-18 | `int64` | 8 |
| 19-38 | `int128` | 16 |

Performance can be impacted by using too large decimals when not required. In particular decimal values with a width above 19 are very slow, as arithmetic involving the `int128` type is much more expensive than operations involving the `int32` or `int64` types. It is therefore recommended to stick with a width of `18` or below, unless there is a good reason for why this is insufficient.

## Floating-Point Types
The data types `REAL` and `DOUBLE` precision are inexact, variable-precision numeric types. In practice, these types are usually implementations of IEEE Standard 754 for Binary Floating-Point Arithmetic (single and double precision, respectively), to the extent that the underlying processor, operating system, and compiler support it.

| Name | Aliases | Description |
|:---|:---|:---|
| `REAL` | `FLOAT4` | single precision floating-point number (4 bytes)|
| `DOUBLE` | | double precision floating-point number (8 bytes) |

Inexact means that some values cannot be converted exactly to the internal format and are stored as approximations, so that storing and retrieving a value might show slight discrepancies. Managing these errors and how they propagate through calculations is the subject of an entire branch of mathematics and computer science and will not be discussed here, except for the following points:

* If you require exact storage and calculations (such as for monetary amounts), use the numeric type instead.
* If you want to do complicated calculations with these types for anything important, especially if you rely on certain behavior in boundary cases (infinity, underflow), you should evaluate the implementation carefully.
* Comparing two floating-point values for equality might not always work as expected.

On most platforms, the `REAL` type has a range of at least 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The `DOUBLE` type typically has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Values that are too large or too small will cause an error. Rounding might take place if the precision of an input number is too high. Numbers too close to zero that are not representable as distinct from zero will cause an underflow error.

In addition to ordinary numeric values, the floating-point types have several special values:

`Infinity`
`-Infinity`
`NaN`

These represent the IEEE 754 special values "infinity", "negative infinity", and "not-a-number", respectively. (On a machine whose floating-point arithmetic does not follow IEEE 754, these values will probably not work as expected.) When writing these values as constants in an SQL command, you must put quotes around them, for example: `UPDATE table SET x = '-Infinity'`. On input, these strings are recognized in a case-insensitive manner.

## Functions
See [Numeric Functions and Operators](/docs/sql/functions/numeric)
