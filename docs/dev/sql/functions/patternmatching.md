---
layout: docu
railroad: expressions/like.js
redirect_from:
- /docs/sql/functions/patternmatching
title: Pattern Matching
---

There are four separate approaches to pattern matching provided by DuckDB: the traditional SQL `LIKE` operator, the more recent `SIMILAR TO` operator (added in SQL:1999), a `GLOB` operator, and POSIX-style regular expressions.

## LIKE

<div id="rrdiagram1"></div>

The `LIKE` expression returns `true` if the string matches the supplied pattern. (As expected, the `NOT LIKE` expression returns `false` if `LIKE` returns `true`, and vice versa. An equivalent expression is `NOT (string LIKE pattern)`.)

If pattern does not contain percent signs or underscores, then the pattern only represents the string itself; in that case `LIKE` acts like the equals operator. An underscore (`_`) in pattern stands for (matches) any single character; a percent sign (`%`) matches any sequence of zero or more characters.

`LIKE` pattern matching always covers the entire string. Therefore, if it's desired to match a sequence anywhere within a string, the pattern must start and end with a percent sign.

Some examples:

```sql
'abc' LIKE 'abc' -- true
'abc' LIKE 'a%'  -- true
'abc' LIKE '_b_' -- true
'abc' LIKE 'c'   -- false
'abc' LIKE 'c%'  -- false
'abc' LIKE '%c'  -- true
'abc' NOT LIKE '%c'  -- false
```

The keyword `ILIKE` can be used instead of `LIKE` to make the match case-insensitive according to the active locale. 

```sql
'abc' ILIKE '%C' -- true
'abc' NOT ILIKE '%C' -- false
```

To search within a string for a character that is a wildcard (`%` or `_`), the pattern must use an `ESCAPE` clause and an escape character to indicate the wildcard should be treated as a literal character instead of a wildcard. See an example below.

Additionally, the function `like_escape` has the same functionality as a `LIKE` expression with an `ESCAPE` clause, but using function syntax. See the [Text Functions Docs](../../sql/functions/char) for details.

```sql
--Search for strings with 'a' then a literal percent sign then 'c'
'a%c' LIKE 'a$%c' ESCAPE '$'        -- true
'azc' LIKE 'a$%c' ESCAPE '$'        -- false

--Case insensitive ILIKE with ESCAPE
'A%c' ILIKE 'a$%c' ESCAPE '$';      --true
```

There are also alternative characters that can be used as keywords in place of `LIKE` expressions. These enhance PostgreSQL compatibility.

<div class="narrow_table"></div>

| LIKE-style | PostgreSQL-style |
|:---|:---|
| `LIKE` | `~~` |
| `NOT LIKE` | `!~~` |
| `ILIKE` | `~~*` |
| `NOT ILIKE` | `!~~*` |


## SIMILAR TO

<div id="rrdiagram2"></div>

The `SIMILAR TO` operator returns true or false depending on whether its pattern matches the given string. It is similar to `LIKE`, except that it interprets the pattern using a regular expression. Like `LIKE`, the `SIMILAR TO` operator succeeds only if its pattern matches the entire string; this is unlike common regular expression behavior where the pattern can match any part of the string.

A regular expression is a character sequence that is an abbreviated definition of a set of strings (a regular set). A string is said to match a regular expression if it is a member of the regular set described by the regular expression. As with `LIKE`, pattern characters match string characters exactly unless they are special characters in the regular expression language — but regular expressions use different special characters than `LIKE` does.

Some examples:

```sql
'abc' SIMILAR TO 'abc'       -- true
'abc' SIMILAR TO 'a'         -- false
'abc' SIMILAR TO '.*(b|d).*' -- true
'abc' SIMILAR TO '(b|c).*'   -- false
'abc' NOT SIMILAR TO 'abc'   -- false
```

There are also alternative characters that can be used as keywords in place of `SIMILAR TO` expressions. These follow POSIX syntax.

<div class="narrow_table"></div>

