---
layout: docu
title: My Workload Is Slow
redirect_from:
  - /docs/guides/performance/my-workload-is-slow
---

If you find that your workload in DuckDB is slow, we recommend performing the following checks. More detailed instructions are linked for each point.

1. Do you have enough memory? DuckDB works best if you have [5-10 GB memory per CPU core]({% link docs/guides/performance/environment.md %}#cpu-and-memory).
1. Are you using a fast disk? Network-attached disks (such as cloud block storage) cause write-intenstive and [larger than memory]({% link docs/guides/performance/how_to_tune_workloads.md %}#spilling-to-disk) workloads to slow down. For running such workloads in cloud environments, it is recommended to use instance-attached storage (NVMe SSDs).
1. Are you using indexes or constraints (primary key, unique, etc.)? If possible, try [disabling them]({% link docs/guides/performance/schema.md %}#indexing), which boosts load and update performance.
1. Are you using the correct types? For example, [use `TIMESTAMP` to encode datetime values]({% link docs/guides/performance/schema.md %}#types).
1. Are you reading from Parquet files? If so, do they have [row group sizes between 100k and 1M]({% link docs/guides/performance/file_formats.md %}#the-effect-of-row-group-sizes) and file sizes between 100 MB to 10 GB?
1. Does the query plan look right? Study it with [`EXPLAIN`]({% link docs/guides/performance/how_to_tune_workloads.md %}#profiling).
1. Is the workload running [in parallel]({% link docs/guides/performance/how_to_tune_workloads.md %}#parallelism)? Use `htop` or the operating system's task manager to observe this.
1. Is DuckDB using too many threads? Try [limiting the amount of threads]({% link docs/guides/performance/how_to_tune_workloads.md %}#parallelism-multi-core-processing).

Are you aware of other common issues? If so, please click the _Report content issue_ link below and describe them along with their workarounds.
