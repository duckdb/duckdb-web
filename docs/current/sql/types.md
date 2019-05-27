
## Types
The table below shows all the built-in general-purpose data types. The alternatives listed in the aliases column can be used to refer to these types as well, however, note that the aliases are not part of the SQL standard and hence might not be accepted by other database engines.

| Name | Aliases | Description |
|:---|:---|:---|
| bigint | int8 | signed eight-byte integer |
| boolean | bool | logical boolean (true/false) |
| date |   | calendar date (year, month day) |
| double | numeric | double precision floating-point number (8 bytes) |
| integer | int, int4, signed | signed four-byte integer |
| real | float4 | single precision floating-point number (4 bytes)|
| smallint | int2 | signed two-byte integer|
| timestamp | datetime | time of day (no time zone) |
| tinyint |   | signed one-byte integer|
| varchar | char, bpchar, text, string| variable-length character string |

* [Numeric Types](https://www.duckdb.org/docs/sql/types/numeric_types)
* [Character Types](https://www.duckdb.org/docs/sql/types/character_types)
* [Date Type](https://www.duckdb.org/docs/sql/types/date_type)
* [Timestamp Type](https://www.duckdb.org/docs/sql/types/timestamp_type)
* [Boolean Type](https://www.duckdb.org/docs/sql/types/boolean_type)