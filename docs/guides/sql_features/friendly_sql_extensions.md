---
layout: docu
title: Friendly SQL Extensions
---

DuckDB offers several extensions to the SQL syntax, known colloquially as "friendly SQL" extensions.

## Friendly SQL Extensions

### `GROUP BY ALL`

### `ORDER BY ALL`

### `SELECT * EXCLUDE`

### `SELECT * REPLACE`

### `UNION BY NAME`



### Case Insensitivity While Maintaining Case


see the [rules for case-sensitivity](../../../docs/sql/keywords_and_identifiers#case-sensitivity-of-identifiers).

### Trailing Commas

DuckDB allows [trailing commas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas), both when listing entities (e.g., column and table names) and when constructing [`LIST` items](../../../docs/sql/data_types/list#creating-lists).

```sql
SELECT
    42 AS x,
    ['a', 'b', 'c',] AS y,
    'hello world' AS z,
;
```

## See Also

* [Friendlier SQL with DuckDB](/2022/05/04/friendlier-sql) blog post
* [Even Friendlier SQL with DuckDB](/2023/08/23/even-friendlier-sql.html) blog post
