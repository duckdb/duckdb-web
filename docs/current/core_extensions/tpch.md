---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpch
layout: docu
redirect_from:
- /docs/extensions/tpch
- /docs/stable/extensions/tpch
- /docs/preview/core_extensions/tpch
- /docs/stable/core_extensions/tpch
title: TPC-H Extension
---

The `tpch` extension implements the data generator and queries for the [TPC-H benchmark](https://www.tpc.org/tpch/).

## Installing and Loading

The `tpch` extension is shipped by default in some DuckDB builds, otherwise it will be transparently [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extensions) on first use.
If you would like to install and load it manually, run:

```sql
INSTALL tpch;
LOAD tpch;
```

## Benchmarking with the TPC-H Workload

To run the full TPC-H workload with DuckDB, use the [standalone DuckDB TPC-H implementation project](https://github.com/duckdb/duckdb-tpch-power-test).

## Usage

### Generating Data

To generate data for scale factor 1, use:

```sql
CALL dbgen(sf = 1);
```

Calling `dbgen` does not clean up existing TPC-H tables.
To clean up existing tables, use `DROP TABLE` before running `dbgen`:

```sql
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS lineitem;
DROP TABLE IF EXISTS nation;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS partsupp;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS supplier;
```

### Running a Query

To run a query, e.g., query 4, use:

```sql
PRAGMA tpch(4);
```

| o_orderpriority | order_count |
| --------------- | ----------: |
| 1-URGENT        |       10594 |
| 2-HIGH          |       10476 |
| 3-MEDIUM        |       10410 |
| 4-NOT SPECIFIED |       10556 |
| 5-LOW           |       10487 |

### Listing Queries

To list all 22 queries, run:

```sql
FROM tpch_queries();
```

This function returns a table with columns `query_nr` and `query`.

### Listing Expected Answers

To produce the expected results for all queries on scale factors 0.01, 0.1 and 1, run:

```sql
FROM tpch_answers();
```

This function returns a table with columns `query_nr`, `scale_factor` and `answer`.

## Generating the Schema

It's possible to generate the schema of TPC-H without any data by setting the scale factor to 0:

```sql
CALL dbgen(sf = 0);
```

## Data Generator Parameters

The data generator function `dbgen` has the following parameters:

| Name        | Type       | Description                                                                                                                       |
| ----------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `catalog`   | `VARCHAR`  | Target catalog                                                                                                                    |
| `children`  | `UINTEGER` | Number of partitions                                                                                                              |
| `overwrite` | `BOOLEAN`  | (Not used)                                                                                                                        |
| `sf`        | `DOUBLE`   | Scale factor                                                                                                                      |
| `step`      | `UINTEGER` | Defines the partition to be generated, indexed from 0 to `children` - 1. Must be defined when the `children` arguments is defined |
| `suffix`    | `VARCHAR`  | Append the `suffix` to table names                                                                                                |

## Pre-Generated Datasets

Pre-generated DuckDB databases for TPC-H are available for download:

* [`tpch-sf1.db`](https://blobs.duckdb.org/data/tpch-sf1.db) (250 MB)
* [`tpch-sf3.db`](https://blobs.duckdb.org/data/tpch-sf3.db) (754 MB)
* [`tpch-sf10.db`](https://blobs.duckdb.org/data/tpch-sf10.db) (2.5 GB)
* [`tpch-sf30.db`](https://blobs.duckdb.org/data/tpch-sf30.db) (7.6 GB)
* [`tpch-sf100.db`](https://blobs.duckdb.org/data/tpch-sf100.db) (26 GB)
* [`tpch-sf300.db`](https://blobs.duckdb.org/data/tpch-sf300.db) (78 GB)
* [`tpch-sf1000.db`](https://blobs.duckdb.org/data/tpch-sf1000.db) (265 GB)
* [`tpch-sf3000.db`](https://blobs.duckdb.org/data/tpch-sf3000.db) (796 GB)

## Limitation

The `tpch(⟨query_id⟩)`{:.language-sql .highlight} function runs a fixed TPC-H query with pre-defined bind parameters (a.k.a. substitution parameters). It is not possible to change the query parameters using the `tpch` extension. To run the queries with the parameters prescribed by the TPC-H benchmark, use a TPC-H framework implementation.
