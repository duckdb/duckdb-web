---
layout: docu
redirect_from:
- /docs/guides/performance/benchmarks
- /docs/stable/guides/performance/benchmarks
- /docs/current/guides/performance/benchmarks
- /docs/lts/guides/performance/benchmarks
- /docs/preview/guides/performance/benchmarks
title: Benchmarks
how_to_topic: performance
---

For several of the recommendations in our performance guide, we use microbenchmarks to back up our claims. For these benchmarks, we use datasets from the [TPC-H benchmark]({% link docs/2.0/core_extensions/tpch.md %}) and the [LDBC Social Network Benchmark’s BI workload](https://github.com/ldbc/ldbc_snb_bi/blob/main/snb-bi-pre-generated-data-sets.md#compressed-csvs-in-the-composite-merged-fk-format).

## Benchmark Environment

The benchmarks in the performance guide were executed with DuckDB v2.0.0 on a MacBook Pro with an 18-core M5 Pro CPU, 48 GiB RAM, and 1 TB SSD.
The scripts are available in the [`microbenchmarks` directory of the `duckdb-web` repository](https://github.com/duckdb/duckdb-web/tree/main/microbenchmarks).

## Datasets

Some benchmarks use the [LDBC BI SF300 dataset's Comment table](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) (20 GB `.tar.zst` archive, 21 GB when decompressed into `.csv.gz` files),
others use the [LDBC BI SF100 dataset's Comment table](https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst) (7 GB `.tar.zst` archive)
or the SF300 Comment table's [`creationDate` column](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) (4 GB `.parquet` file).

The TPC-H datasets used in the benchmarks are generated with the DuckDB [tpch extension]({% link docs/2.0/core_extensions/tpch.md %}).

## A Note on Benchmarks

Running [fair benchmarks is difficult](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf), especially when performing system-to-system comparison.
When running benchmarks on DuckDB, please make sure you are using the latest version (preferably the [preview build]({% link docs/2.0/installation.html %}?version=main)).
If in doubt about your benchmark results, feel free to contact us at `gabor@duckdb.org`.

## Disclaimer on Benchmarks

Note that the benchmark results presented in this guide do not constitute official TPC or LDBC benchmark results. Instead, they merely use the datasets of and some queries provided by the TPC-H and the LDBC BI benchmark frameworks, and omit other parts of the workloads such as updates.
