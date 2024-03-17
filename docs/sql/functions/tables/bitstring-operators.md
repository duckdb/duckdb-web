| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `&` | bitwise AND | `'10101'::BIT & '10001'::BIT` | `10001` |
| `|` | bitwise OR | `'1011'::BIT | '0001'::BIT` | `1011` |
| `xor` | bitwise XOR | `xor('101'::BIT, '001'::BIT)` | `100` |
| `~` | bitwise NOT | `~('101'::BIT)` | `010` |
| `<<` | bitwise shift left | `'1001011'::BIT << 3` | `1011000` |
| `>>` | bitwise shift right | `'1001011'::BIT >> 3` | `0001001` |
