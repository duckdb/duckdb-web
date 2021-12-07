---
layout: docu
title: Data Types
selected: Documentation/Data Types
expanded: Data Types
---
The table below shows all the built-in general-purpose data types. The alternatives listed in the aliases column can be used to refer to these types as well, however, note that the aliases are not part of the SQL standard and hence might not be accepted by other database engines.

| Name | Aliases | Description |
|:---|:---|:---|
| `BIGINT` | `INT8`, `LONG` | signed eight-byte integer |
| `BOOLEAN` | `BOOL`, `LOGICAL` | logical boolean (true/false) |
| `BLOB` | `BYTEA`, `BINARY,` `VARBINARY` | variable-length binary data |
| `DATE` |   | calendar date (year, month day) |
| `DOUBLE` | `FLOAT8`, `NUMERIC`, `DECIMAL` | double precision floating-point number (8 bytes) |
| `DECIMAL(s, p)` | | fixed-precision floating point number with the given scale and precision |
| `HUGEINT` | | signed sixteen-byte integer|
| `INTEGER` | `INT4`, `INT`, `SIGNED` | signed four-byte integer |
| `REAL` | `FLOAT4`, `FLOAT` | single precision floating-point number (4 bytes)|
| `SMALLINT` | `INT2`, `SHORT` | signed two-byte integer|
| `TIME` | | time of day (no time zone) |
| `TIMESTAMP` | `DATETIME` | combination of time and date |
| `TINYINT` | `INT1` | signed one-byte integer|
| `UBIGINT` | | unsigned eight-byte integer |
| `UINTEGER` | | unsigned four-byte integer |
| `USMALLINT` | | unsigned two-byte integer |
| `UTINYINT` | | unsigned one-byte integer |
| `UUID` | | UUID data type |
| `VARCHAR` | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | variable-length character string |

In addition, the composite types `ROW`, `MAP` and `ARRAY` are supported.

* (Multi-dimensional) arrays can be created by appending square brackets `[]` after the type, e.g. `INT[]` to create an integer array.
* `ROW` can be created by specifying the individual columns that reside within the row, e.g. `ROW(a INTEGER, b VARCHAR)`. Note that rows can be nested, and can also contain arrays.

### More
