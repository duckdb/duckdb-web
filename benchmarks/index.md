---
layout: docu
title: Continuous Benchmarking
selected: Introduction
expanded: Benchmarking
---
Continuous benchmarking is run on every commit to detect performance regressions in DuckDB. All queries run with a standard timeout of 30 seconds to avoid the benchmark suite from taking too much time to run. Benchmarks are ran using the benchmark runner, and are defined in the [benchmark subdirectory](https://github.com/cwida/duckdb/tree/master/benchmark) of the DuckDB source repository. The following sets of benchmarks are run:

* [Append](append.html)
* [Aggregates](aggregate.html)
* [Bulk Update](bulkupdate.html)
* [Cast](cast.html)
* [Contains_Tpch](contains_tpch.html)
* [CSV](csv.html)
* [In](in.html)
* [Micro](micro.html)
* [Prefix_Tpch](cast.html)
* [Startup](startup.html)
* [Storage](storage.html)
* [String](string.html)
* [Suffix_Tpch](suffix_tpch.html)
* [TPC-DS](tpcds.html)
* [TPC-H](tpch.html)
<!-- 10. [IMDB](/benchmarks/imdb) -->
