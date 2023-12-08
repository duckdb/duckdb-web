---
layout: docu
title: Benchmarks
---

For several of our recommendations in the performance guide, we use microbenchmarks to back up our claims. For these benchmarks, we use data sets from the [TPC-H benchmark](../docs/extensions/tpch) and the [LDBC Social Network Benchmark’s BI workload](https://github.com/ldbc/ldbc_snb_bi/blob/main/snb-bi-pre-generated-data-sets.md#compressed-csvs-in-the-composite-merged-fk-format). Feel free to reproduce these in your environment to see the effect of changes.

## Benchmark Environment

The benchmarks in the performance guide executed on a 2022 MacBook Pro with a 12-core M2 Pro CPU, 32GiB RAM and 1TB disk.

## A Note on Benchmarks

Running [fair benchmarks is difficult](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf), especially when performing system-to-system comparison. When running benchmarks on DuckDB, please make sure you are using the latest version (preferably the nightly build). If in doubt, feel free to contact us at `gabor@duckdb.org`.

## Disclaimer on Benchmarks

Note that the benchmark results presented in this guide do not constitute official TPC or LDBC benchmark results. Instead, they merely use the data sets of and queries provided by the TPC-H and the LDBC BI benchmark frameworks.
