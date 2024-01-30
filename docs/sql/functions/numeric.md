---
layout: docu
title: Numeric Functions
---

## Numeric Operators

The table below shows the available mathematical operators for numeric types.

<div class="narrow_table"></div>

<!-- markdownlint-disable MD056 -->

| Operator | Description | Example | Result |
|-|-----|--|-|
| `+`      | addition                  | `2 + 3`   | `5`   |
| `-`      | subtraction               | `2 - 3`   | `-1`  |
| `*`      | multiplication            | `2 * 3`   | `6`   |
| `/`      | float division            | `5 / 2`   | `2.5` |
| `//`     | division                  | `5 // 2`  | `2`   |
| `%`      | modulo (remainder)        | `5 % 4`   | `1`   |
| `**`     | exponent                  | `3 ** 4`  | `81`  |
| `^`      | exponent (alias for `**`) | `3 ^ 4`   | `81`  |
| `&`      | bitwise AND               | `91 & 15` | `11`  |
| `|`      | bitwise OR                | `32 | 3`  | `35`  |
| `<<`     | bitwise shift left        | `1 << 4`  | `16`  |
| `>>`     | bitwise shift right       | `8 >> 2`  | `2`   |
| `~`      | bitwise negation          | `~15`     | `-16` |
| `!`      | factorial of `x`          | `4!`      | `24`  |

<!-- markdownlint-enable MD056 -->

### Division and Modulo Operators

There are two division operators: `/` and `//`.
They are equivalent when at least one of the operands is a `FLOAT` or a `DOUBLE`.
When both operands are integers, `/` performs floating points division (`5 / 2 = 2.5`) while `//` performs integer division (`5 // 2 = 2`).

### Supported Types

The modulo, bitwise, and negation and factorial operators work only on integral data types,
whereas the others are available for all numeric data types.

## Numeric Functions

The table below shows the available mathematical functions.

