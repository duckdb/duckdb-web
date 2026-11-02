---
layout: post
title: "Benchmarking DuckDB 2.0-dev on NVIDIA Vera"
authors:
  - Gábor Szárnyas
excerpt: We put NVIDIA's new Vera CPU through its paces using a workload derived from TPC-H on scale factor 1,000.
tag: benchmark
thumb: "/images/blog/thumbs/nvidia-vera-benchmark.svg"
image: "/images/blog/thumbs/nvidia-vera-benchmark.png"
redirect_from:
- /everywhere/nvidia-vera
---

<!-- markdownlint-disable MD001 -->

We love running benchmarks on all sorts of new hardware.
This often includes
[somewhat]({% link _everywhere/raspberry-pi-5.md %})
[exotic]({% link _everywhere/iphone-17-pro.md %})
[hardware]({% link _everywhere/morefine-m700s.md %}) –
where we sometimes need to compile a new DuckDB binary.
This time, in collaboration with the NVIDIA team,
we got our hands on their new Vera chip, aimed at agentic workloads.

[NVIDIA Vera](https://www.nvidia.com/en-us/data-center/vera-cpu/) comes with 88 “Olympus” cores, Spatial Multithreading and
up to 1.2 terabytes per second (TB/s) of memory bandwidth.
What's more, Vera runs arm64 binaries – so it runs DuckDB's regular build without any modifications.

To see how this new hardware performs, we ran a benchmark derived from TPC-H that included both the power test and the throughput test on scale factor 1,000.

> Note This workload is derived from the TPC-H Benchmark and is not comparable to published TPC-H Benchmark results, as this implementation does not comply with all requirements of the TPC-H Benchmark.

## Environment

### System Setup

The machine was a bare-metal server running Ubuntu 26.04.
The hardware included 1536 GB of memory and a single NVMe SSD with 3+ TB of storage, formatted as ext4.
At the time of writing, DuckDB 2.0 was [not released yet]({% post_url 2026-09-02-try-duckdb-20-alpha %}), so we used a [preview build]({% link docs/2.0/installation.html %}?version=preview), `1.6.0.dev379` (a codename for 2.0-dev).
As a baseline, we also ran the benchmark with DuckDB 1.5.5.

To run the experiments, we used our [`duckdb-tpch` benchmark harness](https://github.com/duckdb/duckdb-tpch/).
To re-create our benchmark environment, see our script below.

<!-- markdownlint-disable MD022 MD025 MD034 MD040 -->

<details markdown='1'>
<summary markdown='span'>
Click here to reveal the setup script.
</summary>
```bash
# make sure you have the required tools
sudo apt install git g++ cmake python3-pip

# clone the repository at the commit used for the experiments
git clone https://github.com/duckdb/duckdb-tpch
cd duckdb-tpch
git reset --hard cf096cea8a0a054cefe0e695c842ca5bca6ec04d

# install the required Python dependencies
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install duckdb==1.6.0.dev379
# for the DuckDB 1.5.5 baseline, install this version instead:
# python3 -m pip install duckdb==1.5.5

# build the dbgen tool
cd tpch_tools_3.0.1/dbgen/
make
cd ../..

# generate the dataset, query streams and update streams
export SF=1000
./generate.sh
```
</details>

<!-- markdownlint-enable MD022 MD025 MD034 MD040 -->

> Tip To generate the large-scale dataset efficiently,
> the repository uses the wonderful [`tpchgen-cli` tool](https://pypi.org/project/tpchgen-cli/),
> a parallel Rust rewrite of the `dbgen` data generator.
> It also uses the old generator to produce update and query streams.

This workload is relatively large-scale (SF1,000) and highly concurrent during the throughput run.
To get the best performance out of DuckDB, we set the following flags:

```sql
SET block_allocator_memory = '500G';
SET allocator_background_threads = true;
```

The server had a dual-socket [NVIDIA Vera CPU](https://www.nvidia.com/en-us/data-center/vera-cpu/), packing 88 cores per socket with [Spatial Multithreading](https://developer.nvidia.com/blog/inside-nvidia-vera-cpu-olympus-cores-built-for-maximum-single-threaded-performance-in-agentic-ai/).
We ran DuckDB on a single socket using the `numactl` command:

```bash
numactl --cpunodebind=0 --membind=0 python3 benchmark.py
```

For this test, we also pinned the number of threads to just 88:

```sql
SET threads = 88;
```

> Update DuckDB 2.1 will ship improvements for [NUMA-awarerness and many-core setups](https://github.com/duckdb/duckdb/pull/27782).

### Deviations from the Specification

Our implementation deviates from the specification in the following ways:

* The results were not audited by a TPC-certified auditor, and we did not publish a Full Disclosure Report or an Executive Summary.
* We did not price the system, so there is no price/performance figure.
* DuckDB 2.0.0-alpha was a pre-release version, not generally available at the time of the benchmark.
* We restricted DuckDB to a single socket of the dual-socket server.
* We generated the base tables with `tpchgen-cli` instead of `dbgen`.
* We converted the refresh data from `dbgen`'s flat files to Parquet before the benchmark.
* The initial database load is not part of the reported results.
* We did not run the ACID tests.
* We report the median of three runs (after a discarded warmup run) instead of the lower of two runs.

## Benchmark Runs and Results

We performed an initial warmup run and discarded its result.
Then, we conducted three complete runs in sequence and took the median value of the _QphH@Size_ composite scores:

| Run              | DuckDB 1.5.5     | DuckDB 2.0.0-alpha |
|------------------|-----------------:|-------------------:|
| Run 1            | 2,488,209.48     | 3,073,292.99       |
| Run 2            | 2,389,726.36     | 3,131,306.27       |
| Run 3            | 2,482,589.73     | 3,052,102.87       |
| **Median score** | **2,482,589.73** | **3,073,292.99**   |

DuckDB 2.0.0-alpha shows a 24% improvement over DuckDB 1.5.5 – and this is something all users will benefit from once [DuckDB 2.0.0 is out]({% link release_calendar.md %}).

> Update DuckDB 2.0 [is out]({% post_url 2026-10-21-announcing-duckdb-200 %})!

We attribute the high performance of Vera to three key factors.
First, the high memory bandwidth enables fast scans.
Second, combined with low memory latency, it keeps the cores continuously occupied during processing.
Finally, the Olympus cores' large caches allow efficient access to the hash tables built during aggregations and joins.

We are looking forward to continuing this benchmark by using DuckDB 2.0.0's stable build, running on the full dual-socket setup, and incorporating different benchmarks.
