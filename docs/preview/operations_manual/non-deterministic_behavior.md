---
layout: docu
title: Non-Deterministic Behavior
---

Several operators in DuckDB exhibit non-deterministic behavior.
Most notably, SQL uses set semantics, which allows results to be returned in a different order.
DuckDB exploits this to improve performance, particularly when performing multi-threaded query execution.
Other factors, such as using different compilers, operating systems and hardware architectures, can also cause changes in ordering.
This page documents the cases where non-determinism is an _expected behavior_.
If you would like to make your queries deterministic, see the [“Working Around Non-Determinism” section](#working-around-non-determinism).

## Set Semantics

One of the most common sources of non-determinism is the set semantics used by SQL.
E.g., if you run the following query repeatedly, you may get two different results:

```sql
SELECT *
FROM (
    SELECT 'A' AS x
    UNION
    SELECT 'B' AS x
);
```

Both results `A`, `B` and `B`, `A` are correct.

## Different Results on Different Platforms: `array_distinct`

The `array_distinct` function may return results [in a different order on different platforms](https://github.com/duckdb/duckdb/issues/13746):

```sql
SELECT array_distinct(['A', 'A', 'B', NULL, NULL]) AS arr;
```

For this query, both `[A, B]` and `[B, A]` are valid results.

## Floating-Point Aggregate Operations with Multi-Threading

Floating-point inaccuracies may produce different results when run in multi-threaded configurations:
For example, [`stddev` and `corr` may produce non-deterministic results](https://github.com/duckdb/duckdb/issues/13763):

```sql
CREATE TABLE tbl AS
    SELECT 'ABCDEFG'[floor(random() * 7 + 1)::INT] AS s, 3.7 AS x, i AS y
    FROM range(1, 1_000_000) r(i);

SELECT s, stddev(x) AS standard_deviation, corr(x, y) AS correlation
FROM tbl
GROUP BY s
ORDER BY s;
```

The expected standard deviations and correlations from this query are 0 for all values of `s`.
However, when executed on multiple threads, the query may return small numbers (`0 <= z < 10e-16`) due to floating-point inaccuracies.

## Working Around Non-Determinism

For the majority of use cases, non-determinism is not causing any issues.
However, there are some cases where deterministic results are desirable.
In these cases, try the following workarounds:

1. Limit the number of threads to prevent non-determinism introduced by multi-threading.

   ```sql
   SET threads = 1;
   ```

2. Enforce ordering. For example, you can use the [`ORDER BY ALL` clause]({% link docs/preview/sql/query_syntax/orderby.md %}#order-by-all):

   ```sql
   SELECT *
   FROM (
       SELECT 'A' AS x
       UNION
       SELECT 'B' AS x
   )
   ORDER BY ALL;
   ```

   You can also sort lists using [`list_sort`]({% link docs/preview/sql/functions/list.md %}#list_sortlist):

   ```sql
   SELECT list_sort(array_distinct(['A', 'A', 'B', NULL, NULL])) AS i
   ORDER BY i;
   ```

   It's also possible to introduce a [deterministic shuffling]({% post_url 2024-08-19-duckdb-tricks-part-1 %}#shuffling-data).
