---
layout: docu
title: Union
selected: Documentation/Data Types/Union
expanded: Nested
---

## Union Data Type

A `UNION` *type* (not to be confused with the SQL `UNION` operator) is a nested type capable of holding one of multiple "alternative" values, much like the `union` in C. The main difference being that these `UNION` types are *tagged unions* and thus always carry a discriminator "tag" which signals which alternative it is currently holding, even if the inner value itself is null. `UNION` types are thus more similar to C++17's `std::variant`, Rust's `Enum` or the "sum type" present in most functional languages.

`UNION` types must always have at least one member, and while they can contain multiple members of the same type, the tag names must be unique. `UNION` types can have at most 256 members.
 
Under the hood, `UNION` types are implemented on top of `STRUCT` types, and simply keep the "tag" as the first entry.

`UNION` values can be created with the [`UNION_VALUE(tag := expr)`](../functions/nested#union-functions) function or by [casting from a member type](#casting-to-unions).

### Example 
```sql
-- Create a table with a union column
CREATE TABLE tbl1(u UNION(num INT, str VARCHAR));

-- Any type can be implicitly cast to a union containing the type.
-- Any union can also be implicitly cast to a another union if 
-- the source union members are a subset of the targets.
-- Note: only if the cast is unambiguous! 
-- More details in the 'Union casts' section below.
INSERT INTO tbl1 values (1) , ('two') , (union_value(str := 'three'));
-- Union use the member types varchar cast functions when casting to varchar.
SELECT u from tbl1;
-- returns:
--    1
--    two
--    three
-- Select all the 'str' members
SELECT union_extract(u, 'str') FROM tbl1;
-- Alternatively, you can use 'dot syntax' like with structs
SELECT u.str FROM tbl1;
-- returns: 
--    NULL
--    two
--    three

-- Select the currently active tag from the union as an enum.
SELECT union_tag(u) FROM tbl1;
-- returns:
--    num
--    str
--    str
```

## Union casts
Compared to other nested types, `UNION`s allow a set of implicit casts to facilitate unintrusive and natural usage when working with their members as "subtypes".
However, these casts have been designed with two principles in mind, to avoid ambiguity and to avoid casts that could lead to loss of information. This prevents `UNION`s from being completely "transparent", while still allowing `UNION` types to have a "supertype" relationship with their members.

Thus `UNION` types can't be implicitly cast to any of their member types in general, since the information in the other members not matching the target type would be "lost". If you want to coerce a `UNION` into one of its members, you should use the `union_extract` function explicitly instead.

The only exception to this is when casting a `UNION` to `VARCHAR`, in which case the members will all use their corresponding `VARCHAR` casts. Since everything can be cast to `VARCHAR`, this is "safe" in a sense. 

### Casting to unions
A type can always be implicitly cast to a `UNION` if it can be implicitly cast to one of the `UNION` member types.

- If there are multiple candidates, the lowest cast cost is used. 
- If the cast still is ambiguous, i.e. there are multiple candidates with the same implicit casting cost, an error is raised. 

So how do we disambiguate if we want to create a `UNION` with multiple members of the same type? By using the `union_value` function, which takes a keyword argument specifying the tag. For example, `union_value(num := 2::INT)` will create a `UNION` with a single member of type `INT` with the tag `num`. This can then be used to disambiguate in an explicit (or implicit, read on below!) `UNION` to `UNION` cast, like `CAST(union_value(b := 2) AS UNION(a INT, b INT))`.

### Casting between unions
`UNION` types can be cast between each other if the source type is a "subset" of the target type. In other words, all the tags in the source `UNION` must be present in the target `UNION`, and all the types of the matching tags must be implicitly castable between source and target. In essence, this means that `UNION` types are covariant with respect to their members.


|Ok| Source                |          Target       |               Comments             |
|----|---------------------|-----------------------|------------------------------------|
| ✅ | UNION(a A, b B)      | UNION(a A, b B, c C) |                                     |
| ✅ | UNION(a A, b B)      | UNION(a A, b C)      | if B can be implicitly cast to C   |
| ❌ | UNION(a A, b B, c C) | UNION(a A, b B)      |                                    |
| ❌ | UNION(a A, b B)      | UNION(a A, b C)      | if B can't be implicitly cast to C |
| ❌ | UNION(A, B, D)       | UNION(A, B, C)       |                                    |


## Comparison and Sorting
Since `UNION` types are implemented on top of `STRUCT` types internally, they can be used with all the comparison operators as well as in both `WHERE` and `HAVING` clauses with [the same semantics as `STRUCT`s](struct#comparison-operators). The "tag" is always stored as the first struct entry, which ensures that the `UNION` types are compared and ordered by "tag" first.

## Functions
See [Nested Functions](../../sql/functions/nested#union-functions).
    