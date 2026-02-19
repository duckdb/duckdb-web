---
layout: docu
title: Union Type
---

A `UNION` *type* (not to be confused with the SQL [`UNION` operator]({% link docs/preview/sql/query_syntax/setops.md %}#union-all-by-name)) is a nested type capable of holding one of multiple “alternative” values, much like the `union` in C. The main difference is that these `UNION` types are *tagged unions* and thus always carry a discriminator “tag” which signals which alternative it is currently holding, even if the inner value itself is null. `UNION` types are thus more similar to C++17's `std::variant`, Rust's `Enum` or the “sum type” present in most functional languages.

`UNION` types must always have at least one member, and while they can contain multiple members of the same type, the tag names must be unique. `UNION` types can have at most 256 members.

Under the hood, `UNION` types are implemented on top of `STRUCT` types, and simply keep the “tag” as the first entry.

`UNION` values can be created with the [`union_value(tag := expr)`]({% link docs/preview/sql/functions/union.md %}) function or by [casting from a member type](#casting-to-unions).

## Example

Create a table with a `UNION` column:

```sql
CREATE TABLE tbl1 (u UNION(num INTEGER, str VARCHAR));
INSERT INTO tbl1 VALUES (1), ('two'), (union_value(str := 'three'));
```

Any type can be implicitly cast to a `UNION` containing the type. Any `UNION` can also be implicitly cast to another `UNION` if the source `UNION` members are a subset of the target's (if the cast is unambiguous).

`UNION` uses the member types' `VARCHAR` cast functions when casting to `VARCHAR`:

```sql
SELECT u FROM tbl1;
```

|   u   |
|-------|
| 1     |
| two   |
| three |

Select all the `str` members:

```sql
SELECT union_extract(u, 'str') AS str
FROM tbl1;
```

|  str  |
|-------|
| NULL  |
| two   |
| three |

Alternatively, you can use 'dot syntax' similarly to [`STRUCT`s]({% link docs/preview/sql/data_types/struct.md %}).

```sql
SELECT u.str
FROM tbl1;
```

|  str  |
|-------|
| NULL  |
| two   |
| three |

Select the currently active tag from the `UNION` as an `ENUM`.

```sql
SELECT union_tag(u) AS t
FROM tbl1;
```

|  t  |
|-----|
| num |
| str |
| str |

## Union Casts

Compared to other nested types, `UNION`s allow a set of implicit casts to facilitate unintrusive and natural usage when working with their members as “subtypes”.
However, these casts have been designed with two principles in mind, to avoid ambiguity and to avoid casts that could lead to loss of information. This prevents `UNION`s from being completely “transparent”, while still allowing `UNION` types to have a “supertype” relationship with their members.

Thus `UNION` types can't be implicitly cast to any of their member types in general, since the information in the other members not matching the target type would be “lost”. If you want to coerce a `UNION` into one of its members, you should use the `union_extract` function explicitly instead.

The only exception to this is when casting a `UNION` to `VARCHAR`, in which case the members will all use their corresponding `VARCHAR` casts. Since everything can be cast to `VARCHAR`, this is “safe” in a sense.

### Casting to Unions

A type can always be implicitly cast to a `UNION` if it can be implicitly cast to one of the `UNION` member types.

* If there are multiple candidates, the built in implicit casting priority rules determine the target type. For example, a `FLOAT` → `UNION(i INTEGER, v VARCHAR)` cast will always cast the `FLOAT` to the `INTEGER` member before `VARCHAR`.
* If the cast still is ambiguous, i.e., there are multiple candidates with the same implicit casting priority, an error is raised. This usually happens when the `UNION` contains multiple members of the same type, e.g., a `FLOAT` → `UNION(i INTEGER, num INTEGER)` is always ambiguous.

So how do we disambiguate if we want to create a `UNION` with multiple members of the same type? By using the `union_value` function, which takes a keyword argument specifying the tag. For example, `union_value(num := 2::INTEGER)` will create a `UNION` with a single member of type `INTEGER` with the tag `num`. This can then be used to disambiguate in an explicit (or implicit, read on below!) `UNION` to `UNION` cast, like `CAST(union_value(b := 2) AS UNION(a INTEGER, b INTEGER))`.

### Casting between Unions

`UNION` types can be cast between each other if the source type is a “subset” of the target type. In other words, all the tags in the source `UNION` must be present in the target `UNION`, and all the types of the matching tags must be implicitly castable between source and target. In essence, this means that `UNION` types are covariant with respect to their members.

| Ok | Source                 | Target                 | Comments                               |
|----|------------------------|------------------------|----------------------------------------|
| ✅ | `UNION(a A, b B)`      | `UNION(a A, b B, c C)` |                                        |
| ✅ | `UNION(a A, b B)`      | `UNION(a A, b C)`      | if `B` can be implicitly cast to `C`   |
| ❌ | `UNION(a A, b B, c C)` | `UNION(a A, b B)`      |                                        |
| ❌ | `UNION(a A, b B)`      | `UNION(a A, b C)`      | if `B` can't be implicitly cast to `C` |
| ❌ | `UNION(A, B, D)`       | `UNION(A, B, C)`       |                                        |

## Comparison and Sorting

Since `UNION` types are implemented on top of `STRUCT` types internally, they can be used with all the comparison operators as well as in both `WHERE` and `HAVING` clauses with the [same semantics as `STRUCT`s]({% link docs/preview/sql/data_types/struct.md %}#comparison-operators). The “tag” is always stored as the first struct entry, which ensures that the `UNION` types are compared and ordered by “tag” first.

## Functions

See [Union Functions]({% link docs/preview/sql/functions/union.md %}).
