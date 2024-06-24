---
layout: docu
title: "EXPLAIN: Inspect Query Plans"
---

In order to view the query plan of a query, prepend `EXPLAIN` to a query.

```sql
EXPLAIN SELECT * FROM tbl;
```

By default only the final physical plan is shown. In order to see the unoptimized and optimized logical plans, change the `explain_output` setting:

```sql
SET explain_output = 'all';
```

Below is an example of running `EXPLAIN` on [`Q13`](https://github.com/duckdb/duckdb/blob/main/extension/tpch/dbgen/queries/q13.sql) of the [TPC-H benchmark]({% link docs/extensions/tpch.md %}) on the scale factor 1 data set.

```sql
EXPLAIN
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
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│          ORDER_BY         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          ORDERS:          │
│     count_star() DESC     │
│   c_orders.c_count DESC   │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          c_count          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│     count(o_orderkey)     │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
│         count(#1)         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         c_custkey         │
│         o_orderkey        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           RIGHT           │
│   o_custkey = c_custkey   ├──────────────┐
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│         EC: 300000        │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│           FILTER          ││         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  (o_comment !~~ '%special ││          customer         │
│        %requests%')       ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││         c_custkey         │
│         EC: 300000        ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│                           ││         EC: 150000        │
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
└───────────────────────────┘
```

## See Also

For more information, see the [Profiling page]({% link docs/dev/profiling.md %}).
