| Operator | Description | Example | Result |
|-|--|---|-|
| `&&`  | Alias for `list_intersect`                                                                | `[1, 2, 3, 4, 5] && [2, 5, 5, 6]` | `[2, 5]`             |
| `@>`  | Alias for `list_has_all`, where the list on the **right** of the operator is the sublist. | `[1, 2, 3, 4] @> [3, 4, 3]`       | `true`               |
| `<@`  | Alias for `list_has_all`, where the list on the **left** of the operator is the sublist.  | `[1, 4] <@ [1, 2, 3, 4]`          | `true`               |
| `<=>` | Alias for `list_cosine_similarity`                                                        | `[1, 2, 3] <=> [1, 2, 5]`         | `0.9759000729485332` |
| `<->` | Alias for `list_distance`                                                                 | `[1, 2, 3] <-> [1, 2, 5]`         | `2.0`                |
