---
layout: docu
title: List Tables
selected: List Tables
---

# How to list all tables

The `SHOW TABLES` command can be used to obtain a list of all tables:

```sql
SHOW TABLES;
```

To view the schema of an individual table, use the `DESCRIBE` command.

```sql
DESCRIBE nation;
```

The `DESCRIBE` command can also be used without a parameter to view all tables together with their columns and column types.

```sql
DESCRIBE;
```

Below is an example of `DESCRIBE` without any parameters on the `TPC-H` dataset.

```
┌────────────┬────────────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────┬───────────┐
│ table_name │                                    column_names                                    │                                    column_types                                    │ temporary │
├────────────┼────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────┤
│ customer   │ [c_acctbal, c_address, c_comment, c_custkey, c_mktsegment, c_name, c_nationkey,... │ [DECIMAL(15,2), VARCHAR, VARCHAR, INTEGER, VARCHAR, VARCHAR, INTEGER, VARCHAR]     │ false     │
│ lineitem   │ [l_comment, l_commitdate, l_discount, l_extendedprice, l_linenumber, l_linestat... │ [VARCHAR, DATE, DECIMAL(15,2), DECIMAL(15,2), INTEGER, VARCHAR, INTEGER, INTEGE... │ false     │
│ nation     │ [n_comment, n_name, n_nationkey, n_regionkey]                                      │ [VARCHAR, VARCHAR, INTEGER, INTEGER]                                               │ false     │
│ orders     │ [o_clerk, o_comment, o_custkey, o_orderdate, o_orderkey, o_orderpriority, o_ord... │ [VARCHAR, VARCHAR, INTEGER, DATE, INTEGER, VARCHAR, VARCHAR, INTEGER, DECIMAL(1... │ false     │
│ part       │ [p_brand, p_comment, p_container, p_mfgr, p_name, p_partkey, p_retailprice, p_s... │ [VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, INTEGER, DECIMAL(15,2), INTEGER, ... │ false     │
│ partsupp   │ [ps_availqty, ps_comment, ps_partkey, ps_suppkey, ps_supplycost]                   │ [INTEGER, VARCHAR, INTEGER, INTEGER, DECIMAL(15,2)]                                │ false     │
│ region     │ [r_comment, r_name, r_regionkey]                                                   │ [VARCHAR, VARCHAR, INTEGER]                                                        │ false     │
│ supplier   │ [s_acctbal, s_address, s_comment, s_name, s_nationkey, s_phone, s_suppkey]         │ [DECIMAL(15,2), VARCHAR, VARCHAR, VARCHAR, INTEGER, VARCHAR, INTEGER]              │ false     │
└────────────┴────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────┴───────────┘
```

The SQL-standard [`information_schema`](/docs/sql/information_schema) views are also defined. 

DuckDB also defines `sqlite_master`, and many [Postgres system catalog tables](https://www.postgresql.org/docs/14/catalogs.html) for compatibility with SQLite and Postgres respectively.

