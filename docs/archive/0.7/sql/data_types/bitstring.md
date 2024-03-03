---
layout: docu
title: Bitstring Type
selected: Documentation/Data Types/Bit
expanded: Data Types
blurb: The bitstring type are strings of 1's and 0's.
---

| Name | Aliases | Description |
|:---|:---|:---|
| `BIT` | `BITSTRING` | variable-length strings of 1's and 0's |


Bitstrings are strings of 1's and 0's. The bit type data is of variable length. A bitstring value requires 1 byte for each group of 8 bits, plus a fixed amount to store some metadata. 

By default bitstrings will not be padded with zeroes. 
Bitstrings can be very large, having the same size restrictions as `BLOB`s.


```sql
-- create a bitstring 
SELECT '101010'::BIT
```

## Functions
See [Bitstring Functions](../functions/bitstring).