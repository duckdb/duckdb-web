---
blurb: The bitstring type is a string of 1s and 0s.
layout: docu
redirect_from:
  - /docs/sql/data_types/bitstring
title: Bitstring Type
---

| Name | Aliases | Description |
|:---|:---|:---|
| `BITSTRING` | `BIT` | Variable-length strings of 1s and 0s |

Bitstrings are strings of 1s and 0s. The bit type data is of variable length. A bitstring value requires 1 byte for each group of 8 bits, plus a fixed amount to store some metadata.

By default bitstrings will not be padded with zeroes.
Bitstrings can be very large, having the same size restrictions as `BLOB`s.

## Creating a Bitstring

A string encoding a bitstring can be cast to a `BITSTRING`:

```sql
SELECT '101010'::BITSTRING AS b;
```

<div class="monospace_table"></div>

|   b    |
|--------|
| 101010 |

Creating a `BITSTRING` with a predefined length is possible with the `bitstring` function. The resulting bitstring will be left-padded with zeroes.

```sql
SELECT bitstring('0101011', 12) AS b;
```

|      b       |
|--------------|
| 000000101011 |

Numeric values (integer and float values) can also be converted to a `BITSTRING` via casting. For example:

```sql
SELECT 123::BITSTRING AS b;
```

<div class="monospace_table"></div>

|                b                 |
|----------------------------------|
| 00000000000000000000000001111011 |

## Functions

See [Bitstring Functions]({% link docs/stable/sql/functions/bitstring.md %}).
