---
layout: post
title: "duckdb_stats: A Statistical Inference Layer for DuckDB"
authors:
  - "lihongyan (alitrack)"
tag: project
category: community
excerpt: ""
---

|-------|-------|
| **Implementation** | [Code](https://github.com/alitrack/duckdb_stats) |

64 SQL macros that fill the gap between DuckDB's built-in statistics (aggregations, distributions, t-tests via the stats_duck community extension) and what a real analysis needs: confidence intervals, effect sizes, power and sample size, one/two-way ANOVA with Tukey/Scheffé/Dunnett post-hoc, Fisher's exact test, odds/risk ratios with CIs, NNT, weighted statistics, Gini and HHI. Zero compilation — one community extension plus one SQL file, DuckDB 1.4+.

Scope was derived by mapping all 386 functions of statcpp (a C++ statistics library, 30 modules) onto DuckDB's three layers: distribution families and hypothesis tests to stats_duck, ML/clustering/survival to duckdb-ml, and the entire inferential layer to these macros. The module-by-module coverage matrix is in the repo. All macros are verified against SciPy with fixed seeds (58 assertions, zero failures at release).
