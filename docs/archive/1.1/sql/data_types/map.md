---
layout: docu
title: Map Type
---

`MAP`s are similar to `STRUCT`s in that they are an ordered list of “entries” where a key maps to a value. However, `MAP`s do not need to have the same keys present for each row, and thus are suitable for other use cases. `MAP`s are useful when the schema is unknown beforehand or when the schema varies per row; their flexibility is a key differentiator.

`MAP`s must have a single type for all keys, and a single type for all values. Keys and values can be any type, and the type of the keys does not need to match the type of the values (e.g., a `MAP` of `VARCHAR` to `INT` is valid). `MAP`s may not have duplicate keys. `MAP`s return an empty list if a key is not found rather than throwing an error as structs do.

In contrast, `STRUCT`s must have string keys, but each key may have a value of a different type. See the [data types overview]({% link docs/archive/1.1/sql/data_types/overview.md %}) for a comparison between nested data types.

To construct a `MAP`, use the bracket syntax preceded by the `MAP` keyword.

## Creating Maps

A map with `VARCHAR` keys and `INTEGER` values. This returns `{key1=10, key2=20, key3=30}`:

```sql
SELECT MAP {'key1': 10, 'key2': 20, 'key3': 30};
```

Alternatively use the map_from_entries function. This returns `{key1=10, key2=20, key3=30}`:

```sql
SELECT map_from_entries([('key1', 10), ('key2', 20), ('key3', 30)]);
```

A map can be also created using two lists: keys and values. This returns `{key1=10, key2=20, key3=30}`:

```sql
SELECT MAP(['key1', 'key2', 'key3'], [10, 20, 30]);
```

A map can also use INTEGER keys and NUMERIC values. This returns `{1=42.001, 5=-32.100}`:

```sql
SELECT MAP {1: 42.001, 5: -32.1};
```

Keys and/or values can also be nested types. This returns `{[a, b]=[1.1, 2.2], [c, d]=[3.3, 4.4]}`:

```sql
SELECT MAP {['a', 'b']: [1.1, 2.2], ['c', 'd']: [3.3, 4.4]};
```

Create a table with a map column that has INTEGER keys and DOUBLE values:

```sql
CREATE TABLE tbl (col MAP(INTEGER, DOUBLE));
```

## Retrieving from Maps

`MAP`s use bracket notation for retrieving values. Selecting from a `MAP` returns a `LIST` rather than an individual value, with an empty `LIST` meaning that the key was not found.

Use bracket notation to retrieve a list containing the value at a key's location. This returns `[5]`. Note that the expression in bracket notation must match the type of the map's key:

```sql
SELECT MAP {'key1': 5, 'key2': 43}['key1'];
```

To retrieve the underlying value, use list selection syntax to grab the first element. This returns `5`:

```sql
SELECT MAP {'key1': 5, 'key2': 43}['key1'][1];
```

If the element is not in the map, an empty list will be returned. This returns `[]`. Note that the expression in bracket notation must match the type of the map's key else an error is returned:

```sql
SELECT MAP {'key1': 5, 'key2': 43}['key3'];
```

The element_at function can also be used to retrieve a map value. This returns `[5]`:

```sql
SELECT element_at(MAP {'key1': 5, 'key2': 43}, 'key1');
```

## Comparison Operators

Nested types can be compared using all the [comparison operators]({% link docs/archive/1.1/sql/expressions/comparison_operators.md %}).
These comparisons can be used in [logical expressions]({% link docs/archive/1.1/sql/expressions/logical_operators.md %})
for both `WHERE` and `HAVING` clauses, as well as for creating [Boolean values]({% link docs/archive/1.1/sql/data_types/boolean.md %}).

The ordering is defined positionally in the same way that words can be ordered in a dictionary.
`NULL` values compare greater than all other values and are considered equal to each other.

At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_, however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Functions

See [Map Functions]({% link docs/archive/1.1/sql/functions/map.md %}).