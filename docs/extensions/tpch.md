---
layout: docu
title: TPC-H Extension
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpch
---

The `tpch` extension implements the data generator and queries for the [TPC-H benchmark](https://www.tpc.org/tpch/).

## Installing and Loading

The `tpch` extension is shipped by default in some DuckDB builds, otherwise it will be transparently autoloaded on first use.
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

## Data Generator Parameters

The data generator function `dbgen` has the following parameters:

<div class="narrow_table"></div>

| Name | Type | Description |
|--|--|------------|
| `catalog`   | `VARCHAR`  | Target catalog                                                                                                                    |
| `children`  | `UINTEGER` | Number of partitions                                                                                                              |
| `overwrite` | `BOOLEAN`  | (Not used)                                                                                                                        |
| `sf`        | `DOUBLE`   | Scale factor                                                                                                                      |
| `step`      | `UINTEGER` | Defines the partition to be generated, indexed from 0 to `children` - 1. Must be defined when the `children` arguments is defined |
| `suffix`    | `VARCHAR`  | Append the `suffix` to table names                                                                                                |

## Generating Larger Than Memory Data Sets

To generate data sets for large scale factors, which yield larger than memory data sets, run the `dbgen` function in steps. For example, you may generate SF300 in 10 steps:

```sql
CALL dbgen(sf = 300, children = 10, step = 0);
CALL dbgen(sf = 300, children = 10, step = 1);
...
CALL dbgen(sf = 300, children = 10, step = 9);
```

## Limitations

* The data generator function `dbgen` is single-threaded and does not support concurrency. Running multiple steps to parallelize over different partitions is also not supported at the moment.
* The `tpch(⟨query_id⟩)` function runs a fixed TPC-H query with pre-defined bind parameters (a.k.a. substitution parameters). It is not possible to change the query parameters using the `tpch` extension.
