---
layout: docu
title: Text Functions
---

## Text Functions and Operators

This section describes functions and operators for examining and manipulating string values. The `␣` symbol denotes a space character.

<!-- markdownlint-disable MD056 -->

| Name | Description |
|:--|:-------|
| [`string ^@ search_string`](#string--search_string) | Return true if `string` begins with `search_string`. |
| [`string || string`](#string--string) | String concatenation. |
| [`string[index]`](#stringindex) | Extract a single character using a (1-based) index. |
| [`string[begin:end]`](#stringbeginend) | Extract a string using slice conventions. Missing `begin` or `end` arguments are interpreted as the beginning or end of the list respectively. Negative values are accepted. |
| [`string LIKE target`](#string-like-target) | Returns true if the `string` matches the like specifier (see [Pattern Matching](../../sql/functions/patternmatching)). |
| [`string SIMILAR TO regex`](#string-similar-to-regex) | Returns `true` if the `string` matches the `regex`; identical to `regexp_full_match` (see [Pattern Matching](../../sql/functions/patternmatching)). |
| [`array_extract(list, index)`](#array_extractlist-index) | Extract a single character using a (1-based) index. |
| [`array_slice(list, begin, end)`](#array_slicelist-begin-end) | Extract a string using slice conventions. Negative values are accepted. |
| [`ascii(string)`](#asciistring) | Returns an integer that represents the Unicode code point of the first character of the `string`. |
| [`bar(x, min, max[, width])`](#barx-min-max-width) | Draw a band whose width is proportional to (`x - min`) and equal to `width` characters when `x` = `max`. `width` defaults to 80. |
| [`bit_length(string)`](#bit_lengthstring) | Number of bits in a string. |
| [`chr(x)`](#chrx) | Returns a character which is corresponding the ASCII code value or Unicode code point. |
| [`concat_ws(separator, string, ...)`](#concat_wsseparator-string-) | Concatenate strings together separated by the specified separator. |
| [`concat(string, ...)`](#concatstring-) | Concatenate many strings together. |
| [`contains(string, search_string)`](#containsstring-search_string) | Return true if `search_string` is found within `string`. |
| [`ends_with(string, search_string)`](#ends_withstring-search_string) | Return true if `string` ends with `search_string`. |
| [`format_bytes(bytes)`](#format_bytesbytes) | Converts bytes to a human-readable representation using units based on powers of 2 (KiB, MiB, GiB, etc.). |
| [`format(format, parameters, ...)`](#formatformat-parameters) | Formats a string using the [fmt syntax](#fmt-syntax). |
| [`from_base64(string)`](#from_base64string) | Convert a base64 encoded string to a character string. |
| [`greatest(x1, x2, ...)`](#greatestx1-x2) | Selects the largest value using lexicographical ordering. Note that lowercase characters are considered "larger" than uppercase characters and [collations](../expressions/collations) are not supported. |
| [`hash(value)`](#hashvalue) | Returns a `UBIGINT` with the hash of the `value`. |
| [`ilike_escape(string, like_specifier, escape_character)`](#ilike_escapestring-like_specifier-escape_character) | Returns true if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| [`instr(string, search_string)`](#instrstring-search_string) | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| [`least(x1, x2, ...)`](#leastx1-x2-) | Selects the smallest value using lexicographical ordering. Note that uppercase characters are considered "smaller" than lowercase characters, and [collations](../expressions/collations) are not supported. |
| [`left_grapheme(string, count)`](#left_graphemestring-count) | Extract the left-most grapheme clusters. |
| [`left(string, count)`](#leftstring-count) | Extract the left-most count characters. |
| [`length_grapheme(string)`](#length_graphemestring) | Number of grapheme clusters in `string`. |
| [`length(string)`](#lengthstring) | Number of characters in `string`. |
| [`like_escape(string,  like_specifier, escape_character)`](#like_escapestring-like_specifier-escape_character) | Returns true if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| [`lower(string)`](#lowerstring) | Convert `string` to lower case. |
| [`lpad(string, count, character)`](#lpadstring-count-character) | Pads the `string`  with the character from the left until it has count characters. |
| [`ltrim(string, characters)`](#ltrimstring-characters) | Removes any occurrences of any of the `characters` from the left side of the `string`. |
| [`ltrim(string)`](#ltrimstring) | Removes any spaces from the left side of the `string`. |
| [`md5(value)`](#md5value) | Returns the [MD5 hash](https://en.wikipedia.org/wiki/MD5) of the `value`. |
| [`nfc_normalize(string)`](#nfc_normalizestring) | Convert string to Unicode NFC normalized string. Useful for comparisons and ordering if text data is mixed between NFC normalized and not. |
| [`not_ilike_escape(string,  like_specifier, escape_character)`](#not_ilike_escapestring-like_specifier-escape_character) | Returns false if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| [`not_like_escape(string,  like_specifier, escape_character)`](#not_like_escapestring-like_specifier-escape_character) | Returns false if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| [`ord(string)`](#ordstring) | Return ASCII character code of the leftmost character in a string. |
| [`parse_dirname(path, separator)`](#parse_dirnamepath-separator) | Returns the top-level directory name from the given path. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| [`parse_dirpath(path, separator)`](#parse_dirpathpath-separator) | Returns the head of the path (the pathname until the last slash) similarly to Python's [`os.path.dirname`](https://docs.python.org/3.7/library/os.path.html#os.path.dirname) function. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| [`parse_filename(path, trim_extension, separator)`](#parse_filenamepath-trim_extension-separator) | Returns the last component of the path similarly to Python's [`os.path.basename`](https://docs.python.org/3.7/library/os.path.html#os.path.basename) function. If `trim_extension` is true, the file extension will be removed (defaults to `false`). `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| [`parse_path(path, separator)`](#parse_pathpath-separator) | Returns a list of the components (directories and filename) in the path similarly to Python's [`pathlib.parts`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts) function. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| [`position(search_string in string)`](#positionsearch_stringinstring) | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| [`printf(format, parameters...)`](#printfformat-parameters) | Formats a `string` using [printf syntax](#printf-syntax). |
| [`read_text(source)`](#read_textsource) | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide](../../guides/import/read_file#read_text) for more details. |
| [`regexp_escape(string)`](#regexp_escapestring) | Escapes special patterns to turn `string` into a regular expression similarly to Python's [`re.escape` function](https://docs.python.org/3/library/re.html#re.escape). |
| [`regexp_extract_all(string, regex[, group = 0])`](#regexp_extract_allstring-regex-group0) | Split the `string` along the `regex` and extract all occurrences of `group`. |
| [`regexp_extract(string, pattern , name_list)`](#regexp_extractstring-pattern-name_list) | If `string` contains the regexp `pattern`, returns the capturing groups as a struct with corresponding names from `name_list` (see [Pattern Matching](patternmatching#using-regexp_extract)). |
| [`regexp_extract(string, pattern [, idx])`](#regexp_extractstring-pattern-idx) | If `string` contains the regexp `pattern`, returns the capturing group specified by optional parameter `idx` (see [Pattern Matching](patternmatching#using-regexp_extract)). |
| [`regexp_full_match(string, regex)`](#regexp_full_matchstring-regex) | Returns `true` if the entire `string` matches the `regex` (see [Pattern Matching](patternmatching)). |
| [`regexp_matches(string, pattern)`](#regexp_matchesstring-pattern) | Returns `true` if  `string` contains the regexp `pattern`, `false` otherwise (see [Pattern Matching](patternmatching#using-regexp_matches)). |
| [`regexp_replace(string, pattern, replacement)`](#regexp_replacestring-pattern-replacement) | If `string` contains the regexp `pattern`, replaces the matching part with `replacement` (see [Pattern Matching](patternmatching#using-regexp_replace)). |
| [`regexp_split_to_array(string, regex)`](#regexp_split_to_arraystring-regex) | Splits the `string` along the `regex`. |
| [`regexp_split_to_table(string, regex)`](#regexp_split_to_tablestring-regex) | Splits the `string` along the `regex` and returns a row for each part. |
| [`repeat(string, count)`](#repeatstring-count) | Repeats the `string` `count` number of times. |
| [`replace(string, source, target)`](#replacestring-source-target) | Replaces any occurrences of the `source` with `target` in `string`. |
| [`reverse(string)`](#reversestring) | Reverses the `string`. |
| [`right_grapheme(string, count)`](#right_graphemestring-count) | Extract the right-most `count` grapheme clusters. |
| [`right(string, count)`](#rightstring-count) | Extract the right-most `count` characters. |
| [`rpad(string, count, character)`](#rpadstring-count-character) | Pads the `string` with the character from the right until it has `count` characters. |
| [`rtrim(string, characters)`](#rtrimstring-characters) | Removes any occurrences of any of the `characters` from the right side of the `string`. |
| [`rtrim(string)`](#rtrimstring) | Removes any spaces from the right side of the `string`. |
| [`sha256(value)`](#sha256value) | Returns a `VARCHAR` with the SHA-256 hash of the `value`. |
| [`split_part(string, separator, index)`](#split_partstring-separator-index) | Split the `string` along the `separator` and return the data at the (1-based) `index` of the list. If the `index` is outside the bounds of the list, return an empty string (to match PostgreSQL's behavior). |
| [`starts_with(string, search_string)`](#starts_withstring-search_string) | Return true if `string` begins with `search_string`. |
| [`str_split_regex(string, regex)`](#str_split_regexstring-regex) | Splits the `string` along the `regex`. |
| [`string_split_regex(string, regex)`](#string_split_regexstring-regex) | Splits the `string` along the `regex`. |
| [`string_split(string, separator)`](#string_splitstring-separator) | Splits the `string` along the `separator`. |
| [`strip_accents(string)`](#strip_accentsstring) | Strips accents from `string`. |
| [`strlen(string)`](#strlenstring) | Number of bytes in `string`. |
| [`strpos(string, search_string)`](#strposstring-search_string) | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| [`substring(string, start, length)`](#substringstring-start-length) | Extract substring of `length` characters starting from character `start`. Note that a `start` value of `1` refers to the `first` character of the string. |
| [`substring_grapheme(string, start, length)`](#substring_graphemestring-start-length) | Extract substring of `length` grapheme clusters starting from character `start`. Note that a `start` value of `1` refers to the `first` character of the string. |
| [`to_base64(blob)`](#to_base64blob) | Convert a blob to a base64 encoded string. |
| [`trim(string, characters)`](#trimstring-characters) | Removes any occurrences of any of the `characters` from either side of the `string`. |
| [`trim(string)`](#trimstring) | Removes any spaces from either side of the `string`. |
| [`unicode(string)`](#unicodestring) | Returns the Unicode code of the first character of the `string`. |
| [`upper(string)`](#upperstring) | Convert `string` to upper case. |

<!-- markdownlint-enable MD056 -->

### `string ^@ search_string`

<div class="nostroke_table"></div>

| **Description** | Return true if `string` begins with `search_string`. |
| **Example** | `'abc' ^@ 'a'` |
| **Result** | `true` |
| **Alias** | `starts_with` |

### `string || string`

<div class="nostroke_table"></div>

| **Description** | String concatenation. |
| **Example** | `'Duck' || 'DB'` |
| **Result** | `DuckDB` |
| **Alias** | `concat` |

### `string[index]`

<div class="nostroke_table"></div>

| **Description** | Extract a single character using a (1-based) index. |
| **Example** | `'DuckDB'[4]` |
| **Result** | `k` |
| **Alias** | `array_extract` |

### `string[begin:end]`

<div class="nostroke_table"></div>

| **Description** | Extract a string using slice conventions. Missing `begin` or `end` arguments are interpreted as the beginning or end of the list respectively. Negative values are accepted. |
| **Example** | `'DuckDB'[:4]` |
| **Result** | `Duck` |
| **Alias** | `array_slice` |

### `string LIKE target`

<div class="nostroke_table"></div>

| **Description** | Returns true if the `string` matches the like specifier (see [Pattern Matching](../../sql/functions/patternmatching)). |
| **Example** | `'hello' LIKE '%lo'` |
| **Result** | `true` |

### `string SIMILAR TO regex`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the `string` matches the `regex`; identical to `regexp_full_match` (see [Pattern Matching](../../sql/functions/patternmatching)) |
| **Example** | `'hello' SIMILAR TO 'l+'` |
| **Result** | `false` |

### `array_extract(list, index)`

<div class="nostroke_table"></div>

| **Description** | Extract a single character using a (1-based) index. |
| **Example** | `array_extract('DuckDB', 2)` |
| **Result** | `u` |
| **Aliases** | `list_element`, `list_extract` |

### `array_slice(list, begin, end)`

<div class="nostroke_table"></div>

| **Description** | Extract a string using slice conventions. Negative values are accepted. |
| **Example 1** | `array_slice('DuckDB', 3, 4)` |
| **Result** | `ck` |
| **Example 2** | `array_slice('DuckDB', 3, NULL)` |
| **Result** | `NULL` |
| **Example 3** | `array_slice('DuckDB', 0, -3)` |
| **Result** | `Duck` |

### `ascii(string)`

<div class="nostroke_table"></div>

| **Description** | Returns an integer that represents the Unicode code point of the first character of the `string`. |
| **Example** | `ascii('Ω')` |
| **Result** | `937` |

### `bar(x, min, max[, width])`

<div class="nostroke_table"></div>

| **Description** | Draw a band whose width is proportional to (`x - min`) and equal to `width` characters when `x` = `max`. `width` defaults to 80. |
| **Example** | `bar(5, 0, 20, 10)` |
| **Result** | `██▌` |

### `bit_length(string)`

<div class="nostroke_table"></div>

| **Description** | Number of bits in a string. |
| **Example** | `bit_length('abc')` |
| **Result** | `24` |

### `chr(x)`

<div class="nostroke_table"></div>

| **Description** | Returns a character which is corresponding the ASCII code value or Unicode code point. |
| **Example** | `chr(65)` |
| **Result** | A |

### `concat_ws(separator, string, ...)`

<div class="nostroke_table"></div>

| **Description** | Concatenate strings together separated by the specified separator. |
| **Example** | `concat_ws(', ', 'Banana', 'Apple', 'Melon')` |
| **Result** | `Banana, Apple, Melon` |

### `concat(string, ...)`

<div class="nostroke_table"></div>

| **Description** | Concatenate many strings together. |
| **Example** | `concat('Hello', ' ', 'World')` |
| **Result** | `Hello World` |

### `contains(string, search_string)`

<div class="nostroke_table"></div>

| **Description** | Return true if `search_string` is found within `string`. |
| **Example** | `contains('abc', 'a')` |
| **Result** | `true` |

### `ends_with(string, search_string)`

<div class="nostroke_table"></div>

| **Description** | Return true if `string` ends with `search_string`. |
| **Example** | `ends_with('abc', 'c')` |
| **Result** | `true` |
| **Alias** | `suffix` |

### `format_bytes(bytes)`

<div class="nostroke_table"></div>

| **Description** | Converts bytes to a human-readable representation using units based on powers of 2 (KiB, MiB, GiB, etc.). |
| **Example** | `format_bytes(16384)` |
| **Result** | `16.0 KiB` |

### `format(format, parameters, ...)`

<div class="nostroke_table"></div>

| **Description** | Formats a string using the [fmt syntax](#fmt-syntax). |
| **Example** | `format('Benchmark "{}" took {} seconds', 'CSV', 42)` |
| **Result** | `Benchmark "CSV" took 42 seconds` |

### `from_base64(string)`

<div class="nostroke_table"></div>

| **Description** | Convert a base64 encoded string to a character string. |
| **Example** | `from_base64('QQ==')` |
| **Result** | `'A'` |

### `greatest(x1, x2, ...)`

<div class="nostroke_table"></div>

| **Description** | Selects the largest value using lexicographical ordering. Note that lowercase characters are considered "larger" than uppercase characters and [collations](../expressions/collations) are not supported. |
| **Example** | `greatest('abc', 'bcd', 'cde', 'EFG')` |
| **Result** | `'cde'` |

### `hash(value)`

<div class="nostroke_table"></div>

| **Description** | Returns a `UBIGINT` with the hash of the `value`. |
| **Example** | `hash('🦆')` |
| **Result** | `2595805878642663834` |

### `ilike_escape(string, like_specifier, escape_character)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| **Example** | `ilike_escape('A%c', 'a$%C', '$')` |
| **Result** | `true` |

### `instr(string, search_string)`

<div class="nostroke_table"></div>

| **Description** | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| **Example** | `instr('test test', 'es')` |
| **Result** | 2 |

### `least(x1, x2,  ... )`

<div class="nostroke_table"></div>

| **Description** | Selects the smallest value using lexicographical ordering. Note that uppercase characters are considered "smaller" than lowercase characters, and [collations](../expressions/collations) are not supported. |
| **Example** | `least('abc', 'BCD', 'cde', 'EFG')` |
| **Result** | `'BCD'` |

### `left_grapheme(string, count)`

<div class="nostroke_table"></div>

| **Description** | Extract the left-most grapheme clusters. |
| **Example** | `left_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` |
| **Result** | `🤦🏼‍♂️` |

### `left(string, count)`

<div class="nostroke_table"></div>

| **Description** | Extract the left-most count characters. |
| **Example** | `left('Hello🦆', 2)` |
| **Result** | `He` |

### `length_grapheme(string)`

<div class="nostroke_table"></div>

| **Description** | Number of grapheme clusters in `string`. |
| **Example** | `length_grapheme('🤦🏼‍♂️🤦🏽‍♀️')` |
| **Result** | `2` |

### `length(string)`

<div class="nostroke_table"></div>

| **Description** | Number of characters in `string`. |
| **Example** | `length('Hello🦆')` |
| **Result** | `6` |

### `like_escape(string,  like_specifier, escape_character)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| **Example** | `like_escape('a%c', 'a$%c', '$')` |
| **Result** | `true` |

### `lower(string)`

<div class="nostroke_table"></div>

| **Description** | Convert `string` to lower case. |
| **Example** | `lower('Hello')` |
| **Result** | `hello` |
| **Alias** | `lcase` |

### `lpad(string, count, character)`

<div class="nostroke_table"></div>

| **Description** | Pads the `string`  with the character from the left until it has count characters. |
| **Example** | `lpad('hello', 8, '>')` |
| **Result** | `>>>hello` |

### `ltrim(string, characters)`

<div class="nostroke_table"></div>

| **Description** | Removes any occurrences of any of the `characters` from the left side of the `string`. |
| **Example** | `ltrim('>>>>test<<', '><')` |
| **Result** | `test<<` |

### `ltrim(string)`

<div class="nostroke_table"></div>

| **Description** | Removes any spaces from the left side of the `string`. |
| **Example** | `ltrim('␣␣␣␣test␣␣')` |
| **Result** | `test␣␣` |

### `md5(value)`

<div class="nostroke_table"></div>

| **Description** | Returns the [MD5 hash](https://en.wikipedia.org/wiki/MD5) of the `value`. |
| **Example** | `md5('123')` |
| **Result** | `202cb962ac59075b964b07152d234b70` |

### `nfc_normalize(string)`

<div class="nostroke_table"></div>

| **Description** | Convert string to Unicode NFC normalized string. Useful for comparisons and ordering if text data is mixed between NFC normalized and not. |
| **Example** | `nfc_normalize('ardèch')` |
| **Result** | `ardèch` |

### `not_ilike_escape(string,  like_specifier, escape_character)`

<div class="nostroke_table"></div>

| **Description** | Returns false if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| **Example** | `not_ilike_escape('A%c', 'a$%C', '$')` |
| **Result** | `false` |

### `not_like_escape(string,  like_specifier, escape_character)`

<div class="nostroke_table"></div>

| **Description** | Returns false if the `string` matches the `like_specifier` (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. `escape_character` is used to search for wildcard characters in the `string`. |
| **Example** | `not_like_escape('a%c', 'a$%c', '$')` |
| **Result** | `false` |

### `ord(string)`

<div class="nostroke_table"></div>

| **Description** | Return ASCII character code of the leftmost character in a string. |
| **Example** | `ord('ü')` |
| **Result** | `252` |

### `parse_dirname(path, separator)`

<div class="nostroke_table"></div>

| **Description** | Returns the top-level directory name from the given path. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| **Example** | `parse_dirname('path/to/file.csv', 'system')` |
| **Result** | `path` |

### `parse_dirpath(path, separator)`

<div class="nostroke_table"></div>

| **Description** | Returns the head of the path (the pathname until the last slash) similarly to Python's [`os.path.dirname`](https://docs.python.org/3.7/library/os.path.html#os.path.dirname) function. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| **Example** | `parse_dirpath('/path/to/file.csv', 'forward_slash')` |
| **Result** | `/path/to` |

### `parse_filename(path, trim_extension, separator)`

<div class="nostroke_table"></div>

| **Description** | Returns the last component of the path similarly to Python's [`os.path.basename`](https://docs.python.org/3.7/library/os.path.html#os.path.basename) function. If `trim_extension` is true, the file extension will be removed (defaults to `false`). `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| **Example** | `parse_filename('path/to/file.csv', true, 'system')` |
| **Result** | `file` |

### `parse_path(path, separator)`

<div class="nostroke_table"></div>

| **Description** | Returns a list of the components (directories and filename) in the path similarly to Python's [`pathlib.parts`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts) function. `separator` options: `system`, `both_slash` (default), `forward_slash`, `backslash`. |
| **Example** | `parse_path('/path/to/file.csv', 'system')` |
| **Result** | `[/, path, to, file.csv]` |

### `position(search_string in string)`

<div class="nostroke_table"></div>

| **Description** | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| **Example** | `position('b' in 'abc')` |
| **Result** | `2` |

### `printf(format, parameters...)`

<div class="nostroke_table"></div>

| **Description** | Formats a `string` using [printf syntax](#printf-syntax). |
| **Example** | `printf('Benchmark "%s" took %d seconds', 'CSV', 42)` |
| **Result** | `Benchmark "CSV" took 42 seconds` |

### `read_text(source)`

<div class="nostroke_table"></div>

| **Description** | Returns the content from `source` (a filename, a list of filenames, or a glob pattern) as a `VARCHAR`. The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use `read_blob` instead. See the [`read_text` guide](../../guides/import/read_file#read_text) for more details. |
| **Example** | `read_text('hello.txt')` |
| **Result** | `hello\n` |

### `regexp_escape(string)`

<div class="nostroke_table"></div>

| **Description** | Escapes special patterns to turn `string` into a regular expression similarly to Python's [`re.escape` function](https://docs.python.org/3/library/re.html#re.escape). |
| **Example** | `regexp_escape('http://d.org')` |
| **Result** | `http\:\/\/d\.org` |

### `regexp_extract_all(string, regex[, group = 0])`

<div class="nostroke_table"></div>

| **Description** | Split the `string` along the `regex` and extract all occurrences of `group`. |
| **Example** | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` |
| **Result** | `[hello, world]` |

### `regexp_extract(string, pattern , name_list)`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, returns the capturing groups as a struct with corresponding names from `name_list` (see [Pattern Matching](patternmatching#using-regexp_extract)). |
| **Example** | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` |
| **Result** | `{'y':'2023', 'm':'04', 'd':'15'}` |

### `regexp_extract(string, pattern [, idx])`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, returns the capturing group specified by optional parameter `idx` (see [Pattern Matching](patternmatching#using-regexp_extract)). |
| **Example** | `regexp_extract('hello_world', '([a-z ]+)_?', 1)` |
| **Result** | `hello` |

### `regexp_full_match(string, regex)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the entire `string` matches the `regex` (see [Pattern Matching](patternmatching)). |
| **Example** | `regexp_full_match('anabanana', '(an)`')` |
| **Result** | `false` |

### `regexp_matches(string, pattern)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if  `string` contains the regexp `pattern`, `false` otherwise (see [Pattern Matching](patternmatching#using-regexp_matches)). |
| **Example** | `regexp_matches('anabanana', '(an)`')` |
| **Result** | `true` |

### `regexp_replace(string, pattern, replacement)`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, replaces the matching part with `replacement` (see [Pattern Matching](patternmatching#using-regexp_replace)). |
| **Example** | `regexp_replace('hello', '[lo]', '-')` |
| **Result** | `he-lo` |

### `regexp_split_to_array(string, regex)`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `regex`. |
| **Example** | `regexp_split_to_array('hello␣world; 42', ';?␣')` |
| **Result** | `['hello', 'world', '42']` |
| **Aliases** | `string_split_regex`, `str_split_regex` |

### `regexp_split_to_table(string, regex)`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `regex` and returns a row for each part. |
| **Example** | `regexp_split_to_table('hello␣world; 42', ';?␣')` |
| **Result** | Two rows: `'hello'`, `'world'` |

### `repeat(string, count)`

<div class="nostroke_table"></div>

| **Description** | Repeats the `string` `count` number of times. |
| **Example** | `repeat('A', 5)` |
| **Result** | `AAAAA` |

### `replace(string, source, target)`

<div class="nostroke_table"></div>

| **Description** | Replaces any occurrences of the `source` with `target` in `string`. |
| **Example** | `replace('hello', 'l', '-')` |
| **Result** | `he--o` |

### `reverse(string)`

<div class="nostroke_table"></div>

| **Description** | Reverses the `string`. |
| **Example** | `reverse('hello')` |
| **Result** | `olleh` |

### `right_grapheme(string, count)`

<div class="nostroke_table"></div>

| **Description** | Extract the right-most `count` grapheme clusters. |
| **Example** | `right_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` |
| **Result** | `🤦🏽‍♀️` |

### `right(string, count)`

<div class="nostroke_table"></div>

| **Description** | Extract the right-most `count` characters. |
| **Example** | `right('Hello🦆', 3)` |
| **Result** | `lo🦆` |

### `rpad(string, count, character)`

<div class="nostroke_table"></div>

| **Description** | Pads the `string` with the character from the right until it has `count` characters. |
| **Example** | `rpad('hello', 10, '<')` |
| **Result** | `hello<<<<<` |

### `rtrim(string, characters)`

<div class="nostroke_table"></div>

| **Description** | Removes any occurrences of any of the `characters` from the right side of the `string`. |
| **Example** | `rtrim('>>>>test<<', '><')` |
| **Result** | `>>>>test` |

### `rtrim(string)`

<div class="nostroke_table"></div>

| **Description** | Removes any spaces from the right side of the `string`. |
| **Example** | `rtrim('␣␣␣␣test␣␣')` |
| **Result** | `␣␣␣␣test` |

### `sha256(value)`

<div class="nostroke_table"></div>

| **Description** | Returns a `VARCHAR` with the SHA-256 hash of the `value`. |
| **Example** | `sha256('🦆')` |
| **Result** | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |

### `split_part(string, separator, index)`

<div class="nostroke_table"></div>

| **Description** | Split the `string` along the `separator` and return the data at the (1-based) `index` of the list. If the `index` is outside the bounds of the list, return an empty string (to match PostgreSQL's behavior). |
| **Example** | `split_part('a;b;c', ';', 2)` |
| **Result** | `b` |

### `starts_with(string, search_string)`

<div class="nostroke_table"></div>

| **Description** | Return true if `string` begins with `search_string`. |
| **Example** | `starts_with('abc', 'a')` |
| **Result** | `true` |

### `str_split_regex(string, regex)`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `regex`. |
| **Example** | `str_split_regex('hello␣world; 42', ';?␣')` |
| **Result** | `['hello', 'world', '42']` |
| **Aliases** | `string_split_regex`, `regexp_split_to_array` |

### `string_split_regex(string, regex)`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `regex`. |
| **Example** | `string_split_regex('hello␣world; 42', ';?␣')` |
| **Result** | `['hello', 'world', '42']` |
| **Aliases** | `str_split_regex`, `regexp_split_to_array` |

### `string_split(string, separator)`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `separator`. |
| **Example** | `string_split('hello␣world', '␣')` |
| **Result** | `['hello', 'world']` |
| **Aliases** | `str_split`, `string_to_array` |

### `strip_accents(string)`

<div class="nostroke_table"></div>

| **Description** | Strips accents from `string`. |
| **Example** | `strip_accents('mühleisen')` |
| **Result** | `muhleisen` |

### `strlen(string)`

<div class="nostroke_table"></div>

| **Description** | Number of bytes in `string`. |
| **Example** | `strlen('🦆')` |
| **Result** | `4` |

### `strpos(string, search_string)`

<div class="nostroke_table"></div>

| **Description** | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. |
| **Example** | `strpos('test test', 'es')` |
| **Result** | 2 |
| **Alias** | `instr` |

### `substring(string, start, length)`

<div class="nostroke_table"></div>

| **Description** | Extract substring of `length` characters starting from character `start`. Note that a `start` value of `1` refers to the `first` character of the string. |
| **Example** | `substring('Hello', 2, 2)` |
| **Result** | `el` |
| **Alias** | `substr` |

### `substring_grapheme(string, start, length)`

<div class="nostroke_table"></div>

| **Description** | Extract substring of `length` grapheme clusters starting from character `start`. Note that a `start` value of `1` refers to the `first` character of the string. |
| **Example** | `substring_grapheme('🦆🤦🏼‍♂️🤦🏽‍♀️🦆', 3, 2)` |
| **Result** | `🤦🏽‍♀️🦆` |

### `to_base64(blob)`

<div class="nostroke_table"></div>

| **Description** | Convert a blob to a base64 encoded string. |
| **Example** | `to_base64('A'::blob)` |
| **Result** | `QQ==` |
| **Alias** | `base64` |

### `trim(string, characters)`

<div class="nostroke_table"></div>

| **Description** | Removes any occurrences of any of the `characters` from either side of the `string`. |
| **Example** | `trim('>>>>test<<', '><')` |
| **Result** | `test` |

### `trim(string)`

<div class="nostroke_table"></div>

| **Description** | Removes any spaces from either side of the `string`. |
| **Example** | `trim('␣␣␣␣test␣␣')` |
| **Result** | `test` |

### `unicode(string)`

<div class="nostroke_table"></div>

| **Description** | Returns the Unicode code of the first character of the `string`. Returns `-1` when `string` is empty, and `NULL` when `string` is `NULL`. |
| **Example** | `[unicode('âbcd'), unicode('â'), unicode(''), unicode(NULL)]` |
| **Result** | `[226, 226, -1, NULL]` |

### `upper(string)`

<div class="nostroke_table"></div>

| **Description** | Convert `string` to upper case. |
| **Example** | `upper('Hello')` |
| **Result** | `HELLO` |
| **Alias** | `ucase` |

## Text Similarity Functions

These functions are used to measure the similarity of two strings using various [similarity measures](https://en.wikipedia.org/wiki/Similarity_measure).

| Name | Description |
|:--|:-------|
| [`damerau_levenshtein(s1, s2)`](#damerau_levenshteins1-s2) | Extension of Levenshtein distance to also include transposition of adjacent characters as an allowed edit operation. In other words, the minimum number of edit operations (insertions, deletions, substitutions or transpositions) required to change one string to another. Characters of different cases (e.g., `a` and `A`) are considered different. |
| [`editdist3(s1, s2)`](#editdist3s1-s2) | Alias of `levenshtein` for SQLite compatibility. The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Characters of different cases (e.g., `a` and `A`) are considered different. |
| [`hamming(s1, s2)`](#hammings1-s2) | The Hamming distance between to strings, i.e., the number of positions with different characters for two strings of equal length. Strings must be of equal length. Characters of different cases (e.g., `a` and `A`) are considered different. |
| [`jaccard(s1, s2)`](#jaccards1-s2) | The Jaccard similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| [`jaro_similarity(s1, s2)`](#jaro_similaritys1-s2) | The Jaro similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| [`jaro_winkler_similarity(s1, s2)`](#jaro_winkler_similaritys1-s2) | The Jaro-Winkler similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| [`levenshtein(s1, s2)`](#levenshteins1-s2) | The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Characters of different cases (e.g., `a` and `A`) are considered different. |
| [`mismatches(s1, s2)`](#mismatchess1-s2) | Alias for `hamming(s1, s2)`. The number of positions with different characters for two strings of equal length. Strings must be of equal length. Characters of different cases (e.g., `a` and `A`) are considered different. |

### `damerau_levenshtein(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | Extension of Levenshtein distance to also include transposition of adjacent characters as an allowed edit operation. In other words, the minimum number of edit operations (insertions, deletions, substitutions or transpositions) required to change one string to another. Characters of different cases (e.g., `a` and `A`) are considered different. |
| **Example** | `damerau_levenshtein('duckdb', 'udckbd')` |
| **Result** | `2` |

### `editdist3(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | Alias of `levenshtein` for SQLite compatibility. The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Characters of different cases (e.g., `a` and `A`) are considered different. |
| **Example** | `editdist3('duck', 'db')` |
| **Result** | `3` |

### `hamming(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | The Hamming distance between to strings, i.e., the number of positions with different characters for two strings of equal length. Strings must be of equal length. Characters of different cases (e.g., `a` and `A`) are considered different. |
| **Example** | `hamming('duck', 'luck')` |
| **Result** | `1` |

### `jaccard(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | The Jaccard similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| **Example** | `jaccard('duck', 'luck')` |
| **Result** | `0.6` |

### `jaro_similarity(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | The Jaro similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| **Example** | `jaro_similarity('duck', 'duckdb')` |
| **Result** | `0.88` |

### `jaro_winkler_similarity(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | The Jaro-Winkler similarity between two strings. Characters of different cases (e.g., `a` and `A`) are considered different. Returns a number between 0 and 1. |
| **Example** | `jaro_winkler_similarity('duck', 'duckdb')` |
| **Result** | `0.93` |

### `levenshtein(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Characters of different cases (e.g., `a` and `A`) are considered different. |
| **Example** | `levenshtein('duck', 'db')` |
| **Result** | `3` |

### `mismatches(s1, s2)`

<div class="nostroke_table"></div>

| **Description** | Alias for `hamming(s1, s2)`. The number of positions with different characters for two strings of equal length. Strings must be of equal length. Characters of different cases (e.g., `a` and `A`) are considered different. |
| **Example** | `mismatches('duck', 'luck')` |
| **Result** | `1` |

## Formatters

### `fmt` Syntax

The `format(format, parameters...)` function formats strings, loosely following the syntax of the [{fmt} open-source formatting library](https://fmt.dev/latest/syntax.html).

```sql
-- Format without additional parameters
SELECT format('Hello world'); -- Hello world
-- Format a string using {}
SELECT format('The answer is {}', 42); -- The answer is 42
-- Format a string using positional arguments
SELECT format('I''d rather be {1} than {0}.', 'right', 'happy'); -- I'd rather be happy than right.
```

#### Format Specifiers

<div class="narrow_table"></div>

| Specifier | Description | Example |
|:-|:------|:---|
| `{:d}`   | integer                                | `123456`       |
| `{:E}`   | scientific notation                    | `3.141593E+00` |
| `{:f}`   | float                                  | `4.560000`     |
| `{:o}`   | octal                                  | `361100`       |
| `{:s}`   | string                                 | `asd`          |
| `{:x}`   | hexadecimal                            | `1e240`        |
| `{:tX}`  | integer, `X` is the thousand separator | `123 456`      |

#### Formatting Types

```sql
-- Integers
SELECT format('{} + {} = {}', 3, 5, 3 + 5); -- 3 + 5 = 8
-- Booleans
SELECT format('{} != {}', true, false); -- true != false
-- Format datetime values
SELECT format('{}', DATE '1992-01-01'); -- 1992-01-01
SELECT format('{}', TIME '12:01:00'); -- 12:01:00
SELECT format('{}', TIMESTAMP '1992-01-01 12:01:00'); -- 1992-01-01 12:01:00
-- Format BLOB
SELECT format('{}', BLOB '\x00hello'); -- \x00hello
-- Pad integers with 0s
SELECT format('{:04d}', 33); -- 0033
-- Create timestamps from integers
SELECT format('{:02d}:{:02d}:{:02d} {}', 12, 3, 16, 'AM'); -- 12:03:16 AM
-- Convert to hexadecimal
SELECT format('{:x}', 123_456_789); -- 75bcd15
-- Convert to binary
SELECT format('{:b}', 123_456_789); -- 111010110111100110100010101
```

#### Print Numbers with Thousand Separators

```sql
SELECT format('{:,}',  123_456_789); -- 123,456,789
SELECT format('{:t.}', 123_456_789); -- 123.456.789
SELECT format('{:''}', 123_456_789); -- 123'456'789
SELECT format('{:_}',  123_456_789); -- 123_456_789
SELECT format('{:t }', 123_456_789); -- 123 456 789
SELECT format('{:tX}', 123_456_789); -- 123X456X789
```

### `printf` Syntax

The `printf(format, parameters...)` function formats strings using the [`printf` syntax](https://cplusplus.com/reference/cstdio/printf/).

```sql
-- Format without additional parameters
SELECT printf('Hello world');
-- output: Hello world
```

```sql
-- Format a string using arguments in a given order
SELECT printf('The answer to %s is %d', 'life', 42);
-- output: The answer to life is 42
```

```sql
-- Format a string using positional arguments '%position$formatter',
-- e.g., the second parameter as a string is encoded as '%2$s'
SELECT printf('I''d rather be %2$s than %1$s.', 'right', 'happy');
-- output: I'd rather be happy than right.
```

#### Format Specifiers

<div class="narrow_table"></div>

| Specifier | Description | Example |
|:-|:------|:---|
| `%c`   | character code to character                                    | `a`            |
| `%d`   | integer                                                        | `123456`       |
| `%Xd`  | integer with thousand seperarator `X` from `,`, `.`, `''`, `_` | `123_456`      |
| `%E`   | scientific notation                                            | `3.141593E+00` |
| `%f`   | float                                                          | `4.560000`     |
| `%hd`  | integer                                                        | `123456`       |
| `%hhd` | integer                                                        | `123456`       |
| `%lld` | integer                                                        | `123456`       |
| `%o`   | octal                                                          | `361100`       |
| `%s`   | string                                                         | `asd`          |
| `%x`   | hexadecimal                                                    | `1e240`        |

#### Formatting Types

```sql
-- Integers
SELECT printf('%d + %d = %d', 3, 5, 3 + 5); -- 3 + 5 = 8
-- Booleans
SELECT printf('%s != %s', true, false); -- true != false
-- Format datetime values
SELECT printf('%s', DATE '1992-01-01'); -- 1992-01-01
SELECT printf('%s', TIME '12:01:00'); -- 12:01:00
SELECT printf('%s', TIMESTAMP '1992-01-01 12:01:00'); -- 1992-01-01 12:01:00
-- Format BLOB
SELECT printf('%s', BLOB '\x00hello'); -- \x00hello
-- Pad integers with 0s
SELECT printf('%04d', 33); -- 0033
-- Create timestamps from integers
SELECT printf('%02d:%02d:%02d %s', 12, 3, 16, 'AM'); -- 12:03:16 AM
-- Convert to hexadecimal
SELECT printf('%x', 123_456_789); -- 75bcd15
-- Convert to binary
SELECT printf('%b', 123_456_789); -- 111010110111100110100010101
```

#### Thousand Separators

```sql
SELECT printf('%,d',  123_456_789); -- 123,456,789
SELECT printf('%.d',  123_456_789); -- 123.456.789
SELECT printf('%''d', 123_456_789); -- 123'456'789
SELECT printf('%_d',  123_456_789); -- 123_456_789
```
