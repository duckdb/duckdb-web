---
layout: docu
title: Numeric Functions
---

## Numeric Operators

The table below shows the available mathematical operators for numeric types.

<div class="narrow_table"></div>

| Operator | Description | Function Alias | Example | Result |
|-|-|---|-|-|
| `+`      | addition                  | `add(x, y)`      | `2 + 3`   | `5`   |
| `-`      | subtraction               | `subtract(x, y)` | `2 - 3`   | `-1`  |
| `*`      | multiplication            | `multiply(x, y)` | `2 * 3`   | `6`   |
| `/`      | float division            |                  | `5 / 2`   | `2.5` |
| `//`     | division                  | `divide(x, y)`   | `5 // 2`  | `2`   |
| `%`      | modulo (remainder)        |                  | `5 % 4`   | `1`   |
| `**`     | exponent                  |                  | `3 ** 4`  | `81`  |
| `^`      | exponent (alias for `**`) |                  | `3 ^ 4`   | `81`  |
| `&`      | bitwise AND               |                  | `91 & 15` | `11`  |
| `|`      | bitwise OR                |                  | `32 | 3`  | `35`  |
| `<<`     | bitwise shift left        |                  | `1 << 4`  | `16`  |
| `>>`     | bitwise shift right       |                  | `8 >> 2`  | `2`   |
| `~`      | bitwise negation          |                  | `~15`     | `-16` |
| `!`      | factorial of `x`          |                  | `4!`      | `24`  |

### Division and Modulo Operators

There are two division operators: `/` and `//`.
They are equivalent when at least one of the operands is a `FLOAT` or a `DOUBLE`.
When both operands are integers, `/` performs floating points division (`5 / 2 = 2.5`) while `//` performs integer division (`5 // 2 = 2`).

### Supported Types

The modulo, bitwise, and negation and factorial operators work only on integral data types,
whereas the others are available for all numeric data types.

## Numeric Functions

The table below shows the available mathematical functions.

| Function | Description | Example | Result |
|:---|:---|:---|:--|
| `abs(x)` | Absolute value | `abs(-17.4)` | 17.4 |
| `acos(x)` | Computes the arccosine of x | `acos(0.5)` | 1.0471975511965976 |
| `asin(x)` | Computes the arcsine of x | `asin(0.5)` | 0.5235987755982989 |
| `atan(x)` | Computes the arctangent of x | `atan(0.5)` | 0.4636476090008061 |
| `atan2(y, x)` | Computes the arctangent (y, x) | `atan2(0.5, 0.5)` | 0.7853981633974483 |
| `bit_count(x)` | Returns the number of bits that are set | `bit_count(31)` | 5 |
| `cbrt(x)` | Returns the cube root of the number | `cbrt(8)` | 2 |
| `ceil(x)` | Rounds the number up | `ceil(17.4)` | 18 |
| `ceiling(x)` | Rounds the number up. Alias of `ceil` | `ceiling(17.4)` | 18 |
| `cos(x)` | Computes the cosine of x | `cos(90)` | -0.4480736161291701 |
| `cot(x)` | Computes the cotangent of x | `cot(0.5)` | 1.830487721712452 |
| `degrees(x)` | Converts radians to degrees | `degrees(pi())` | 180 |
| `even(x)` | Round to next even number by rounding away from zero | `even(2.9)` | 4 |
| `exp(x)` | Computes `e ** x` | `exp(0.693)` | 2 |
| `factorial(x)` | See `!` operator. Computes the product of the current integer and all integers below it | `factorial(4)` | 24 |
| `fdiv(x, y)` | Performs integer division (`x // y`). Returns a `DOUBLE` value | `fdiv(5, 2)` | `2.0` |
| `fmod(x, y)` | Calculates the modulo value. Returns a `DOUBLE` value | `fmod(5, 2)` | `1.0` |
| `floor(x)` | Rounds the number down | `floor(17.4)` | 17 |
| `gamma(x)` | Interpolation of (x-1) factorial (so decimal inputs are allowed) | `gamma(5.5)` | 52.34277778455352 |
| `gcd(x, y)` | Computes the greatest common divisor of x and y | `gcd(42, 57)` | 3 |
| `greatest_common_divisor(x, y)` | Computes the greatest common divisor of x and y | `greatest_common_divisor(42, 57)` | 3 |
| `greatest(x1, x2, ...)` | Selects the largest value | `greatest(3, 2, 4, 4)` | 4 |
| `isfinite(x)` | Returns true if the floating point value is finite, false otherwise | `isfinite(5.5)` | `true` |
| `isinf(x)` | Returns true if the floating point value is infinite, false otherwise | `isinf('Infinity'::float)` | `true` |
| `isnan(x)` | Returns true if the floating point value is not a number, false otherwise | `isnan('NaN'::float)` | `true` |
| `lcm(x, y)` | Computes the least common multiple of x and y | `lcm(42, 57)` | 798 |
| `least_common_multiple(x, y)` | Computes the least common multiple of x and y | `least_common_multiple(42, 57)` | 798 |
| `least(x1, x2, ...)` | Selects the smallest value | `least(3, 2, 4, 4)` | 2 |
| `lgamma(x)` | Computes the log of the `gamma` function | `lgamma(2)` | 0 |
| `ln(x)` | Computes the natural logarithm of *x* | `ln(2)` | 0.693 |
| `log(x)` | Computes the 10-log of *x* | `log(100)` | 2 |
| `log2(x)` | Computes the 2-log of *x* | `log2(8)` | 3 |
| `log10(x)` | Alias of `log`. computes the 10-log of *x* | `log10(1000)` | 3 |
| `nextafter(x, y)` | Return the next floating point value after *x* in the direction of *y* | `nextafter(1::float, 2::float)` | 1.0000001 |
| `pi()` | Returns the value of pi | `pi()` | 3.141592653589793 |
| `pow(x, y)` | Computes x to the power of y | `pow(2, 3)` | 8 |
| `power(x, y)` | Alias of `pow`. computes x to the power of y | `power(2, 3)` | 8 |
| `radians(x)` | Converts degrees to radians | `radians(90)` | 1.5707963267948966 |
| `random()` | Returns a random number between 0 and 1 | `random()` | various |
| `round(v NUMERIC, s INT)` | Round to *s* decimal places. Values *s < 0* are allowed | `round(42.4332, 2)` | 42.43 |
| `round_even(v NUMERIC, s INT)` | Alias of `roundbankers(v, s)`. Round to *s* decimal places using the [_rounding half to even_ rule](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even). Values *s < 0* are allowed | `round_even(24.5, 0)` | `24.0` |
| `setseed(x)` | Sets the seed to be used for the random function | `setseed(0.42)` | |
| `sin(x)` | Computes the sin of x | `sin(90)` | 0.8939966636005579 |
| `sign(x)` | Returns the sign of x as -1, 0 or 1 | `sign(-349)` | -1 |
| `signbit(x)` | Returns whether the signbit is set or not | `signbit(-0.0)` | `true` |
| `sqrt(x)` | Returns the square root of the number | `sqrt(9)` | 3 |
| `xor(x)` | Bitwise XOR | `xor(17, 5)` | 20 |
| `tan(x)` | Computes the tangent of x | `tan(90)` | -1.995200412208242 |
| `@` | Absolute value (parentheses optional if operating on a column) | `@(-2)` | 2 |
