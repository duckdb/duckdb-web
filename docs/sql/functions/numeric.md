---
layout: docu
title: Numeric Functions
selected: Documentation/Functions/Numeric Functions
expanded: Functions
---
## Numeric Operators
The table below shows the available mathematical operators for numeric types.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition | `2 + 3` | 5 |
| `-` | subtraction | `2 - 3` | -1 |
| `*` | multiplication | `2 * 3` | 6 |
| `/` | division | `4 / 2` | 2 |
| `%` | modulo (remainder) | `5 % 4` | 1 |
| `**` | exponent | `3 ** 4` | 81 |
| `^` | exponent (alias for `**`) | `3 ^ 4` | 81 |
| `&` | bitwise AND | `91 & 15` | 11 |
| `|` | bitwise OR | `32 | 3` | 35 |
| `<<` | bitwise shift left | `1 << 4` | 16 |
| `>>` | bitwise shift right | `8 >> 2` | 2 |
| `!` | factorial of x. Computes the product of the current integer and all integers below it  | `4!` | 24 |

The modulo, bitwise, and factorial operators work only on integral data types,
whereas the others are available for all numeric data types.

## Numeric Functions
The table below shows the available mathematical functions.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `abs(x)` | absolute value | `abs(-17.4)` | 17.4 |
| `acos(x)` | computes the arccosine of x | `acos(0.5)` | 1.0471975511965976 |
| `asin(x)` | computes the arcsine of x | `asin(0.5)` | 0.5235987755982989 |
| `atan(x)` | computes the arctangent of x | `atan(0.5)` | 0.4636476090008061 |
| `atan2(x, y)` | computes the arctangent (x, y) | `atan2(0.5, 0.5)` | 0.7853981633974483 |
| `bit_count(x)` | returns the number of bits that are set | `bit_count(31)` | 5 |
| `cbrt(x)` | returns the cube root of the number | `cbrt(8)` | 2 |
| `ceil(x)` | rounds the number up | `ceil(17.4)` | 18 |
| `ceiling(x)` | rounds the number up. Alias of `ceil`. | `ceiling(17.4)` | 18 |
| `cos(x)` | computes the cosine of x | `cos(90)` | -0.4480736161291701 |
| `cot(x)` | computes the cotangent of x | `cot(0.5)` | 1.830487721712452 |
| `degrees(x)` | converts radians to degrees | `degrees(pi())` | 180 |
| `even(x)` | round to next even number by rounding away from zero. | `even(2.9)` | 4 |
| `factorial(x)` | See `!` operator. Computes the product of the current integer and all integers below it | `factorial(4)` | 24 |
| `floor(x)` | rounds the number down | `floor(17.4)` | 17 |
| `gamma(x)` | interpolation of (x-1) factorial (so decimal inputs are allowed) | `gamma(5.5)` | 52.34277778455352 |
| `gcd(x, y)` | computes the greatest common divisor of x and y | `gcd(42, 57)` | 3 |
| `greatest_common_divisor(x, y)` | computes the greatest common divisor of x and y | `greatest_common_divisor(42, 57)` | 3 |
| `greatest(x1, x2, ...)` | selects the largest value | `greatest(3, 2, 4, 4)` | 4 |
| `isfinite(x)` | Returns true if the floating point value is finite, false otherwise | `isfinite(5.5)` | true |
| `isinf(x)` | Returns true if the floating point value is infinite, false otherwise | `isinf('Infinity'::float)` | true |
| `isnan(x)` | Returns true if the floating point value is not a number, false otherwise | `isnan('NaN'::float)` | true |
| `lcm(x, y)` | computes the least common multiple of x and y | `lcm(42, 57)` | 798 |
| `least_common_multiple(x, y)` | computes the least common multiple of x and y | `least_common_multiple(42, 57)` | 798 |
| `least(x1, x2, ...)` | selects the smallest value | `least(3, 2, 4, 4)` | 2 |
| `lgamma(x)` | computes the log of the `gamma` function. | `lgamma(2)` | 0 |
| `ln(x)` | computes the natural logarithm of *x* | `ln(2)` | 0.693 |
| `log(x)` | computes the 10-log of *x* | `log(100)` | 2 |
| `log2(x)` | computes the 2-log of *x* | `log2(8)` | 3 |
| `log10(x)` | alias of `log`. computes the 10-log of *x* | `log10(1000)` | 3 |
| `nextafter(x, y)` | return the next floating point value after *x* in the direction of *y* | `nextafter(1::float, 2::float)` | 1.0000001 |
| `pi()` | returns the value of pi | `pi()` | 3.141592653589793 |
| `pow(x, y)` | computes x to the power of y | `pow(2, 3)` | 8 |
| `power(x, y)` | Alias of `pow`. computes x to the power of y | `power(2, 3)` | 8 |
| `radians(x)` | converts degrees to radians | `radians(90)` | 1.5707963267948966 |
| `random()` | returns a random number between 0 and 1 | `random()` | various |
| `round(v numeric, s int)` | round to *s* decimal places | `round(42.4332, 2)` | 42.43 |
| `setseed(x)` | sets the seed to be used for the random function | `setseed(0.42)` | |
| `sin(x)` | computes the sin of x | `sin(90)` | 0.8939966636005579 |
| `sign(x)` | returns the sign of x as -1, 0 or 1 | `sign(-349)` | -1 |
| `signbit(x)` | returns whether the signbit is set or not | `signbit(-0.0)` | true |
| `sqrt(x)` | returns the square root of the number | `sqrt(9)` | 3 |
| `xor(x)` | bitwise XOR | `xor(17, 5)` | 20 |
| `tan(x)` | computes the tangent of x | `tan(90)` | -1.995200412208242 |
| `@` | absolute value (parentheses optional if operating on a column) | `@(-2)` | 2 |
