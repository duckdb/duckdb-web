---
layout: docu
title: TPC-DS Extension
---

The `tpcds` extension implements the data generator and queries for the [TPC-DS benchmark](https://www.tpc.org/tpcds/).

## Installing and Loading

The `tpcds` extension will be transparently autoloaded on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL tpcds;
LOAD tpcds;
```

## Usage

To generate data for scale factor 1, use:

```sql
CALL dsdgen(sf = 1);
```

To run a query, e.g., query 8, use:

```sql
PRAGMA tpcds(8);
```
```text
┌──────────────┬────────────────────┐
│ s_store_name │ sum(ss_net_profit) │
│   varchar    │   decimal(38,2)    │
├──────────────┼────────────────────┤
│ able         │       -10354620.18 │
│ ation        │       -10576395.52 │
│ bar          │       -10625236.01 │
│ ese          │       -10076698.16 │
│ ought        │       -10994052.78 │
└──────────────┴────────────────────┘
```

## Limitations

The `tpchds({query_id})` function runs a fixed TPC-DS query with pre-defined bind parameters (a.k.a. substitution parameters).
It is not possible to change the query parameters using the `tpcds` extension.

## GitHub

The `tpcds` extension is part of the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/extension/tpcds).
