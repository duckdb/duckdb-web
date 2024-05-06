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
-- limit depth of recurisve unnest using max_depth
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 2);
```

The `unnest` special function is used to unnest lists or structs by one level. The function can be used as a regular scalar function, but only in the `SELECT` clause. Invoking `unnest` with the `recursive` parameter will unnest lists and structs of multiple levels. The depth of unnesting can be limited using the `max_depth` parameter (which assumes `recursive` unnesting by default).

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

### Seeting the Maximum Depth of Unnesting

The `max_depth` parameter allows limiting the maximum depth of recursive unnesting (which is assumed by default and does not have to be specified separately).
For example, unnestig to `max_depth` of 2 yields the following:

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 2) AS x;
```

|     x     |
|-----------|
| [1, 2]    |
| [3, 4]    |
| [5, 6]    |
| [7, 8, 9] |
| []        |
| [10, 11]  |

Meanwhile, unnesting to `max_depth` of 3 results in

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 3) AS x;
```

| x  |
|---:|
| 1  |
| 2  |
| 3  |
| 4  |
| 5  |
| 6  |
| 7  |
| 8  |
| 9  |
| 10 |
| 11 |

### Keeping track of the index

To keep track of each entry's position within the original list, `unnest` may be combined with [`generate_subscripts`](../functions/nested#generate_subscripts):

```sql
SELECT unnest(l) as x, generate_subscripts(l, 1) AS index FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

| x | index |
|---|-------|
| 1 | 1     |
| 2 | 2     |
| 3 | 3     |
| 4 | 1     |
| 5 | 2     |
