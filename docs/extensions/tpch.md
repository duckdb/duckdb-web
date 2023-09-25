---
layout: docu
title: TPC-H Extension
---

The `tpch` extension implements the data generator and queries for the [TPC-H benchmark](https://www.tpc.org/tpch/).

## Installing and Loading

The `tpch` extension is shipped by default in some DuckDB builds, otheriwse it will be transparently autoloaded on first use.
If you would like to install and load it manually, run:

```sql
INSTALL tpch;
LOAD tpch;
```

## Usage

To generate data for scale factor 1, use:

```sql
CALL dbgen(sf=1);
```

To run a query, e.g., query 4, use:

```sql
PRAGMA tpch(4);
```
```text
┌─────────────────┬─────────────┐
│ o_orderpriority │ order_count │
│     varchar     │    int64    │
├─────────────────┼─────────────┤
│ 1-URGENT        │       21188 │
│ 2-HIGH          │       20952 │
│ 3-MEDIUM        │       20820 │
│ 4-NOT SPECIFIED │       21112 │
│ 5-LOW           │       20974 │
└─────────────────┴─────────────┘
```
