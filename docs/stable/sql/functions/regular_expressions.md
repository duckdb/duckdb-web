---
layout: docu
railroad: expressions/like.js
redirect_from:
  - /docs/sql/functions/regular_expressions
title: Regular Expressions
---

<!-- markdownlint-disable MD001 -->

DuckDB offers [pattern matching operators]({% link docs/stable/sql/functions/pattern_matching.md %})
([`LIKE`]({% link docs/stable/sql/functions/pattern_matching.md %}#like),
[`SIMILAR TO`]({% link docs/stable/sql/functions/pattern_matching.md %}#similar-to),
[`GLOB`]({% link docs/stable/sql/functions/pattern_matching.md %}#glob)),
as well as support for regular expressions via functions.

## Regular Expression Syntax

DuckDB uses the [RE2 library](https://github.com/google/re2) as its regular expression engine. For the regular expression syntax, see the [RE2 docs](https://github.com/google/re2/wiki/Syntax).

## Functions

All functions accept an optional set of [options](#options-for-regular-expression-functions).

| Name | Description |
|:--|:-------|
| [`regexp_extract(string, pattern[, group = 0][, options])`](#regexp_extractstring-pattern-group--0-options) | If `string` contains the regexp `pattern`, returns the capturing group specified by optional parameter `group`; otherwise, returns the empty string. The `group` must be a constant value. If no `group` is given, it defaults to 0. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| [`regexp_extract(string, pattern, name_list[, options])`](#regexp_extractstring-pattern-name_list-options) | If `string` contains the regexp `pattern`, returns the capturing groups as a struct with corresponding names from `name_list`; otherwise, returns a struct with the same keys and empty strings as values. |
| [`regexp_extract_all(string, regex[, group = 0][, options])`](#regexp_extract_allstring-regex-group--0-options) | Finds non-overlapping occurrences of `regex` in `string` and returns the corresponding values of `group`. |
| [`regexp_full_match(string, regex[, options])`](#regexp_full_matchstring-regex-options) | Returns `true` if the entire `string` matches the `regex`. |
| [`regexp_matches(string, pattern[, options])`](#regexp_matchesstring-pattern-options) | Returns `true` if `string` contains the regexp `pattern`, `false` otherwise. |
| [`regexp_replace(string, pattern, replacement[, options])`](#regexp_replacestring-pattern-replacement-options) | If `string` contains the regexp `pattern`, replaces the matching part with `replacement`. By default, only the first occurrence is replaced. A set of optional [`options`](#options-for-regular-expression-functions), including the global flag `g`, can be set. |
| [`regexp_split_to_array(string, regex[, options])`](#regexp_split_to_arraystring-regex-options) | Alias of `string_split_regex`. Splits the `string` along the `regex`. |
| [`regexp_split_to_table(string, regex[, options])`](#regexp_split_to_tablestring-regex-options) | Splits the `string` along the `regex` and returns a row for each part. |

#### `regexp_extract(string, pattern[, group = 0][, options])`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, returns the capturing group specified by optional parameter `group`; otherwise, returns the empty string. The `group` must be a constant value. If no `group` is given, it defaults to 0. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_extract('abc', '([a-z])(b)', 1)` |
| **Result** | `a` |

#### `regexp_extract(string, pattern, name_list[, options])`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, returns the capturing groups as a struct with corresponding names from `name_list`; otherwise, returns a struct with the same keys and empty strings as values. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` |
| **Result** | `{'y':'2023', 'm':'04', 'd':'15'}` |

#### `regexp_extract_all(string, regex[, group = 0][, options])`

<div class="nostroke_table"></div>

| **Description** | Finds non-overlapping occurrences of `regex` in `string` and returns the corresponding values of `group`. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_extract_all('Peter: 33, Paul:14', '(\w+):\s*(\d+)', 2)` |
| **Result** | `[33, 14]` |

#### `regexp_full_match(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the entire `string` matches the `regex`. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_full_match('anabanana', '(an)*')` |
| **Result** | `false` |

#### `regexp_matches(string, pattern[, options])`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if `string` contains the regexp `pattern`, `false` otherwise. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_matches('anabanana', '(an)*')` |
| **Result** | `true` |

#### `regexp_replace(string, pattern, replacement[, options])`

<div class="nostroke_table"></div>

| **Description** | If `string` contains the regexp `pattern`, replaces the matching part with `replacement`. By default, only the first occurrence is replaced. A set of optional [`options`](#options-for-regular-expression-functions), including the global flag `g`, can be set. |
| **Example** | `regexp_replace('hello', '[lo]', '-')` |
| **Result** | `he-lo` |

#### `regexp_split_to_array(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Alias of `string_split_regex`. Splits the `string` along the `regex`. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_split_to_array('hello world; 42', ';? ')` |
| **Result** | `['hello', 'world', '42']` |

#### `regexp_split_to_table(string, regex[, options])`

<div class="nostroke_table"></div>

| **Description** | Splits the `string` along the `regex` and returns a row for each part. A set of optional [`options`](#options-for-regular-expression-functions) can be set. |
| **Example** | `regexp_split_to_table('hello world; 42', ';? ')` |
| **Result** | Three rows: `'hello'`, `'world'`, `'42'` |

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

| Option | Description |
|:---|:---|
| `'c'`               | Case-sensitive matching                             |
| `'i'`               | Case-insensitive matching                           |
| `'l'`               | Match literals instead of regular expression tokens |
| `'m'`, `'n'`, `'p'` | Newline sensitive matching                          |
| `'g'`               | Global replace, only available for `regexp_replace` |
| `'s'`               | Non-newline sensitive matching                      |

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

The `regexp_extract` function is used to extract a part of a string that matches the regexp pattern.
A specific capturing group within the pattern can be extracted using the `group` parameter. If `group` is not specified, it defaults to 0, extracting the first match with the whole pattern.

```sql
SELECT regexp_extract('abc', '.b.');           -- abc
SELECT regexp_extract('abc', '.b.', 0);        -- abc
SELECT regexp_extract('abc', '.b.', 1);        -- (empty)
SELECT regexp_extract('abc', '([a-z])(b)', 1); -- a
SELECT regexp_extract('abc', '([a-z])(b)', 2); -- b
```

The `regexp_extract` function also supports a `name_list` argument, which is a `LIST` of strings. Using `name_list`, the `regexp_extract` will return the corresponding capture groups as fields of a `STRUCT`:

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
Binder Error:
Not enough group names in regexp_extract
```

If the number of column names is less than the number of capture groups, then only the first groups are returned.
If the number of column names is greater, then an error is generated.

## Limitations

Regular expressions only support 9 capture groups: `\1`, `\2`, `\3`, ..., `\9`.
Capture groups with two or more digits are not supported.
