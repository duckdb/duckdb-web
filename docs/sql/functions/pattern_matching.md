---
layout: docu
title: Pattern Matching
railroad: expressions/like.js
redirect_from:
  - docs/sql/functions/patternmatching
  - docs/sql/functions/patternmatching.html
---

There are four separate approaches to pattern matching provided by DuckDB:
the traditional SQL [`LIKE` operator](#like),
the more recent [`SIMILAR TO` operator](#similar-to) (added in SQL:1999),
a [`GLOB` operator](#glob),
and POSIX-style [regular expressions](#regular-expressions).

## `LIKE`

<div id="rrdiagram1"></div>

The `LIKE` expression returns `true` if the string matches the supplied pattern. (As expected, the `NOT LIKE` expression returns `false` if `LIKE` returns `true`, and vice versa. An equivalent expression is `NOT (string LIKE pattern)`.)

If pattern does not contain percent signs or underscores, then the pattern only represents the string itself; in that case `LIKE` acts like the equals operator. An underscore (`_`) in pattern stands for (matches) any single character; a percent sign (`%`) matches any sequence of zero or more characters.

`LIKE` pattern matching always covers the entire string. Therefore, if it's desired to match a sequence anywhere within a string, the pattern must start and end with a percent sign.

Some examples:

```sql
SELECT 'abc' LIKE 'abc'; -- true
SELECT 'abc' LIKE 'a%' ; -- true
SELECT 'abc' LIKE '_b_'; -- true
SELECT 'abc' LIKE 'c';   -- false
SELECT 'abc' LIKE 'c%' ; -- false
SELECT 'abc' LIKE '%c';  -- true
SELECT 'abc' NOT LIKE '%c'; -- false
```

The keyword `ILIKE` can be used instead of `LIKE` to make the match case-insensitive according to the active locale. 

```sql
SELECT 'abc' ILIKE '%C'; -- true
SELECT 'abc' NOT ILIKE '%C'; -- false
```

To search within a string for a character that is a wildcard (`%` or `_`), the pattern must use an `ESCAPE` clause and an escape character to indicate the wildcard should be treated as a literal character instead of a wildcard. See an example below.

Additionally, the function `like_escape` has the same functionality as a `LIKE` expression with an `ESCAPE` clause, but using function syntax. See the [Text Functions Docs](../../sql/functions/char) for details.

```sql
-- Search for strings with 'a' then a literal percent sign then 'c'
SELECT 'a%c' LIKE 'a$%c' ESCAPE '$'; -- true
SELECT 'azc' LIKE 'a$%c' ESCAPE '$'; -- false

-- Case-insensitive ILIKE with ESCAPE
SELECT 'A%c' ILIKE 'a$%c' ESCAPE '$'; -- true
```

There are also alternative characters that can be used as keywords in place of `LIKE` expressions. These enhance PostgreSQL compatibility.

<div class="narrow_table"></div>

| LIKE-style | PostgreSQL-style |
|:---|:---|
| `LIKE` | `~~` |
| `NOT LIKE` | `!~~` |
| `ILIKE` | `~~*` |
| `NOT ILIKE` | `!~~*` |

## `SIMILAR TO`

<div id="rrdiagram2"></div>

The `SIMILAR TO` operator returns true or false depending on whether its pattern matches the given string. It is similar to `LIKE`, except that it interprets the pattern using a [regular expression](regular_expressions). Like `LIKE`, the `SIMILAR TO` operator succeeds only if its pattern matches the entire string; this is unlike common regular expression behavior where the pattern can match any part of the string.

A regular expression is a character sequence that is an abbreviated definition of a set of strings (a regular set). A string is said to match a regular expression if it is a member of the regular set described by the regular expression. As with `LIKE`, pattern characters match string characters exactly unless they are special characters in the regular expression language — but regular expressions use different special characters than `LIKE` does.

Some examples:

```sql
SELECT 'abc' SIMILAR TO 'abc';       -- true
SELECT 'abc' SIMILAR TO 'a';         -- false
SELECT 'abc' SIMILAR TO '.*(b|d).*'; -- true
SELECT 'abc' SIMILAR TO '(b|c).*';   -- false
SELECT 'abc' NOT SIMILAR TO 'abc';   -- false
```

There are also alternative characters that can be used as keywords in place of `SIMILAR TO` expressions. These follow POSIX syntax.

<div class="narrow_table"></div>

| `SIMILAR TO`-style | POSIX-style |
|:---|:---|
| `SIMILAR TO` | `~` |
| `NOT SIMILAR TO` | `!~` |

## `GLOB`

<div id="rrdiagram3"></div>

The `GLOB` operator returns `true` or `false` if the string matches the `GLOB` pattern. The `GLOB` operator is most commonly used when searching for filenames that follow a specific pattern (for example a specific file extension). Use the question mark (`?`) wildcard to match any single character, and use the asterisk (`*`()) to match zero or more characters. In addition, use bracket syntax (`[ ]`) to match any single character contained within the brackets, or within the character range specified by the brackets. An exclamation mark (`!`) may be used inside the first bracket to search for a character that is not contained within the brackets. To learn more, visit the [Glob Programming Wikipedia page](https://en.wikipedia.org/wiki/Glob_(programming)).

Some examples:

```sql
SELECT 'best.txt' GLOB '*.txt';            -- true
SELECT 'best.txt' GLOB '????.txt';         -- true
SELECT 'best.txt' GLOB '?.txt';            -- false
SELECT 'best.txt' GLOB '[abc]est.txt';     -- true
SELECT 'best.txt' GLOB '[a-z]est.txt';     -- true

-- The bracket syntax is case-sensitive
SELECT 'Best.txt' GLOB '[a-z]est.txt';     -- false
SELECT 'Best.txt' GLOB '[a-zA-Z]est.txt';  -- true

-- The ! applies to all characters within the brackets
SELECT 'Best.txt' GLOB '[!a-zA-Z]est.txt'; -- false

-- To negate a GLOB operator, negate the entire expression 
-- (NOT GLOB is not valid syntax)
SELECT NOT 'best.txt' GLOB '*.txt';        -- false
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

DuckDB's regex support is documented on the [Regular Expressions page](regular_expressions).
