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

It is possible to supply a maximum length along with the type by initializing a type as `VARCHAR(n)`,  where `n` is a positive integer. **Note that specifying this length is not required, and specifying this length will not improve performance or reduce storage space of the strings in the database.** Specifying a maximum length is useful **only** for data integrity reasons, not for performance reasons. In fact, the following SQL statements are equivalent:

```sql
-- the following statements are equivalent
CREATE TABLE strings(
	val VARCHAR(10) -- val has a maximum length of 10 characters
);
CREATE TABLE strings(
	val VARCHAR CHECK(LENGTH(val) <= 10) -- val has a maximum length of 10 characters
);
```

The `VARCHAR` field allows storage of unicode characters. Internally, the data is encoded as UTF-8.

## Functions
See [Character Functions](/docs/sql/functions/char) and [Pattern Matching](/docs/sql/functions/patternmatching).
