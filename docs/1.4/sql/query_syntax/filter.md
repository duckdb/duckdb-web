---
layout: docu
railroad: query_syntax/filter.js
title: FILTER Clause
---

The `FILTER` clause may optionally follow an aggregate function in a `SELECT` statement. This will filter the rows of data that are fed into the aggregate function in the same way that a `WHERE` clause filters rows, but localized to the specific aggregate function.

There are multiple types of situations where this is useful, including when evaluating multiple aggregates with different filters, and when creating a pivoted view of a dataset. `FILTER` provides a cleaner syntax for pivoting data when compared with the more traditional `CASE WHEN` approach discussed below.

Some aggregate functions also do not filter out `NULL` values, so using a `FILTER` clause will return valid results when at times the `CASE WHEN` approach will not. This occurs with the functions `first` and `last`, which are desirable in a non-aggregating pivot operation where the goal is to simply re-orient the data into columns rather than re-aggregate it. For `list` and `array_agg`, `FILTER` excludes rows that do not satisfy its condition, whereas a `CASE WHEN` expression can contribute `NULL` placeholders for those rows. However, `FILTER` does **not** automatically remove `NULL` values from rows that do satisfy the condition. To omit them, include an explicit condition on the aggregated value, such as `list(x) FILTER (WHERE x IS NOT NULL)`.

## Examples

### Filtering `NULL` Values from Lists

A `FILTER` condition acts on rows, not on the values stored in the resulting list. Here the first expression keeps the `NULL` value because `y` is `true` for that row, while the second explicitly excludes null values from `x`:

```sql
SELECT
    list(x) FILTER (WHERE y) AS selected_rows,
    list(x) FILTER (WHERE x IS NOT NULL) AS non_null_values
FROM (VALUES (NULL::INTEGER, true), (2, true), (1, false)) t(x, y);
```

The results are `[NULL, 2]` for `selected_rows` and `[2, 1]` for `non_null_values`.

Return the following:

* The total number of rows
* The number of rows where `i <= 5`
* The number of rows where `i` is odd

```sql
SELECT
    count() AS total_rows,
    count() FILTER (i <= 5) AS lte_five,
    count() FILTER (i % 2 = 1) AS odds
FROM generate_series(1, 10) tbl(i);
```

<div class="monospace_table"></div>

| total_rows | lte_five | odds |
|:---|:---|:---|
| 10 | 5 | 5 |

> Simply counting rows that satisfy a condition can also be achieved without `FILTER` clause, using the boolean `sum` aggregate function, e.g., `sum(i <= 5)`.

Different aggregate functions may be used, and multiple `WHERE` expressions are also permitted:

```sql
SELECT
    sum(i) FILTER (i <= 5) AS lte_five_sum,
    median(i) FILTER (i % 2 = 1) AS odds_median,
    median(i) FILTER (i % 2 = 1 AND i <= 5) AS odds_lte_five_median
FROM generate_series(1, 10) tbl(i);
```

<div class="monospace_table"></div>

| lte_five_sum | odds_median | odds_lte_five_median |
|:---|:---|:---|
| 15 | 5.0 | 3.0 |

The `FILTER` clause can also be used to pivot data from rows into columns. This is a static pivot, as columns must be defined prior to runtime in SQL. However, this kind of statement can be dynamically generated in a host programming language to leverage DuckDB's SQL engine for rapid, larger than memory pivoting.

First generate an example dataset:

```sql
CREATE TEMP TABLE stacked_data AS
    SELECT
        i,
        CASE WHEN i <= rows * 0.25  THEN 2022
             WHEN i <= rows * 0.5   THEN 2023
             WHEN i <= rows * 0.75  THEN 2024
             WHEN i <= rows * 0.875 THEN 2025
             ELSE NULL
             END AS year
    FROM (
        SELECT
            i,
            count(*) OVER () AS rows
        FROM generate_series(1, 100_000_000) tbl(i)
    ) tbl;
```

“Pivot” the data out by year (move each year out to a separate column):

```sql
SELECT
    count(i) FILTER (year = 2022) AS "2022",
    count(i) FILTER (year = 2023) AS "2023",
    count(i) FILTER (year = 2024) AS "2024",
    count(i) FILTER (year = 2025) AS "2025",
    count(i) FILTER (year IS NULL) AS "NULLs"
FROM stacked_data;
```

This syntax produces the same results as the `FILTER` clauses above:

```sql
SELECT
    count(CASE WHEN year = 2022 THEN i END) AS "2022",
    count(CASE WHEN year = 2023 THEN i END) AS "2023",
    count(CASE WHEN year = 2024 THEN i END) AS "2024",
    count(CASE WHEN year = 2025 THEN i END) AS "2025",
    count(CASE WHEN year IS NULL THEN i END) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 25000000 | 25000000 | 25000000 | 12500000 | 12500000 |

However, the `CASE WHEN` approach will not work as expected when using an aggregate function that does not ignore `NULL` values. The `first` function falls into this category, so `FILTER` is preferred in this case.

“Pivot” the data out by year (move each year out to a separate column):

```sql
SELECT
    first(i) FILTER (year = 2022) AS "2022",
    first(i) FILTER (year = 2023) AS "2023",
    first(i) FILTER (year = 2024) AS "2024",
    first(i) FILTER (year = 2025) AS "2025",
    first(i) FILTER (year IS NULL) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1474561 | 25804801 | 50749441 | 76431361 | 87500001 |

This will produce `NULL` values whenever the first evaluation of the `CASE WHEN` clause returns a `NULL`:

```sql
SELECT
    first(CASE WHEN year = 2022 THEN i END) AS "2022",
    first(CASE WHEN year = 2023 THEN i END) AS "2023",
    first(CASE WHEN year = 2024 THEN i END) AS "2024",
    first(CASE WHEN year = 2025 THEN i END) AS "2025",
    first(CASE WHEN year IS NULL THEN i END) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1228801 | NULL | NULL | NULL | NULL  |

## Aggregate Function Syntax (Including `FILTER` Clause)

<div id="rrdiagram"></div>
