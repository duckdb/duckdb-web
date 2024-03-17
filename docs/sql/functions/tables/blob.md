| Function | Description | Example | Result |
|:-|:--|:---|:-|
| *`blob`* `||` *`blob`* | Blob concatenation | `'\xAA'::BLOB || '\xBB'::BLOB` | `\xAA\xBB` |
| `decode(`*`blob`*`)` | Convert blob to varchar. Fails if blob is not valid UTF-8. | `decode('\xC3\xBC'::BLOB)` | `ü` |
| `encode(`*`string`*`)` | Convert varchar to blob. Converts UTF-8 characters into literal encoding. | `encode('my_string_with_ü')` | `my_string_with_\xC3\xBC` |
| `octet_length(`*`blob`*`)` | Number of bytes in blob | `octet_length('\xAA\xBB'::BLOB)` | `2` |
| `read_blob(`*`source`*`)` | Returns the content from *`source`* (a filename, a list of filenames, or a glob pattern) as a `BLOB`. See the [`read_blob` guide](../../guides/import/read_file#read_blob) for more details. | `read_blob('hello.bin')` | `hello\x0A` |
