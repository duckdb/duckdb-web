---
blurb: The blob (Binary Large OBject) type represents an arbitrary binary object stored
  in the database system.
layout: docu
redirect_from:
- /docs/sql/data_types/blob
- /docs/stable/sql/data_types/blob
- /docs/current/sql/data_types/blob
- /docs/lts/sql/data_types/blob
- /docs/preview/sql/data_types/blob
tested: true
title: Blob Type
---

| Name | Aliases | Description |
|:---|:---|:---|
| `BLOB` | `BYTEA`, `BINARY`, `VARBINARY` | Variable-length binary data |

The blob (**B**inary **L**arge **OB**ject) type represents an arbitrary binary object stored in the database system. The blob type can contain any type of binary data with no restrictions. What the actual bytes represent is opaque to the database system.

Create a `BLOB` value with a single byte (170):

```sql
SELECT '\xAA'::BLOB;
```

Create a `BLOB` value with three bytes (170, 171, 172):

```sql
SELECT '\xAA\xAB\xAC'::BLOB;
```

Create a `BLOB` value with two bytes (65, 66):

```sql
SELECT 'AB'::BLOB;
```

A `BLOB` value can also be created using a hex string literal, which is a string of hexadecimal digits prefixed with `X`. The number of hex digits must be even. For example, create a `BLOB` value with two bytes (202, 254):

```sql
SELECT X'CAFE';
```

> New Starting with DuckDB 2.0, `X'…'` literals are `BLOB` values. In earlier versions, `X'CAFE'` was parsed as the `VARCHAR` string `'xCAFE'`.

Blobs are typically used to store non-textual objects that the database does not provide explicit support for, such as images. While blobs can hold objects up to 4 GB in size, typically it is not recommended to store very large objects within the database system. In many situations it is better to store the large file on the file system, and store the path to the file in the database system in a `VARCHAR` field.

## Functions

See [Blob Functions]({% link docs/2.0/sql/functions/blob.md %}).
