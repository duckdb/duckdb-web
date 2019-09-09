---
layout: default
title: Continuous Benchmarking
selected: Benchmarking
expanded: Benchmarking
---
Continuous benchmarking is run on every commit to detect performance regressions in DuckDB. All queries run with a standard timeout of 30 seconds to avoid the benchmark suite from taking too much time to run. Benchmarks are ran using the benchmark runner, and are defined in the [benchmark subdirectory](https://github.com/cwida/duckdb/tree/master/benchmark) of the DuckDB source repository. The following sets of benchmarks are run:

1. [Aggregates](/benchmarks/aggregate)
2. [Append](/benchmarks/append)
3. [CSV](/benchmarks/csv)
4. [In](/benchmarks/in)
5. [Micro](/benchmarks/micro)
6. [Storage](/benchmarks/storage)
7. [TPC-DS](/benchmarks/tpcds)
8. [TPC-H](/benchmarks/tpch)
8. [IMDB](/benchmarks/imdb)
