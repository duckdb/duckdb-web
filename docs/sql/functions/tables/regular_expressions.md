| Function | Description | Example | Result |
|:---|:---|:---|:--|
| `regexp_extract_all(`*`string`*`, `*`regex`*`[, `*`group`*` = 0])` | Split the *string* along the *regex* and extract all occurrences of *group* | `regexp_extract_all('hello_world', '([a-z ]+)_?', 1)` | `[hello, world]` |
| `regexp_extract(`*`string`*`, `*`pattern `*`, `*`name_list`*`)`; | If *string* contains the regexp *pattern*, returns the capturing groups as a struct with corresponding names from *name_list* | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` | `{'y':'2023', 'm':'04', 'd':'15'}` |
| `regexp_extract(`*`string`*`, `*`pattern `*`[, `*`idx`*`])`; | If *string* contains the regexp *pattern*, returns the capturing group specified by optional parameter *idx* | `regexp_extract('hello_world', '([a-z ]+)_?', 1)` | `hello` |
| `regexp_full_match(`*`string`*`, `*`regex`*`)`| Returns `true` if the entire *string* matches the *regex* | `regexp_full_match('anabanana', '(an)*')` | `false` |
| `regexp_matches(`*`string`*`, `*`pattern`*`)` | Returns `true` if  *string* contains the regexp *pattern*, `false` otherwise | `regexp_matches('anabanana', '(an)*')` | `true` |
| `regexp_replace(`*`string`*`, `*`pattern`*`, `*`replacement`*`)`; | If *string* contains the regexp *pattern*, replaces the matching part with *replacement* | `regexp_replace('hello', '[lo]', '-')` | `he-lo` |
| `regexp_split_to_array(`*`string`*`, `*`regex`*`)` | Alias of `string_split_regex`. Splits the *string* along the *regex* | `regexp_split_to_array('hello␣world; 42', ';?␣')` | `['hello', 'world', '42']` |
| `regexp_split_to_table(`*`string`*`, `*`regex`*`)` | Splits the *string* along the *regex* and returns a row for each part | `regexp_split_to_array('hello␣world; 42', ';?␣')` | Two rows: `'hello'`, `'world'` |
