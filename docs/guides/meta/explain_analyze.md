---
layout: docu
title: "EXPLAIN ANALYZE: Profile Queries"
---

In order to profile a query, prepend `EXPLAIN ANALYZE` to a query.

```sql
EXPLAIN ANALYZE SELECT * FROM tbl;
```

The query plan will be pretty-printed to the screen using timings for every operator.

Note that the **cumulative** wall-clock time that is spent on every operator is shown. When multiple threads are processing the query in parallel, the total processing time of the query may be lower than the sum of all the times spent on the individual operators.

Below is an example of running `EXPLAIN ANALYZE` on [`Q13`](https://github.com/duckdb/duckdb/blob/main/extension/tpch/dbgen/queries/q13.sql) of the [TPC-H benchmark]({% link docs/extensions/tpch.md %}) on the scale factor 1 data set.

```sql
EXPLAIN ANALYZE
    SELECT
        c_count,
        count(*) AS custdist
    FROM (
            SELECT
                c_custkey,
                count(o_orderkey)
            FROM
                customer
            LEFT OUTER JOIN orders ON c_custkey = o_custkey
            AND o_comment NOT LIKE '%special%requests%'
            GROUP BY c_custkey
        ) AS c_orders (c_custkey, c_count)
    GROUP BY
        c_count
    ORDER BY
        custdist DESC,
        c_count DESC;
```

```text
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││        Total Time: 0.0487s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│      RESULT_COLLECTOR     │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      EXPLAIN_ANALYZE      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          ORDER_BY         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          ORDERS:          │
│     count_star() DESC     │
│   c_orders.c_count DESC   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             42            │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
│        count_star()       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             42            │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          c_count          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           150000          │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│     count(o_orderkey)     │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           150000          │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
│         count(#1)         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           150000          │
│          (0.09s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         c_custkey         │
│         o_orderkey        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          1534302          │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           RIGHT           │
│   o_custkey = c_custkey   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ├──────────────┐
│         EC: 300000        │              │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│          1534302          │              │
│          (0.08s)          │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│           FILTER          ││         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  (o_comment !~~ '%special ││          customer         │
│        %requests%')       ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││         c_custkey         │
│         EC: 300000        ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││         EC: 150000        │
│          1484298          ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          (0.10s)          ││           150000          │
│                           ││          (0.00s)          │
└─────────────┬─────────────┘└───────────────────────────┘
┌─────────────┴─────────────┐
│         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           orders          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         o_custkey         │
│         o_comment         │
│         o_orderkey        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│        EC: 1500000        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          1500000          │
│          (0.01s)          │
└───────────────────────────┘
```

## See Also

For more information, see the [Profiling page]({% link docs/dev/profiling.md %}).
