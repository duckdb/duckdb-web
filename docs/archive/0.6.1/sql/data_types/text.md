---
layout: docu
title: Text Types
selected: Documentation/Data Types/Text
expanded: Data Types
blurb: In DuckDB, strings can be stored in the VARCHAR field.
---
In DuckDB, strings can be stored in the `VARCHAR` field.

| Name | Aliases | Description |
|:---|:---|:---|
| `VARCHAR` | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | variable-length character string |
| `VARCHAR(n)` |  | variable-length character string with maximum length n |

It is possible to supply a number along with the type by initializing a type as `VARCHAR(n)`,  where `n` is a positive integer. **Note that specifying this length is not required and has no effect on the system. Specifying this length will not improve performance or reduce storage space of the strings in the database.** This variant is supported for compatibility reasons with other systems that do require a length to be specified for strings.

If you wish to restrict the number of characters in a `VARCHAR` column for data integrity reasons the `CHECK` constraint should be used, for example:


```sql
CREATE TABLE strings(
	val VARCHAR CHECK(LENGTH(val) <= 10) -- val has a maximum length of 10 characters
);
```

The `VARCHAR` field allows storage of unicode characters. Internally, the data is encoded as UTF-8.

## Functions
See [Character Functions](../../sql/functions/char) and [Pattern Matching](../../sql/functions/patternmatching).
