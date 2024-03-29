---
layout: docu
title: Numeric Types
blurb: Numeric types are used to store numbers, and come in different shapes and sizes.
---

## Integer Types

The types `TINYINT`, `SMALLINT`, `INTEGER`, `BIGINT` and `HUGEINT` store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.
The types `UTINYINT`, `USMALLINT`, `UINTEGER`, `UBIGINT` and `UHUGEINT` store whole unsigned numbers. Attempts to store negative numbers or values outside of the allowed range will result in an error

| Name | Aliases | Min | Max |
|:--|:--|----:|----:|
| `TINYINT` | `INT1` | -128 | 127 |
| `SMALLINT` | `INT2`, `SHORT` | -32768 | 32767 |
| `INTEGER` | `INT4`, `INT`, `SIGNED` | -2147483648 | 2147483647 |
| `BIGINT` | `INT8`, `LONG` | -9223372036854775808 | 9223372036854775807 |
| `HUGEINT` | - | -170141183460469231731687303715884105728 | 170141183460469231731687303715884105727 |
| `UTINYINT` | - | 0 | 255 |
| `USMALLINT` | -| 0 | 65535 |
| `UINTEGER` | - | 0 | 4294967295 |
| `UBIGINT` | - | 0 | 18446744073709551615 |
| `UHUGEINT` | - | 0 | 340282366920938463463374607431768211455 |

The type integer is the common choice, as it offers the best balance between range, storage size, and performance. The `SMALLINT` type is generally only used if disk space is at a premium. The `BIGINT` and `HUGEINT` types are designed to be used when the range of the integer type is insufficient.

## Fixed-Point Decimals

The data type `DECIMAL(WIDTH, SCALE)` (also available under the alias `NUMERIC(WIDTH, SCALE)`) represents an exact fixed-point decimal value. When creating a value of type `DECIMAL`, the `WIDTH` and `SCALE` can be specified to define which size of decimal values can be held in the field. The `WIDTH` field determines how many digits can be held, and the `scale` determines the amount of digits after the decimal point. For example, the type `DECIMAL(3, 2)` can fit the value `1.23`, but cannot fit the value `12.3` or the value `1.234`. The default `WIDTH` and `SCALE` is `DECIMAL(18, 3)`, if none are specified.

Internally, decimals are represented as integers depending on their specified width.

<div class="narrow_table"></div>

| Width | Internal | Size (Bytes) |
|:---|:---|---:|
| 1-4 | `INT16` | 2 |
| 5-9 | `INT32` | 4 |
| 10-18 | `INT64` | 8 |
| 19-38 | `INT128` | 16 |

Performance can be impacted by using too large decimals when not required. In particular decimal values with a width above 19 are slow, as arithmetic involving the `INT128` type is much more expensive than operations involving the `INT32` or `INT64` types. It is therefore recommended to stick with a width of `18` or below, unless there is a good reason for why this is insufficient.

## Floating-Point Types

The data types `REAL` and `DOUBLE` precision are variable-precision numeric types. In practice, these types are usually implementations of IEEE Standard 754 for Binary Floating-Point Arithmetic (single and double precision, respectively), to the extent that the underlying processor, operating system, and compiler support it.

<div class="narrow_table"></div>

| Name | Aliases | Description |
|:--|:--|:--------|
| `REAL` | `FLOAT4`, `FLOAT` | single precision floating-point number (4 bytes) |
| `DOUBLE` | `FLOAT8` | double precision floating-point number (8 bytes) |

Like for fixed-point data types, conversion from literals or casts from other datatypes to floating-point types stores inputs that cannot be represented exactly as approximations. However, it can be harder to predict what inputs are affected by this. For example, it is not surprising that `1.3::DECIMAL(1, 0) - 0.7::DECIMAL(1, 0) != 0.6::DECIMAL(1, 0)` but it may he surprising that `1.3::REAL - 0.7::REAL != 0.6::REAL`.

Additionally, whereas multiplication, addition, and subtraction of fixed-point decimal data types is exact, these operations are only approximate on floating-point binary data types.

For more complex mathematical operations, however, floating-point arithmetic is used internally and more precise results can be obtained if intermediate steps are _not_ cast to fixed point formats of the same width as in- and outputs. For example, `(10::REAL / 3::REAL)::REAL * 3 = 10` whereas (10::DECIMAL(18, 3) / 3::DECIMAL(18, 3))::DECIMAL(18, 3) * 3 = 9.999`. 

In general, we advise that:

* If you require exact storage of numbers with a known number of decimal digits and require exact additions, subtractions, and multiplications (such as for monetary amounts), use the [`DECIMAL` data type](#fixed-point-decimals) or its `NUMERIC` alias instead.
* If you want to do fast or complicated calculations, the floating-point data types may be more appropriate. However, if you use the results for anything important, you should evaluate your implementation carefully for corner cases (ranges, infinities, underflows, invalid operations) that may be handled in a non-standard manner by your platform and you should familiarize yourself with common floating-point pitfalls. The article ["What Every Computer Scientist Should Know About
Floating-Point Arithmetic" by David Goldberg](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) and [the floating point series on Bruce Dawson's blog](https://randomascii.wordpress.com/2017/06/19/sometimes-floating-point-math-is-perfect/) provide excellent starting points. 

On most platforms, the `REAL` type has a range of at least 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The `DOUBLE` type typically has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Positive numbers outside of these ranges (and negative numbers ourside the mirrored ranges) may cause errors on some platforms but will usually be converted to zero or infinity, respectively. 

In addition to ordinary numeric values, the floating-point types have several special values:

* `Infinity`
* `-Infinity`
* `NaN`

These represent the IEEE 754 special values "infinity", "negative infinity", and "not-a-number", respectively. (On a machine whose floating-point arithmetic does not follow IEEE 754, these values will probably not work as expected.) When writing these values as constants in an SQL command, you must put quotes around them, for example: `UPDATE table SET x = '-Infinity'`. On input, these strings are recognized in a case-insensitive manner.

## Universally Unique Identifiers (`UUID`s)

DuckDB supports universally unique identifiers (UUIDs) through the `UUID` type. These use 128 bits and are represented internally as `HUGEINT` values.
When printed, they are shown with hexadecimal characters, separated by dashes as follows: `⟨8 characters⟩-⟨4 characters⟩-⟨4 characters⟩-⟨4 characters⟩-⟨12 characters⟩` (using 36 characters in total). For example, `4ac7a9e9-607c-4c8a-84f3-843f0191e3fd` is a valid UUID.

To generate a new UUID, use the [`uuid()` utility function](../functions/utility#utility-functions).

## Functions

See [Numeric Functions and Operators](../../sql/functions/numeric).
