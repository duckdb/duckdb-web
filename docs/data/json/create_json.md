

## JSON Creation Functions

The following functions are used to create JSON.

<div class="narrow_table"></div>

| Function | Description |
|:--|:----|
| `to_json(any)` | Create `JSON` from a value of `any` type. Our `LIST` is converted to a JSON array, and our `STRUCT` and `MAP` are converted to a JSON object. |
| `json_quote(any)` | Alias for `to_json`. |
| `array_to_json(list)` | Alias for `to_json` that only accepts `LIST`. |
| `row_to_json(list)` | Alias for `to_json` that only accepts `STRUCT`. |
| `json_array([any, ...])` | Create a JSON array from `any` number of values. |
| `json_object([key, value, ...])` | Create a JSON object from any number of `key`, `value` pairs. |
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
SELECT json_array(42, 'duck', NULL);
```

```text
[42,"duck",null]
```

```sql
SELECT json_object('duck', 42);
```

```text
{"duck":42}
```

```sql
SELECT json_merge_patch('{"duck": 42}', '{"goose": 123}');
```

```text
{"goose":123,"duck":42}
```
