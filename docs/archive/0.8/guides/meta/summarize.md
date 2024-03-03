---
layout: docu
title: Summarize
selected: Summarize
---

# How to quickly get a feel for a dataset using summarize

The `SUMMARIZE` command can be used to easily compute a number of aggregates over a table or a query. The `SUMMARIZE` command launches a query that computes a number of aggregates over all columns, including `min`, `max`, `avg`, `std` and `approx_count_distinct`.

In order to summarize the contents of a table, use `SUMMARIZE` followed by the table name.

```sql
SUMMARIZE tbl;
```

In order to summarize a query, prepend `SUMMARIZE` to a query. 

```sql
SUMMARIZE SELECT * FROM tbl;
```

Below is an example of `SUMMARIZE` on the `lineitem` table of TPC-H `SF1`.

```
┌─────────────────┬───────────────┬─────────────┬─────────────────────────────────────────────┬───────────────┬─────────────────────┬──────────────────────┬─────────┬─────────┬─────────┬─────────┬─────────────────┐
│   column_name   │  column_type  │     min     │                     max                     │ approx_unique │         avg         │         std          │   q25   │   q50   │   q75   │  count  │ null_percentage │
├─────────────────┼───────────────┼─────────────┼─────────────────────────────────────────────┼───────────────┼─────────────────────┼──────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
│ l_orderkey      │ INTEGER       │ 1           │ 6000000                                     │ 1486805       │ 3000279.604204982   │ 1732187.8734803426   │ 1497471 │ 3022276 │ 4523225 │ 6001215 │ 0.0%            │
│ l_partkey       │ INTEGER       │ 1           │ 200000                                      │ 196125        │ 100017.98932999402  │ 57735.69082650517    │ 50056   │ 99973   │ 150007  │ 6001215 │ 0.0%            │
│ l_suppkey       │ INTEGER       │ 1           │ 10000                                       │ 10010         │ 5000.602606138924   │ 2886.9619987306205   │ 2499    │ 5001    │ 7498    │ 6001215 │ 0.0%            │
│ l_linenumber    │ INTEGER       │ 1           │ 7                                           │ 7             │ 3.0005757167506912  │ 1.7324314036519335   │ 1       │ 3       │ 4       │ 6001215 │ 0.0%            │
│ l_quantity      │ INTEGER       │ 1           │ 50                                          │ 50            │ 25.507967136654827  │ 14.426262537016953   │ 12      │ 25      │ 37      │ 6001215 │ 0.0%            │
│ l_extendedprice │ DECIMAL(15,2) │ 901.00      │ 104949.50                                   │ 939196        │ 38255.138484656854  │ 23300.438710962204   │ 18747   │ 36719   │ 55141   │ 6001215 │ 0.0%            │
│ l_discount      │ DECIMAL(15,2) │ 0.00        │ 0.10                                        │ 11            │ 0.04999943011540163 │ 0.031619855108125976 │ 0       │ 0       │ 0       │ 6001215 │ 0.0%            │
│ l_tax           │ DECIMAL(15,2) │ 0.00        │ 0.08                                        │ 9             │ 0.04001350893110812 │ 0.02581655179884275  │ 0       │ 0       │ 0       │ 6001215 │ 0.0%            │
│ l_returnflag    │ VARCHAR       │ A           │ R                                           │ 3             │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_linestatus    │ VARCHAR       │ F           │ O                                           │ 2             │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_shipdate      │ DATE          │ 1992-01-02  │ 1998-12-01                                  │ 2554          │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_commitdate    │ DATE          │ 1992-01-31  │ 1998-10-31                                  │ 2491          │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_receiptdate   │ DATE          │ 1992-01-04  │ 1998-12-31                                  │ 2585          │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_shipinstruct  │ VARCHAR       │ COLLECT COD │ TAKE BACK RETURN                            │ 4             │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_shipmode      │ VARCHAR       │ AIR         │ TRUCK                                       │ 7             │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
│ l_comment       │ VARCHAR       │  Tiresias   │ zzle? slyly final platelets sleep quickly.  │ 4587836       │ NULL                │ NULL                 │ NULL    │ NULL    │ NULL    │ 6001215 │ 0.0%            │
└─────────────────┴───────────────┴─────────────┴─────────────────────────────────────────────┴───────────────┴─────────────────────┴──────────────────────┴─────────┴─────────┴─────────┴─────────┴─────────────────┘
```