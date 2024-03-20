---
blurb: The bitstring type are strings of 1's and 0's.
expanded: Data Types
layout: docu
redirect_from:
- docs/archive/0.7.1/sql/data_types/bitstring
selected: Documentation/Data Types/Bit
title: Bitstring Type
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