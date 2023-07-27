---
layout: docu
title: Explain
selected: Explain
---

# How to view the query plan of a query

In order to view the query plan of a query, prepend `EXPLAIN` to a query.

```sql
EXPLAIN SELECT * FROM tbl;
```

By default only the final physical plan is shown. In order to see the unoptimized and optimized logical plans, change the `explain_output` setting:

```sql
SET explain_output='all'; 
```

Below is an example of running `EXPLAIN` on `Q1` of the TPC-H benchmark.

```
┌───────────────────────────┐
│          ORDER_BY         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│ lineitem.l_returnflag ASC │
│ lineitem.l_linestatus ASC │
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
└───────────────────────────┘    
```
