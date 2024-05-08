---
layout: docu
title: Regular Expressions
railroad: expressions/like.js
---

DuckDB offers [pattern matching operators](pattern_matching)
([`LIKE`](pattern_matching#like),
[`SIMILAR TO`](pattern_matching#similar-to),
[`GLOB`](pattern_matching#glob)),
as well as support for regular expressions via functions.

## Regular Expression Syntax

DuckDB uses the [RE2 library](https://github.com/google/re2) as its regular expression engine. For the regular expression syntax, see the [RE2 docs](https://github.com/google/re2/wiki/Syntax).

## Functions

| Name | Description |
|:--|:-------|
| [`regexp_extract_all(string, regex[, group = 0][, options])`](#regexp_extract_allstring-regex-group--0-options) | Split the *string* along the *regex* and extract all occurrences of *group*. |
| [`regexp_extract(string, pattern, name_list[, options])`](#regexp_extractstring-pattern-name_list-options) | If *string* contains the regexp *pattern*, returns the capturing groups as a struct with corresponding names from *name_list*. |
| [`regexp_extract(string, pattern[, idx][, options])`](#regexp_extractstring-pattern-idx-options) | If *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx*. The *idx* must be a constant value. |
| [`regexp_full_match(string, regex[, options])`](#regexp_full_matchstring-regex-options) | Returns `true` if the entire *string* matches the *regex*. |
| [`regexp_matches(string, pattern[, options])`](#regexp_matchesstring-pattern-options) | Returns `true` if  *string* contains the regexp *pattern*, `false` otherwise. |
| [`regexp_replace(string, pattern, replacement[, options])`](#regexp_replacestring-pattern-replacement-options) | If *string* contains the regexp *pattern*, replaces the matching part with *replacement*. |
| [`regexp_split_to_array(string, regex[, options])`](#regexp_split_to_arraystring-regex-options) | Alias of `string_split_regex`. Splits the *string* along the *regex*. |
| [`regexp_split_to_table(string, regex[, options])`](#regexp_split_to_tablestring-regex-options) | Splits the *string* along the *regex* and returns a row for each part. |

### `regexp_extract_all(string, regex[, group = 0][, options])`

<div class="nostroke_table"></div>

| **Description** | Split the *string* along the *regex* and extract all occurrences of *group*. |
| **Example** | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` |
| **Result** | `[hello, world]` |

### `regexp_extract(string, pattern, name_list[, options])`

<div class="nostroke_table"></div>

| **Description** | If *string* contains the regexp *pattern*, returns the capturing groups as a struct with corresponding names from *name_list*. |
| **Example** | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` |
| **Result** | `{'y':'2023', 'm':'04', 'd':'15'}` |

### `regexp_extract(string, pattern[, idx][, options])`

<div class="nostroke_table"></div>

| **Description** | If *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx*. The *idx* must be a constant value. |
| **Example** | `regexp_extract('hello_world', '([a-z ]+)_?', 1)` |
| **Result** | `hello` |

### `regexp_full_match(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the entire *string* matches the *regex*. |
| **Example** | `regexp_full_match('anabanana', '(an)*')` |
| **Result** | `false` |

### `regexp_matches(string, pattern[, options])`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if  *string* contains the regexp *pattern*, `false` otherwise. |
| **Example** | `regexp_matches('anabanana', '(an)*')` |
| **Result** | `true` |

### `regexp_replace(string, pattern, replacement[, options])`

<div class="nostroke_table"></div>

| **Description** | If *string* contains the regexp *pattern*, replaces the matching part with *replacement*. |
| **Example** | `regexp_replace('hello', '[lo]', '-')` |
| **Result** | `he-lo` |

### `regexp_split_to_array(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Alias of `string_split_regex`. Splits the *string* along the *regex*. |
| **Example** | `regexp_split_to_array('hello␣world; 42', ';?␣')` |
| **Result** | `['hello', 'world', '42']` |

### `regexp_split_to_table(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Splits the *string* along the *regex* and returns a row for each part. |
| **Example** | `regexp_split_to_array('hello␣world; 42', ';?␣')` |
| **Result** | Two rows: `'hello'`, `'world'` |

The `regexp_matches` function is similar to the `SIMILAR TO` operator, however, it does not require the entire string to match. Instead, `regexp_matches` returns `true` if the string merely contains the pattern (unless the special tokens `^` and `$` are used to anchor the regular expression to the start and end of the string). Below are some examples:

```sql
SELECT regexp_matches('abc', 'abc');       -- true
SELECT regexp_matches('abc', '^abc$');     -- true
SELECT regexp_matches('abc', 'a');         -- true
SELECT regexp_matches('abc', '^a$');       -- false
SELECT regexp_matches('abc', '.*(b|d).*'); -- true
SELECT regexp_matches('abc', '(b|c).*');   -- true
SELECT regexp_matches('abc', '^(b|c).*');  -- false
SELECT regexp_matches('abc', '(?i)A');     -- true
SELECT regexp_matches('abc', 'A', 'i');    -- true
```

## Options for Regular Expression Functions

The regex functions support the following `options`.

<div class="narrow_table"></div>

| Option | Description |
|:---|:---|
| `'c'`               | case-sensitive matching                             |
| `'i'`               | case-insensitive matching                           |
| `'l'`               | match literals instead of regular expression tokens |
| `'m'`, `'n'`, `'p'` | newline sensitive matching                          |
| `'g'`               | global replace, only available for `regexp_replace` |
| `'s'`               | non-newline sensitive matching                      |

For example:

```sql
SELECT regexp_matches('abcd', 'ABC', 'c'); -- false
SELECT regexp_matches('abcd', 'ABC', 'i'); -- true
SELECT regexp_matches('ab^/$cd', '^/$', 'l'); -- true
SELECT regexp_matches(E'hello\nworld', 'hello.world', 'p'); -- false
SELECT regexp_matches(E'hello\nworld', 'hello.world', 's'); -- true
```

### Using `regexp_matches`

The `regexp_matches` operator will be optimized to the `LIKE` operator when possible. To achieve best performance, the `'c'` option (case-sensitive matching) should be passed if applicable. Note that by default the [`RE2` library](#regular-expression-syntax) doesn't match the `.` character to newline.

<div class="narrow_table"></div>

| Original | Optimized equivalent |
|:---|:---|
| `regexp_matches('hello world', '^hello', 'c')`      | `prefix('hello world', 'hello')` |
| `regexp_matches('hello world', 'world$', 'c')`      | `suffix('hello world', 'world')` |
| `regexp_matches('hello world', 'hello.world', 'c')` | `LIKE 'hello_world'`             |
| `regexp_matches('hello world', 'he.*rld', 'c')`     | `LIKE '%he%rld'`                 |

### Using `regexp_replace`

The `regexp_replace` function can be used to replace the part of a string that matches the regexp pattern with a replacement string. The notation `\d` (where `d` is a number indicating the group) can be used to refer to groups captured in the regular expression in the replacement string. Note that by default, `regexp_replace` only replaces the first occurrence of the regular expression. To replace all occurrences, use the global replace (`g`) flag.

Some examples for using `regexp_replace`:

```sql
SELECT regexp_replace('abc', '(b|c)', 'X');        -- aXc
SELECT regexp_replace('abc', '(b|c)', 'X', 'g');   -- aXX
SELECT regexp_replace('abc', '(b|c)', '\1\1\1\1'); -- abbbbc
SELECT regexp_replace('abc', '(.*)c', '\1e');      -- abe
SELECT regexp_replace('abc', '(a)(b)', '\2\1');    -- bac
```

### Using `regexp_extract`

The `regexp_extract` function is used to extract a part of a string that matches the regexp pattern. A specific capturing group within the pattern can be extracted using the *`idx`* parameter. If *`idx`* is not specified, it defaults to 0, extracting the first match with the whole pattern.

```sql
SELECT regexp_extract('abc', '.b.');     -- abc
SELECT regexp_extract('abc', '.b.', 0);  -- abc
SELECT regexp_extract('abc', '.b.', 1);  -- (empty)
SELECT regexp_extract('abc', '([a-z])(b)', 1); -- a
SELECT regexp_extract('abc', '([a-z])(b)', 2); -- b
```

If *`ids`* is a `LIST` of strings, then `regexp_extract` will return the corresponding capture groups as fields of a `STRUCT`:

```sql
SELECT regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd']);
```

```text
{'y': 2023, 'm': 04, 'd': 15}
```

```sql
SELECT regexp_extract('2023-04-15 07:59:56', '^(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', ['y', 'm', 'd']);
```

```text
{'y': 2023, 'm': 04, 'd': 15}
```

```sql
SELECT regexp_extract('duckdb_0_7_1', '^(\w+)_(\d+)_(\d+)', ['tool', 'major', 'minor', 'fix']);
```

```console
Binder Error: Not enough group names in regexp_extract
```

If the number of column names is less than the number of capture groups, then only the first groups are returned.
If the number of column names is greater, then an error is generated.
