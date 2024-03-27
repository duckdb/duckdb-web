---
layout: docu
title: Blob Functions
---

This section describes functions and operators for examining and manipulating blob values.

<!-- markdownlint-disable MD056 -->

| Name | Description |
|:--|:-------|
| [`blob || blob`](#blob--blob) | Blob concatenation. |
| [`decode(blob)`](#decodeblob) | Converts `BLOB` to `VARCHAR`. Fails if blob is not valid UTF-8. |
| [`encode(string)`](#encodestring) | Converts `VARCHAR` to `BLOB`. Converts UTF-8 characters into literal encoding. |
| [`octet_length(blob)`](#octet_lengthblob) | Number of bytes in `BLOB`. |
| [`read_blob(source)`](#read_blobsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/import/read_file#read_blob) for more details. |

<!-- markdownlint-enable MD056 -->

### `blob || blob`

<div class="nostroke_table"></div>

| **Description** | `BLOB` concatenation. |
| **Example** | `'\xAA'::BLOB || '\xBB'::BLOB` |
| **Result** | `\xAA\xBB` |

### `decode(blob)`

<div class="nostroke_table"></div>

| **Description** | Convert `BLOB` to `VARCHAR`. Fails if blob is not valid UTF-8. |
| **Example** | `decode('\xC3\xBC'::BLOB)` |
| **Result** | `ü` |

### `encode(string)`

<div class="nostroke_table"></div>

| **Description** | Convert `VARCHAR` to `BLOB`. Converts UTF-8 characters into literal encoding. |
| **Example** | `encode('my_string_with_ü')` |
| **Result** | `my_string_with_\xC3\xBC` |

### `octet_length(blob)`

<div class="nostroke_table"></div>

| **Description** | Number of bytes in `VARCHAR`. |
| **Example** | `octet_length('\xAA\xBB'::BLOB)` |
| **Result** | `2` |

### `read_blob(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/import/read_file#read_blob) for more details. |
| **Example** | `read_blob('hello.bin')` |
| **Result** | `hello\x0A` |
