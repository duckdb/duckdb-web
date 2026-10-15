---
layout: docu
railroad: query_syntax/orderby.js
title: LIMIT and OFFSET Clauses
---

`LIMIT` is an output modifier. Logically it is applied at the very end of the query. The `LIMIT` clause restricts the amount of rows fetched. The `OFFSET` clause indicates at which position to start reading the values, i.e., the first `OFFSET` values are ignored.

Note that while `LIMIT` can be used without an `ORDER BY` clause, the results might not be deterministic without the `ORDER BY` clause. This can still be useful, however, for example when you want to inspect a quick snapshot of the data.

## Examples

Select the first 5 rows from the addresses table:

```sql
SELECT *
FROM addresses
LIMIT 5;
```

Select the 5 rows from the addresses table, starting at position 5 (i.e., ignoring the first 5 rows):

```sql
SELECT *
FROM addresses
LIMIT 5
OFFSET 5;
```

Select the top 5 cities with the highest population:

```sql
SELECT city, count(*) AS population
FROM addresses
GROUP BY city
ORDER BY population DESC
LIMIT 5;
```

Select 10% of the rows from the addresses table:

```sql
SELECT *
FROM addresses
LIMIT 10%;
```

## FETCH FIRST

> New The SQL-standard `FETCH FIRST` syntax is introduced in DuckDB 2.0.

As an alternative to `LIMIT`, DuckDB supports the SQL-standard `FETCH FIRST ... ROWS ONLY` syntax. It can be combined with `OFFSET`, in which case `FETCH NEXT` reads better:

```sql
SELECT *
FROM addresses
ORDER BY city
FETCH FIRST 5 ROWS ONLY;
```

```sql
SELECT *
FROM addresses
ORDER BY city
OFFSET 5 ROWS
FETCH NEXT 10 ROWS ONLY;
```

`FIRST` and `NEXT` are interchangeable, as are `ROW` and `ROWS`. Omitting the row count fetches a single row:

```sql
SELECT *
FROM addresses
ORDER BY city
FETCH FIRST ROW ONLY;
```

## Syntax

<div id="rrdiagram"></div>
