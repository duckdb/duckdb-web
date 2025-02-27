---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpch
layout: docu
title: TPC-H Extension
---

The `tpch` extension implements the data generator and queries for the [TPC-H benchmark](https://www.tpc.org/tpch/).

## Installing and Loading

The `tpch` extension is shipped by default in some DuckDB builds, otherwise it will be transparently [autoloaded]({% link docs/1.1/extensions/overview.md %}#autoloading-extensions) on first use.
If you would like to install and load it manually, run:

```sql
INSTALL tpch;
LOAD tpch;
```

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
|-----------------|------------:|
| 1-URGENT        | 10594       |
| 2-HIGH          | 10476       |
| 3-MEDIUM        | 10410       |
| 4-NOT SPECIFIED | 10556       |
| 5-LOW           | 10487       |

### Listing Queries

To list all 22 queries, run:

```sql
FROM tpch_queries();
```

This function returns a table with columns `query_nr` and `query`.

### Listing Expected Answers

To produced the expected results for all queries on scale factors 0.01, 0.1, and 1, run:

```sql
FROM tpch_answers();
```

This function returns a table with columns `query_nr`, `scale_factor`, and `answer`.

## Generating the Schema

It's possible to generate the schema of TPC-H without any data by setting the scale factor to 0:

```sql
CALL dbgen(sf = 0);
```

## Data Generator Parameters

The data generator function `dbgen` has the following parameters:

| Name | Type | Description |
|--|--|------------|
| `catalog`   | `VARCHAR`  | Target catalog                                                                                                                    |
| `children`  | `UINTEGER` | Number of partitions                                                                                                              |
| `overwrite` | `BOOLEAN`  | (Not used)                                                                                                                        |
| `sf`        | `DOUBLE`   | Scale factor                                                                                                                      |
| `step`      | `UINTEGER` | Defines the partition to be generated, indexed from 0 to `children` - 1. Must be defined when the `children` arguments is defined |
| `suffix`    | `VARCHAR`  | Append the `suffix` to table names                                                                                                |

## Pre-Generated Data Sets

Pre-generated DuckDB databases for TPC-H are available for download:

* [`tpch-sf1.db`](https://blobs.duckdb.org/data/tpch-sf1.db) (250 MB)
* [`tpch-sf3.db`](https://blobs.duckdb.org/data/tpch-sf3.db) (754 MB)
* [`tpch-sf10.db`](https://blobs.duckdb.org/data/tpch-sf10.db) (2.5 GB)
* [`tpch-sf30.db`](https://blobs.duckdb.org/data/tpch-sf30.db) (7.6 GB)
* [`tpch-sf100.db`](https://blobs.duckdb.org/data/tpch-sf100.db) (26 GB)
* [`tpch-sf300.db`](https://blobs.duckdb.org/data/tpch-sf300.db) (78 GB)
* [`tpch-sf1000.db`](https://blobs.duckdb.org/data/tpch-sf1000.db) (265 GB)
* [`tpch-sf3000.db`](https://blobs.duckdb.org/data/tpch-sf3000.db) (796 GB)

## Resource Usage of the Data Generator

Generating TPC-H data sets for large scale factors takes a significant amount of time.
Additionally, when the generation is done in a single step, it requires a large amount of memory.
The following table gives an estimate on the resources required to produce DuckDB database files containing the generated TPC-H data set using 128 threads.

| Scale factor | Database size | Data generation time | Generator's memory usage |
|-------------:|--------------:|---------------------:|-------------------------:|
|          100 |         26 GB | 17 minutes           |                    71 GB |
|          300 |         78 GB | 51 minutes           |                   211 GB |
|         1000 |        265 GB | 2h 53 minutes        |                   647 GB |
|         3000 |        796 GB | 8h 30 minutes        |                  1799 GB |

The numbers shown above were achieved by running the `dbgen` function in a single step, for example:

```sql
CALL dbgen(sf = 300);
```

If you have a limited amount of memory available, you can run the `dbgen` function in steps.
For example, you may generate SF300 in 10 steps:

```sql
CALL dbgen(sf = 300, children = 10, step = 0);
CALL dbgen(sf = 300, children = 10, step = 1);
...
CALL dbgen(sf = 300, children = 10, step = 9);
```

## Limitation

The `tpch(⟨query_id⟩)` function runs a fixed TPC-H query with pre-defined bind parameters (a.k.a. substitution parameters). It is not possible to change the query parameters using the `tpch` extension. To run the queries with the parameters prescribed by the TPC-H benchmark, use a TPC-H framework implementation.