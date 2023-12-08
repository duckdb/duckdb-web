---
layout: docu
redirect_from:
- /docs/extensions/autocomplete
title: AutoComplete Extension
---

The `autocomplete` extension adds supports for autocomplete in the [CLI client](../api/cli).
The extension is shipped by default with the CLI client.

## Auto-Completion Rules

The DuckDB shell auto-completes four different groups: (1) keywords, (2) table names + table functions, (3) column names + scalar functions, and (4) file names. The shell looks at the position in the SQL statement to determine which of these auto-completions to trigger. For example:

```sql
S -> SELECT
```
```sql
SELECT s -> student_id
```
```sql
SELECT student_id F -> FROM
```
```sql
SELECT student_id FROM g -> grades
```
```sql
SELECT student_id FROM 'd -> data/
```
```sql
SELECT student_id FROM 'data/ -> data/grades.csv
```

## Functions

<div class="narrow_table"></div>

| Function                                | Description                                            |
|:----------------------------------------|:-------------------------------------------------------|
| `sql_auto_complete(`*`query_string`*`)` | Attempts autocompletion on the given *`query_string`*. |

## Example

```sql
SELECT * FROM sql_auto_complete('SEL');
```

Returns:

<div class="narrow_table"></div>

| suggestion  | suggestion_start |
|-------------|------------------|
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
