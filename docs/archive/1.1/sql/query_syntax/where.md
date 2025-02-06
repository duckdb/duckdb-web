---
layout: docu
railroad: query_syntax/where.js
title: WHERE Clause
---

The `WHERE` clause specifies any filters to apply to the data. This allows you to select only a subset of the data in which you are interested. Logically the `WHERE` clause is applied immediately after the `FROM` clause.

## Examples

Select all rows that where the `id` is equal to 3:

```sql
SELECT *
FROM table_name
WHERE id = 3;
```

Select all rows that match the given **case-sensitive** `LIKE` expression:

```sql
SELECT *
FROM table_name
WHERE name LIKE '%mark%';
```

Select all rows that match the given **case-insensitive** expression formulated with the `ILIKE` operator:

```sql
SELECT *
FROM table_name
WHERE name ILIKE '%mark%';
```

Select all rows that match the given composite expression:

```sql
SELECT *
FROM table_name
WHERE id = 3 OR id = 7;
```

## Syntax

<div id="rrdiagram"></div>