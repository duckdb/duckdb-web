---
layout: docu
title: Bitstring Functions
---

This section describes functions and operators for examining and manipulating bit values.
Bitstrings must be of equal length when performing the bitwise operands AND, OR and XOR. When bit shifting, the original length of the string is preserved.

## Bitstring Operators

The table below shows the available mathematical operators for `BIT` type.

<div class="narrow_table"></div>

<!-- markdownlint-disable MD056 -->

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `&` | Bitwise AND | `'10101'::BIT & '10001'::BIT` | `10001` |
| `|` | Bitwise OR | `'1011'::BIT | '0001'::BIT` | `1011` |
| `xor` | Bitwise XOR | `xor('101'::BIT, '001'::BIT)` | `100` |
| `~` | Bitwise NOT | `~('101'::BIT)` | `010` |
| `<<` | Bitwise shift left | `'1001011'::BIT << 3` | `1011000` |
| `>>` | Bitwise shift right | `'1001011'::BIT >> 3` | `0001001` |

<!-- markdownlint-enable MD056 -->

## Bitstring Functions

The table below shows the available scalar functions for `BIT` type.

| Name | Description |
|:--|:-------|
| [`bit_count(`*`bitstring`*`)`](#bit_countbitstring) | Returns the number of set bits in the bitstring. |
| [`bit_length(`*`bitstring`*`)`](#bit_lengthbitstring) | Returns the number of bits in the bitstring. |
| [`bit_position(`*`substring`*`, `*`bitstring`*`)`](#bit_positionsubstring-bitstring) | Returns first starting index of the specified substring within bits, or zero if it's not present. The first (leftmost) bit is indexed 1. |
| [`bitstring(`*`bitstring`*`, `*`length`*`)`](#bitstringbitstring-length) | Returns a bitstring of determined length. |
| [`get_bit(`*`bitstring`*`, `*`index`*`)`](#get_bitbitstring-index) | Extracts the nth bit from bitstring; the first (leftmost) bit is indexed 0. |
| [`length(`*`bitstring`*`)`](#lengthbitstring) | Alias for `bit_length`. |
| [`octet_length(`*`bitstring`*`)`](#octet_lengthbitstring) | Returns the number of bytes in the bitstring. |
| [`set_bit(`*`bitstring`*`, `*`index`*`, `*`new_value`*`)`](#set_bitbitstring-index-new_value) | Sets the nth bit in bitstring to newvalue; the first (leftmost) bit is indexed 0. Returns a new bitstring. |

### `bit_count(`*`bitstring`*`)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of set bits in the bitstring. |
| **Example** | `bit_count('1101011'::BIT)` |
| **Result** | `5` |

### `bit_length(`*`bitstring`*`)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of bits in the bitstring. |
| **Example** | `bit_length('1101011'::BIT)` |
| **Result** | `7` |

### `bit_position(`*`substring`*`, `*`bitstring`*`)`

<div class="nostroke_table"></div>

| **Description** | Returns first starting index of the specified substring within bits, or zero if it's not present. The first (leftmost) bit is indexed 1 |
| **Example** | `bit_position('010'::BIT, '1110101'::BIT)` |
| **Result** | `4` |

### `bitstring(`*`bitstring`*`, `*`length`*`)`

<div class="nostroke_table"></div>

| **Description** | Returns a bitstring of determined length. |
| **Example** | `bitstring('1010'::BIT, 7)` |
| **Result** | `0001010` |

### `get_bit(`*`bitstring`*`, `*`index`*`)`

<div class="nostroke_table"></div>

| **Description** | Extracts the nth bit from bitstring; the first (leftmost) bit is indexed 0. |
| **Example** | `get_bit('0110010'::BIT, 2)` |
| **Result** | `1` |

### `length(`*`bitstring`*`)`

<div class="nostroke_table"></div>

| **Description** | Alias for `bit_length`. |
| **Example** | `length('1101011'::BIT)` |
| **Result** | `7` |

### `octet_length(`*`bitstring`*`)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of bytes in the bitstring. |
| **Example** | `octet_length('1101011'::BIT)` |
| **Result** | `1` |

### `set_bit(`*`bitstring`*`, `*`index`*`, `*`new_value`*`)`

<div class="nostroke_table"></div>

| **Description** | Sets the nth bit in bitstring to newvalue; the first (leftmost) bit is indexed 0. Returns a new bitstring. |
| **Example** | `set_bit('0110010'::BIT, 2, 0)` |
| **Result** | `0100010` |

## Bitstring Aggregate Functions

These aggregate functions are available for `BIT` type.

| Name | Description |
|:--|:-------|
| [`bit_and(arg)`](#bit_andarg) | Returns the bitwise AND operation performed on all bitstrings in a given expression. |
| [`bit_or(arg)`](#bit_orarg) | Returns the bitwise OR operation performed on all bitstrings in a given expression. |
| [`bit_xor(arg)`](#bit_xorarg) | Returns the bitwise XOR operation performed on all bitstrings in a given expression. |
| [`bitstring_agg(arg)`](#bitstring_aggarg) | Returns a bitstring with bits set for each distinct position defined in `arg`. |
| [`bitstring_agg(arg, min, max)`](#bitstring_aggarg-min-max) | Returns a bitstring with bits set for each distinct position defined in `arg`. All positions must be within the range [`min`, `max`] or an "Out of Range Error" will be thrown. |

### `bit_and(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise AND operation performed on all bitstrings in a given expression. |
| **Example** | `bit_and(A)` |

### `bit_or(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise OR operation performed on all bitstrings in a given expression. |
| **Example** | `bit_or(A)` |

### `bit_xor(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise XOR operation performed on all bitstrings in a given expression. |
| **Example** | `bit_xor(A)` |

### `bitstring_agg(arg)`

<div class="nostroke_table"></div>

| **Description** | The `bitstring_agg` function takes any integer type as input and returns a bitstring with bits set for each distinct value. The left-most bit represents the smallest value in the column and the right-most bit the maximum value. If possible, the min and max are retrieved from the column statistics. Otherwise, it is also possible to provide the min and max values. |
| **Example** | `bitstring_agg(A)` |

> Tip The combination of `bit_count` and `bitstring_agg` could be used as an alternative to `count(DISTINCT ...)`, with possible performance improvements in cases of low cardinality and dense values.

### `bitstring_agg(arg, min, max)`

<div class="nostroke_table"></div>

| **Description** | Returns a bitstring with bits set for each distinct position defined in `arg`. All positions must be within the range [`min`, `max`] or an "Out of Range Error" will be thrown. |
| **Example** | `bitstring_agg(A, 1, 42)` |
