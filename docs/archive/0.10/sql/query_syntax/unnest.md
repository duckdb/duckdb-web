---
layout: docu
title: Unnesting
---

## Examples

Unnest a list, generating 3 rows (1, 2, 3):

```sql
SELECT unnest([1, 2, 3]);
```

Unnesting a struct, generating two columns (a, b):

```sql
SELECT unnest({'a': 42, 'b': 84});
```

Recursive unnest of a list of structs:

```sql
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
```

Limit depth of recursive unnest using `max_depth`:

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 2);
```

The `unnest` special function is used to unnest lists or structs by one level. The function can be used as a regular scalar function, but only in the `SELECT` clause. Invoking `unnest` with the `recursive` parameter will unnest lists and structs of multiple levels. The depth of unnesting can be limited using the `max_depth` parameter (which assumes `recursive` unnesting by default).

### Unnesting Lists

Unnest a list, generating 3 rows (1, 2, 3):

```sql
SELECT unnest([1, 2, 3]);
```

Unnest a scalar list, generating 3 rows ((1, 10), (2, 11), (3, NULL)):

```sql
SELECT unnest([1, 2, 3]), unnest([10, 11]);
```

Unnest a scalar list, generating 3 rows ((1, 10), (2, 10), (3, 10)):

```sql
SELECT unnest([1, 2, 3]), 10;
```

Unnest a list column generated from a subquery:

```sql
SELECT unnest(l) + 10 FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

Empty result:

```sql
SELECT unnest([]);
```

Empty result:

```sql
SELECT unnest(NULL);
```

Using `unnest` on a list will emit one tuple per entry in the list. When `unnest` is combined with regular scalar expressions, those expressions are repeated for every entry in the list. When multiple lists are unnested in the same `SELECT` clause, the lists are unnested side-by-side. If one list is longer than the other, the shorter list will be padded with `NULL` values.

An empty list and a `NULL` list will both unnest to zero elements.

### Unnesting Structs

Unnesting a struct, generating two columns (a, b):

```sql
SELECT unnest({'a': 42, 'b': 84});
```

Unnesting a struct, generating two columns (a, b):

```sql
SELECT unnest({'a': 42, 'b': {'x': 84}});
```

`unnest` on a struct will emit one column per entry in the struct.

### Recursive Unnest

Unnesting a list of lists recursively, generating 5 rows (1, 2, 3, 4, 5):

```sql
SELECT unnest([[1, 2, 3], [4, 5]], recursive := true);
```

Unnesting a list of structs recursively, generating two rows of two columns (a, b):

```sql
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
```

Unnesting a struct, generating two columns (a, b):

```sql
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

Meanwhile, unnesting to `max_depth` of 3 results in:

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

### Keeping Track of List Entry Positions

To keep track of each entry's position within the original list, `unnest` may be combined with [`generate_subscripts`](../functions/nested#generate_subscripts):

```sql
SELECT unnest(l) as x, generate_subscripts(l, 1) AS index
FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

| x | index |
|--:|------:|
| 1 | 1     |
| 2 | 2     |
| 3 | 3     |
| 4 | 1     |
| 5 | 2     |