---
layout: docu
title: Text Functions
selected: Documentation/Functions/Text Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating string values. `␣` denotes a space character.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`string`* `^@` *`search_string`* | Alias for `starts_with`. | `'abc' ^@ 'a'` | `true` |
| *`string`* `||` *`string`* | String concatenation | `'Duck' || 'DB'` | `DuckDB` |
| *`string`*`[`*`index`*`]` | Alias for `array_extract`. | `'DuckDB'[4]` | `'k'` |
| *`string`*`[`*`begin`*`:`*`end`*`]` | Alias for `array_slice`. Missing arguments are interprete as `NULL`s. | `'DuckDB'[:4]` | `'Duck'` |
| `array_extract(`*`list`*`, `*`index`*`)` | Extract a single character using a (1-based) index. | `array_extract('DuckDB', 2)` | `'u'` |
| `array_slice(`*`list`*`, `*`begin`*`, `*`end`*`)` | Extract a string using slice conventions. `NULL`s are interpreted as the bounds of the string. Negative values are accepted. | `array_slice('DuckDB', 5, NULL)` | `'DB'` |
| `ascii(`*`string`*`)`| Returns an integer that represents the Unicode code point of the first character of the *string* | `ascii('Ω')` | `937` |
| `bar(`*`x`*`, `*`min`*`, `*`max`*`[, `*`width`*`])` | Draw a band whose width is proportional to (*x* - *min*) and equal to *width* characters when *x* = *max*. *width* defaults to 80. | `bar(5, 0, 20, 10)` | `██▌` |
| `base64(`*`blob`*`)`| Convert a blob to a base64 encoded string. Alias of to_base64. | `base64('A'::blob)` | `'QQ=='` |
| `bit_length(`*`string`*`)`| Number of bits in a string. | `bit_length('abc')` | `24` |
| `concat(`*`string`*`, ...)` | Concatenate many strings together | `concat('Hello', ' ', 'World')` | `Hello World` |
| `concat_ws(`*`separator`*`, `*`string`*`, ...)` | Concatenate strings together separated by the specified separator | `concat_ws(',', 'Banana', 'Apple', 'Melon')` | `Banana,Apple,Melon` |
| `contains(`*`string`*`, `*`search_string`*`)` | Return true if *search_string* is found within *string* | `contains('abc','a')` | `true` |
| `format(`*`format`*`, `*`parameters`*`...)` | Formats a string using fmt syntax | `format('Benchmark "{}" took {} seconds', 'CSV', 42)` | `Benchmark "CSV" took 42 seconds` |
| `from_base64(`*`string`*`)`| Convert a base64 encoded string to a character string. | `from_base64('QQ==')` | `'A'` |
| `hash(`*`value`*`)` | Returns an integer with the hash of the *value* | `hash('🦆')` | `2595805878642663834` |
| `instr(`*`string`*`, `*`search_string`*`)`| Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. | `instr('test test','es')` | 2 |
| `lcase(`*`string`*`)` | Alias of `lower`. Convert *string* to lower case | `lcase('Hello')` | `hello` |
| `left(`*`string`*`, `*`count`*`)`| Extract the left-most count characters | `left('Hello🦆', 2)` | `He` |
| `left_grapheme(`*`string`*`, `*`count`*`)`| Extract the left-most grapheme clusters | `left_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` | `🤦🏼‍♂️` |
| `length(`*`string`*`)` | Number of characters in *string* | `length('Hello🦆')` | `6` |
| `length_grapheme(`*`string`*`)` | Number of grapheme clusters in *string* | `length_grapheme('🤦🏼‍♂️🤦🏽‍♀️')` | `2` |
| *`string`*` LIKE `*`target`* | Returns true if the *string* matches the like specifier (see [Pattern Matching](../../sql/functions/patternmatching)) | `'hello' LIKE '%lo'` | `true` |
| `like_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns true if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)). *escape_character* is used to search for wildcard characters in the *string*. | `like_escape('a%c', 'a$%c', '$')` | `true` |
| `list_element(`*`string`*`, `*`index`*`)` | An alias for `array_extract`. | `list_element('DuckDB', 2)` | `'u'` |
| `list_extract(`*`string`*`, `*`index`*`)` | An alias for `array_extract`. | `list_extract('DuckDB', 2)` | `'u'` |
| `lower(`*`string`*`)` | Convert *string* to lower case | `lower('Hello')` | `hello` |
| `lpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the *string*  with the character from the left until it has count characters | `lpad('hello', 10, '>')` | `>>>>>hello` |
| `ltrim(`*`string`*`)`| Removes any spaces from the left side of the *string* | `ltrim('␣␣␣␣test␣␣')` | `test␣␣` |
| `ltrim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the left side of the *string* | `ltrim('>>>>test<<', '><')` | `test<<` |
| `md5(`*`value`*`)` | Returns the [MD5 hash](https://en.wikipedia.org/wiki/MD5) of the *value*  | `md5('123')` | `'202cb962ac59075b964b07152d234b70'` |
| `nfc_normalize(`*`string`*`)`| Convert string to Unicode NFC normalized string. Useful for comparisons and ordering if text data is mixed between NFC normalized and not. | `nfc_normalize('ardèch')` | ``arde`ch`` |
| `not_like_escape(`*`string`*`, `*`like_specifier`*`, `*`escape_character`*`)` | Returns false if the *string* matches the *like_specifier* (see [Pattern Matching](../../sql/functions/patternmatching)). *escape_character* is used to search for wildcard characters in the *string*. | `like_escape('a%c', 'a$%c', '$')` | `true` |
| `ord(`*`string`*`)`| Return ASCII character code of the leftmost character in a string.  | `ord('ü')` | `252` |
| `position(`*`search_string`*` in `*`string`*`)` | Return location of first occurrence of `search_string` in `string`, counting from 1. Returns 0 if no match found. | `position('b' in 'abc')` | `2` |
| `prefix(`*`string`*`, `*`search_string`*`)` | Return true if *string* starts with *search_string*. | `prefix('abc', 'ab')` | `true` |
| `printf(`*`format`*`, `*`parameters`*`...)` | Formats a *string* using printf syntax | `printf('Benchmark "%s" took %d seconds', 'CSV', 42)` | `Benchmark "CSV" took 42 seconds`     |
| `regexp_full_match(`*`string`*`, `*`regex`*`)`| Returns true if the entire *string* matches the *regex* (see [Pattern Matching](../../sql/functions/patternmatching)) | `regexp_full_match('anabanana', '(an)*')` | `false` |
| `regexp_matches(`*`string`*`, `*`regex`*`)`| Returns true if a part of *string* matches the *regex* (see [Pattern Matching](../../sql/functions/patternmatching)) | `regexp_matches('anabanana', '(an)*')` | `true` |
| `regexp_replace(`*`string`*`, `*`regex`*`, `*`replacement`*`, `*`modifiers`*`)`| Replaces the first occurrence of *regex* with the *replacement*, use `'g'` modifier to replace all occurrences instead (see [Pattern Matching](../../sql/functions/patternmatching)) | `select regexp_replace('hello', '[lo]', '-')` | `he-lo` |
| `regexp_split_to_array(`*`string`*`, `*`regex`*`)` | Alias of `string_split_regex`. Splits the *string* along the *regex* | `regexp_split_to_array('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` |
| `regexp_extract(`*`string`*`, `*`regex`*`[, `*`group`*` = 0])` | Split the *string* along the *regex* and extract first occurrence of *group* | `regexp_extract('hello_world', '([a-z ]+)_?', 1)` | `hello` |
| `regexp_extract_all(`*`string`*`, `*`regex`*`[, `*`group`*` = 0])` | Split the *string* along the *regex* and extract all occurrences of *group* | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` | `[hello, world]` |
| `repeat(`*`string`*`, `*`count`*`)`| Repeats the *string* *count* number of times | `repeat('A', 5)` | `AAAAA` |
| `replace(`*`string`*`, `*`source`*`, `*`target`*`)`| Replaces any occurrences of the *source* with *target* in *string* | `replace('hello', 'l', '-')` | `he--o` |
| `reverse(`*`string`*`)`| Reverses the *string* | `reverse('hello')` | `olleh` |
| `right(`*`string`*`, `*`count`*`)`| Extract the right-most *count* characters | `right('Hello🦆', 3)` | `lo🦆` |
| `right_grapheme(`*`string`*`, `*`count`*`)`| Extract the right-most *count* grapheme clusters | `right_grapheme('🤦🏼‍♂️🤦🏽‍♀️', 1)` | `🤦🏽‍♀️` |
| `rpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the *string* with the character from the right until it has *count* characters | `rpad('hello', 10, '<')` | `hello<<<<<` |
| `rtrim(`*`string`*`)`| Removes any spaces from the right side of the *string* | `rtrim('␣␣␣␣test␣␣')` | `␣␣␣␣test` |
| `rtrim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the right side of the *string* | `rtrim('>>>>test<<', '><')` | `>>>>test` |
| `split_part(`*`string`*`, `*`separator`*`, `*`index`*`)` | Split the *string* along the *separator* and return the data at the (1-based) *index* of the list. If the *index* is outside the bounds of the list, return an empty string (to match Postgres behavior). | `split_part('a|b|c', '|', 2)` | `b` |
| `starts_with(`*`string`*`, `*`search_string`*`)`| Return true if *string* begins with *search_string* | `starts_with('abc','a')` | `true` |
| *`string`*` SIMILAR TO `*`regex`* | Returns `true` if the *string* matches the *regex*; identical to `regexp_full_match` (see [Pattern Matching](../../sql/functions/patternmatching)) | `'hello' SIMILAR TO 'l+'` | `false` |
| `strlen(`*`string`*`)` | Number of bytes in *string* | `strlen('🦆')` | `4` |
| `strpos(`*`string`*`, `*`search_string`*`)`| Alias of `instr`. Return location of first occurrence of *search_string* in *string*, counting from 1. Returns 0 if no match found. | `strpos('test test','es')` | 2 |
| `strip_accents(`*`string`*`)`| Strips accents from *string* | `strip_accents('mühleisen')` | `muhleisen` |
| `str_split(`*`string`*`, `*`separator`*`)` | Alias of `string_split`. Splits the *string* along the *separator* | `str_split('hello␣world', '␣')` | `['hello', 'world']` |
| `str_split_regex(`*`string`*`, `*`regex`*`)` | Alias of `string_split_regex`. Splits the *string* along the *regex* | `str_split_regex('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` |
| `string_split(`*`string`*`, `*`separator`*`)` | Splits the *string* along the *separator* | `string_split('hello␣world', '␣')` | `['hello', 'world']` |
| `string_split_regex(`*`string`*`, `*`regex`*`)` | Splits the *string* along the *regex* | `string_split_regex('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` |
| `string_to_array(`*`string`*`, `*`separator`*`)` | Alias of `string_split`. Splits the *string* along the *separator* | `string_to_array('hello␣world', '␣')` | `['hello', 'world']` |
| `substr(`*`string`*`, `*`start`*`, `*`length`*`)` | Alias of `substring`. Extract substring of *length* characters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substr('Hello', 2, 2)` | `el` |
| `substring(`*`string`*`, `*`start`*`, `*`length`*`)` | Extract substring of *length* characters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substring('Hello', 2, 2)` | `el` |
| `substring_grapheme(`*`string`*`, `*`start`*`, `*`length`*`)` | Extract substring of *length* grapheme clusters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substring_grapheme('🦆🤦🏼‍♂️🤦🏽‍♀️🦆', 3, 2)` | `🤦🏽‍♀️🦆` |
| `suffix(`*`string`*`, `*`search_string`*`)` | Return true if *string* ends with *search_string*. | `suffix('abc', 'bc')` | `true` |
| `strpos(`*`string`*`, `*`characters`*`)`| Alias of `instr`. Return location of first occurrence of *characters* in *string*, counting from 1. Returns 0 if no match found. | `strpos('test test','es')` | 2 |
| `to_base64(`*`blob`*`)`| Convert a blob to a base64 encoded string. Alias of base64. | `to_base64('A'::blob)` | `QQ==` |
| `trim(`*`string`*`)`| Removes any spaces from either side of the *string* | `trim('␣␣␣␣test␣␣')` | `test` |
| `trim(`*`string`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from either side of the *string* | `trim('>>>>test<<', '><')` | `test` |
| `ucase(`*`string`*`)`| Alias of `upper`. Convert *string* to upper case | `ucase('Hello')` | `HELLO` |
| `unicode(`*`string`*`)`| Returns the unicode code of the first character of the *string* | `unicode('ü')` | `252` |
| `upper(`*`string`*`)`| Convert *string* to upper case | `upper('Hello')` | `HELLO` |


## Text Similarity Functions
These functions are used to measure the similarity of two strings using various metrics.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `editdist3(`*`string`*`,` *`string`*`)` | Alias of `levenshtein` for SQLite compatibility. The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Different case is considered different. | `editdist3('duck','db')` | 3 |
| `hamming(`*`string`*`,` *`string`*`)` | The number of positions with different characters for 2 strings of equal length. Different case is considered different. | `hamming('duck','luck')` | 1 |
| `jaccard(`*`string`*`,` *`string`*`)` | The Jaccard similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaccard('duck','luck')` | 0.6 |
| `jaro_similarity(`*`string`*`,` *`string`*`)` | The Jaro similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaro_similarity('duck','duckdb')` | 0.88 |
| `jaro_winkler_similarity(`*`string`*`,` *`string`*`)` | The Jaro-Winkler similarity between two strings. Different case is considered different. Returns a number between 0 and 1. | `jaro_winkler_similarity('duck','duckdb')` | 0.93 |
| `levenshtein(`*`string`*`,` *`string`*`)` | The minimum number of single-character edits (insertions, deletions or substitutions) required to change one string to the other. Different case is considered different. | `levenshtein('duck','db')` | 3 |
| `mismatches(`*`string`*`,` *`string`*`)` | The number of positions with different characters for 2 strings of equal length. Different case is considered different. | `mismatches('duck','luck')` | 1 |
