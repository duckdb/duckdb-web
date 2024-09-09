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

## Text Type Values

Values of the text type are character strings, also known as string values or simply strings. At runtime, string values are constructed in one of the following ways:

* referencing columns whose declared or implied type is the text data type
* [string literals]({% link docs/sql/data_types/literal_types.md %}#string-literals)
* [casting]({% link docs/sql/expressions/cast.md %}#explicit-casting) expressions to a text type
* applying a [string operator]({% link docs/sql/functions/char.md %}#text-functions-and-operators), or invoking a function that returns a text type value

## Strings with Special Characters

To use special characters in string, use [escape string literals]({% link docs/sql/data_types/literal_types.md %}#escape-string-literals) or [dollar-quoted string literals]({% link docs/sql/data_types/literal_types.md %}#dollar-quoted-string-literals). Alternatively, you can use concatenation and the [`chr` character function]({% link docs/sql/functions/char.md %}):

```sql
SELECT 'Hello' || chr(10) || 'world' AS msg;
```

<!-- This output intentionally uses the duckbox formatter -->

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

## Functions

See [Character Functions]({% link docs/sql/functions/char.md %}) and [Pattern Matching]({% link docs/sql/functions/pattern_matching.md %}).
