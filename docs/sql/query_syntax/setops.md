---
layout: docu
title: Set Operations
selected: Documentation/SQL/Query Syntax/Set Operations
expanded: SQL
railroad: query_syntax/setops.js
---

Set operations allow queries to be combined according to [set operation semantics](https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations). Set operations refer to the `UNION [ALL]`, `INTERSECT` and `EXCEPT` clauses.

Traditional set operations unify queries **by column position**, and require the to-be-combined queries to have the same number of input columns. If the columns are not of the same type, casts may be added.  The result will use the column names from the first query.

DuckDB also supports `UNION BY NAME`, which joins columns by name instead of by position. `UNION BY NAME` does not require the inputs to have the same number of columns. `NULL` values will be added in case of missing columns. 

## Examples
```sql
-- the values [0..10) and [0..5)
SELECT * FROM range(10) t1 UNION ALL SELECT * FROM range(5) t2;
-- the values [0..10) (`UNION` eliminates duplicates)
SELECT * FROM range(10) t1 UNION SELECT * FROM range(5) t2;
-- the values [0..5] (all values that are both in t1 and t2)
SELECT * FROM range(10) t1 INTERSECT SELECT * FROM range(6) t2;
-- the values [5..10)
SELECT * FROM range(10) t1 EXCEPT SELECT * FROM range(5) t2;
-- two rows, (24, NULL) and (NULL, Amsterdam)
SELECT 24 AS id UNION ALL BY NAME SELECT 'Amsterdam' as City;
```

## Syntax
<div id="rrdiagram"></div>

## Example Table
```sql
CREATE TABLE capitals(city VARCHAR, country VARCHAR);
INSERT INTO capitals VALUES ('Amsterdam', 'NL'), ('Berlin', 'Germany');

CREATE TABLE weather(city VARCHAR, degrees INTEGER, date DATE);
INSERT INTO weather VALUES ('Amsterdam', 10, '2022-10-14'), ('Seattle', 8, '2022-10-12');
```

## UNION (ALL)

The `UNION` clause can be used to combine rows from multiple queries. The queries are required to have the same number of columns and the same column types.

The `UNION` clause performs duplicate elimination by default - only unique rows will be included in the result.

`UNION ALL` returns all rows of both queries *without* duplicate elimination.

```sql
SELECT city FROM capitals UNION SELECT city FROM weather;
-- Amsterdam, Berlin, Seattle

SELECT city FROM capitals UNION ALL SELECT city FROM weather;
-- Amsterdam, Amsterdam, Berlin, Seattle
```

## INTERSECT

The `INTERSECT` clause can be used to select all rows that occur in the result of **both** queries. Note that `INTERSECT` performs duplicate elimination, so only unique rows are returned.

```sql
SELECT city FROM capitals INTERSECT SELECT city FROM weather;
-- Amsterdam
```

## EXCEPT

The `EXCEPT` clause can be used to select all rows that **only** occur in the left query. Note that `EXCEPT` performs duplicate elimination, so only unique rows are returned.

```sql
SELECT city FROM capitals EXCEPT SELECT city FROM weather;
-- Berlin
```

## UNION (ALL) BY NAME

The `UNION (ALL) BY NAME` clause can be used to combine rows from different tables by name, instead of by position. `UNION BY NAME` does not require both queries to have the same number of columns. Any columns that are only found in one of the queries are filled with `NULL` values for the other query.   

```sql
SELECT * FROM capitals UNION BY NAME SELECT * FROM weather;
```

```
┌───────────┬─────────┬─────────┬────────────┐
│   city    │ country │ degrees │    date    │
│  varchar  │ varchar │  int32  │    date    │
├───────────┼─────────┼─────────┼────────────┤
│ Amsterdam │ NULL    │      10 │ 2022-10-14 │
│ Seattle   │ NULL    │       8 │ 2022-10-12 │
│ Amsterdam │ NL      │    NULL │ NULL       │
│ Berlin    │ Germany │    NULL │ NULL       │
└───────────┴─────────┴─────────┴────────────┘
```

`UNION BY NAME` performs duplicate elimination, whereas `UNION ALL BY NAME` does not.
