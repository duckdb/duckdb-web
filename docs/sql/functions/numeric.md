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
| `&` | bitwise AND | `91 & 15` | 11 |
| `|` | bitwise OR | `32 | 3` | 35 |
| `#` | bitwise XOR | `17 # 5` | 20 |
| `<<` | bitwise shift left | `1 << 4` | 16 |
| `>>` | bitwise shift right | `8 >> 2` | 2 |

The modulo and bitwise operators work only on integral data types, whereas the others are available for all numeric data types.

## Numeric Functions
The table below shows the available mathematical functions.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `abs(x)` | absolute value | `abs(-17.4)` | 17.4 |
| `acos(x)` | computes the arccosine of x | `acos(0.5)` | 1.0471975511965976 |
| `asin(x)` | computes the arcsine of x | `asin(0.5)` | 0.5235987755982989 |
| `atan2(x)` | computes the arctangent of x | `atan2(0.5)` | 0.4636476090008061 |
| `atan2(x, y)` | computes the arctangent (x, y) | `atan2(0.5, 0.5)` | 0.7853981633974483 |
| `bit_count(x)` | returns the number of bits that are set | `bit_count(31)` | 5 |
| `cbrt(x)` | returns the cube root of the number | `cbrt(8)` | 2 |
| `ceil(x)` | rounds the number up | `ceil(17.4)` | 18 |
| `chr(x)` | returns a character which is corresponding the the ASCII code value or Unicode code point | `chr(65)` | A |
| `cos(x)` | computes the cosine of x | `cos(90)` | -0.4480736161291701 |
| `cot(x)` | computes the cotangent of x | `cot(0.5)` | 1.830487721712452 |
| `degrees(x)` | converts radians to degrees | `degrees(pi())` | 180 |
| `floor(x)` | rounds the number down | `floor(17.4)` | 17 |
| `greatest(x1, x2, ...)` | selects the largest value | `greatest(3, 2, 4, 4)` | 4 |
| `least(x1, x2, ...)` | selects the smallest value | `least(3, 2, 4, 4)` | 2 |
| `ln(x)` | computes the natural logarithm of *x* | `ln(2)` | 0.693 |
| `log(x)` | computes the 10-log of *x* | `log(100)` | 2 |
| `log2(x)` | computes the 2-log of *x* | `log2(8)` | 3 |
| `pi()` | returns the value of pi | `pi()` | 3.141592653589793 |
| `pow(x, y)` | computes x to the power of y | `pow(2, 3)` | 8 |
| `radians(x)` | converts degrees to radians | `radians(90)` | 1.5707963267948966 |
| `random()` | returns a random number between 0 and 1 | `random()` | ... |
| `round(v numeric, s int)` | round to *s* decimal places | `round(42.4332, 2)` | 42.43 |
| `setseed(x)` | sets the seed to be used for the random function | `setseed(0.42)` | |
| `sin(x)` | computes the sin of x | `sin(90)` | 0.8939966636005579 |
| `sign(x)` | returns the sign of x as -1, 0 or 1 | `sign(-349)` | -1 |
| `sqrt(x)` | returns the square root of the number | `sqrt(9)` | 3 |
| `tan(x)` | computes the tangent of x | `tan(90)` | -1.995200412208242 |
