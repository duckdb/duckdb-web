---
layout: post
title: "NVIDIA Vera"
date: 2026-09-15
author: "The DuckDB and NVIDIA teams"
thumb: "/images/everywhere/thumbs/nvidia-vera.jpg"
image: "/images/everywhere/thumbs/nvidia-vera.jpg"
excerpt: ""
tags: ["PCs"]
thirdparty: true
---

We ran the full TPC-H benchmark with the scale factor 1,000 dataset using the [`duckdb-tpch` project](https://github.com/duckdb/duckdb-tpch).
Our setup included two server platforms: x86 baseline (Intel Xeon 6) and NVIDIA Vera.
We also compared two DuckDB versions: the latest stable version (v1.5.5) and the upcoming release's [alpha version]({% post_url 2026-09-02-try-duckdb-20-alpha %}) (v2.0.0-alpha), with the latter shipping several optimizations that make complex workloads such as TPC-H faster.

## Platforms

### x86 Baseline: Intel Xeon 6

We ran the benchmark on a server with an Intel Xeon 6 CPU.

* **CPU:** Intel Xeon 6 CPU, 96 cores with [hyper-threading](https://en.wikipedia.org/wiki/Hyper-threading)
* **Memory:** 768 GB
* **Disk:** 1 NVMe SSD disk with 3TB+ storage, formatted to ext4
* **Operating system:** Ubuntu 26.04

DuckDB flags:

```sql
SET threads = 96;
SET block_allocator_memory = '500G';
SET allocator_background_threads = true;
```

### NVIDIA Vera

We conducted the benchmark on a dual-socket system but restricted DuckDB to a single socket.

* **CPU:** NVIDIA Vera CPU, 88 cores with [Spatial Multithreading](https://alphaeloper.nvidia.com/blog/inside-nvidia-vera-cpu-olympus-cores-built-for-maximum-single-threaded-performance-in-agentic-ai/)
* **Memory:** 768 GB
* **Disk:** 1 NVMe SSD disk with 3TB+ storage, formatted to ext4
* **Operating system:** Ubuntu 26.04

DuckDB flags:

```sql
SET threads = 88;
SET block_allocator_memory = '500G';
SET allocator_background_threads = true;
```

## DuckDB Versions

We ran DuckDB using the Python client and benchmarked two DuckDB versions:

* DuckDB v1.5.5
* DuckDB v2.0.0-alpha (Python package: `1.6.0.dev379`)

## Benchmark Methodology

We perform an initial warmup run and discard its result, then conduct three runs and take the median value of the QphH@SF composite scores.

## Benchmark Results

|                  | Setup 1          | Setup 2          | Setup 3          | Setup 4          |
| ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| CPU              | Intel            | Intel            | Vera             | Vera             |
| DuckDB           | 1.5.5            | 2.0.0-alpha      | 1.5.5            | 2.0.0-alpha      |
| Run 1            | 1,643,610.87     | 2,120,588.82     | 2,488,209.48     | 3,073,292.99     |
| Run 2            | 1,700,471.78     | 2,022,795.01     | 2,389,726.36     | 3,131,306.27     |
| Run 3            | 1,673,422.48     | 2,109,782.19     | 2,482,589.73     | 3,052,102.87     |
| **Median score** | **1,673,422.48** | **2,109,782.19** | **2,482,589.73** | **3,073,292.99** |

The results show a 24–26% improvement for DuckDB v2.0.0-alpha over DuckDB v1.5.5,
and a 46–48% performance advantage for the Vera platform over the Xeon baseline.

We'll share more details in an upcoming blog post.
Stay tuned!
