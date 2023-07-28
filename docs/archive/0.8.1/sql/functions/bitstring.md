---
layout: docu
title: Bitstring Functions
selected: Documentation/Functions/Bitstring Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating bit values.
Bitstrings must be of equal length when performing the bitwise operands AND, OR and XOR. When bit shifting, the original length of the string is preserved.

## Bitstring Operators
The table below shows the available mathematical operators for `BIT` type.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `&` | bitwise AND | `'10101'::BIT & '10001'::BIT` | `10001` |
| `|` | bitwise OR | `'1011'::BIT | '0001'::BIT` | `1011` |
| `xor` | bitwise XOR | `xor('101'::BIT, '001'::BIT)` | `100` |
| `~` | bitwise NOT | `~('101'::BIT)` | `010` |
| `<<` | bitwise shift left | `'1001011'::BIT << 3` | `1011000` |
| `>>` | bitwise shift right | `'1001011'::BIT >> 3` | `0001001` |


## Bitstring Functions
The table below shows the available scalar functions for `BIT` type.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `bit_count(`*`bitstring`*`)` | Returns the number of set bits in the bitstring. | `bit_count('1101011'::BIT)` | `5` |
| `bit_length(`*`bitstring`*`)` | Returns the number of bits in the bitstring. | `bit_length('1101011'::BIT)` | `7` |
| `bit_position(`*`substring`*`, `*`bitstring`*`)` | Returns first starting index of the specified substring within bits, or zero if it's not present. The first (leftmost) bit is indexed 1 | `bit_position('010'::BIT, '1110101'::BIT)` | `4` |
| `bitstring(`*`bitstring`*`, `*`length`*`)` | Returns a bitstring of determined length. | `bitstring('1010'::BIT, 7)` | `0001010` |
| `get_bit(`*`bitstring`*`, `*`index`*`)` | Extracts the nth bit from bitstring; the first (leftmost) bit is indexed 0. | `get_bit('0110010'::BIT, 2)` | `1` |
| `length(`*`bitstring`*`)` | Alias for `bit_length`. | `length('1101011'::BIT)` | `7` |
| `octet_length(`*`bitstring`*`)` | Returns the number of bytes in the bitstring. | `octet_length('1101011'::BIT)` | `1` |
| `set_bit(`*`bitstring`*`, `*`index`*`, `*`new_value`*`)` | Sets the nth bit in bitstring to newvalue; the first (leftmost) bit is indexed 0. Returns a new bitstring. | `set_bit('0110010'::BIT, 2, 0)` | `0100010` |

## Bitstring Aggregate Functions
These aggregate functions are available for `BIT` type.

| Function | Description | Example |
|:---|:---|:---|
| `bit_and(arg)` |Returns the bitwise AND operation performed on all bitstrings in a given expression. | `bit_and(A)` |
| `bit_or(arg)` |Returns the bitwise OR operation performed on all bitstrings in a given expression.  | `bit_or(A)` |
| `bit_xor(arg)` |Returns the bitwise XOR operation performed on all bitstrings in a given expression. | `bit_xor(A)` |
| `bitstring_agg(arg)` |Returns a bitstring with bits set for each distinct value. | `bitstring_agg(A)` |
| `bitstring_agg(arg, min, max)` |Returns a bitstring with bits set for each distinct value. | `bitstring_agg(A, 1, 42)` |

### Bitstring Aggregation
The `BITSTRING_AGG` function takes any integer type as input and returns a bitstring with bits set for each distinct value. 
The left-most bit represents the smallest value in the column and the right-most bit the maximum value. If possible, the min and max are retrieved from the column statistics. Otherwise, it is also possible to provide the min and max values.  
  
The combination of `BIT_COUNT` and `BITSTRING_AGG` could be used as an alternative to `COUNT DISTINCT`, with possible performance improvements in cases of low cardinality and dense values.
