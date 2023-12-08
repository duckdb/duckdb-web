---
layout: docu
title: Performance Guide
---

DuckDB aims to automatically achieve high performance using proven default configurations and having a forgiving architecture. Of course, there are still opportunities for tuning the system for specific workloads. This page contains guidelines for achieving good performance when loading and processing data with DuckDB.

The guides include several microbenchmarks, these use the [LDBC BI SF300 data set](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) (20GB `.tar.zst` archive, 21GB when decompressed into `.csv.gz` files).

## Pages in This Section
