---
layout: post
title: "When Contiguous Hash Joins Pay Off in DuckDB and DataFusion"
authors:
  - Maxim Rusanov
excerpt: "An independent technical report on when faster hash-join probes offset the cost of reorganizing the build side."
tag: paper
category: community
venue: "Zenodo"
---

| | |
|-------|-------|
| **Technical report** | [Zenodo](https://doi.org/10.5281/zenodo.24519118) |
| **Implementation** | [DuckDB prototype and reproduction instructions](https://github.com/rusanoph/unchained-hash-join-research/tree/v1.0.0/duckdb) |
| **Dataset** | [Benchmark observations and analysis scripts](https://doi.org/10.5281/zenodo.24519430) |

## Abstract

This independent study asks when scanning contiguous ranges of hash-join candidates repays the cost of constructing them. Paired single-thread SQL benchmarks compare experimental layouts with native execution in DuckDB 1.5.6 and Apache DataFusion 55.2.0. DuckDB's prototype copies staged build rows into contiguous buckets. Its policy improved aggregate performance on the tested SNAP graph queries, but stock DuckDB was faster overall on the Join Order Benchmark, LDBC BI, and TPC-DS. One Join Order Benchmark join reorganized 5.54 million build rows for three probe rows. DataFusion groups Arrow row IDs and saw lower aggregate query times on its tested SNAP and Join Order Benchmark workloads with automatic index selection. A break-even model relates these outcomes to build-side data movement, the frequency and locality of probes, and the cost of gathering payloads.
