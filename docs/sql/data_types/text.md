---
layout: docu
title: Text Types
blurb: In DuckDB, strings can be stored in the VARCHAR field.
---

In DuckDB, strings can be stored in the `VARCHAR` field.
The field allows storage of Unicode characters. Internally, the data is encoded as UTF-8.

<div class="narrow_table"></div>

| Name | Aliases | Description |
|:---|:---|:---|
| `VARCHAR` | `CHAR`, `BPCHAR`, `STRING`, `TEXT` | Variable-length character string |
| `VARCHAR(n)` | `STRING(n)`, `TEXT(n)` | Variable-length character string. The maximum length _n_ has no effect and is only provided for compatibility. |

## Specifying a Length Limit

Specifying the length for the `VARCHAR`, `STRING`, and `TEXT` types is not required and has no effect on the system. Specifying the length will not improve performance or reduce storage space of the strings in the database. These variants variant is supported for compatibility reasons with other systems that do require a length to be specified for strings.

If you wish to restrict the number of characters in a `VARCHAR` column for data integrity reasons the `CHECK` constraint should be used, for example:

```sql
CREATE TABLE strings (
    val VARCHAR CHECK (length(val) <= 10) -- val has a maximum length of 10
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

## Strings with Special Characters

To use special characters in string, use [escape string literals](literal_types#escape-string-literals) or [dollar-quoted string literals](literal_types#dollar-quoted-string-literals). Alternatively, you can use concatenation and the [`chr` character function](../../sql/functions/char):

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
