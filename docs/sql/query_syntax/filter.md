---
layout: docu
title: FILTER Clause
selected: Documentation/SQL/Query Syntax/Filter
expanded: SQL
railroad: query_syntax/filter.js
---
The `FILTER` clause may optionally follow an aggregate function in a `SELECT` statement. This will filter the rows of data that are fed into the aggregate function in the same way that a `WHERE` clause filters rows, but localized to the specific aggregate function. `FILTER`s are not currently able to be used when the aggregate function is in a windowing context. 

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
-- Compare total row count to:
--   The number of rows where i <= 5 
--   The number of rows where i is odd 
SELECT 
    count(*) as total_rows,
    count(*) FILTER (WHERE i <= 5) as lte_five,
    count(*) FILTER (WHERE i % 2 = 1) as odds
FROM generate_series(1,10) tbl(i);
```

| total_rows | lte_five | odds |
|:---|:---|:---|
| 10 | 5 | 5 |

```sql
-- Different aggregate functions may be used also
--   The sum of i for rows where i <= 5 
--   The median of i where i is odd 
SELECT 
    sum(i) FILTER (WHERE i <= 5) as lte_five_sum,
    median(i) FILTER (WHERE i % 2 = 1) as odds_median
FROM generate_series(1,10) tbl(i);
```

| lte_five_sum | odds_median |
|:---|:---|
| 15 | 5.0 |

```sql
SELECT sum(i) FILTER (WHERE i % 10 = 1), sum(i) FILTER (WHERE i % 100 = 1) from generate_series(1,100000000) tbl(i);

SELECT sum(CASE WHEN i % 10 = 1 THEN i END), sum(CASE WHEN i % 100 = 1 THEN i END) from generate_series(1,100000000) tbl(i);

CREATE TEMP TABLE stacked_data as SELECT i, CASE WHEN i <= rows * 0.25 THEN 2022 WHEN i <= rows * 0.5 THEN 2023 WHEN i <= rows * 0.75 THEN 2024 ELSE 2025 END as year from (select i, count(*) over () as rows from generate_series(1,100000000) tbl(i)) tbl;

SELECT
    sum(i) FILTER (WHERE year = 2022) as "2022",
    sum(i) FILTER (WHERE year = 2023) as "2023",
    sum(i) FILTER (WHERE year = 2024) as "2024",
    sum(i) FILTER (WHERE year = 2025) as "2025"
FROM stacked_data;

SELECT
    sum(CASE WHEN year = 2022 THEN i END) as "2022",
    sum(CASE WHEN year = 2023 THEN i END) as "2023",
    sum(CASE WHEN year = 2024 THEN i END) as "2024",
    sum(CASE WHEN year = 2025 THEN i END) as "2025"
FROM stacked_data;




```

## Aggregate Function Syntax (Including Filter Clause)
<div id="rrdiagram"></div>
