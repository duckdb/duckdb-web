---
layout: docu
title: Blob Functions
selected: Documentation/Functions/Blob Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating blob values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`blob`* `||` *`blob`* | Blob concatenation | `'\xAA'::BLOB || '\xBB'::BLOB` | \xAA\xBB |
| `decode(`*`blob`*`)` | Convert blob to varchar. Fails if blob is not valid utf-8. | `decode('\xC3\xBC'::BLOB)` | ü |
| `encode(`*`string`*`)` | Convert varchar to blob. Converts utf-8 characters into literal encoding. | `encode('my_string_with_ü')` | my_string_with_\xC3\xBC |
| `octet_length(`*`blob`*`)` | Number of bytes in blob | `octet_length('\xAA\xBB'::BLOB)` | 2 |
