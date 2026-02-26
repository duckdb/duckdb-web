---
layout: docu
title: Numeric Functions
---

<!-- markdownlint-disable MD001 -->

## Numeric Operators

The table below shows the available mathematical operators for [numeric types]({% link docs/preview/sql/data_types/numeric.md %}).

<!-- markdownlint-disable MD056 -->

| Operator | Description | Example | Result |
|-|-----|--|-|
| `+`      | Addition                  | `2 + 3`   | `5`   |
| `-`      | Subtraction               | `2 - 3`   | `-1`  |
| `*`      | Multiplication            | `2 * 3`   | `6`   |
| `/`      | Float division            | `5 / 2`   | `2.5` |
| `//`     | Division                  | `5 // 2`  | `2`   |
| `%`      | Modulo (remainder)        | `5 % 4`   | `1`   |
| `**`     | Exponent                  | `3 ** 4`  | `81`  |
| `^`      | Exponent (alias for `**`) | `3 ^ 4`   | `81`  |
| `&`      | Bitwise AND               | `91 & 15` | `11`  |
| `|`      | Bitwise OR                | `32 | 3`  | `35`  |
| `<<`     | Bitwise shift left        | `1 << 4`  | `16`  |
| `>>`     | Bitwise shift right       | `8 >> 2`  | `2`   |
| `~`      | Bitwise negation          | `~15`     | `-16` |
| `!`      | Factorial of `x`          | `4!`      | `24`  |

<!-- markdownlint-enable MD056 -->

### Division and Modulo Operators

There are two division operators: `/` and `//`.
They are equivalent when at least one of the operands is a `FLOAT` or a `DOUBLE`.
When both operands are integers, `/` performs floating points division (`5 / 2 = 2.5`) while `//` performs integer division (`5 // 2 = 2`).

### Supported Types

The modulo, bitwise, negation, and factorial operators work only on integral data types,
whereas the others are available for all numeric data types.

## Numeric Functions

The table below shows the available mathematical functions.

