---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpcds
layout: docu
redirect_from:
- /docs/extensions/tpcds
- /docs/lts/extensions/tpcds
- /docs/preview/core_extensions/tpcds
- /docs/stable/core_extensions/tpcds
title: TPC-DS Extension
---

The `tpcds` extension implements the data generator and queries for the [TPC-DS benchmark](https://www.tpc.org/tpcds/).

## Installing and Loading

The `tpcds` extension will be transparently [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
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

| s_store_name | sum(ss_net_profit) |
|--------------|-------------------:|
| able         | -10354620.18       |
| ation        | -10576395.52       |
| bar          | -10625236.01       |
| ese          | -10076698.16       |
| ought        | -10994052.78       |

## Generating the Schema

It's possible to generate the schema of TPC-DS without any data by setting the scale factor to 0:

```sql
CALL dsdgen(sf = 0);
```

## Pre-Generated Datasets

Pre-generated DuckDB databases for TPC-DS are available for download:

* [`tpcds-sf10.db`](https://blobs.duckdb.org/data/tpcds-sf10.db) (2.9 GB)
* [`tpcds-sf30.db`](https://blobs.duckdb.org/data/tpcds-sf30.db) (7.7 GB)
* [`tpcds-sf100.db`](https://blobs.duckdb.org/data/tpcds-sf100.db) (26.6 GB)
* [`tpcds-sf300.db`](https://blobs.duckdb.org/data/tpcds-sf300.db) (79.3 GB)

## Limitations

The `tpcds(⟨query_id⟩)`{:.language-sql .highlight} function runs a fixed TPC-DS query with pre-defined bind parameters (a.k.a. substitution parameters).
It is not possible to change the query parameters using the `tpcds` extension.
