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

### Generating Data

To generate data for scale factor 1, use:

```sql
CALL dbgen(sf = 1);
```

### Running a Query

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

| Name        | Type       | Description                                                                                                                       |
| ----------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `catalog`   | `VARCHAR`  | Target catalog                                                                                                                    |
| `children`  | `UINTEGER` | Number of partitions (max. 1000)                                                                                                  |
| `overwrite` | `BOOLEAN`  | (Not used)                                                                                                                        |
| `sf`        | `DOUBLE`   | Scale factor                                                                                                                      |
| `step`      | `UINTEGER` | Defines the partition to be generated, indexed from 0 to `children` - 1. Must be defined when the `children` arguments is defined |
| `suffix`    | `VARCHAR`  | Append the `suffix` to table names                                                                                                |

## Limitations

The `tpch({query_id})` function runs a fixed TPC-H query with pre-defined bind parameters (a.k.a. substitution parameters).
It is not possible to change the query parameters using the `tpch` extension.
