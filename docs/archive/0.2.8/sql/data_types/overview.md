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
| `HUGEINT` | | signed sixteen-byte integer|
| `INTEGER` | `INT4`, `INT`, `SIGNED` | signed four-byte integer |
| `REAL` | `FLOAT4`, `FLOAT` | single precision floating-point number (4 bytes)|
| `SMALLINT` | `INT2`, `SHORT` | signed two-byte integer|
| `TIMESTAMP` | `DATETIME` | time of day (no time zone) |
| `TINYINT` | `INT1` | signed one-byte integer|
| `VARCHAR` | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | variable-length character string |

### More
