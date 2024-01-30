---
layout: docu
title: Text Functions
---

This section describes functions and operators for examining and manipulating string values. The `␣` symbol denotes a space character.

<!-- markdownlint-disable MD056 -->

| Function | Description | Example | Result | Alias |
|:--|:--|:---|:--|:--|
| *`string`* `^@` *`search_string`* | Alias for `starts_with`. | `'abc' ^@ 'a'` | `true` | `starts_with` |
| *`string`* `||` *`string`* | String concatenation | `'Duck' || 'DB'` | `DuckDB` | |
| *`string`*`[`*`index`*`]` | Alias for `array_extract`. | `'DuckDB'[4]` | `'k'` | `array_extract` |
| *`string`*`[`*`begin`*`:`*`end`*`]` | Alias for `array_slice`. Missing `begin` or `end` arguments are interpreted as the beginning or end of the list respectively. | `'DuckDB'[:4]` | `'Duck'` | `array_slice` |
| *`string`*` LIKE `*`target`* | Returns true if the *string* matches the like specifier (see [Pattern Matching](../../sql/functions/patternmatching)) | `'hello' LIKE '%lo'` | `true` | |
| *`string`*` SIMILAR TO `*`regex`* | Returns `true` if the *string* matches the *regex*; identical to `regexp_full_match` (see [Pattern Matching](../../sql/functions/patternmatching)) | `'hello' SIMILAR TO 'l+'` | `false` | |
| `array_extract(`*`list`*`, `*`index`*`)` | Extract a single character using a (1-based) index. | `array_extract('DuckDB', 2)` | `'u'` | `list_element`, `list_extract` | |
| `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`)` | Extract a string using slice conventions. Negative values are accepted. | `array_slice('DuckDB', 5, NULL)` | `'DB'` | |
| `ascii(`*`string`*`)`| Returns an integer that represents the Unicode code point of the first character of the *string* | `ascii('Ω')` | `937` | |
| `bar(`*`x`*`, `*`min`*`, `*`max`*`[, `*`width`*`])` | Draw a band whose width is proportional to (*x* - *min*) and equal to *width* characters when *x* = *max*. *width* defaults to 80. | `bar(5, 0, 20, 10)` | `██▌` | |
| `bit_length(`*`string`*`)`| Number of bits in a string. | `bit_length('abc')` | `24` | |
| `chr(`*`x`*`)` | Returns a character which is corresponding the ASCII code value or Unicode code point | `chr(65)` | A | |
| `concat_ws(`*`separator`*`, `*`string`*`, ...)` | Concatenate strings together separated by the specified separator | `concat_ws(', ', 'Banana', 'Apple', 'Melon')` | `Banana, Apple, Melon` | |
| `concat(`*`string`*`, ...)` | Concatenate many strings together | `concat('Hello', ' ', 'World')` | `Hello World` | |
| `contains(`*`string`*`, `*`search_string`*`)` | Return true if *search_string* is found within *string* | `contains('abc', 'a')` | `true` | |
| `ends_with(`*`string`*`, `*`search_string`*`)`| Return true if *string* ends with *search_string* | `ends_with('abc', 'c')` | `true` | `suffix` |
| `format_bytes(`*`bytes`*`)` | Converts bytes to a human-readable representation using units based on powers of 2 (KiB, MiB, GiB, etc.). | `format_bytes(16384)` | `16.0 KiB` | |
| `format(`*`format`*`, `*`parameters`*`...)` | Formats a string using the [fmt syntax](#fmt-syntax) | `format('Benchmark "{}" took {} seconds', 'CSV', 42)` | `Benchmark "CSV" took 42 seconds` | |
| `from_base64(`*`string`*`)`| Convert a base64 encoded string to a character string. | `from_base64('QQ==')` | `'A'` | |
| `hash(`*`value`*`)` | Returns a `UBIGINT` with the hash of the *value* | `hash('🦆')` | `2595805878642663834` | |
| `ilike_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns true if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. *escape_character* is used to search for wildcard characters in the *string*. | `ilike_escape('A%c', 'a$%C', '$')` | `true` | |
| `instr(`*`string`*`, `*`search_string`*`)`| Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. | `instr('test test', 'es')` | 2 | |
| `left_grapheme(`*`string`*`, `*`count`*`)`| Extract the left-most grapheme clusters | `left_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` | `🤦🏼‍♂️` | |
| `left(`*`string`*`, `*`count`*`)`| Extract the left-most count characters | `left('Hello🦆', 2)` | `He` | |
| `length_grapheme(`*`string`*`)` | Number of grapheme clusters in *string* | `length_grapheme('🤦🏼‍♂️🤦🏽‍♀️')` | `2` | |
| `length(`*`string`*`)` | Number of characters in *string* | `length('Hello🦆')` | `6` | |
| `like_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns true if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. *escape_character* is used to search for wildcard characters in the *string*. | `like_escape('a%c', 'a$%c', '$')` | `true` | |
| `lower(`*`string`*`)` | Convert *string* to lower case | `lower('Hello')` | `hello` | `lcase` |
| `lpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the *string*  with the character from the left until it has count characters | `lpad('hello', 10, '>')` | `>>>>>hello` | |
| `ltrim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the left sduide of the *string* | `ltrim('>>>>test<<', '><')` | `test<<` | |
| `ltrim(`*`string`*`)`| Removes any spaces from the left side of the *string* | `ltrim('␣␣␣␣test␣␣')` | `test␣␣` | |
| `md5(`*`value`*`)` | Returns the [MD5 hash](https://en.wikipedia.org/wiki/MD5) of the *value*  | `md5('123')` | `'202cb962ac59075b964b07152d234b70'` | |
| `nfc_normalize(`*`string`*`)`| Convert string to Unicode NFC normalized string. Useful for comparisons and ordering if text data is mixed between NFC normalized and not. | `nfc_normalize('ardèch')` | `ardèch` | |
| `not_ilike_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns false if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)) using case-sensitive matching. *escape_character* is used to search for wildcard characters in the *string*. | `not_ilike_escape('A%c', 'a$%C', '$')` | `false` | |
| `not_like_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns false if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)) using case-insensitive matching. *escape_character* is used to search for wildcard characters in the *string*. | `not_like_escape('a%c', 'a$%c', '$')` | `false` | |
| `ord(`*`string`*`)`| Return ASCII character code of the leftmost character in a string.  | `ord('ü')` | `252` | |
| `parse_dirname(`*`path`*`, `*`separator`*`)`| Returns the top-level directory name from the given path. *`separator`* options: `system`, `both_slash` (default), `forward_slash`, `backslash`.  | `parse_dirname('path/to/file.csv', 'system')` | `path` | |
| `parse_dirpath(`*`path`*`, `*`separator`*`)`| Returns the head of the path (the pathname until the last slash) similarly to Python's [`os.path.dirname`](https://docs.python.org/3.7/library/os.path.html#os.path.dirname) function. *`separator`* options: `system`, `both_slash` (default), `forward_slash`, `backslash`.  | `parse_dirpath('/path/to/file.csv', 'forward_slash')` | `/path/to` | |
| `parse_filename(`*`path`*`, `*`trim_extension`*`, `*`separator`*`)`| Returns the last component of the path similarly to Python's [`os.path.basename`](https://docs.python.org/3.7/library/os.path.html#os.path.basename) function. If *`trim_extension`* is true, the file extension will be removed (defaults to `false`). *`separator`* options: `system`, `both_slash` (default), `forward_slash`, `backslash`.  | `parse_filename('path/to/file.csv', true, 'system')` | `file` | |
| `parse_path(`*`path`*`, `*`separator`*`)`| Returns a list of the components (directories and filename) in the path similarly to Python's [`pathlib.parts`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts) function. *`separator`* options: `system`, `both_slash` (default), `forward_slash`, `backslash`.  | `parse_path('/path/to/file.csv', 'system')` | `[/, path, to, file.csv]` | |
| `position(`*`search_string`*` in `*`string`*`)` | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. | `position('b' in 'abc')` | `2` | |
| `printf(`*`format`*`, `*`parameters`*`...)` | Formats a *string* using [printf syntax](#printf-syntax) | `printf('Benchmark "%s" took %d seconds', 'CSV', 42)` | `Benchmark "CSV" took 42 seconds`     | |
| `regexp_escape(`*`string`*`)` | Escapes special patterns to turn *string* into a regular expression similarly to Python's [`re.escape` function](https://docs.python.org/3/library/re.html#re.escape) | `regexp_escape('https://duckdb.org')` | `https\:\/\/duckdb\.org` |
| `regexp_extract_all(`*`string`*`, `*`regex`*`[, `*`group`*` = 0])` | Split the *string* along the *regex* and extract all occurrences of *group* | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` | `[hello, world]` |
| `regexp_extract(`*`string`*`, `*`pattern `*`, `*`name_list`*`)`; | If *string* contains the regexp *pattern*, returns the capturing groups as a struct with corresponding names from *name_list* (see [Pattern Matching](patternmatching#using-regexp_extract)) | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` | `{'y':'2023', 'm':'04', 'd':'15'}` |
| `regexp_extract(`*`string`*`, `*`pattern `*`[, `*`idx`*`])`; | If *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx* (see [Pattern Matching](patternmatching#using-regexp_extract))| `regexp_extract('hello_world', '([a-z ]+)_?', 1)` | `hello` |
| `regexp_full_match(`*`string`*`, `*`regex`*`)`| Returns `true` if the entire *string* matches the *regex* (see [Pattern Matching](patternmatching)) | `regexp_full_match('anabanana', '(an)*')` | `false` |
| `regexp_matches(`*`string`*`, `*`pattern`*`)` | Returns `true` if  *string* contains the regexp *pattern*, `false` otherwise (see [Pattern Matching](patternmatching#using-regexp_matches))| `regexp_matches('anabanana', '(an)*')` | `true` |
| `regexp_replace(`*`string`*`, `*`pattern`*`, `*`replacement`*`)`; | If *string* contains the regexp *pattern*, replaces the matching part with *replacement* (see [Pattern Matching](patternmatching#using-regexp_replace))| `regexp_replace('hello', '[lo]', '-')` | `he-lo` |
| `regexp_split_to_array(`*`string`*`, `*`regex`*`)` | Splits the *string* along the *regex* | `regexp_split_to_array('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` | `string_split_regex`, `str_split_regex`|
| `repeat(`*`string`*`, `*`count`*`)`| Repeats the *string* *count* number of times | `repeat('A', 5)` | `AAAAA` | |
| `replace(`*`string`*`, `*`source`*`, `*`target`*`)`| Replaces any occurrences of the *source* with *target* in *string* | `replace('hello', 'l', '-')` | `he--o` | |
| `reverse(`*`string`*`)`| Reverses the *string* | `reverse('hello')` | `olleh` | |
| `right_grapheme(`*`string`*`, `*`count`*`)`| Extract the right-most *count* grapheme clusters | `right_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` | `🤦🏽‍♀️` | |
| `right(`*`string`*`, `*`count`*`)`| Extract the right-most *count* characters | `right('Hello🦆', 3)` | `lo🦆` | |
| `rpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the *string* with the character from the right until it has *count* characters | `rpad('hello', 10, '<')` | `hello<<<<<` | |
| `rtrim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the right side of the *string* | `rtrim('>>>>test<<', '><')` | `>>>>test` | |
| `rtrim(`*`string`*`)`| Removes any spaces from the right side of the *string* | `rtrim('␣␣␣␣test␣␣')` | `␣␣␣␣test` | |
| `sha256(`*`value`*`)` | Returns a `VARCHAR` with the SHA-256 hash of the *`value`*| `sha-256('🦆')` | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |
| `split_part(`*`string`*`, `*`separator`*`, `*`index`*`)` | Split the *string* along the *separator* and return the data at the (1-based) *index* of the list. If the *index* is outside the bounds of the list, return an empty string (to match PostgreSQL's behavior). | `split_part('a|b|c', '|', 2)` | `b` | |
| `starts_with(`*`string`*`, `*`search_string`*`)`| Return true if *string* begins with *search_string* | `starts_with('abc', 'a')` | `true` | |
| `str_split_regex(`*`string`*`, `*`regex`*`)` | Splits the *string* along the *regex* | `str_split_regex('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` | `string_split_regex`, `regexp_split_to_array` |
| `string_split_regex(`*`string`*`, `*`regex`*`)` | Splits the *string* along the *regex* | `string_split_regex('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` | `str_split_regex`, `regexp_split_to_array` |
| `string_split(`*`string`*`, `*`separator`*`)` | Splits the *string* along the *separator* | `string_split('hello␣world', '␣')` | `['hello', 'world']` | `str_split`, `string_to_array` |
| `strip_accents(`*`string`*`)`| Strips accents from *string* | `strip_accents('mühleisen')` | `muhleisen` | |
| `strlen(`*`string`*`)` | Number of bytes in *string* | `strlen('🦆')` | `4` | |
| `strpos(`*`string`*`, `*`search_string`*`)`| Alias for `instr`. Return location of first occurrence of *search_string* in *string*, counting from 1. Returns 0 if no match found. | `strpos('test test', 'es')` | 2 | `instr` |
| `substring(`*`string`*`, `*`start`*`, `*`length`*`)` | Extract substring of *length* characters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substring('Hello', 2, 2)` | `el` | `substr` |
| `substring_grapheme(`*`string`*`, `*`start`*`, `*`length`*`)` | Extract substring of *length* grapheme clusters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substring_grapheme('🦆🤦🏼‍♂️🤦🏽‍♀️🦆', 3, 2)` | `🤦🏽‍♀️🦆` | |
| `to_base64(`*`blob`*`)`| Convert a blob to a base64 encoded string. | `to_base64('A'::blob)` | `QQ==` | `base64` |
| `trim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from either side of the *string* | `trim('>>>>test<<', '><')` | `test` | |
| `trim(`*`string`*`)`| Removes any spaces from either side of the *string* | `trim('␣␣␣␣test␣␣')` | `test` | |
| `unicode(`*`string`*`)`| Returns the unicode code of the first character of the *string* | `unicode('ü')` | `252` | |
| `upper(`*`string`*`)`| Convert *string* to upper case | `upper('Hello')` | `HELLO` | `ucase` |

<!-- markdownlint-enable MD056 -->

## Text Similarity Functions

These functions are used to measure the similarity of two strings using various [similarity measures](https://en.wikipedia.org/wiki/Similarity_measure).

| Function | Description | Example | Result |
|:--|:--|:---|:-|
| `damerau_levenshtein(`*`s1`*`,` *`s2`*`)` | Extension of Levenshtein distance to also include transposition of adjacent characters as an allowed edit operation. In other words, the minimum number of edit operations (insertions, deletions, substitutions or transpositions) required to change one string to another. Different case is considered different. | `damerau_levenshtein('duckdb', 'udckbd')` | `2` |
| `editdist3(`*`s1`*`,` *`s2`*`)` | Alias of `levenshtein` for SQLite compatibility. The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Different case is considered different. | `editdist3('duck', 'db')` | `3` |
| `jaccard(`*`s1`*`,` *`s2`*`)` | The Jaccard similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaccard('duck', 'luck')` | `0.6` |
| `jaro_similarity(`*`s1`*`,` *`s2`*`)` | The Jaro similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaro_similarity('duck', 'duckdb')` | `0.88` |
| `jaro_winkler_similarity(`*`s1`*`,` *`s2`*`)` | The Jaro-Winkler similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaro_winkler_similarity('duck', 'duckdb')` | `0.93` |
| `levenshtein(`*`s1`*`,` *`s2`*`)` | The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Different case is considered different. | `levenshtein('duck', 'db')` | `3` |
| `mismatches(`*`s1`*`,` *`s2`*`)` | Alias for `hamming(`*`s1`*`,` *`s2`*`)`. The number of positions with different characters for two strings of equal length. Different case is considered different. | `mismatches('duck', 'luck')` | `1` |

## Formatters

### `fmt` Syntax

The `format(`*`format`*`, `*`parameters`*`...)` function formats strings, loosely following the syntax of the [{fmt} open-source formatting library](https://fmt.dev/latest/syntax.html).

```sql
-- Format without additional parameters
SELECT format('Hello world'); -- Hello world
-- Format a string using {}
SELECT format('The answer is {}', 42); -- The answer is 42
// s == "The answer is 42."
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
SELECT format('{:x}', 123456789); -- 75bcd15
-- Convert to binary
SELECT format('{:b}', 123456789); -- 111010110111100110100010101
```

#### Print Numbers with Thousand Separators

```sql
SELECT format('{:,}',  123456789); -- 123,456,789
SELECT format('{:t.}', 123456789); -- 123.456.789
SELECT format('{:''}', 123456789); -- 123'456'789
SELECT format('{:_}',  123456789); -- 123_456_789
SELECT format('{:t }', 123456789); -- 123 456 789
SELECT format('{:tX}', 123456789); -- 123X456X789
```

### `printf` Syntax

The `printf(`*`format`*`, `*`parameters`*`...)` function formats strings using the [`printf` syntax](https://cplusplus.com/reference/cstdio/printf/).

```sql
-- Format without additional parameters
SELECT printf('Hello world'); -- Hello world
-- Format a string using {}
SELECT printf('The answer is %d', 42); -- The answer is 42
// s == "The answer is 42."
-- Format a string using positional arguments '%position$formatter',
-- e.g., the second parameter as a string is encoded as '%2$s'
SELECT printf('I''d rather be %2$s than %1$s.', 'right', 'happy'); -- I'd rather be happy than right.
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
SELECT printf('%x', 123456789); -- 75bcd15
-- Convert to binary
SELECT printf('%b', 123456789); -- 111010110111100110100010101
```

#### Thousand Separators

```sql
SELECT printf('%,d', 123456789);  -- 123,456,789
SELECT printf('%.d', 123456789);  -- 123.456.789
SELECT printf('%''d', 123456789); -- 123'456'789
SELECT printf('%_d', 123456789);  -- 123_456_789
```
