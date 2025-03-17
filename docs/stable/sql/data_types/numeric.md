---
blurb: Numeric types are used to store numbers, and come in different shapes and sizes.
layout: docu
redirect_from:
- /docs/sql/data_types/numeric
title: Numeric Types
---

## Integer Types

The types `TINYINT`, `SMALLINT`, `INTEGER`, `BIGINT` and `HUGEINT` store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.
The types `UTINYINT`, `USMALLINT`, `UINTEGER`, `UBIGINT` and `UHUGEINT` store whole unsigned numbers. Attempts to store negative numbers or values outside of the allowed range will result in an error.

<div class="center_aligned_header_table"></div>

| Name        | Aliases                          |     Min |       Max | Size in bytes |
| :---------- | :------------------------------- | ------: | --------: | ------------: |
| `TINYINT`   | `INT1`                           |   - 2^7 |   2^7 - 1 |             1 |
| `SMALLINT`  | `INT2`, `INT16` `SHORT`          |  - 2^15 |  2^15 - 1 |             2 |
| `INTEGER`   | `INT4`, `INT32`, `INT`, `SIGNED` |  - 2^31 |  2^31 - 1 |             4 |
| `BIGINT`    | `INT8`, `INT64` `LONG`           |  - 2^63 |  2^63 - 1 |             8 |
| `HUGEINT`   | `INT128`                         | - 2^127 | 2^127 - 1 |            16 |
| `UTINYINT`  | -                                |       0 |   2^8 - 1 |             1 |
| `USMALLINT` | -                                |       0 |  2^16 - 1 |             2 |
| `UINTEGER`  | -                                |       0 |  2^32 - 1 |             4 |
| `UBIGINT`   | -                                |       0 |  2^64 - 1 |             8 |
| `UHUGEINT`  | -                                |       0 | 2^128 - 1 |            16 |

The type integer is the common choice, as it offers the best balance between range, storage size, and performance. The `SMALLINT` type is generally only used if disk space is at a premium. The `BIGINT` and `HUGEINT` types are designed to be used when the range of the integer type is insufficient.

## Variable Integer

The previously mentioned integer types all have in common that the numbers in the minimum and maximum range all have the same storage size, `UTINYINT` is 1 byte, `SMALLINT` is 2 bytes, etc.
But sometimes you need numbers that are even bigger than what is supported by a `HUGEINT`! For these situations the `VARINT` type can come in handy, as the `VARINT` type has a *much* bigger limit (the value can consist of up to 1,262,612 digits).
The minimum storage size for a `VARINT` is 4 bytes, every digit takes up an extra bit, rounded up to 8 (12 digits take 12 bits, rounded up to 16, becomes two extra bytes).

Both negative and positive values are supported by the `VARINT` type.

## Fixed-Point Decimals

The data type `DECIMAL(WIDTH, SCALE)` (also available under the alias `NUMERIC(WIDTH, SCALE)`) represents an exact fixed-point decimal value. When creating a value of type `DECIMAL`, the `WIDTH` and `SCALE` can be specified to define which size of decimal values can be held in the field. The `WIDTH` field determines how many digits can be held, and the `scale` determines the amount of digits after the decimal point. For example, the type `DECIMAL(3, 2)` can fit the value `1.23`, but cannot fit the value `12.3` or the value `1.234`. The default `WIDTH` and `SCALE` is `DECIMAL(18, 3)`, if none are specified.

Addition, subtraction, and multiplication of two fixed-point decimals returns another fixed-point decimal with the required `WIDTH` and `SCALE` to contain the exact result, or throws an error if the required `WIDTH` would exceed the maximal supported `WIDTH`, which is currently 38.

