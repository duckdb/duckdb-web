---
layout: docu
railroad: query_syntax/groupby.js
title: GROUP BY Clause
---

The `GROUP BY` clause specifies which grouping columns should be used to perform any aggregations in the `SELECT` clause.
If the `GROUP BY` clause is specified, the query is always an aggregate query, even if no aggregations are present in the `SELECT` clause.

When a `GROUP BY` clause is specified, all tuples that have matching data in the grouping columns (i.e., all tuples that belong to the same group) will be combined.
The values of the grouping columns themselves are unchanged, and any other columns can be combined using an [aggregate function]({% link docs/archive/1.1/sql/functions/aggregates.md %}) (such as `count`, `sum`, `avg`, etc).

## `GROUP BY ALL`

Use `GROUP BY ALL` to `GROUP BY` all columns in the `SELECT` statement that are not wrapped in aggregate functions.
This simplifies the syntax by allowing the columns list to be maintained in a single location, and prevents bugs by keeping the `SELECT` granularity aligned to the `GROUP BY` granularity (e.g., it prevents duplication).
See examples below and additional examples in the [“Friendlier SQL with DuckDB” blog post]({% post_url 2022-05-04-friendlier-sql %}#group-by-all).

## Multiple Dimensions

Normally, the `GROUP BY` clause groups along a single dimension.
Using the [`GROUPING SETS`, `CUBE` or `ROLLUP` clauses]({% link docs/archive/1.1/sql/query_syntax/grouping_sets.md %}) it is possible to group along multiple dimensions.
See the [`GROUPING SETS`]({% link docs/archive/1.1/sql/query_syntax/grouping_sets.md %}) page for more information.

## Examples

Count the number of entries in the `addresses` table that belong to each different city:

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city;
```

Compute the average income per city per street_name:

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY city, street_name;
```

### `GROUP BY ALL` Examples

Group by city and street_name to remove any duplicate values:

```sql
SELECT city, street_name
FROM addresses
GROUP BY ALL;
```

Compute the average income per city per street_name. Since income is wrapped in an aggregate function, do not include it in the `GROUP BY`:

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY ALL;
-- GROUP BY city, street_name:
```

## Syntax

<div id="rrdiagram"></div>