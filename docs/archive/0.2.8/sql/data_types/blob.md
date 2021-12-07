---
layout: docu
title: Blob Type
selected: Documentation/Data Types/Blob
expanded: Data Types
---

| Name | Aliases | Description |
|:---|:---|:---|
| blob | bytea | variable-length binary data |

The blob (**B**inary **L**arge **OB**ject) type represents an arbitrary binary object stored in the database system. The blob type can contain any type of binary data with no restrictions. What the actual bytes represent is opaque to the database system.

```sql
-- create a blob value with a single byte (170)
SELECT '\xAA'::BLOB;
-- create a blob value with two bytes (65, 66)
SELECT 'AB'::BLOB;
```

Blobs are typically used to store non-textual objects that the database does not provide explicit support for, such as images. While blobs can hold objects up to 4GB in size, typically it is not recommended to store very large objects within the database system. In many situations it is better to store the large file on the file system, and store the path to the file in the database system in a `VARCHAR` field.

## Operators
See [Blob Functions](../functions/blob).
