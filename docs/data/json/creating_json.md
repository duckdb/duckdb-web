---
layout: docu
title: Creating JSON
---

## JSON Creation Functions

The following functions are used to create JSON.


| Function | Description |
|:--|:----|
| `to_json(any)` | Create `JSON` from a value of `any` type. Our `LIST` is converted to a JSON array, and our `STRUCT` and `MAP` are converted to a JSON object. |
| `json_quote(any)` | Alias for `to_json`. |
| `array_to_json(list)` | Alias for `to_json` that only accepts `LIST`. |
| `row_to_json(list)` | Alias for `to_json` that only accepts `STRUCT`. |
| `json_array(any, ...)` | Create a JSON array from the values in the argument lists. |
| `json_object(key, value, ...)` | Create a JSON object from `key`, `value` pairs in the argument list. Requires an even number of arguments. |
| `json_merge_patch(json, json)` | Merge two JSON documents together. |

Examples:

```sql
SELECT to_json('duck');
```

```text
"duck"
```

```sql
SELECT to_json([1, 2, 3]);
```

```text
[1,2,3]
```

```sql
SELECT to_json({duck : 42});
```

```text
{"duck":42}
```

```sql
SELECT to_json(map(['duck'],[42]));
```

```text
{"duck":42}
```

```sql
SELECT json_array('duck', 42, 'goose', 123);
```

```text
["duck",42,"goose",123]
```

```sql
SELECT json_object('duck', 42, 'goose', 123);
```

```text
{"duck":42,"goose":123}
```

```sql
SELECT json_merge_patch('{"duck": 42}', '{"goose": 123}');
```

```text
{"goose":123,"duck":42}
```