| Function | Description |
|:---|:---|
| [`@`](#) | Absolute value (parentheses optional if operating on a column) |
| [`abs(x)`](#absx) | Absolute value |
| [`acos(x)`](#acosx) | Computes the arccosine of x |
| [`add(x, y)`](#addx-y) | Alias for `x + y` |
| [`asin(x)`](#asinx) | Computes the arcsine of x |
| [`atan(x)`](#atanx) | Computes the arctangent of x |
| [`atan2(y, x)`](#atan2y-x) | Computes the arctangent (y, x) |
| [`bit_count(x)`](#bit_countx) | Returns the number of bits that are set |
| [`cbrt(x)`](#cbrtx) | Returns the cube root of the number |
| [`ceil(x)`](#ceilx) | Rounds the number up |
| [`ceiling(x)`](#ceilingx) | Rounds the number up. Alias of `ceil` |
| [`cos(x)`](#cosx) | Computes the cosine of x |
| [`cot(x)`](#cotx) | Computes the cotangent of x |
| [`degrees(x)`](#degreesx) | Converts radians to degrees |
| [`divide(x, y)`](#dividex-y) | Alias for `x // y` |
| [`even(x)`](#evenx) | Round to next even number by rounding away from zero |
| [`exp(x)`](#expx) | Computes `e ** x` |
| [`factorial(x)`](#factorialx) | See `!` operator. Computes the product of the current integer and all integers below it |
| [`fdiv(x, y)`](#fdivx-y) | Performs integer division (`x // y`) but returns a `DOUBLE` value |
| [`floor(x)`](#floorx) | Rounds the number down |
| [`fmod(x, y)`](#fmodx-y) | Calculates the modulo value. Always returns a `DOUBLE` value |
| [`gamma(x)`](#gammax) | Interpolation of (x-1) factorial (so decimal inputs are allowed) |
| [`gcd(x, y)`](#gcdx-y) | Computes the greatest common divisor of x and y |
| [`greatest_common_divisor(x, y)`](#greatest_common_divisorx-y) | Computes the greatest common divisor of x and y |
| [`greatest(x1, x2, ...)`](#greatestx1-x2-) | Selects the largest value |
| [`isfinite(x)`](#isfinitex) | Returns true if the floating point value is finite, false otherwise |
| [`isinf(x)`](#isinfx) | Returns true if the floating point value is infinite, false otherwise |
| [`isnan(x)`](#isnanx) | Returns true if the floating point value is not a number, false otherwise |
| [`lcm(x, y)`](#lcmx-y) | Computes the least common multiple of x and y |
| [`least_common_multiple(x, y)`](#least_common_multiplex-y) | Computes the least common multiple of x and y |
| [`least(x1, x2, ...)`](#leastx1-x2-) | Selects the smallest value |
| [`lgamma(x)`](#lgammax) | Computes the log of the `gamma` function |
| [`ln(x)`](#lnx) | Computes the natural logarithm of *x* |
| [`log(x)`](#logx) | Computes the 10-log of *x* |
| [`log10(x)`](#log10x) | Alias of `log`. computes the 10-log of *x* |
| [`log2(x)`](#log2x) | Computes the 2-log of *x* |
| [`multiply(x, y)`](#multiplyx-y) | Alias for `x * y` |
| [`nextafter(x, y)`](#nextafterx-y) | Return the next floating point value after *x* in the direction of *y* |
| [`pi()`](#pi) | Returns the value of pi |
| [`pow(x, y)`](#powx-y) | Computes x to the power of y |
| [`power(x, y)`](#powerx-y) | Alias of `pow`. computes x to the power of y |
| [`radians(x)`](#radiansx) | Converts degrees to radians |
| [`random()`](#random) | Returns a random number between 0 and 1 |
| [`round_even(v NUMERIC, s INT)`](#round_evenvnumeric-sint) | Alias of `roundbankers(v, s)`. Round to *s* decimal places using the [_rounding half to even_ rule](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even). Values *s < 0* are allowed |
| [`round(v NUMERIC, s INT)`](#roundvnumeric-sint) | Round to *s* decimal places. Values *s < 0* are allowed |
| [`setseed(x)`](#setseedx) | Sets the seed to be used for the random function |
| [`sign(x)`](#signx) | Returns the sign of x as -1, 0 or 1 |
| [`signbit(x)`](#signbitx) | Returns whether the signbit is set or not |
| [`sin(x)`](#sinx) | Computes the sin of x |
| [`sqrt(x)`](#sqrtx) | Returns the square root of the number |
| [`subtract(x, y)`](#subtractx-y) | Alias for `x - y` |
| [`tan(x)`](#tanx) | Computes the tangent of x |
| [`trunc(x)`](#truncx) | Truncates the number |
| [`xor(x)`](#xorx) | Bitwise XOR |

### `@`

* **Description:** Absolute value (parentheses optional if operating on a column)
* **Example:** `@(-2)`
* **Result:** `2`

### `abs(x)`

* **Description:** Absolute value
* **Example:** `abs(-17.4)`
* **Result:** `17.4`

### `acos(x)`

* **Description:** Computes the arccosine of x
* **Example:** `acos(0.5)`
* **Result:** `1.0471975511965976`

### `add(x, y)`

* **Description:** Alias for `x + y`
* **Example:** `add(2, 3)`
* **Result:** `5`

### `asin(x)`

* **Description:** Computes the arcsine of x
* **Example:** `asin(0.5)`
* **Result:** `0.5235987755982989`

### `atan(x)`

* **Description:** Computes the arctangent of x
* **Example:** `atan(0.5)`
* **Result:** `0.4636476090008061`

### `atan2(y, x)`

* **Description:** Computes the arctangent (y, x)
* **Example:** `atan2(0.5, 0.5)`
* **Result:** `0.7853981633974483`

### `bit_count(x)`

* **Description:** Returns the number of bits that are set
* **Example:** `bit_count(31)`
* **Result:** `5`

### `cbrt(x)`

* **Description:** Returns the cube root of the number
* **Example:** `cbrt(8)`
* **Result:** `2`

### `ceil(x)`

* **Description:** Rounds the number up
* **Example:** `ceil(17.4)`
* **Result:** `18`

### `ceiling(x)`

* **Description:** Rounds the number up. Alias of `ceil`
* **Example:** `ceiling(17.4)`
* **Result:** `18`

### `cos(x)`

* **Description:** Computes the cosine of x
* **Example:** `cos(90)`
* **Result:** `-0.4480736161291701`

### `cot(x)`

* **Description:** Computes the cotangent of x
* **Example:** `cot(0.5)`
* **Result:** `1.830487721712452`

### `degrees(x)`

* **Description:** Converts radians to degrees
* **Example:** `degrees(pi())`
* **Result:** `180`

### `divide(x, y)`

* **Description:** Alias for `x // y`
* **Example:** `divide(5, 2)`
* **Result:** `2`

### `even(x)`

* **Description:** Round to next even number by rounding away from zero
* **Example:** `even(2.9)`
* **Result:** `4`

### `exp(x)`

* **Description:** Computes `e ** x`
* **Example:** `exp(0.693)`
* **Result:** `2`

### `factorial(x)`

* **Description:** See `!` operator. Computes the product of the current integer and all integers below it
* **Example:** `factorial(4)`
* **Result:** `24`

### `fdiv(x, y)`

* **Description:** Performs integer division (`x // y`) but returns a `DOUBLE` value
* **Example:** `fdiv(5, 2)`
* **Result:** `2.0`

### `floor(x)`

* **Description:** Rounds the number down
* **Example:** `floor(17.4)`
* **Result:** `17`

### `fmod(x, y)`

* **Description:** Calculates the modulo value. Always returns a `DOUBLE` value
* **Example:** `fmod(5, 2)`
* **Result:** `1.0`

### `gamma(x)`

* **Description:** Interpolation of (x-1) factorial (so decimal inputs are allowed)
* **Example:** `gamma(5.5)`
* **Result:** `52.34277778455352`

### `gcd(x, y)`

* **Description:** Computes the greatest common divisor of x and y
* **Example:** `gcd(42, 57)`
* **Result:** `3`

### `greatest_common_divisor(x, y)`

* **Description:** Computes the greatest common divisor of x and y
* **Example:** `greatest_common_divisor(42, 57)`
* **Result:** `3`

### `greatest(x1, x2, ...)`

* **Description:** Selects the largest value
* **Example:** `greatest(3, 2, 4, 4)`
* **Result:** `4`

### `isfinite(x)`

* **Description:** Returns true if the floating point value is finite, false otherwise
* **Example:** `isfinite(5.5)`
* **Result:** `true`

### `isinf(x)`

* **Description:** Returns true if the floating point value is infinite, false otherwise
* **Example:** `isinf('Infinity'::float)`
* **Result:** `true`

### `isnan(x)`

* **Description:** Returns true if the floating point value is not a number, false otherwise
* **Example:** `isnan('NaN'::float)`
* **Result:** `true`

### `lcm(x, y)`

* **Description:** Computes the least common multiple of x and y
* **Example:** `lcm(42, 57)`
* **Result:** `798`

### `least_common_multiple(x, y)`

* **Description:** Computes the least common multiple of x and y
* **Example:** `least_common_multiple(42, 57)`
* **Result:** `798`

### `least(x1, x2, ...)`

* **Description:** Selects the smallest value
* **Example:** `least(3, 2, 4, 4)`
* **Result:** `2`

### `lgamma(x)`

* **Description:** Computes the log of the `gamma` function
* **Example:** `lgamma(2)`
* **Result:** `0`

### `ln(x)`

* **Description:** Computes the natural logarithm of *x*
* **Example:** `ln(2)`
* **Result:** `0.693`

### `log(x)`

* **Description:** Computes the 10-log of *x*
* **Example:** `log(100)`
* **Result:** `2`

### `log10(x)`

* **Description:** Alias of `log`. computes the 10-log of *x*
* **Example:** `log10(1000)`
* **Result:** `3`

### `log2(x)`

* **Description:** Computes the 2-log of *x*
* **Example:** `log2(8)`
* **Result:** `3`

### `multiply(x, y)`

* **Description:** Alias for `x * y`
* **Example:** `multiply(2, 3)`
* **Result:** `6`

### `nextafter(x, y)`

* **Description:** Return the next floating point value after *x* in the direction of *y*
* **Example:** `nextafter(1::float, 2::float)`
* **Result:** `1.0000001`

### `pi()`

* **Description:** Returns the value of pi
* **Example:** `pi()`
* **Result:** `3.141592653589793`

### `pow(x, y)`

* **Description:** Computes x to the power of y
* **Example:** `pow(2, 3)`
* **Result:** `8`

### `power(x, y)`

* **Description:** Alias of `pow`. computes x to the power of y
* **Example:** `power(2, 3)`
* **Result:** `8`

### `radians(x)`

* **Description:** Converts degrees to radians
* **Example:** `radians(90)`
* **Result:** `1.5707963267948966`

### `random()`

* **Description:** Returns a random number between 0 and 1
* **Example:** `random()`
* **Result:** various

### `round_even(v NUMERIC, s INT)`

* **Description:** Alias of `roundbankers(v, s)`. Round to *s* decimal places using the [_rounding half to even_ rule](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even). Values *s < 0* are allowed
* **Example:** `round_even(24.5, 0)`
* **Result:** `24.0`

### `round(v NUMERIC, s INT)`

* **Description:** Round to *s* decimal places. Values *s < 0* are allowed
* **Example:** `round(42.4332, 2)`
* **Result:** `42.43`

### `setseed(x)`

* **Description:** Sets the seed to be used for the random function
* **Example:** `setseed(0.42)`
* **Result:** None

### `sign(x)`

* **Description:** Returns the sign of x as -1, 0 or 1
* **Example:** `sign(-349)`
* **Result:** `-1`

### `signbit(x)`

* **Description:** Returns whether the signbit is set or not
* **Example:** `signbit(-0.0)`
* **Result:** `true`

### `sin(x)`

* **Description:** Computes the sin of x
* **Example:** `sin(90)`
* **Result:** `0.8939966636005579`

### `sqrt(x)`

* **Description:** Returns the square root of the number
* **Example:** `sqrt(9)`
* **Result:** `3`

### `subtract(x, y)`

* **Description:** Alias for `x - y`
* **Example:** `subtract(2, 3)`
* **Result:** `-1`

### `tan(x)`

* **Description:** Computes the tangent of x
* **Example:** `tan(90)`
* **Result:** `-1.995200412208242`

### `trunc(x)`

* **Description:** Truncates the number
* **Example:** `trunc(17.4)`
* **Result:** `17`

### `xor(x)`

* **Description:** Bitwise XOR
* **Example:** `xor(17, 5)`
* **Result:** `20`
