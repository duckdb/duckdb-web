---
github_directory: https://github.com/sirius-db/sirius/tree/main/sirius-duckdb
layout: docu
redirect_from:
- /docs/current/core_extensions/sirius
- /docs/lts/core_extensions/sirius
- /docs/preview/core_extensions/sirius
- /docs/stable/core_extensions/sirius
title: Sirius Extension
---

The `sirius` extension runs SQL queries on NVIDIA GPUs using [Sirius](https://www.sirius-db.com/), a GPU-native SQL engine.
Once loaded, Sirius runs the queries it supports on the GPU, and DuckDB's CPU engine runs everything else.
No query changes are needed.

The `sirius` extension is available from DuckDB v2.0.1 on the `linux_amd64` and `linux_arm64` platforms.

## Requirements

* Linux with glibc 2.28 or newer on x86-64 or arm64. macOS, Windows, musl-based distributions, WebAssembly, and NVIDIA Jetson are not supported.
* An NVIDIA GPU with compute capability 7.5 or newer (Turing, Ampere, Ada Lovelace, Hopper, or Blackwell).
* An NVIDIA driver that supports CUDA 12.8 or newer (driver version 570.26 or newer).
* `io_uring` enabled in the kernel. Containers must allow the `io_uring_setup`, `io_uring_enter`, and `io_uring_register` system calls.

## Installing and Loading

To install and load the extension, run:

```sql
INSTALL AND LOAD httpfs;
SET http_timeout = 900;
INSTALL AND LOAD sirius;
```

> Tip The default timeout is 30 seconds, which can incur timeouts when downloading the extension on a slow network connection.
> The `http_timeout` option allows you to adjust the timeout to accommodate this.

The `sirius` extension is a small loader without a CUDA dependency.
`LOAD sirius` asks the NVIDIA driver which CUDA version it supports and loads the matching Sirius backend:

| Driver supports            | Backend         |
|----------------------------|-----------------|
| CUDA 12.8 or a later 12.x  | `sirius_cuda12` |
| CUDA 13.0 or newer         | `sirius_cuda13` |

If the backend is not installed yet and [`autoinstall_known_extensions`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is enabled (the default), the first `LOAD sirius` downloads it from the [community extensions repository]({% link community_extensions/index.md %}) (or the configured auto-install repository).
The backend is large, so the loader prints a line to `stderr` when the download starts and another when it finishes or fails.
Later loads reuse the installed backend.

> Warning Do not install or load `sirius_cuda12` or `sirius_cuda13` directly: `LOAD sirius` selects the right backend for your driver and falls back to the CPU when no usable NVIDIA driver is found.

## Checking the Status

The `sirius_status` table function shows how `LOAD sirius` set up GPU execution:

```sql
SELECT * FROM sirius_status();
```

```text
┌──────────────┬─────────────────────┬───────────────┬────────────────┬───────────────┬─────────────────┐
│ driver_found │ cuda_driver_version │    backend    │ backend_loaded │ gpu_execution │ fallback_reason │
│   boolean    │       varchar       │    varchar    │    boolean     │    boolean    │     varchar     │
├──────────────┼─────────────────────┼───────────────┼────────────────┼───────────────┼─────────────────┤
│ true         │ 12.8                │ sirius_cuda12 │ true           │ true          │ NULL            │
└──────────────┴─────────────────────┴───────────────┴────────────────┴───────────────┴─────────────────┘
```

| Column                | Description                                                                                  |
|-----------------------|----------------------------------------------------------------------------------------------|
| `driver_found`        | Whether `libcuda.so.1` could be opened                                                       |
| `cuda_driver_version` | The CUDA version the driver supports, such as `12.8`, or `NULL` if unknown                   |
| `backend`             | The selected backend, `sirius_cuda12` or `sirius_cuda13`, or `NULL` without a usable driver |
| `backend_loaded`      | Whether the backend is loaded                                                                |
| `gpu_execution`       | Whether transparent GPU execution is active for this session                                 |
| `fallback_reason`     | Why GPU execution is unavailable, or `NULL` once the backend is loaded                       |

## Running Queries on the GPU

With the backend loaded, plain SQL runs on the GPU where Sirius supports it:

```sql
SELECT store, count(*) AS orders, sum(price) AS revenue
FROM 'sales.parquet'
GROUP BY store
ORDER BY store;
```

The `gpu_execution` setting controls this transparent execution:

```sql
-- Run the rest of this session on DuckDB's CPU engine
SET gpu_execution = false;
-- Change the default for the database
SET GLOBAL gpu_execution = false;
```

The `gpu_execution` table function runs a single query through Sirius, even when the setting is off:

```sql
FROM gpu_execution('SELECT count(*) FROM ''sales.parquet''');
```

## CPU Fallback

If no usable driver is found, or the backend cannot be installed or loaded, `LOAD sirius` still succeeds and all queries run on DuckDB's CPU engine.
In that case, the `gpu_execution` setting defaults to `false`, and `SET gpu_execution = true` or a call to the `gpu_execution` table function fails with the reason.
The `fallback_reason` column of `sirius_status()` shows the reason too:

```sql
SELECT fallback_reason FROM sirius_status();
```

The driver is probed once per process, so restart DuckDB after installing or upgrading the NVIDIA driver.
If the backend fails after its own initialization has started, for example due to a GPU error or an invalid configuration file, `LOAD sirius` fails instead of falling back.
`LOAD sirius` also fails if `gpu_execution` was set to `true` before loading and no backend can be loaded.

## Updating

`LOAD sirius` reuses an installed backend and does not update it.
To update both the loader and the backend, run the following and restart DuckDB:

```sql
UPDATE EXTENSIONS;
```

## Functions and Settings

The Sirius backends add more table functions and settings, for example to pin tables in GPU memory, run vector searches, read Parquet files from S3, and tune memory use.
These are documented on the pages of the backends:

* [`sirius_cuda12`](https://duckdb.org/community_extensions/extensions/sirius_cuda12)
* [`sirius_cuda13`](https://duckdb.org/community_extensions/extensions/sirius_cuda13)

For the configuration file, logging, and telemetry, see the [Sirius documentation](https://github.com/sirius-db/sirius/blob/main/docs/README.md) and its [configuration reference](https://github.com/sirius-db/sirius/blob/main/docs/super-sirius/configuration.md).
