---
layout: docu
title: UNNEST
selected: Documentation/SQL/Query Syntax/UNNEST
expanded: SQL
---

The `UNNEST` function is used to unnest a list by one level. The function can be used as a regular scalar function, but only in the `SELECT` clause. `UNNEST` is a special function in the sense that it changes the cardinality of the result. The result of the `UNNEST` function is one tuple per entry in the list.

When `UNNEST` is combined with regular scalar expressions, those expressions are repeated for every entry in the list. When multiple lists are unnested in the same `SELECT` clause, the lists are unnested side-by-side. If one list is longer than the other, the shorter list will be padded with `NULL` values.

An empty list and a `NULL` list will both unnest to zero elements.

## Examples
```sql
-- unnest a scalar list, generating 3 rows (1, 2, 3)
SELECT UNNEST([1, 2, 3]);
-- unnest a scalar list, generating 3 rows ((1, 10), (2, 11), (3, NULL))
SELECT UNNEST([1, 2, 3]), UNNEST([10, 11]);
-- unnest a scalar list, generating 3 rows ((1, 10), (2, 10), (3, 10))
SELECT UNNEST([1, 2, 3]), 10;
-- unnest a list column generated from a subquery
SELECT UNNEST(l) + 10 FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
-- empty result
SELECT UNNEST([]);
```
