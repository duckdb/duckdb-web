char1.md

| *`string`* `||` *`string`* | String concatenation | `'Duck' || 'DB'` | `DuckDB` | |

bitstring-operators.md

| `|` | bitwise OR | `'1011'::BIT | '0001'::BIT` | `1011` |

blob.md

| *`blob`* `||` *`blob`* | Blob concatenation | `'\xAA'::BLOB || '\xBB'::BLOB` | `\xAA\xBB` |

nested-list-operations.md

| `||`  | Alias for `list_concat`                                                                   | `[1, 2, 3] || [4, 5, 6]`          | `[1, 2, 3, 4, 5, 6]` |

