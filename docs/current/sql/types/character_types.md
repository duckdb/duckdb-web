---
layout: default
title: Text Types
selected: Documentation/Data Types/Text
expanded: Data Types
---
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

## Functions
See [Character Functions](../functions/character_functions) and [Pattern Matching](../functions/regex)