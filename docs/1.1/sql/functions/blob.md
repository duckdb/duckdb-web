---
layout: docu
redirect_from:
- docs/archive/1.1/test/functions/blob
title: Blob Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions and operators for examining and manipulating [`BLOB` values]({% link docs/1.1/sql/data_types/blob.md %}).

<!-- markdownlint-disable MD056 -->

| Name | Description |
|:--|:-------|
| [`blob || blob`](#blob--blob) | `BLOB` concatenation. |
| [`decode(blob)`](#decodeblob) | Converts `blob` to `VARCHAR`. Fails if `blob` is not valid UTF-8. |
| [`encode(string)`](#encodestring) | Converts the `string` to `BLOB`. Converts UTF-8 characters into literal encoding. |
| [`hex(blob)`](#hexblob) | Converts `blob` to `VARCHAR` using hexadecimal encoding. |
| [`octet_length(blob)`](#octet_lengthblob) | Number of bytes in `blob`. |
| [`read_blob(source)`](#read_blobsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide]({% link docs/1.1/guides/file_formats/read_file.md %}#read_blob) for more details. |

<!-- markdownlint-enable MD056 -->

#### `blob || blob`

<div class="nostroke_table"></div>

| **Description** | `BLOB` concatenation. |
| **Example** | `'\xAA'::BLOB || '\xBB'::BLOB` |
| **Result** | `\xAA\xBB` |

#### `decode(blob)`

<div class="nostroke_table"></div>

| **Description** | Convert `blob` to `VARCHAR`. Fails if `blob` is not valid UTF-8. |
| **Example** | `decode('\xC3\xBC'::BLOB)` |
| **Result** | `ü` |

#### `encode(string)`

<div class="nostroke_table"></div>

| **Description** | Converts the `string` to `BLOB`. Converts UTF-8 characters into literal encoding. |
| **Example** | `encode('my_string_with_ü')` |
| **Result** | `my_string_with_\xC3\xBC` |

#### `hex(blob)`

<div class="nostroke_table"></div>

| **Description** | Converts `blob` to `VARCHAR` using hexadecimal encoding. |
| **Example** | `hex('\xAA\xBB'::BLOB)` |
| **Result** | `AABB` |

#### `octet_length(blob)`

<div class="nostroke_table"></div>

| **Description** | Number of bytes in `blob`. |
| **Example** | `octet_length('\xAA\xBB'::BLOB)` |
| **Result** | `2` |

#### `read_blob(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide]({% link docs/1.1/guides/file_formats/read_file.md %}#read_blob) for more details. |
| **Example** | `read_blob('hello.bin')` |
| **Result** | `hello\x0A` |