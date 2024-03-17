| Function | Description | Example |
|:---|:----|:--|
| `bit_and(arg)` |Returns the bitwise AND operation performed on all bitstrings in a given expression. | `bit_and(A)` |
| `bit_or(arg)` |Returns the bitwise OR operation performed on all bitstrings in a given expression.  | `bit_or(A)` |
| `bit_xor(arg)` |Returns the bitwise XOR operation performed on all bitstrings in a given expression. | `bit_xor(A)` |
| `bitstring_agg(arg, min, max)` |Returns a bitstring with bits set for each distinct position defined in `arg`. All positions must be within the range [`min`, `max`] or an "Out of Range Error" will be thrown. | `bitstring_agg(A, 1, 42)` |
| `bitstring_agg(arg)` |Returns a bitstring with bits set for each distinct position defined in `arg`. | `bitstring_agg(A)` |
