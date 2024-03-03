---
layout: docu
title: LIMIT Clause
selected: Documentation/SQL/Query Syntax/Limit
expanded: SQL
railroad: query_syntax/orderby.js
---

`LIMIT` is an output modifier. Logically it is applied at the very end of the query. The `LIMIT` clause restricts the amount of rows fetched. The `OFFSET` clause indicates at which position to start reading the values, i.e. the first `OFFSET` values are ignored.

Note that while `LIMIT` can be used without an `ORDER BY` clause, the results might not be deterministic without the `ORDER BY` clause. This can still be useful, however, for example when you want to inspect a quick snapshot of the data.


### Examples

```sql
-- select the first 5 rows from the addresses table
SELECT *
FROM addresses
LIMIT 5;
-- select the 5 rows from the addresses table, starting at position 5 (i.e. ignoring the first 5 rows)
SELECT *
FROM addresses
LIMIT 5
OFFSET 5;
-- select the top 5 cities with the highest population
SELECT city, COUNT(*) AS population
FROM addresses
GROUP BY city
ORDER BY population DESC
LIMIT 5;
```

### Syntax
<div id="rrdiagram"></div>
