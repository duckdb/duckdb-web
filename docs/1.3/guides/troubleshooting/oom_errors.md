---
layout: docu
title: Out of Memory Errors
---

DuckDB has a state of the art out-of-core query engine that can spill to disk for larger-than-memory processing.
We continuously strive to improve DuckDB to improve its scalability and prevent out of memory errors whenever possible.
That said, you may still experience out-of-memory errors if you run queries with multiple [blocking operators]({% link docs/1.3/guides/performance/how_to_tune_workloads.md %}#blocking-operators), certain aggregation functions, `PIVOT` operations, etc., or if you have very little available memory compared to the dataset size.

## Types of Out of Memory Errors

Out of memory errors mainly occur in two forms:

### `OutOfMemoryException`

Most of the time DuckDB runs out of memory with an `OutOfMemoryException`.
For example:

```console
duckdb.duckdb.OutOfMemoryException: Out of Memory Error: failed to pin block of size 256.0 KiB (476.7 MiB/476.8 MiB used)
```

### OOM Reaper (Linux)

Many Linux distributions have an [OOM killer or OOM reaper process](https://learn.redhat.com/t5/Platform-Linux/Out-of-Memory-Killer/td-p/48828)
whose goal is to prevent memory overcommitment.
If the OOM reaper killed your process, you often see the following message where DuckDB was running:

```console
Killed
```

To get more detailed information, check the diagnostic messages using the [`dmesg` command](https://en.wikipedia.org/wiki/Dmesg) (you may need `sudo`):

```bash
sudo dmesg
```

If the process was killed by the OOM killer/reaper, you will find an entry like this:

```console
[Fri Apr 18 02:04:10 2025] Out of memory: Killed process 54400 (duckdb) total-vm:1037911068kB, anon-rss:770031964kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:1814612kB oom_score_adj:0
```

## Troubleshooting Out of Memory Errors

To prevent out of memory errors, try to reduce memory usage.
To this end, please consult the [“How to Tune Workloads” site]({% link docs/1.3/guides/performance/how_to_tune_workloads.md %}).
In short:

* Reduce the number of threads using the `SET threads = ...` command.
* If your query reads a large mount of data from a file or writes a large amount of data, try setting the `preserve_insertion_order` option to `false`: `SET preserve_insertion_order = false`.
* Reduce the memory limit below the default 80% (see the [Limits page]({% link docs/1.3/operations_manual/limits.md %})). This can be helpful because some DuckDB operations circumvent the buffer manager and can reserve more memory than allowed by the memory limit. If you observe this, set the memory limit to 50-60% of the total system memory by using `SET memory_limit = ...`.
* Break up the query into subqueries. This allows you to see where the intermediate results “blow up”, causing the query to run out of memory.

## See Also

For more information on DuckDB's memory management, see the [“Memory Management in DuckDB” blog post]({% post_url 2024-07-09-memory-management %}).
