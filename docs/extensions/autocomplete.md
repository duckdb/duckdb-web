---
layout: docu
title: AutoComplete Extension
---

This extension adds supports for autocomplete in the [CLI client](../api/cli).

| Function                                | Description                                            |
|:----------------------------------------|:-------------------------------------------------------|
| `sql_auto_complete(`*`query_string`*`)` | Attempts autocompletion on the given *`query_string`*. |

## Example

```sql
SELECT * FROM sql_auto_complete('SEL');
```

Returns:

| suggestion  | suggestion_start |
| ----------- | ---------------- |
| SELECT      |                0 |
| DELETE      |                0 |
| INSERT      |                0 |
| CALL        |                0 |
| LOAD        |                0 |
| CALL        |                0 |
| ALTER       |                0 |
| BEGIN       |                0 |
| EXPORT      |                0 |
| CREATE      |                0 |
| PREPARE     |                0 |
| EXECUTE     |                0 |
| EXPLAIN     |                0 |
| ROLLBACK    |                0 |
| DESCRIBE    |                0 |
| SUMMARIZE   |                0 |
| CHECKPOINT  |                0 |
| DEALLOCATE  |                0 |
| UPDATE      |                0 |
| DROP        |                0 |
