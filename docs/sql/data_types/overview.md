---
layout: docu
title: Data Types
blurb: The table below shows all the built-in general-purpose data types.
---

## General-Purpose Data Types

The table below shows all the built-in general-purpose data types. The alternatives listed in the aliases column can be used to refer to these types as well, however, note that the aliases are not part of the SQL standard and hence might not be accepted by other database engines.

| Name | Aliases | Description |
|:--|:--|:----|
| `BIGINT` | `INT8`, `LONG` | signed eight-byte integer |
| `BIT` | `BITSTRING` | string of 1s and 0s |
| `BLOB` | `BYTEA`, `BINARY,` `VARBINARY` | variable-length binary data |
| `BOOLEAN` | `BOOL`, `LOGICAL` | logical boolean (true/false) |
| `DATE` |   | calendar date (year, month day) |
| `DECIMAL(prec, scale)` | `NUMERIC(prec, scale)` | fixed-precision number with the given width (precision) and scale, defaults to `prec = 18` and `scale = 3` |
| `DOUBLE` | `FLOAT8`, | double precision floating-point number (8 bytes) |
| `HUGEINT` | | signed sixteen-byte integer|
| `INTEGER` | `INT4`, `INT`, `SIGNED` | signed four-byte integer |
| `INTERVAL` |  | date / time delta |
| `REAL` | `FLOAT4`, `FLOAT` | single precision floating-point number (4 bytes)|
| `SMALLINT` | `INT2`, `SHORT` | signed two-byte integer|
| `TIME` | | time of day (no time zone) |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMPTZ` | combination of time and date that uses the current time zone |
| `TIMESTAMP` | `DATETIME` | combination of time and date |
| `TINYINT` | `INT1` | signed one-byte integer|
| `UBIGINT` | | unsigned eight-byte integer |
| `UHUGEINT` | | unsigned sixteen-byte integer |
| `UINTEGER` | | unsigned four-byte integer |
| `USMALLINT` | | unsigned two-byte integer |
| `UTINYINT` | | unsigned one-byte integer |
| `UUID` | | UUID data type |
| `VARCHAR` | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | variable-length character string |

Implicit and explicit typecasting is possible between numerous types, see the [Typecasting](typecasting) page for details.

## Nested / Composite Types

DuckDB supports five nested data types: `ARRAY`, `LIST`, `MAP`, `STRUCT`, and `UNION`. Each supports different use cases and has a different structure.

| Name | Description | Rules when used in a column | Build from values | Define in DDL/CREATE |
|:-|:---|:---|:--|:--|
| [`ARRAY`](../../sql/data_types/array) | An ordered, fixed-length sequence of data values of the same type. | Each row must have the same data type within each instance of the `ARRAY` and the same number of elements. | `[1, 2, 3]` | `INTEGER[3]` |
| [`LIST`](../../sql/data_types/list) | An ordered sequence of data values of the same type. | Each row must have the same data type within each instance of the `LIST`, but can have any number of elements. | `[1, 2, 3]` | `INTEGER[]` |
| [`MAP`](../../sql/data_types/map) | A dictionary of multiple named values, each key having the same type and each value having the same type. Keys and values can be any type and can be different types from one another. | Rows may have different keys. | `map([1, 2], ['a', 'b'])` | `MAP(INTEGER, VARCHAR)` |
| [`STRUCT`](../../sql/data_types/struct) | A dictionary of multiple named values, where each key is a string, but the value can be a different type for each key. | Each row must have the same keys. | `{'i': 42, 'j': 'a'}` | `STRUCT(i INTEGER, j VARCHAR)` |
| [`UNION`](../../sql/data_types/union) | A union of multiple alternative data types, storing one of them in each value at a time. A union also contains a discriminator "tag" value to inspect and access the currently set member type. | Rows may be set to different member types of the union. | `union_value(num := 2)` | `UNION(num INTEGER, text VARCHAR)` |

### Updating Values of Nested Types

When performing _updates_ on values of nested types, DuckDB performs a _delete_ operation followed by an _insert_ operation.
When used in a table with ART indexes (either via explicit indexes or primary keys/unique constraints), this can lead to [unexpected constraint violations](../indexes#over-eager-unique-constraint-checking).
For example:

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');

UPDATE tbl
  SET j = [2]
  WHERE i = 1;
```

```console
Constraint Error: Duplicate key "i: 1" violates primary key constraint.
If this is an unexpected constraint violation please double check with the known index limitations section in our documentation (https://duckdb.org/docs/sql/indexes).
```

## Nesting

`ARRAY`, `LIST`, `MAP`, `STRUCT`, and `UNION` types can be arbitrarily nested to any depth, so long as the type rules are observed.

```sql
-- Struct with lists
SELECT {'birds': ['duck', 'goose', 'heron'], 'aliens': NULL, 'amphibians': ['frog', 'toad']};
-- Struct with list of maps
SELECT {'test': [map([1, 5], [42.1, 45]), map([1, 5], [42.1, 45])]};
-- A list of unions
SELECT [union_value(num := 2), union_value(str := 'ABC')::UNION(str VARCHAR, num INTEGER)];
```

## Performance Implications

The choice of data types can have a strong effect on performance. Please consult the [Performance Guide](../../guides/performance/schema) for details.

