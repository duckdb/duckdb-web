---
layout: docu
title: FILTER Clause
selected: Documentation/SQL/Query Syntax/Filter
expanded: SQL
railroad: query_syntax/filter.js
---
The `FILTER` clause may optionally follow an aggregate function in a `SELECT` statement. This will filter the rows of data that are fed into the aggregate function in the same way that a `WHERE` clause filters rows, but localized to the specific aggregate function. Filters are able to be used when the aggregate function is in a windowing context as well. The filter is applied prior to the application of the window.

There are multiple types of situations where this is useful, including when evaluating multiple aggregates with different filters, and when creating a pivoted view of a dataset. There is also a performance advantage to using `FILTER` over the more traditional `CASE WHEN` approach discussed below. 

<!-- 
Brainstorming 

    High level description

    Examples

    Equivalence to CASE WHEN
        Performance comparison
    
    Syntax diagram

    Also need to add some content to the Aggregate Functions page

-->

## Examples
```sql
-- select all rows that have id equal to 3
SELECT *
FROM table_name
WHERE id=3;
-- select all rows that match the given case-insensitive LIKE expression
SELECT *
FROM table_name
WHERE name ILIKE '%mark%';
-- select all rows that match the given composite expression
SELECT *
FROM table_name
WHERE id=3 OR id=7;
```

## Aggregate Function Syntax (Including Filter Clause)
<div id="rrdiagram"></div>
