---
expanded: Functions
layout: docu
redirect_from:
- docs/archive/0.6.1/sql/functions/blob
selected: Documentation/Functions/Blob Functions
title: Blob Functions
---

This section describes functions and operators for examining and manipulating blob values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`blob`* `||` *`blob`* | Blob concatenation | `'\xAA'::BLOB || '\xBB'::BLOB` | \xAABB |
| `decode(`*`blob`*`)` | Convert blob to varchar. Fails if blob is not valid utf-8. | `decode('\xC3\xBC'::BLOB)` | ü |
| `encode(`*`string`*`)` | Convert varchar to blob. Converts utf-8 characters into literal encoding. | `encode('my_string_with_ü')` | my_string_with_\xC3\xBC |
| `octet_length(`*`blob`*`)` | Number of bytes in blob | `octet_length('\xAABB'::BLOB)` | 2 |