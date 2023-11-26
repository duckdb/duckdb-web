---
layout: docu
title: Text Types
blurb: In DuckDB, strings can be stored in the VARCHAR field.
---

In DuckDB, strings can be stored in the `VARCHAR` field.

<div class="narrow_table"></div>

| Name | Aliases | Description |
|:---|:---|:---|
| `VARCHAR` | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | variable-length character string |
| `VARCHAR(n)` |  | variable-length character string with maximum length n |

It is possible to supply a number along with the type by initializing a type as `VARCHAR(n)`,  where `n` is a positive integer. **Note that specifying this length is not required and has no effect on the system. Specifying this length will not improve performance or reduce storage space of the strings in the database.** This variant is supported for compatibility reasons with other systems that do require a length to be specified for strings.

If you wish to restrict the number of characters in a `VARCHAR` column for data integrity reasons the `CHECK` constraint should be used, for example:


```sql
CREATE TABLE strings (
    val VARCHAR CHECK (length(val) <= 10) -- val has a maximum length of 10 characters
);
```

The `VARCHAR` field allows storage of Unicode characters. Internally, the data is encoded as UTF-8.

## Formatting Strings

Strings in DuckDB are surrounded by single quote (apostrophe) characters (`'`):

```sql
SELECT 'Hello world' AS msg;
```
```text
┌─────────────┐
│     msg     │
│   varchar   │
├─────────────┤
│ Hello world │
└─────────────┘
```

To include a single quote character in a string, use `''`:

```sql
SELECT 'Hello ''world''' AS msg;
```
```text
┌───────────────┐
│      msg      │
│    varchar    │
├───────────────┤
│ Hello 'world' │
└───────────────┘
```

To include special characters such as newline, use the [`chr` character function](../../sql/functions/char):

```sql
SELECT 'Hello' || chr(10) || 'world' AS msg;
```
```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

## Double Quote Characters

Double quote characters (`"`) are used to denote table and column names. Surrounding their names allows the use of keywords, e.g.:

```sql
CREATE TABLE "table" ("order" BIGINT);
```

While DuckDB occasionally accepts both single quote and double quotes for strings (e.g., both `FROM "filename.csv"` and `FROM 'filename.csv'` work), their use is not recommended.

## Functions

See [Character Functions](../../sql/functions/char) and [Pattern Matching](../../sql/functions/patternmatching).