| SIMILAR TO-style | POSIX-style |
|:---|:---|
| `SIMILAR TO` | `~` |
| `NOT SIMILAR TO` | `!~` |

## GLOB

<div id="rrdiagram3"></div>

The `GLOB` operator returns `true` or `false` if the string matches the `GLOB` pattern. The `GLOB` operator is most commonly used when searching for filenames that follow a specific pattern (for example a specific file extension). Use the question mark (`?`) wildcard to match any single character, and use the asterisk (`*`) to match zero or more characters. In addition, use bracket syntax (`[ ]`) to match any single character contained within the brackets, or within the character range specified by the brackets. An exclamation mark (`!`) may be used inside the first bracket to search for a character that is not contained within the brackets. To learn more, visit the [Glob Programming Wikipedia page](https://en.wikipedia.org/wiki/Glob_(programming)).

Some examples:

```sql
'best.txt' GLOB '*.txt'            -- true
'best.txt' GLOB '????.txt'         -- true
'best.txt' GLOB '?.txt'            -- false
'best.txt' GLOB '[abc]est.txt'     -- true
'best.txt' GLOB '[a-z]est.txt'     -- true

-- The bracket syntax is case sensitive
'Best.txt' GLOB '[a-z]est.txt'     -- false
'Best.txt' GLOB '[a-zA-Z]est.txt'  -- true

-- The ! applies to all characters within the brackets
'Best.txt' GLOB '[!a-zA-Z]est.txt' -- false

-- To negate a GLOB operator, negate the entire expression 
-- (NOT GLOB is not valid syntax)
NOT 'best.txt' GLOB '*.txt'        -- false
```

Three tildes (`~~~`) may also be used in place of the `GLOB` keyword.

<div class="narrow_table"></div>

| GLOB-style | Symbolic-style |
|:---|:---|
| `GLOB` | `~~~` |

### Glob Function to Find Filenames

The glob pattern matching syntax can also be used to search for filenames using the `glob` table function. 
It accepts one parameter: the path to search (which may include glob patterns). 

```sql
-- Search the current directory for all files
SELECT * FROM glob('*');
```

<div class="narrow_table"></div>

|     file      |
|---------------|
| duckdb.exe    |
| test.csv      |
| test.json     |
| test.parquet  |
| test2.csv     |
| test2.parquet |
| todos.json    |



## Regular Expressions

| Function | Description | Example | Result |
|:---|:---|:---|:--|
| `regexp_full_match(`*`string`*`, `*`regex`*`)`| Returns `true` if the entire *string* matches the *regex* | `regexp_full_match('anabanana', '(an)*')` | `false` |
| `regexp_matches(`*`string`*`, `*`pattern`*`)` | Returns `true` if  *string* contains the regexp *pattern*, `false` otherwise | `regexp_matches('anabanana', '(an)*')` | `true` |
| `regexp_replace(`*`string`*`, `*`pattern`*`, `*`replacement`*`)`; | If *string* contains the regexp *pattern*, replaces the matching part with *replacement* | `select regexp_replace('hello', '[lo]', '-')` | `he-lo` |
| `regexp_split_to_array(`*`string`*`, `*`regex`*`)` | Alias of `string_split_regex`. Splits the *string* along the *regex* | `regexp_split_to_array('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` |
| `regexp_extract(`*`string`*`, `*`pattern `*`[, `*`idx`*`])`; | If *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx* | `regexp_extract('hello_world', '([a-z ]+)_?', 1)` | `hello` |
| `regexp_extract(`*`string`*`, `*`pattern `*`, `*`name_list`*`)`; | If *string* contains the regexp *pattern*, returns the capturing groups as a struct with corresponding names from *name_list* | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` | `{'y':'2023', 'm':'04', 'd':'15'}` |
| `regexp_extract_all(`*`string`*`, `*`regex`*`[, `*`group`*` = 0])` | Split the *string* along the *regex* and extract all occurrences of *group* | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` | `[hello, world]` |

The `regexp_matches` function is similar to the `SIMILAR TO` operator, however, it does not require the entire string to match. Instead, `regexp_matches` returns `true` if the string merely contains the pattern (unless the special tokens `^` and `$` are used to anchor the regular expression to the start and end of the string). Below are some examples:

```sql
regexp_matches('abc', 'abc')       -- true
regexp_matches('abc', '^abc$')     -- true
regexp_matches('abc', 'a')         -- true
regexp_matches('abc', '^a$')       -- false
regexp_matches('abc', '.*(b|d).*') -- true
regexp_matches('abc', '(b|c).*')   -- true
regexp_matches('abc', '^(b|c).*')  -- false
regexp_matches('abc', '(?i)A')     -- true
```

The `regexp_matches` function also supports the following options.

<div class="narrow_table"></div>

| Option | Description |
|:---|:---|
|`'c'`|case-sensitive matching|
|`'i'`|case-insensitive matching|
|`'l'`|match literals instead of regular expression tokens|
|`'m'`, `'n'`, `'p'`|newline sensitive matching|
|`'s'`| non-newline sensitive matching|
|`'g'`| global replace, only available for regexp_replace|

```sql
regexp_matches('abcd', 'ABC', 'c')-- false
regexp_matches('abcd', 'ABC', 'i') -- true
regexp_matches('ab^/$cd', '^/$', 'l') -- true
regexp_matches('hello\nworld', 'hello.world', 'p') -- false
regexp_matches('hello\nworld', 'hello.world', 's') -- true
```

The `regexp_matches` operator will be optimized to the `LIKE` operator when possible. To achieve the best results, the `'s'` option should be passed. By default the `RE2` library doesn't match '.' to newline.

<div class="narrow_table"></div>

| Original | Optimized equivalent |
|:---|:---|
|`regexp_matches('hello world', '^hello', 's')`|`prefix('hello world', 'hello')`|
|`regexp_matches('hello world', 'world$', 's')`|`suffix('hello world', 'world')`|
|`regexp_matches('hello world', 'hello.world', 's')`|`LIKE 'hello_world'`|
|`regexp_matches('hello world', 'he.*rld', 's')`|`LIKE '%he%rld'`|


The `regexp_replace` function can be used to replace the part of a string that matches the regexp pattern with a replacement string. The notation `\d` (where d is a number indicating the group) can be used to refer to groups captured in the regular expression in the replacement string. Below are some examples:

```sql
regexp_replace('abc', '(b|c)', 'X')        -- aXc
regexp_replace('abc', '(b|c)', '\1\1\1\1') -- abbbbc
regexp_replace('abc', '(.*)c', '\1e')      -- abe
regexp_replace('abc', '(a)(b)', '\2\1')    -- bac
```

The `regexp_extract` function is used to extract a part of a string that matches the regexp pattern. A specific capturing group within the pattern can be extracted using the *`idx`* parameter. If *`idx`* is not specified, it defaults to 0, extracting the first match with the whole pattern.

```sql
regexp_extract('abc', '.b.')     -- abc
regexp_extract('abc', '.b.', 0)  -- abc
regexp_extract('abc', '.b.', 1)  -- (empty)
regexp_extract('abc', '([a-z])(b)', 1) -- a
regexp_extract('abc', '([a-z])(b)', 2) -- b
```

If *`ids`* is a `LIST` of strings, then `regexp_extract` will return the corresponding capture groups as fields of a `STRUCT`:

```sql
regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd']) -- {'y':'2023', 'm':'04', 'd':'15'}
regexp_extract('2023-04-15 07:59:56', '^(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', ['y', 'm', 'd']) -- {'y':'2023', 'm':'04', 'd':'15'}
regexp_extract('duckdb_0_7_1', '^(\w+)_(\d+)_(\d+)', ['tool', 'major', 'minor', 'fix']) -- error
```

If the number of column names is less than the number of capture groups, then only the first groups are returned.
If the number of column names is greater, then an error is generated.

DuckDB uses RE2 as its regex engine. For more information see the [RE2 docs](https://github.com/google/re2/wiki/Syntax)
