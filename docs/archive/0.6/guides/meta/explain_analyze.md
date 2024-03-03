---
layout: docu
title: Profile Queries
selected: Profile Queries
---

In order to profile a query, prepend `EXPLAIN ANALYZE` to a query.

```sql
EXPLAIN ANALYZE SELECT * FROM tbl;
```

The query plan will be pretty-printed to the screen using timings for every operator.

Note that the **cumulative** wall-clock time that is spent on every operator is shown. When multiple threads are processing the query in parallel, the total processing time of the query may be lower than the sum of all the times spent on the individual operators.

Below is an example of running `EXPLAIN ANALYZE` on `Q1` of the TPC-H benchmark.


```
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││        Total Time: 0.0496s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│      EXPLAIN_ANALYZE      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│          ORDER_BY         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│ lineitem.l_returnflag ASC │
│ lineitem.l_linestatus ASC │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             4             │
│          (0.00s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
│             #1            │
│          sum(#2)          │
│          sum(#3)          │
│          sum(#4)          │
│          sum(#5)          │
│          avg(#6)          │
│          avg(#7)          │
│          avg(#8)          │
│        count_star()       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             4             │
│          (0.28s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│        l_returnflag       │
│        l_linestatus       │
│         l_quantity        │
│      l_extendedprice      │
│             #4            │
│   (#4 * (1.00 + l_tax))   │
│         l_quantity        │
│      l_extendedprice      │
│         l_discount        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          5916591          │
│          (0.02s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│        l_returnflag       │
│        l_linestatus       │
│         l_quantity        │
│      l_extendedprice      │
│ (l_extendedprice * (1.00 -│
│        l_discount))       │
│           l_tax           │
│         l_discount        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          5916591          │
│          (0.02s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│          SEQ_SCAN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          lineitem         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│         l_shipdate        │
│        l_returnflag       │
│        l_linestatus       │
│         l_quantity        │
│      l_extendedprice      │
│         l_discount        │
│           l_tax           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│ Filters: l_shipdate<=1998 │
│-09-02 AND l_shipdate ...  │
│            NULL           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          5916591          │
│          (0.08s)          │
└───────────────────────────┘   
```