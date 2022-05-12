---
layout: docu
title: Describe
selected: Describe
---

# How to view the schema of the result of a query

In order to view the schema of the result of a query, prepend `DESCRIBE` to a query.

```sql
DESCRIBE SELECT * FROM tbl;
```

In order to view the schema of a table, use `DESCRIBE` followed by the table name.

```sql
DESCRIBE tbl;
```

Below is an example of `DESCRIBE` on the `lineitem` table of TPC-H.

```
┌─────────────────┬───────────────┬──────┬──────┬─────────┬───────┐
│   column_name   │  column_type  │ null │ key  │ default │ extra │
├─────────────────┼───────────────┼──────┼──────┼─────────┼───────┤
│ l_orderkey      │ INTEGER       │ NO   │ NULL │ NULL    │ NULL  │
│ l_partkey       │ INTEGER       │ NO   │ NULL │ NULL    │ NULL  │
│ l_suppkey       │ INTEGER       │ NO   │ NULL │ NULL    │ NULL  │
│ l_linenumber    │ INTEGER       │ NO   │ NULL │ NULL    │ NULL  │
│ l_quantity      │ INTEGER       │ NO   │ NULL │ NULL    │ NULL  │
│ l_extendedprice │ DECIMAL(15,2) │ NO   │ NULL │ NULL    │ NULL  │
│ l_discount      │ DECIMAL(15,2) │ NO   │ NULL │ NULL    │ NULL  │
│ l_tax           │ DECIMAL(15,2) │ NO   │ NULL │ NULL    │ NULL  │
│ l_returnflag    │ VARCHAR       │ NO   │ NULL │ NULL    │ NULL  │
│ l_linestatus    │ VARCHAR       │ NO   │ NULL │ NULL    │ NULL  │
│ l_shipdate      │ DATE          │ NO   │ NULL │ NULL    │ NULL  │
│ l_commitdate    │ DATE          │ NO   │ NULL │ NULL    │ NULL  │
│ l_receiptdate   │ DATE          │ NO   │ NULL │ NULL    │ NULL  │
│ l_shipinstruct  │ VARCHAR       │ NO   │ NULL │ NULL    │ NULL  │
│ l_shipmode      │ VARCHAR       │ NO   │ NULL │ NULL    │ NULL  │
│ l_comment       │ VARCHAR       │ NO   │ NULL │ NULL    │ NULL  │
└─────────────────┴───────────────┴──────┴──────┴─────────┴───────┘
```
