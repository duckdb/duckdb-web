---
layout: docu
title: Unnesting
---

## Examples

```sql
-- unnest a list, generating 3 rows (1, 2, 3)
SELECT unnest([1, 2, 3]);
-- unnesting a struct, generating two columns (a, b)
SELECT unnest({'a': 42, 'b': 84});
-- recursive unnest of a list of structs
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
```

The `unnest` function is used to unnest lists or structs by one level. The function can be used as a regular scalar function, but only in the `SELECT` clause. Invoking `unnest` with the `recursive` parameter will unnest lists and structs of multiple levels.

### Unnesting Lists

```sql
-- unnest a list, generating 3 rows (1, 2, 3)
SELECT unnest([1, 2, 3]);
-- unnest a scalar list, generating 3 rows ((1, 10), (2, 11), (3, NULL))
SELECT unnest([1, 2, 3]), unnest([10, 11]);
-- unnest a scalar list, generating 3 rows ((1, 10), (2, 10), (3, 10))
SELECT unnest([1, 2, 3]), 10;
-- unnest a list column generated from a subquery
SELECT unnest(l) + 10 FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
-- empty result
SELECT unnest([]);
-- empty result
SELECT unnest(NULL);
```

Using `unnest` on a list will emit one tuple per entry in the list. When `unnest` is combined with regular scalar expressions, those expressions are repeated for every entry in the list. When multiple lists are unnested in the same `SELECT` clause, the lists are unnested side-by-side. If one list is longer than the other, the shorter list will be padded with `NULL` values.

An empty list and a `NULL` list will both unnest to zero elements.

### Unnesting Structs

```sql
-- unnesting a struct, generating two columns (a, b)
SELECT unnest({'a': 42, 'b': 84});
-- unnesting a struct, generating two columns (a, b)
SELECT unnest({'a': 42, 'b': {'x': 84}});
```

`unnest` on a struct will emit one column per entry in the struct.

### Recursive Unnest

```sql
-- unnesting a list of lists recursively, generating 5 rows (1, 2, 3, 4, 5)
SELECT unnest([[1, 2, 3], [4, 5]], recursive := true);
-- unnesting a list of structs recursively, generating two rows of two columns (a, b)
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
-- unnesting a struct, generating two columns (a, b)
SELECT unnest({'a': [1, 2, 3], 'b': 88}, recursive := true);
```

Calling `unnest` with the `recursive` setting will fully unnest lists, followed by fully unnesting structs. This can be useful to fully flatten columns that contain lists within lists, or lists of structs. Note that lists *within* structs are not unnested.
