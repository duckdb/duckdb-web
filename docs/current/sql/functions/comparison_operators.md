
## Comparison Operators
The table below shows the standard comparison operators. Whenever either of the input arguments is `NULL`, the output of the comparison is `NULL`.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| < | less than | 2 < 3 | TRUE |
| > | greater than | 2 > 3 | FALSE |
| <= | less than or equal to | 2 <= 3 | TRUE |
| >= | greater than or equal to | 4 >= NULL | NULL |
| = | equal | NULL = NULL | NULL |
| <> or != | not equal | 2 <> 2 | FALSE |

## Comparison Predicates
Besides the comparison operators there are also a set of comparison operators. These behave much like operators, but have special syntax mandated by the SQL standard. They are shown in the table below.

| Predicate | Description |
|:---|:---|
| a BETWEEN x AND y | equivalent to `a >= x AND a <= y` |
| a NOT BETWEEN x AND y | equivalent to `a < x OR a > y` |
| expression IS NULL | `TRUE` if expression is `NULL`, `FALSE` otherwise |
| expression ISNULL | alias for `IS NULL` (non-standard) |
| expression IS NOT NULL | `FALSE` if expression is `NULL`, `TRUE` otherwise |
| expression NOTNULL | alias for `IS NOT NULL` (non-standard) |
