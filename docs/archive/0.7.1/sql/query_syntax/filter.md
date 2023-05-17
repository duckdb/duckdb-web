---
layout: docu
title: FILTER Clause
selected: Documentation/SQL/Query Syntax/Filter
expanded: SQL
railroad: query_syntax/filter.js
---
The `FILTER` clause may optionally follow an aggregate function in a `SELECT` statement. This will filter the rows of data that are fed into the aggregate function in the same way that a `WHERE` clause filters rows, but localized to the specific aggregate function. `FILTER`s are not currently able to be used when the aggregate function is in a windowing context. 

There are multiple types of situations where this is useful, including when evaluating multiple aggregates with different filters, and when creating a pivoted view of a dataset. `FILTER` provides a cleaner syntax for pivoting data when compared with the more traditional `CASE WHEN` approach discussed below. 

Some aggregate functions also do not filter out null values, so using a `FILTER` clause will return valid results when at times the `CASE WHEN` approach will not. This occurs with the functions `FIRST` and `LAST`, which are desirable in a non-aggregating pivot operation where the goal is to simply re-orient the data into columns rather than re-aggregate it. `FILTER` also improves null handling when using the `LIST` and `ARRAY_AGG` functions, as the `CASE WHEN` approach will include null values in the list result, while the `FILTER` clause will remove them.

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
-- Different aggregate functions may be used, and multiple WHERE expressions are also permitted
--   The sum of i for rows where i <= 5 
--   The median of i where i is odd 
SELECT 
    sum(i) FILTER (WHERE i <= 5) as lte_five_sum,
    median(i) FILTER (WHERE i % 2 = 1) as odds_median,
    median(i) FILTER (WHERE i % 2 = 1 AND i <= 5) as odds_lte_five_median
FROM generate_series(1,10) tbl(i);
```

| lte_five_sum | odds_median | odds_lte_five_median |
|:---|:---|:---|
| 15 | 5.0 | 3.0 |


The `FILTER` clause can also be used to pivot data from rows into columns. This is a static pivot, as columns must be defined prior to runtime in SQL. However, this kind of statement can be dynamically generated in a host programming language to leverage DuckDB's SQL engine for rapid, larger than memory pivoting.
```sql
--First generate an example dataset
CREATE TEMP TABLE stacked_data as 
    SELECT 
        i,
        CASE WHEN i <= rows * 0.25 THEN 2022 
             WHEN i <= rows * 0.5 THEN 2023 
             WHEN i <= rows * 0.75 THEN 2024 
             WHEN i <= rows * 0.875 THEN 2025
             ELSE NULL 
             END as year 
    FROM (
        SELECT 
            i, 
            count(*) over () as rows 
        FROM generate_series(1,100000000) tbl(i)
    ) tbl;

--"Pivot" the data out by year (move each year out to a separate column)
SELECT
    count(i) FILTER (WHERE year = 2022) as "2022",
    count(i) FILTER (WHERE year = 2023) as "2023",
    count(i) FILTER (WHERE year = 2024) as "2024",
    count(i) FILTER (WHERE year = 2025) as "2025",
    count(i) FILTER (WHERE year IS NULL) as "NULLs"
FROM stacked_data;

--This syntax produces the same results as the the FILTER clauses above
SELECT
    count(CASE WHEN year = 2022 THEN i END) as "2022",
    count(CASE WHEN year = 2023 THEN i END) as "2023",
    count(CASE WHEN year = 2024 THEN i END) as "2024",
    count(CASE WHEN year = 2025 THEN i END) as "2025",
    count(CASE WHEN year IS NULL THEN i END) as "NULLs"
FROM stacked_data;
```

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 25000000 | 25000000 | 25000000 | 12500000 | 12500000 |

However, the `CASE WHEN` approach will not work as expected when using an aggregate function that does not ignore `NULL` values. The `FIRST` function falls into this category, so `FILTER` is preferred in this case.

```sql
--"Pivot" the data out by year (move each year out to a separate column)
SELECT
    first(i) FILTER (WHERE year = 2022) as "2022",
    first(i) FILTER (WHERE year = 2023) as "2023",
    first(i) FILTER (WHERE year = 2024) as "2024",
    first(i) FILTER (WHERE year = 2025) as "2025",
    first(i) FILTER (WHERE year IS NULL) as "NULLs"
FROM stacked_data;
```

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1474561 | 25804801 | 50749441 | 76431361 | 87500001 |

```sql
--This will produce NULL values whenever the first evaluation of the CASE WHEN clause returns a NULL
SELECT
    first(CASE WHEN year = 2022 THEN i END) as "2022",
    first(CASE WHEN year = 2023 THEN i END) as "2023",
    first(CASE WHEN year = 2024 THEN i END) as "2024",
    first(CASE WHEN year = 2025 THEN i END) as "2025",
    first(CASE WHEN year IS NULL THEN i END) as "NULLs"
FROM stacked_data;
```

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1228801 | NULL | NULL | NULL | NULL  |

## Aggregate Function Syntax (Including Filter Clause)
<div id="rrdiagram"></div>
