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

The `HAVING` clause can be used after the `GROUP BY` clause to provide filter criteria *after* the grouping has been completed. In terms of syntax the `HAVING` clause is identical to the `WHERE` clause, but while the `WHERE` clause occurs before the grouping, the `HAVING` clause occurs after the grouping.

## Examples

Count the number of entries in the `addresses` table that belong to each different `city`, filtering out cities with a count below 50:

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city
HAVING count(*) >= 50;
```

For each `city` and `street_name`, show the average `income` if it exceeds twice the median `income` for that group:

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY city, street_name
HAVING avg(income) > 2 * median(income);
```

## Syntax

<div id="rrdiagram"></div>
