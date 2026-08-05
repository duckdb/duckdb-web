---
layout: docu
redirect_from:
- /docs/preview/sql/query_syntax/unnest
- /docs/sql/query_syntax/unnest
- /docs/stable/sql/query_syntax/unnest
title: Unnesting
---

Unnesting is an operation that decomposes values of a [composite types]({% link docs/current/sql/data_types/overview.md %}#nested--composite-types) into its components.
Values of the [`LIST`]({% link docs/current/sql/data_types/list.md %}) and [`STRUCT`]({% link docs/current/sql/data_types/struct.md %}) type may be unnested using the [`unnest()` function]({% link docs/current/sql/functions/list.md %}#unnestlist-recursive-max_depth).

* Unnesting turns a `LIST`-typed value into a table column: each list-element creates a row, and each element become a column value.
* Unnesting a `STRUCT`-typed value creates a column for each member. The member key becomes the column name, and the member value becomes a column value. Values of a `STRUCT`-type may also be unnested using [dot-star (`⟨struct⟩.*`{:.language-sql .highlight}) shorthand syntax]({% link docs/current/sql/data_types/struct.md %}#unnest--struct), but the `unnest()` function offers some additional functionality.
* For an [unnamed struct]({ % link /docs/current/sql/data_types/struct %}#creating-structs-with-the-row-function), the unnesting operation is the same as for a named `STRUCT`, but in this case the column name is generated based on the (1-based) ordinal position of the member, prefixed by `element`. The dot-star (`⟨struct⟩.*`{:.language-sql .highlight}) shorthand syntax is not available for unnamed structs: unnamed structs can only be unnested using the `unnest()` function.

# Calling `unnest()`

The `LIST` or `STRUCT` value that is to be unnested is always passed as the first – mandatory – argument to the `unnest()` function.
The `unnest()` function has a number of optional additional arguments to control the behavior for [recursive unnesting](#recursive-unnesting).

The `unnest` function can be called in the [`SELECT`-clause]({% link docs/current/sql/query_syntax/select.md %}) as if it is a scalar function.
The `unnest` function may not be called in other contexts where one would normally be able to invoke scalar functions, like the `WHERE`, `GROUP BY`, or `ORDER BY` clauses.
When applied to values of the `LIST`-type, `unnest()` may also appear in clauses where one could normally use a [table function](#unnest-as-table-function).

## Unnesting `LIST`-Typed Values

To fully understand unnesting `LIST`-typed values, it is useful to distinguish between the 'input' row that provided the `LIST`-typed value that is to be unnested, and the 'ouput' row(s) created by the unnesting operation.
An individual invocation to `unnest()` on the `LIST`-typed value has the effect of duplicating the 'input' row while populating the field corresponding to the `unnest()` call with the element value.
In other words, the original row becomes a repeating group for element unnnested from the `LIST`-typed value.
Consequently, if `unnest()` gets called on an empty list (or a `NULL` value), no elements are unnested, and no 'ouput' rows are generated.

### Unnesting Multiple Lists

Multiple `LIST`-typed values may be unnested within the same `SELECT`-clause, so for one 'input' row there may be multiple row sets resulting from an `unnest()` invocation, and each may have its own number of rows.
Each result becomes a column of the output table, aligning their values by ordinal position, and backfilling columns with `NULL`-values when a particular result has a smaller number of elements than any of the other results.
In a final step, the columns of the input row are added to this result. In other words, the repeating group is created only once, and for all `unnest()` results, rather than again for each individual `unnest()` result.

### Getting the Element Index
Unnesting a value of the `LIST`-type yields only the element values. To also keep track of their indices (the subscripts), you can use the built-in macro [`generate_subscripts()`]({% link docs/current/sql/functions/list.md %}#generate_subscriptslist-dimension).
The `generate_subscripts` macro takes a value of the `LIST`-type as first argument.

### `unnest()` as Table Function

Since a call to `unnest` on a value of the `LIST`-type yields a rowset, it may also be treated as a [table function]({% link docs/current/sql/query_syntax/from.md %}#table-functions). 
This means it may appear in the [`FROM`-clause]({% link docs/current/sql/query_syntax/from.md %}) or a [`CALL`-statement]({% link docs/current/sql/statements/call.md %}).

Calls to `unnest()` in a `FROM`-clause or `CALL`-statement do not accept additional parameters, and can thus not be used for [recursive unnesting](#recursive-unnesting).

# Recursive Unnesting

By default, `unnest()` only unpacks the outermost components of the composite-type value.
Additional parameters may be passed to allow the unnesting operation to be applied to the unnested member values, and to their unnested values, and so on, recursively.
These additional parameters are:

* `recursive`: `BOOLEAN`, default: `false`. Pass `true` to recursively continue applying `unnest` to unnested member values. When explicitly passing `false`, recursion is disabled. In that case, other additional parameters such as `max_depth` and `keep_parent_names` are effectively ignored
* `max_depth`: `UINT32`, default: `1`. This controls how many levels of recursion should at most be applied. Values greater than `1` imply recursion, and in such cases `recursive` need not be explicitly passed as `true`.
* `keep_parent_names`: `BOOLEAN`, default: `false`. Whether to create column names using the keys of all ancestor members. This argument is applicable only when unnesting `STRUCT`-values.

Note that recursive unnesting always respects the type of the outermost call to `unnest()`:

* If a `LIST`-typed value is passed, then `LIST`-typed elements will be recursively unnested, while `STRUCT`-typed elements are not further unpacked.
* If a `STRUCT`-typed value is passed, then `STRUCT`-typed member values will be recursively unnested, while `LIST`-typed member values are not further unpacked.

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

### Unnesting Lists

Unnest a list, generating 3 rows (1, 2, 3):

```sql
SELECT unnest([1, 2, 3]);
```

Unnest a list, generating 3 rows ((1, 10), (2, 10), (3, 10)):

```sql
SELECT unnest([1, 2, 3]), 10;
```

Unnest two lists of different sizes, generating 3 rows ((1, 10), (2, 11), (3, NULL)):

```sql
SELECT unnest([1, 2, 3]), unnest([10, 11]);
```
Unnest a list column from a subquery:

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

Using `unnest` on a list emits one row per list entry. Regular scalar expressions in the same `SELECT` clause are repeated for every emitted row. When multiple lists are unnested in the same `SELECT` clause, the lists are unnested side-by-side. If one list is longer than the other, the shorter list is padded with `NULL` values.

Empty and `NULL` lists both unnest to zero rows.

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

### Setting the Maximum Depth of Unnesting

The `max_depth` parameter allows limiting the maximum depth of recursive unnesting (which is assumed by default and does not have to be specified separately).
For example, unnesting to `max_depth` of 2 yields the following:

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

To keep track of each entry's position within the original list, `unnest` may be combined with [`generate_subscripts`]({% link docs/current/sql/functions/list.md %}#generate_subscripts):

```sql
SELECT unnest(l) AS x, generate_subscripts(l, 1) AS index
FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

| x | index |
|--:|------:|
| 1 | 1     |
| 2 | 2     |
| 3 | 3     |
| 4 | 1     |
| 5 | 2     |

### Keep Column Names When Recursively Unnesting

The `keep_parent_names` parameter can be used to retain the parent column names when recursively unnesting a named struct. For example, unnesting the following query with `keep_parent_names` enabled:

```sql
SELECT unnest([{'a': 0, 'b': {'bb': {'bbb': 1}}}], recursive := true, keep_parent_names := true);
```

yields the following result:

|  a  | b.bb.bbb |
|----:|---------:|
|  0  |    1     |

In this case, the field names are preserved, showing the path to the innermost value. This is particularly useful when working with complex nested data structures, as it maintains the structure and naming convention of the original data. The parameter can also be used in conjunction with the `max_depth` parameter, allowing more control and enabling more precise management of nested structures.
