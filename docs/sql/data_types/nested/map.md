---
layout: docu
title: Map
selected: Documentation/Data Types/Nested/Map
expanded: Nested
---

## Map Data Type

`MAP`s are similar to `STRUCT`s in that they are an ordered list of "entries" where a key maps to a value. However, `MAP`s do not need to have the same keys present on each row, and thus open additional use cases. `MAP`s are useful when the schema is unknown beforehand, and when adding or removing keys in subsequent rows. Their flexibility is a key differentiator.

`MAP`s must have a single type for all keys, and a single type for all values. Keys and values can be any type, and the type of the keys does not need to match the type of the values (Ex: a `MAP` of `INT`s to `VARCHAR`s). `MAP`s may also have duplicate keys. This is possible and useful because maps are ordered. `MAP`s are also more forgiving when extracting values, as they return an empty list if a key is not found rather than throwing an error as structs do.

In contrast, `STRUCT`s must have string keys, but each key may have a value of a different type. `STRUCT`s may not have duplicate keys.

To construct a `MAP`, use the `map` function. Provide a list of keys as the first parameter, and a list of values for the second.

### Creating Maps
```sql
-- A map with integer keys and varchar values. This returns {1=a, 5=e}
select map([1, 5], ['a', 'e']);
-- A map with integer keys and numeric values. This returns {1=42.001, 5=-32.100} 
select map([1, 5], [42.001, -32.1]);
-- Keys and/or values can also be nested types.
-- This returns {[a, b]=[1.1, 2.2], [c, d]=[3.3, 4.4]}
select map([['a', 'b'], ['c', 'd']], [[1.1, 2.2], [3.3, 4.4]]);
-- Create a table with a map column that has integer keys and double values
CREATE TABLE map_table (map_col MAP(INT,DOUBLE));
```
### Retrieving from Maps
`MAP`s use bracket notation for retrieving values. This is due to the variety of types that can be used as a `MAP`'s key. Selecting from a `MAP` also returns a `LIST` rather than an individual value.
```sql
-- Use bracket notation to retrieve a list containing the value at a key's location. This returns [42]
-- Note that the expression in bracket notation must match the type of the map's key
SELECT map([100, 5], [42, 43])[100];
-- To retrieve the underlying value, use list selection syntax to grab the 0th element.
-- This returns 42
SELECT map([100, 5], [42, 43])[100][0];
-- If the element is not in the map, an empty list will be returned. Returns []
-- Note that the expression in bracket notation must match the type of the map's key else an error is returned
SELECT map([100, 5], [42, 43])[123];
-- The element_at function can also be used to retrieve a map value. This returns [42]
SELECT element_at(map([100, 5], [42, 43]),100);
```

## Comparison with other nested types
DuckDB supports three nested data types: lists, structs, and maps. Each supports different use cases and has a different structure. 

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:---|:---|:---|:---|:---|
| [LIST](/docs/sql/data_types/nested/list) | An ordered sequence of data values of the same type. | Each row must have the same data type within each LIST, but can have any number of elements. | [1, 2, 3] | INT[ ] |
| [STRUCT](/docs/sql/data_types/nested/struct) | A dictionary of multiple named values, where each key is a string, but the value can be a different type for each key. | Each row must have the same keys. | {'i': 42, 'j': 'a'} | STRUCT<i: INT, j: VARCHAR> |
| [MAP](/docs/sql/data_types/nested/map) | A dictionary of multiple named values, each key having the same type and each value having the same type. Keys and values can be any type and can be different types from one another. | Rows may have different keys. | map([1,2],['a','b']) | MAP<INT, VARCHAR> |

## Nesting

`LIST`s, `STRUCT`s, and `MAP`s can be arbitrarily nested to any depth, so long as the type rules are observed.

```sql
-- Struct with lists
SELECT {'birds': ['duck', 'goose', 'heron'], 'aliens': NULL, 'amphibians': ['frog', 'toad']};
-- Struct with list of maps
SELECT {'test': [map([1, 5], [42.1, 45]), map([1, 5], [42.1, 45])]};
```

## Comparison Operators

Nested types can be compared using all the [comparison operators](../expressions/comparison_operators).
These comparisons can be used in [logical expressions](../expressions/logical_operators)
for both `WHERE` and `HAVING` clauses, as well as for creating [Boolean values](./boolean).

The ordering is defined positionally in the same way that words can be ordered in a dictionary.
`NULL` values compare greater than all other values and are considered equal to each other.

At the top level, `NULL` nested values obey standard SQL `NULL` comparison rules:
comparing a `NULL` nested value to a non-`NULL` nested value produces a `NULL` result.
Comparing nested value _members_ , however, uses the internal nested value rules for `NULL`s,
and a `NULL` nested value member will compare above a non-`NULL` nested value member.

## Grouping and Joining

Nested types can be used in `GROUP BY` clauses and as expressions for `JOIN`s.

## Functions
See [Nested Functions](/docs/sql/functions/nested).
