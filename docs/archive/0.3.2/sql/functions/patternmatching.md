---
layout: docu
title: Pattern Matching
selected: Documentation/Functions/Pattern Matching
expanded: Functions
railroad: expressions/like.js
---
## Pattern Matching
There are three separate approaches to pattern matching provided by DuckDB: the traditional SQL `LIKE` operator, the more recent `SIMILAR TO` operator (added in SQL:1999), and POSIX-style regular expressions.

## LIKE
<div id="rrdiagram1"></div>

The `LIKE` expression returns true if the string matches the supplied pattern. (As expected, the `NOT LIKE` expression returns false if `LIKE` returns true, and vice versa. An equivalent expression is `NOT (string LIKE pattern)`.)

If pattern does not contain percent signs or underscores, then the pattern only represents the string itself; in that case `LIKE` acts like the equals operator. An underscore (`_`) in pattern stands for (matches) any single character; a percent sign (`%`) matches any sequence of zero or more characters.

Some examples:

```sql
'abc' LIKE 'abc' -- TRUE
'abc' LIKE 'a%'  -- TRUE
'abc' LIKE '_b_' -- TRUE
'abc' LIKE 'c'   -- FALSE
'abc' LIKE 'c%'  -- FALSE
'abc' LIKE '%c'  -- TRUE
```

`LIKE` pattern matching always covers the entire string. Therefore, if it's desired to match a sequence anywhere within a string, the pattern must start and end with a percent sign.

<!--The key word ILIKE can be used instead of LIKE to make the match case-insensitive according to the active locale. This is not in the SQL standard.-->

## SIMILAR TO
<div id="rrdiagram2"></div>

The `SIMILAR TO` operator returns true or false depending on whether its pattern matches the given string. It is similar to `LIKE`, except that it interprets the pattern using a regular expression. Like `LIKE`, the `SIMILAR TO` operator succeeds only if its pattern matches the entire string; this is unlike common regular expression behavior where the pattern can match any part of the string.

A regular expression is a character sequence that is an abbreviated definition of a set of strings (a regular set). A string is said to match a regular expression if it is a member of the regular set described by the regular expression. As with `LIKE`, pattern characters match string characters exactly unless they are special characters in the regular expression language — but regular expressions use different special characters than `LIKE` does.

Some examples:

```sql
'abc' SIMILAR TO 'abc'       -- TRUE
'abc' SIMILAR TO 'a'         -- FALSE
'abc' SIMILAR TO '.*(b|d).*' -- TRUE
'abc' SIMILAR TO '(b|c).*'   -- FALSE
```

## Regular Expressions

| Function | Description |
|:---|:---|
| `regexp_matches(`*`string`*`, `*`pattern`*`)` | returns `TRUE` if  *string* contains the regexp *pattern*, `FALSE` otherwise |
| `regexp_replace(`*`string`*`, `*`pattern`*`, `*`replacement`*`)`; | if *string* contains the regexp *pattern*, replaces the matching part with *replacement* |
| `regexp_extract(`*`string`*`, `*`pattern `*`[, `*`idx`*`])`; | if *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx* |

The `regexp_matches` function is similar to the `SIMILAR TO` operator, however, it does not require the entire string to match. Instead, `regexp_matches` returns `TRUE` if the string merely contains the pattern (unless the special tokens `^` and `$` are used to anchor the regular expression to the start and end of the string). Below are some examples:

```sql
regexp_matches('abc', 'abc')       -- TRUE
regexp_matches('abc', '^abc$')     -- TRUE
regexp_matches('abc', 'a')         -- TRUE
regexp_matches('abc', '^a$')       -- FALSE
regexp_matches('abc', '.*(b|d).*') -- TRUE
regexp_matches('abc', '(b|c).*')   -- TRUE
regexp_matches('abc', '^(b|c).*')  -- FALSE
```

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
