---
layout: docu
title: Benchmarks
---

For several of the recommendations in our performance guide, we use microbenchmarks to back up our claims. For these benchmarks, we use data sets from the [TPC-H benchmark]({% link docs/archive/1.1/extensions/tpch.md %}) and the [LDBC Social Network Benchmark’s BI workload](https://github.com/ldbc/ldbc_snb_bi/blob/main/snb-bi-pre-generated-data-sets.md#compressed-csvs-in-the-composite-merged-fk-format).

<!--
## Benchmark Environment

The benchmarks in the performance guide executed on a 2022 MacBook Pro with a 12-core M2 Pro CPU, 32 GiB RAM and 1 TB disk.
-->

## Data Sets

We use the [LDBC BI SF300 data set's Comment table](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) (20 GB `.tar.zst` archive, 21 GB when decompressed into `.csv.gz` files),
while others use the same table's [`creationDate` column](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) (4 GB `.parquet` file).

The TPC data sets used in the benchmark are generated with the DuckDB [tpch extension]({% link docs/archive/1.1/extensions/tpch.md %}).

## A Note on Benchmarks

Running [fair benchmarks is difficult](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf), especially when performing system-to-system comparison.
When running benchmarks on DuckDB, please make sure you are using the latest version (preferably the [nightly build]({% link docs/archive/1.1/installation/index.html %}?version=main)).
If in doubt about your benchmark results, feel free to contact us at `gabor@duckdb.org`.

## Disclaimer on Benchmarks

Note that the benchmark results presented in this guide do not constitute official TPC or LDBC benchmark results. Instead, they merely use the data sets of and some queries provided by the TPC-H and the LDBC BI benchmark frameworks, and omit other parts of the workloads such as updates.