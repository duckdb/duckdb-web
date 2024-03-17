| Function | Description | Example | Result |
|:--|:----|:----|:-|
| `bit_count(`*`bitstring`*`)` | Returns the number of set bits in the bitstring. | `bit_count('1101011'::BIT)` | `5` |
| `bit_length(`*`bitstring`*`)` | Returns the number of bits in the bitstring. | `bit_length('1101011'::BIT)` | `7` |
| `bit_position(`*`substring`*`, `*`bitstring`*`)` | Returns first starting index of the specified substring within bits, or zero if it's not present. The first (leftmost) bit is indexed 1 | `bit_position('010'::BIT, '1110101'::BIT)` | `4` |
| `bitstring(`*`bitstring`*`, `*`length`*`)` | Returns a bitstring of determined length. | `bitstring('1010'::BIT, 7)` | `0001010` |
| `get_bit(`*`bitstring`*`, `*`index`*`)` | Extracts the nth bit from bitstring; the first (leftmost) bit is indexed 0. | `get_bit('0110010'::BIT, 2)` | `1` |
| `length(`*`bitstring`*`)` | Alias for `bit_length`. | `length('1101011'::BIT)` | `7` |
| `octet_length(`*`bitstring`*`)` | Returns the number of bytes in the bitstring. | `octet_length('1101011'::BIT)` | `1` |
| `set_bit(`*`bitstring`*`, `*`index`*`, `*`new_value`*`)` | Sets the nth bit in bitstring to newvalue; the first (leftmost) bit is indexed 0. Returns a new bitstring. | `set_bit('0110010'::BIT, 2, 0)` | `0100010` |