| Name | Description |
|:--|:-------|
| [`@(x)`](#x) | Absolute value. Parentheses are optional if `x` is a column name. |
| [`abs(x)`](#absx) | Absolute value. |
| [`acos(x)`](#acosx) | Computes the inverse cosine of `x`. |
| [`acosh(x)`](#acoshx) | Computes the inverse hyperbolic cosine of `x`. |
| [`add(x, y)`](#addx-y) | Alias for `x + y`. |
| [`asin(x)`](#asinx) | Computes the inverse sine of `x`. |
| [`asinh(x)`](#asinhx) | Computes the inverse hyperbolic sine of `x`. |
| [`atan(x)`](#atanx) | Computes the inverse tangent of `x`. |
| [`atanh(x)`](#atanhx) | Computes the inverse hyperbolic tangent of `x`. |
| [`atan2(y, x)`](#atan2y-x) | Computes the inverse tangent of `(y, x)`. |
| [`bit_count(x)`](#bit_countx) | Returns the number of bits that are set. |
| [`cbrt(x)`](#cbrtx) | Returns the cube root of the number. |
| [`ceil(x)`](#ceilx) | Rounds the number up. |
| [`ceiling(x)`](#ceilingx) | Rounds the number up. Alias of `ceil`. |
| [`cos(x)`](#cosx) | Computes the cosine of `x`. |
| [`cot(x)`](#cotx) | Computes the cotangent of `x`. |
| [`degrees(x)`](#degreesx) | Converts radians to degrees. |
| [`divide(x, y)`](#dividex-y) | Alias for `x // y`. |
| [`even(x)`](#evenx) | Round to next even number by rounding away from zero. |
| [`exp(x)`](#expx) | Computes `e ** x`. |
| [`factorial(x)`](#factorialx) | See the `!` operator. Computes the product of the current integer and all integers below it. |
| [`fdiv(x, y)`](#fdivx-y) | Performs integer division (`x // y`) but returns a `DOUBLE` value. |
| [`floor(x)`](#floorx) | Rounds the number down. |
| [`fmod(x, y)`](#fmodx-y) | Calculates the modulo value. Always returns a `DOUBLE` value. |
| [`gamma(x)`](#gammax) | Interpolation of the factorial of `x - 1`. Fractional inputs are allowed. |
| [`gcd(x, y)`](#gcdx-y) | Computes the greatest common divisor of `x` and `y`. |
| [`greatest_common_divisor(x, y)`](#greatest_common_divisorx-y) | Computes the greatest common divisor of `x` and `y`. |
| [`greatest(x1, x2, ...)`](#greatestx1-x2-) | Selects the largest value. |
| [`isfinite(x)`](#isfinitex) | Returns true if the floating point value is finite, false otherwise. |
| [`isinf(x)`](#isinfx) | Returns true if the floating point value is infinite, false otherwise. |
| [`isnan(x)`](#isnanx) | Returns true if the floating point value is not a number, false otherwise. |
| [`lcm(x, y)`](#lcmx-y) | Computes the least common multiple of `x` and `y`. |
| [`least_common_multiple(x, y)`](#least_common_multiplex-y) | Computes the least common multiple of `x` and `y`. |
| [`least(x1, x2, ...)`](#leastx1-x2-) | Selects the smallest value. |
| [`lgamma(x)`](#lgammax) | Computes the log of the `gamma` function. |
| [`ln(x)`](#lnx) | Computes the natural logarithm of `x`. |
| [`log(x)`](#logx) | Computes the base-10 logarithm of `x`. |
| [`log10(x)`](#log10x) | Alias of `log`. Computes the base-10 logarithm of `x`. |
| [`log2(x)`](#log2x) | Computes the base-2 log of `x`. |
| [`multiply(x, y)`](#multiplyx-y) | Alias for `x * y`. |
| [`nextafter(x, y)`](#nextafterx-y) | Return the next floating point value after `x` in the direction of `y`. |
| [`pi()`](#pi) | Returns the value of pi. |
| [`pow(x, y)`](#powx-y) | Computes `x` to the power of `y`. |
| [`power(x, y)`](#powerx-y) | Alias of `pow`. Computes `x` to the power of `y`. |
| [`radians(x)`](#radiansx) | Converts degrees to radians. |
| [`random()`](#random) | Returns a random number `x` in the range `0.0 <= x < 1.0`. |
| [`round_even(v NUMERIC, s INTEGER)`](#round_evenv-numeric-s-integer) | Alias of `roundbankers(v, s)`. Round to `s` decimal places using the [_rounding half to even_ rule](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even). Values `s < 0` are allowed. |
| [`round(v NUMERIC, s INTEGER)`](#roundv-numeric-s-integer) | Round to `s` decimal places. Values `s < 0` are allowed. |
| [`setseed(x)`](#setseedx) | Sets the seed to be used for the random function. |
| [`sign(x)`](#signx) | Returns the sign of `x` as -1, 0 or 1. |
| [`signbit(x)`](#signbitx) | Returns whether the signbit is set or not. |
| [`sin(x)`](#sinx) | Computes the sin of `x`. |
| [`sqrt(x)`](#sqrtx) | Returns the square root of the number. |
| [`subtract(x, y)`](#subtractx-y) | Alias for `x - y`. |
| [`tan(x)`](#tanx) | Computes the tangent of `x`. |
| [`trunc(x)`](#truncx) | Truncates the number. |
| [`xor(x, y)`](#xorx-y) | Bitwise XOR. |

#### `@(x)`

<div class="nostroke_table"></div>

| **Description** | Absolute value. Parentheses are optional if `x` is a column name. |
| **Example** | `@(-17.4)` |
| **Result** | `17.4` |
| **Alias** | `abs` |

#### `abs(x)`

<div class="nostroke_table"></div>

| **Description** | Absolute value. |
| **Example** | `abs(-17.4)` |
| **Result** | `17.4` |
| **Alias** | `@` |

#### `acos(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse cosine of `x`. |
| **Example** | `acos(0.5)` |
| **Result** | `1.0471975511965976` |

#### `acosh(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse hyperbolic cosine of `x`. |
| **Example** | `acosh(1.5)` |
| **Result** | `0.9624236501192069` |

#### `add(x, y)`

<div class="nostroke_table"></div>

| **Description** | Alias for `x + y`. |
| **Example** | `add(2, 3)` |
| **Result** | `5` |

#### `asin(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse sine of `x`. |
| **Example** | `asin(0.5)` |
| **Result** | `0.5235987755982989` |

#### `asinh(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse hyperbolic sine of `x`. |
| **Example** | `asinh(0.5)` |
| **Result** | `0.48121182505960347` |

#### `atan(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse tangent of `x`. |
| **Example** | `atan(0.5)` |
| **Result** | `0.4636476090008061` |

#### `atanh(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse hyperbolic tangent of `x`. |
| **Example** | `atanh(0.5)` |
| **Result** | `0.5493061443340549` |

#### `atan2(y, x)`

<div class="nostroke_table"></div>

| **Description** | Computes the inverse tangent (y, x). |
| **Example** | `atan2(0.5, 0.5)` |
| **Result** | `0.7853981633974483` |

#### `bit_count(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of bits that are set. |
| **Example** | `bit_count(31)` |
| **Result** | `5` |

#### `cbrt(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the cube root of the number. |
| **Example** | `cbrt(8)` |
| **Result** | `2` |

#### `ceil(x)`

<div class="nostroke_table"></div>

| **Description** | Rounds the number up. |
| **Example** | `ceil(17.4)` |
| **Result** | `18` |

#### `ceiling(x)`

<div class="nostroke_table"></div>

| **Description** | Rounds the number up. Alias of `ceil`. |
| **Example** | `ceiling(17.4)` |
| **Result** | `18` |

#### `cos(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the cosine of `x`. |
| **Example** | `cos(pi() / 3)` |
| **Result** | `0.5000000000000001 ` |

#### `cot(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the cotangent of `x`. |
| **Example** | `cot(0.5)` |
| **Result** | `1.830487721712452` |

#### `degrees(x)`

<div class="nostroke_table"></div>

| **Description** | Converts radians to degrees. |
| **Example** | `degrees(pi())` |
| **Result** | `180` |

#### `divide(x, y)`

<div class="nostroke_table"></div>

| **Description** | Alias for `x // y`. |
| **Example** | `divide(5, 2)` |
| **Result** | `2` |

#### `even(x)`

<div class="nostroke_table"></div>

| **Description** | Round to next even number by rounding away from zero. |
| **Example** | `even(2.9)` |
| **Result** | `4` |

#### `exp(x)`

<div class="nostroke_table"></div>

| **Description** | Computes `e ** x`. |
| **Example** | `exp(0.693)` |
| **Result** | `2` |

#### `factorial(x)`

<div class="nostroke_table"></div>

| **Description** | See the `!` operator. Computes the product of the current integer and all integers below it. |
| **Example** | `factorial(4)` |
| **Result** | `24` |

#### `fdiv(x, y)`

<div class="nostroke_table"></div>

| **Description** | Performs integer division (`x // y`) but returns a `DOUBLE` value. |
| **Example** | `fdiv(5, 2)` |
| **Result** | `2.0` |

#### `floor(x)`

<div class="nostroke_table"></div>

| **Description** | Rounds the number down. |
| **Example** | `floor(17.4)` |
| **Result** | `17` |

#### `fmod(x, y)`

<div class="nostroke_table"></div>

| **Description** | Calculates the modulo value. Always returns a `DOUBLE` value. |
| **Example** | `fmod(5, 2)` |
| **Result** | `1.0` |

#### `gamma(x)`

<div class="nostroke_table"></div>

| **Description** | Interpolation of the factorial of `x - 1`. Fractional inputs are allowed. |
| **Example** | `gamma(5.5)` |
| **Result** | `52.34277778455352` |

#### `gcd(x, y)`

<div class="nostroke_table"></div>

| **Description** | Computes the greatest common divisor of `x` and `y`. |
| **Example** | `gcd(42, 57)` |
| **Result** | `3` |

#### `greatest_common_divisor(x, y)`

<div class="nostroke_table"></div>

| **Description** | Computes the greatest common divisor of `x` and `y`. |
| **Example** | `greatest_common_divisor(42, 57)` |
| **Result** | `3` |

#### `greatest(x1, x2, ...)`

<div class="nostroke_table"></div>

| **Description** | Selects the largest value. |
| **Example** | `greatest(3, 2, 4, 4)` |
| **Result** | `4` |

#### `isfinite(x)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the floating point value is finite, false otherwise. |
| **Example** | `isfinite(5.5)` |
| **Result** | `true` |

#### `isinf(x)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the floating point value is infinite, false otherwise. |
| **Example** | `isinf('Infinity'::float)` |
| **Result** | `true` |

#### `isnan(x)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the floating point value is not a number, false otherwise. |
| **Example** | `isnan('NaN'::float)` |
| **Result** | `true` |

#### `lcm(x, y)`

<div class="nostroke_table"></div>

| **Description** | Computes the least common multiple of `x` and `y`. |
| **Example** | `lcm(42, 57)` |
| **Result** | `798` |

#### `least_common_multiple(x, y)`

<div class="nostroke_table"></div>

| **Description** | Computes the least common multiple of `x` and `y`. |
| **Example** | `least_common_multiple(42, 57)` |
| **Result** | `798` |

#### `least(x1, x2, ...)`

<div class="nostroke_table"></div>

| **Description** | Selects the smallest value. |
| **Example** | `least(3, 2, 4, 4)` |
| **Result** | `2` |

#### `lgamma(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the log of the `gamma` function. |
| **Example** | `lgamma(2)` |
| **Result** | `0` |

#### `ln(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the natural logarithm of `x`. |
| **Example** | `ln(2)` |
| **Result** | `0.693` |

#### `log(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the base-10 log of `x`. |
| **Example** | `log(100)` |
| **Result** | `2` |

#### `log10(x)`

<div class="nostroke_table"></div>

| **Description** | Alias of `log`. Computes the base-10 log of `x`. |
| **Example** | `log10(1000)` |
| **Result** | `3` |

#### `log2(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the base-2 log of `x`. |
| **Example** | `log2(8)` |
| **Result** | `3` |

#### `multiply(x, y)`

<div class="nostroke_table"></div>

| **Description** | Alias for `x * y`. |
| **Example** | `multiply(2, 3)` |
| **Result** | `6` |

#### `nextafter(x, y)`

<div class="nostroke_table"></div>

| **Description** | Return the next floating point value after `x` in the direction of `y`. |
| **Example** | `nextafter(1::float, 2::float)` |
| **Result** | `1.0000001` |

#### `pi()`

<div class="nostroke_table"></div>

| **Description** | Returns the value of pi. |
| **Example** | `pi()` |
| **Result** | `3.141592653589793` |

#### `pow(x, y)`

<div class="nostroke_table"></div>

| **Description** | Computes `x` to the power of `y`. |
| **Example** | `pow(2, 3)` |
| **Result** | `8` |

#### `power(x, y)`

<div class="nostroke_table"></div>

| **Description** | Alias of `pow`. Computes `x` to the power of `y`. |
| **Example** | `power(2, 3)` |
| **Result** | `8` |

#### `radians(x)`

<div class="nostroke_table"></div>

| **Description** | Converts degrees to radians. |
| **Example** | `radians(90)` |
| **Result** | `1.5707963267948966` |

#### `random()`

<div class="nostroke_table"></div>

| **Description** | Returns a random number `x` in the range `0.0 <= x < 1.0`. |
| **Example** | `random()` |
| **Result** | various |

#### `round_even(v NUMERIC, s INTEGER)`

<div class="nostroke_table"></div>

| **Description** | Alias of `roundbankers(v, s)`. Round to `s` decimal places using the [_rounding half to even_ rule](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even). Values `s < 0` are allowed. |
| **Example** | `round_even(24.5, 0)` |
| **Result** | `24.0` |

#### `round(v NUMERIC, s INTEGER)`

<div class="nostroke_table"></div>

| **Description** | Round to `s` decimal places. Values `s < 0` are allowed. |
| **Example** | `round(42.4332, 2)` |
| **Result** | `42.43` |

#### `setseed(x)`

<div class="nostroke_table"></div>

| **Description** | Sets the seed to be used for the random function. |
| **Example** | `setseed(0.42)` |

#### `sign(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the sign of `x` as -1, 0 or 1. |
| **Example** | `sign(-349)` |
| **Result** | `-1` |

#### `signbit(x)`

<div class="nostroke_table"></div>

| **Description** | Returns whether the signbit is set or not. |
| **Example** | `signbit(-1.0)` |
| **Result** | `true` |

#### `sin(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the sin of `x`. |
| **Example** | `sin(pi() / 6)` |
| **Result** | `0.49999999999999994` |

#### `sqrt(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the square root of the number. |
| **Example** | `sqrt(9)` |
| **Result** | `3` |

#### `subtract(x, y)`

<div class="nostroke_table"></div>

| **Description** | Alias for `x - y`. |
| **Example** | `subtract(2, 3)` |
| **Result** | `-1` |

#### `tan(x)`

<div class="nostroke_table"></div>

| **Description** | Computes the tangent of `x`. |
| **Example** | `tan(pi() / 4)` |
| **Result** | `0.9999999999999999` |

#### `trunc(x)`

<div class="nostroke_table"></div>

| **Description** | Truncates the number. |
| **Example** | `trunc(17.4)` |
| **Result** | `17` |

#### `xor(x, y)`

<div class="nostroke_table"></div>

| **Description** | Bitwise XOR. |
| **Example** | `xor(17, 5)` |
| **Result** | `20` |
