---
layout: docu
title: I/O
---

> Warning DuckDB ships with safe defaults. The configuration options described on this page are advanced options, so proceed with caution when changing them.

Starting with v2.0, DuckDB supports asynchronous I/O. Instead of blocking a worker thread until requested data arrives, DuckDB issues reads in the background and keeps multiple requests in flight while worker threads process data that has already arrived. This can significantly speed up queries when synchronous I/O does not saturate the available bandwidth, e.g., when reading data from object storage such as S3.

For a detailed explanation of the design and benchmark results, see the [“Asynchronous I/O in DuckDB” blog post]({% post_url 2026-07-31-asynchronous-io %}).

## Supported Formats

Asynchronous I/O is currently supported for the following formats:

* [Parquet files]({% link docs/preview/data/parquet/overview.md %})
* uncompressed, seekable [CSV files]({% link docs/preview/data/csv/overview.md %}) encoded in UTF-8

Other formats, such as JSON files and DuckDB's native database format, use synchronous I/O. Asynchronous I/O is used automatically for the supported formats, including when they are read through data lake formats such as [DuckLake](https://ducklake.select/).

## Thread Pools

DuckDB uses two thread pools:

* The regular pool contains the worker threads, which perform the actual query processing (e.g., decoding, joins and aggregations). Its size is controlled by the `threads` setting and defaults to the number of CPU cores. Regular threads prioritize query processing but can also perform I/O tasks when idle.
* The asynchronous pool contains threads dedicated to blocking I/O. As these threads spend most of their time waiting for responses (e.g., HTTP requests), there are more of them than CPU cores: by default, four times the number of system threads, capped at 256. Its size is controlled by the `async_threads` setting.

For example, to set the number of asynchronous I/O threads to 48, run:

```sql
SET async_threads = 48;
```

> Warning The asynchronous pool increases the total number of threads per DuckDB instance. If you run many DuckDB instances in a single process, consider setting `threads` and `async_threads` explicitly.

## Read-Ahead

To keep the asynchronous threads busy, DuckDB reads ahead: it schedules the reads for upcoming scan jobs (e.g., row groups in Parquet files or byte ranges in CSV files) before the worker threads need them. While a worker thread processes the current job, the asynchronous threads fetch the data for the next jobs. If the data for a job has not arrived yet, the worker thread is free to run other tasks in the meantime.

Keeping more fetch tasks in flight consumes more memory. To determine a budget and avoid out-of-memory issues, DuckDB provides the `read_ahead_depth` configuration option. It can have three types of values:

* `-1` (default): unlimited depth, bounded by memory.
* `N > 0`: at most `N` jobs ahead, with no memory budget.
* `0`: read-ahead is off, each scan task schedules I/O only for its own job.

To configure it, use the `SET` clause, e.g.:

```sql
SET read_ahead_depth = 5;
```

In the default mode, the read-ahead budget is negotiated with the same memory manager that distributes memory between operators such as joins, sorts and window functions. Under high memory pressure, the read-ahead queue shrinks to a single job and the scan behaves similarly to a synchronous scan. Once memory frees up, the queue fills up again. To limit the total memory used by DuckDB, use the [`memory_limit` setting]({% link docs/preview/configuration/overview.md %}).

## Tuning

The default settings work well in most cases. On machines with high network bandwidth, you can further increase throughput by fixing the read-ahead depth and adjusting the number of asynchronous threads and the HTTP retry settings. For example, the following configuration saturated a 25 Gbit/s network on a 64-core EC2 instance reading Parquet files from S3:

```sql
SET read_ahead_depth = 64;
SET async_threads = 48;
SET http_retries = 8;
SET http_retry_wait_ms = 50;
SET http_retry_backoff = 2;
```

As the row group is the unit of parallelism for Parquet scans, asynchronous I/O works best if Parquet files have at least as many row groups as the number of threads. Files with only a few very large row groups cannot keep enough requests in flight to saturate the network.

## Synchronizing Writes to Disk

When DuckDB persists changes to a database on the local file system, it asks the operating system to flush the written data to stable storage. The `fsync_mode` configuration option controls how this is done. It can have three values:

* `STANDARD` (default): uses the regular sync call of the platform, i.e., `fdatasync` or `fsync` on Unix-like systems and `FlushFileBuffers` on Windows.
* `FULL`: on macOS, uses `F_FULLFSYNC`, which also instructs the drive to flush its write cache and thus guarantees durability in case of a power failure. If the file system does not support `F_FULLFSYNC`, DuckDB falls back to the `STANDARD` behavior. On other platforms, `FULL` is equivalent to `STANDARD`.
* `NONE`: skips the sync call. Writes are handed over to the operating system, which flushes them to disk at its own pace.

For example, to disable syncing for a performance-critical workload, run:

```sql
SET fsync_mode = 'NONE';
```

The option is global, i.e., it applies to the whole DuckDB instance.

> Warning Setting `fsync_mode` to `NONE` may cause data loss or database corruption if the operating system crashes or the machine loses power. Only use it if the database can be recreated from other sources.
