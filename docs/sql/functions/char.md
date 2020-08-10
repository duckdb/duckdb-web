---
layout: docu
title: Text Functions
selected: Documentation/Functions/Text Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating string values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *`string`* `||` *`string`* | String concatenation | `'Duck' || 'DB'` | DuckDB |
| `concat(`*`string`*`, ...)` | Concatenate many strings together | `concat('Hello', ' ', 'World')` | Hello World |
| `concat_ws(`*`separator`*`, `*`string`*`, ...)` | Concatenate strings together separated by the specified separator | `concat_ws(',', 'Banana', 'Apple', 'Melon')` | Banana,Apple,Melon |
| `format(`*`format`*`, `*`parameters`*`...)` | Formats a string using fmt syntax | `format('Benchmark "{}" took {} seconds', 'CSV', 42)` | Benchmark "CSV" took 42 seconds |
| `left(`*`string`*`, `*`count`*`)`| Extract the left-most count characters | `left('hello', 2)` | he |
| `length(`*`string`*`)` | Number of characters in string | `length('Hello')` | 5 |
| *`string`*` LIKE `*`target`* | Returns true if the string matches the like specifier (see [Pattern Matching](/docs/sql/functions/patternmatching)) | `'hello' LIKE '%lo'` | true |
| `lower(`*`string`*`)` | Convert string to lower case | `lower('Hello')` | hello |
| `lpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the string  with the character from the left until it has count characters | `lpad('hello', 10, '>')` | >>>>>hello |
| `ltrim(`*`text`*`)`| Removes any spaces from the left side of the string | `ltrim('    test  ')` | test   |
| `ltrim(`*`text`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the left side of the string | `ltrim('>>>>test<<', '><')` | test<< |
| `upper(`*`string`*`)`| Convert string to upper case | `upper('Hello')` | HELLO |
| `printf(`*`format`*`, `*`parameters`*`...)` | Formats a string using printf syntax | `printf('Benchmark "%s" took %d seconds', 'CSV', 42)` | Benchmark "CSV" took 42 seconds |
| `regexp_full_match(`*`string`*`, `*`regex`*`)`| Returns true if the entire string matches the regex (see [Pattern Matching](/docs/sql/functions/patternmatching)) | `regexp_full_match('anabanana', '(an)*')` | false |
| `regexp_matches(`*`string`*`, `*`regex`*`)`| Returns true if a part of string matches the regex (see [Pattern Matching](/docs/sql/functions/patternmatching)) | `regexp_matches('anabanana', '(an)*')` | true |
| `regexp_replace(`*`string`*`, `*`regex`*`, `*`replacement`*`, `*`modifiers`*`)`| Replaces the first occurrence of *regex* with the *replacement*, use `'g'` modifier to replace all occurrences instead (see [Pattern Matching](/docs/sql/functions/patternmatching)) | `select regexp_replace('hello', '[lo]', '-')` | he-lo |
| `repeat(`*`string`*`, `*`count`*`)`| Repeats the string *count* number of times | `repeat('A', 5)` | AAAAA |
| `replace(`*`string`*`, `*`source`*`, `*`target`*`)`| Replaces any occurrences of the *source* with *target* in *string* | `replace('hello', 'l', '-')` | he--o |
| `reverse(`*`string`*`)`| Reverses the string | `reverse('hello')` | olleh |
| `right(`*`string`*`, `*`count`*`)`| Extract the right-most *count* characters | `right('hello', 3)` | llo |
| `rpad(`*`string`*`, `*`count`*`, `*`character`*`)`| Pads the string with the character from the right until it has *count* characters | `rpad('hello', 10, '<')` | hello<<<<< |
| `rtrim(`*`text`*`)`| Removes any spaces from the right side of the string | `rtrim('    test  ')` |     test |
| `rtrim(`*`text`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from the right side of the string | `rtrim('>>>>test<<', '><')` | >>>>test |
| *`string`*` SIMILAR TO `*`regex`* | Returns true if the string matches the regex; identical to regexp_full_match (see [Pattern Matching](/docs/sql/functions/patternmatching)) | `'hello' SIMILAR TO 'l+'` | false |
| `strlen(`*`string`*`)` | Number of bytes in string | `length('🤦🏼‍♂️')` | 17 |
| `strip_accents(`*`text`*`)`| Strips accents from text | `strip_accents('mühleisen')` | muhleisen |
| `substring(`*`string`*`, `*`start`*`, `*`length`*`)` | Extract substring of *length* characters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | `substring('Hello', 2, 2)` | el |
| `trim(`*`text`*`)`| Removes any spaces from either side of the string | `trim('    test  ')` | test |
| `trim(`*`text`*`, `*`characters`*`)`| Removes any occurrences of any of the *characters* from either side of the string | `trim('>>>>test<<', '><')` | test |
| `unicode(`*`string`*`)`| Returns the unicode code of the first character of the string | `unicode('ü')` | 252 |
