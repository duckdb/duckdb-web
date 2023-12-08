---
layout: docu
title: My Workload is Slow
---

If you find that your workload in DuckDB is slow, we recommend performing the following checks. More detailed instructions are linked for each point.

1. Are you using the correct types? For example, [use `TIMESTAMP` to encode datetime values](schema#types).
1. Are you using constraints (primary key, unique, etc.) or indexes? If so, try [disabling them](schema#indexing).
1. Are you reading from Parquet files? If so, do they have [row group sizes between 100k and 1M](file-formats#the-effect-of-row-group-sizes)?
2. Do you have enough memory? DuckDB works best if you have [5GB memory/CPU core](environment#cpu-and-memory).
3. Are you using a fast disk? Network-attached disks can cause the workload to slow down for [larger than memory workloads](environment#disk).
4. Study the query plan using [`EXPLAIN`](how-to-tune-workloads#profiling) to ensure there are no exploding joins.
5. Is the workload running [in parallel](how-to-tune-workloads#paralellism)? Use `htop` or the task manager to observe this.
6. Is DuckDB using too many threads? Try [limiting the amount of threads](how-to-tune-workloads#parallelism).
