---
layout: docu
railroad: query_syntax/groupby.js
redirect_from:
- /docs/sql/query_syntax/having
- /docs/stable/sql/query_syntax/having
- /docs/current/sql/query_syntax/having
- /docs/lts/sql/query_syntax/having
- /docs/preview/sql/query_syntax/having
title: HAVING Clause
---

The `HAVING` clause applies filter criteria *after* grouping is completed. It is typically used in addition to a [`GROUP BY` clause]({% link docs/2.0/sql/query_syntax/groupby.md %}). In queries that use both, the `HAVING` clause must directly follow the `GROUP BY` clause. 

The `HAVING` keyword is followed by a `BOOLEAN` expression that acts as a filter condition. The condition is evaluated for each grouping, keeping only those row groupings for which the condition evaluates to `TRUE`. In this respect, the `HAVING` clause is similar to the [`WHERE` clause]({% link docs/2.0/sql/query_syntax/where.md %}), except that the `WHERE` clause is applied to individual rows prior to grouping, while the `HAVING` clause is applied after grouping. For this reason, the condition of the `HAVING` clause can use aggregate functions, which is not allowed in the `WHERE` clause.

## Examples

For each `city`, return the number of rows from the `addresses` table, keeping only those cities with `50` or more addresses:

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city
HAVING count(*) >= 50;
```

Return average `income` per `city` and `street_name` for those `city`/`street_name` groupings where the median `income` exceeds `50000`:

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY city, street_name
HAVING median(income) > 50000;
``` 

## Syntax

<div id="rrdiagram"></div>
