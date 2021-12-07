---
layout: docu
title: Blob Functions
selected: Documentation/Functions/Blob Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating blob values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`blob`* `||` *`blob`* | Blob concatenation | `'\xAA'::BLOB || '\xBB'::BLOB` | \xAABB |
| `octet_length(`*`blob`*`)` | Number of bytes in blob | `octet_length('\xAABB'::BLOB)` | 2 |
