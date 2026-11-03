---
layout: docu
redirect_from:
- /docs/api/python/types
- /docs/clients/python/types
- /docs/stable/clients/python/types
- /docs/current/clients/python/types
- /docs/lts/clients/python/types
- /docs/preview/clients/python/types
title: Types API
---

The `DuckDBPyType` class, `duckdb.sqltypes.DuckDBPyType`, represents one of the [data types]({% link docs/2.0/sql/data_types/overview.md %}). Use `DuckDBPyType` to describe SQL types when declaring function parameters, return types, or casts. Python types such as `int` are accepted too: `int` describes `BIGINT`. Converting a data value such as `5` follows different rules; see [Python Object Conversion]({% link docs/2.0/clients/python/conversion.md %}#object-conversion-python-object-to-duckdb).

## Converting from Other Types

Wherever a `DuckDBPyType` is expected, any of the options listed below can be given instead.

### Python Built-Ins

The table below shows the mapping of Python Built-in types to DuckDB type.

<div class="monospace_table"></div>

| Built-in types | DuckDB type |
|:---------------|:------------|
| bool           | BOOLEAN     |
| bytearray      | BLOB        |
| bytes          | BLOB        |
| float          | DOUBLE      |
| int            | BIGINT      |
| str            | VARCHAR     |

### NumPy Scalar Types

The table below shows the mapping of NumPy scalar types to DuckDB type. A NumPy dtype object does not convert: `DuckDBPyType(numpy.dtype("int32"))` raises a `NotImplementedException`.

<div class="monospace_table"></div>

| Type          | DuckDB type |
|:--------------|:------------|
| numpy.bool_   | BOOLEAN     |
| numpy.float32 | FLOAT       |
| numpy.float64 | DOUBLE      |
| numpy.int16   | SMALLINT    |
| numpy.int32   | INTEGER     |
| numpy.int64   | BIGINT      |
| numpy.int8    | TINYINT     |
| numpy.uint16  | USMALLINT   |
| numpy.uint32  | UINTEGER    |
| numpy.uint64  | UBIGINT     |
| numpy.uint8   | UTINYINT    |

### Type Names

A string is read as a SQL type name, such as `"INTEGER"`, `"INT[]"`, `"STRUCT(a INT)"`, or `"MAP(INT, VARCHAR)"`:

```python
import duckdb
from duckdb.sqltypes import DuckDBPyType

print(DuckDBPyType("MAP(INT, VARCHAR)"))
```

```text
MAP(INTEGER, VARCHAR)
```

A type created with [`CREATE TYPE`]({% link docs/2.0/sql/statements/create_type.md %}) exists only in its database, so name the connection: `DuckDBPyType("mood", connection=con)` or `con.type("mood")`. Without a connection, the name is looked up on the default connection.

```python
con = duckdb.connect()
con.execute("CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy')")
print(con.type("mood"))
```

```text
ENUM('sad', 'ok', 'happy')
```

### Nested Types

#### `list[child_type]`

`list` type objects map to a `LIST` type of the child type, which can itself be nested.

```python
import duckdb.sqltypes

print(duckdb.sqltypes.DuckDBPyType(list[int]))
```

```text
BIGINT[]
```

#### `dict[key_type, value_type]`

`dict` type objects map to a `MAP` type of the key type and the value type.

```python
import duckdb.sqltypes

print(duckdb.sqltypes.DuckDBPyType(dict[str, int]))
```

```text
MAP(VARCHAR, BIGINT)
```

#### `{'a': field_one, 'b': field_two, ..., 'n': field_n}`

`dict` objects map to a `STRUCT` composed of the keys and values of the dict.

```python
import duckdb.sqltypes

print(duckdb.sqltypes.DuckDBPyType({'a': str, 'b': int}))
```

```text
STRUCT(a VARCHAR, b BIGINT)
```

#### `Union[type_1, ... type_n]`

`typing.Union` objects, and unions written as `type_1 | type_2`, map to a `UNION` type of the provided types.

```python
import duckdb.sqltypes
from typing import Union

print(duckdb.sqltypes.DuckDBPyType(Union[int, str, bool, bytearray]))
print(duckdb.sqltypes.DuckDBPyType(int | str))
```

```text
UNION(u1 BIGINT, u2 VARCHAR, u3 BOOLEAN, u4 BLOB)
UNION(u1 BIGINT, u2 VARCHAR)
```

### Creation Functions

For the built-in types, you can use the constants defined in `duckdb.sqltypes`:

<div class="monospace_table"></div>

| DuckDB type    |
|:---------------|
| BIGINT         |
| BIT            |
| BLOB           |
| BOOLEAN        |
| DATE           |
| DOUBLE         |
| FLOAT          |
| HUGEINT        |
| INTEGER        |
| INTERVAL       |
| SMALLINT       |
| SQLNULL        |
| TIME_NS        |
| TIME_TZ        |
| TIME           |
| TIMESTAMP_MS   |
| TIMESTAMP_NS   |
| TIMESTAMP_S    |
| TIMESTAMP_TZ   |
| TIMESTAMP      |
| TINYINT        |
| UBIGINT        |
| UHUGEINT       |
| UINTEGER       |
| USMALLINT      |
| UTINYINT       |
| UUID           |
| VARCHAR        |
| VARIANT        |

For the complex types there are methods available on the `DuckDBPyConnection` object or the `duckdb` module.
Anywhere a `DuckDBPyType` is accepted, we will also accept one of the type objects that can implicitly convert to a `DuckDBPyType`.

```python
from duckdb.sqltypes import INTEGER, VARCHAR

print(duckdb.list_type(INTEGER))
print(duckdb.array_type(INTEGER, 3))
print(duckdb.struct_type({"a": INTEGER, "b": VARCHAR}))
print(duckdb.map_type(VARCHAR, INTEGER))
print(duckdb.decimal_type(10, 2))
```

```text
INTEGER[]
INTEGER[3]
STRUCT(a INTEGER, b VARCHAR)
MAP(VARCHAR, INTEGER)
DECIMAL(10,2)
```

#### `list_type`

Parameters:

* `type: DuckDBPyType`

#### `array_type`

Parameters:

* `type: DuckDBPyType`
* `size: int`

#### `struct_type` | `row_type`

Parameters:

* `fields: Union[list[DuckDBPyType], dict[str, DuckDBPyType]]`

A list names the fields `v1`, `v2`, and so on. An empty dict or list gives an empty `STRUCT`.

#### `map_type`

Parameters:

* `key: DuckDBPyType`
* `value: DuckDBPyType`

#### `decimal_type`

Parameters:

* `width: int`
* `scale: int`

A `DECIMAL` has a width of 1 to 38 and a scale of 0 to the width.

#### `union_type`

Parameters:

* `members: Union[list[DuckDBPyType], dict[str, DuckDBPyType]]`

#### `string_type`

Parameters:

* `collation: str`, by default `""`

#### `enum_type`

`enum_type` is not implemented and raises a `NotImplementedException`. Create an `ENUM` type with SQL and get it with `con.type()`, as shown under [Type Names](#type-names).

## Inspecting Types

A `DuckDBPyType` has an `id`, such as `'struct'`. A nested type, an `ENUM`, or a `DECIMAL` also has `children`, a list of pairs of a name and a type or a value. The field of a `STRUCT` type is also available by attribute or by key:

```python
point = duckdb.struct_type({"x": INTEGER, "y": VARCHAR})
print(point.id)
print(point.children)
print(point.x, point["y"])
```

```text
struct
[('x', INTEGER), ('y', VARCHAR)]
INTEGER VARCHAR
```
