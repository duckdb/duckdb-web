
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

## Integer Types
The types `tinyint`, `smallint`, `integer`, and `bigint` store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error.

| Name | Aliases | Min | Max |
|:---|:---|---:|---:|
| tinyint |   | -127 | 127 |
| smallint | int2 | -32767 | 32767 |
| integer | int, int4, signed | -2147483647 | 2147483647 |
| bigint | int8 | -9223372036854775808 | 9223372036854775808 |

The type integer is the common choice, as it offers the best balance between range, storage size, and performance. The smallint type is generally only used if disk space is at a premium. The bigint type is designed to be used when the range of the integer type is insufficient.

## Floating-Point Types
The data types `real` and `double` precision are inexact, variable-precision numeric types. In practice, these types are usually implementations of IEEE Standard 754 for Binary Floating-Point Arithmetic (single and double precision, respectively), to the extent that the underlying processor, operating system, and compiler support it.

| Name | Aliases | Description |
|:---|:---|:---|
| real | float4 | single precision floating-point number (4 bytes)|
| double | numeric | double precision floating-point number (8 bytes) |

Inexact means that some values cannot be converted exactly to the internal format and are stored as approximations, so that storing and retrieving a value might show slight discrepancies. Managing these errors and how they propagate through calculations is the subject of an entire branch of mathematics and computer science and will not be discussed here, except for the following points:

* If you require exact storage and calculations (such as for monetary amounts), use the numeric type instead.
* If you want to do complicated calculations with these types for anything important, especially if you rely on certain behavior in boundary cases (infinity, underflow), you should evaluate the implementation carefully.
* Comparing two floating-point values for equality might not always work as expected.

On most platforms, the `real` type has a range of at least 1E-37 to 1E+37 with a precision of at least 6 decimal digits. The `double precision` type typically has a range of around 1E-307 to 1E+308 with a precision of at least 15 digits. Values that are too large or too small will cause an error. Rounding might take place if the precision of an input number is too high. Numbers too close to zero that are not representable as distinct from zero will cause an underflow error.

In addition to ordinary numeric values, the floating-point types have several special values:

`Infinity`
`-Infinity`
`NaN`

These represent the IEEE 754 special values “infinity”, “negative infinity”, and “not-a-number”, respectively. (On a machine whose floating-point arithmetic does not follow IEEE 754, these values will probably not work as expected.) When writing these values as constants in an SQL command, you must put quotes around them, for example UPDATE table SET x = '-Infinity'. On input, these strings are recognized in a case-insensitive manner.

## Character Types
In DuckDB, strings can be stored in the `varchar` field.

| Name | Aliases | Description |
|:---|:---|:---|
| varchar | char, bpchar, text, string| variable-length character string |
| varchar(n) |  | variable-length character string with maximum length n |

It is possible to supply a maximum length along with the type by initializing a type as `varchar(n)`,  where `n` is a positive integer. **Note that specifying this length is not required, and specifying this length will not improve performance or reduce storage space of the strings in the database.** Specifying a maximum length is useful **only** for data integrity reasons, not for performance reasons. In fact, the following SQL statements are equivalent:

```sql
-- the following statements are equivalent
CREATE TABLE strings(
	val VARCHAR(10) -- val has a maximum length of 10 characters
);
CREATE TABLE strings(
	val VARCHAR CHECK(LENGTH(val) <= 10) -- val has a maximum length of 10 characters
);
```

The `varchar` field allows storage of unicode characters. Internally, the data is encoded as UTF-8.