Division of fixed-point decimals does not typically produce numbers with finite decimal expansion. Therefore, DuckDB uses approximate [floating-point arithmetic](#floating-point-types) for all divisions that involve fixed-point decimals and accordingly returns floating-point data types.

Internally, decimals are represented as integers depending on their specified `WIDTH`.

| Width | Internal | Size (bytes) |
| :---- | :------- | -----------: |
| 1-4   | `INT16`  |            2 |
| 5-9   | `INT32`  |            4 |
| 10-18 | `INT64`  |            8 |
| 19-38 | `INT128` |           16 |

Performance can be impacted by using too large decimals when not required. In particular decimal values with a width above 19 are slow, as arithmetic involving the `INT128` type is much more expensive than operations involving the `INT32` or `INT64` types. It is therefore recommended to stick with a `WIDTH` of `18` or below, unless there is a good reason for why this is insufficient.

## Floating-Point Types

The data types `FLOAT` and `DOUBLE` precision are variable-precision numeric types. In practice, these types are usually implementations of IEEE Standard 754 for Binary Floating-Point Arithmetic (single and double precision, respectively), to the extent that the underlying processor, operating system, and compiler support it.

| Name     | Aliases          | Description                                      |
| :------- | :--------------- | :----------------------------------------------- |
| `FLOAT`  | `FLOAT4`, `REAL` | Single precision floating-point number (4 bytes) |
| `DOUBLE` | `FLOAT8`         | Double precision floating-point number (8 bytes) |

Like for fixed-point data types, conversion from literals or casts from other datatypes to floating-point types stores inputs that cannot be represented exactly as approximations. However, it can be harder to predict what inputs are affected by this. For example, it is not surprising that `1.3::DECIMAL(1, 0) - 0.7::DECIMAL(1, 0) != 0.6::DECIMAL(1, 0)` but it may he surprising that `1.3::FLOAT - 0.7::FLOAT != 0.6::FLOAT`.

Additionally, whereas multiplication, addition, and subtraction of fixed-point decimal data types is exact, these operations are only approximate on floating-point binary data types.

For more complex mathematical operations, however, floating-point arithmetic is used internally and more precise results can be obtained if intermediate steps are _not_ cast to fixed point formats of the same width as in- and outputs. For example, `(10::FLOAT / 3::FLOAT)::FLOAT * 3 = 10` whereas `(10::DECIMAL(18, 3) / 3::DECIMAL(18, 3))::DECIMAL(18, 3) * 3 = 9.999`.

In general, we advise that:

- If you require exact storage of numbers with a known number of decimal digits and require exact additions, subtractions, and multiplications (such as for monetary amounts), use the [`DECIMAL` data type](#fixed-point-decimals) or its `NUMERIC` alias instead.
- If you want to do fast or complicated calculations, the floating-point data types may be more appropriate. However, if you use the results for anything important, you should evaluate your implementation carefully for corner cases (ranges, infinities, underflows, invalid operations) that may be handled differently from what you expect and you should familiarize yourself with common floating-point pitfalls. The article [“What Every Computer Scientist Should Know About Floating-Point Arithmetic” by David Goldberg](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) and the [floating point series on Bruce Dawson's blog](https://randomascii.wordpress.com/2017/06/19/sometimes-floating-point-math-is-perfect/) provide excellent starting points.

On most platforms, the `FLOAT` type has a range of at least 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The `DOUBLE` type typically has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Positive numbers outside of these ranges (and negative numbers ourside the mirrored ranges) may cause errors on some platforms but will usually be converted to zero or infinity, respectively.

In addition to ordinary numeric values, the floating-point types have several special values representing IEEE 754 special values:

- `Infinity`: infinity
- `-Infinity`: negative infinity
- `NaN`: not a number

On machines with the required CPU/FPU support, DuckDB follows the IEEE 754 specification regarding these special values, with two exceptions:

- `NaN` compares equal to `NaN` and greater than any other floating point number.
- Some floating point functions, like `sqrt` / `sin` / `asin` throw errors rather than return `NaN` for values outside their ranges of definition.

To insert these values as literals in a SQL command, you must put quotes around them, you may abbreviate `Infinity` as `Inf`, and you may use any capitalization. For example:

```sql
SELECT
    sqrt(2) > '-inf',
    'nan' > sqrt(2);
```

<div class="monospace_table"></div>

| `(sqrt(2) > '-inf')` | `('nan' > sqrt(2))` |
|---------------------:|--------------------:|
|                 true |                true |

## Universally Unique Identifiers (`UUID`s)

DuckDB supports universally unique identifiers (UUIDs) through the `UUID` type. These use 128 bits and are represented internally as `HUGEINT` values.
When printed, they are shown with lowercase hexadecimal characters, separated by dashes as follows: `⟨8 characters⟩-⟨4 characters⟩-⟨4 characters⟩-⟨4 characters⟩-⟨12 characters⟩`{:.language-sql .highlight} (using 36 characters in total including the dashes). For example, `4ac7a9e9-607c-4c8a-84f3-843f0191e3fd` is a valid UUID.

To generate a new UUID, use the [`uuid()` utility function]({% link docs/stable/sql/functions/utility.md %}#uuid).

## Functions

See [Numeric Functions and Operators]({% link docs/stable/sql/functions/numeric.md %}).
