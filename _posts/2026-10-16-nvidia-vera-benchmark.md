---
layout: post
title: "Benchmarking DuckDB 2.0-dev on NVIDIA Vera"
authors:
  - Gábor Szárnyas
excerpt: We put NVIDIA's new Vera CPU through its paces and compared it to an x86 baseline using a workload derived from TPC-H on scale factor 1,000.
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
As an x86 baseline, we also ran the benchmark on an Intel Xeon 6 machine.

> Note This workload is derived from the TPC-H Benchmark and is not comparable to published TPC-H Benchmark results, as this implementation does not comply with all requirements of the TPC-H Benchmark.

## Environment

### System Setup

We used two bare-metal machines running Ubuntu 26.04:

* an NVIDIA Vera server with 1536 GB of memory, and
* an x86 baseline, an [`m8id.metal-48xl` EC2 instance](https://aws.amazon.com/ec2/instance-types/m8i/) with an Intel Xeon 6975P-C CPU and 768 GiB of memory.

On both machines, we stored the database on a single NVMe SSD with 3+ TB of storage, formatted as ext4.
At the time of writing, DuckDB 2.0 was [not released yet]({% post_url 2026-09-02-try-duckdb-20-alpha %}), so we used a [preview build]({% link docs/2.0/installation.html %}?version=preview), `1.6.0.dev379` (a codename for 2.0-dev).
As a software baseline, we also ran the benchmark with DuckDB 1.5.5.

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

### NVIDIA Vera

The server had a dual-socket [NVIDIA Vera CPU](https://www.nvidia.com/en-us/data-center/vera-cpu/), packing 88 cores per socket with [Spatial Multithreading](https://developer.nvidia.com/blog/inside-nvidia-vera-cpu-olympus-cores-built-for-maximum-single-threaded-performance-in-agentic-ai/).
We ran DuckDB on a single socket using the `numactl` command:

```batch
numactl --cpunodebind=0 --membind=0 python3 benchmark.py
```

For this test, we also pinned the number of threads to just 88:

```sql
SET threads = 88;
```

### x86 Baseline: Intel Xeon 6

The x86 baseline ran on an [`m8id.metal-48xl` EC2 instance](https://aws.amazon.com/ec2/instance-types/m8i/), which has a single-socket Intel Xeon 6 CPU, packing 96 cores with [hyper-threading](https://en.wikipedia.org/wiki/Hyper-threading), yielding 192 threads.
However, we found that DuckDB performs best when using 96 threads, so we configured it accordingly:

```sql
SET threads = 96;
```

### Hardware Specifications

The table below summarizes the specifications of the two CPUs:

| Specification          | NVIDIA Vera (per socket) | Intel Xeon 6975P-C |
| ---------------------- | ------------------------ | ------------------ |
| Cores / threads        | 88 / 176                 | 96 / 192           |
| Threads used by DuckDB | 88                       | 96                 |
| L3 cache               | 164 MB                   | 480 MB             |
| Memory bandwidth       | up to 1.2 TB/s           | not published      |
| TDP                    | 250–450 W (configurable) | not published      |

For Vera, the cache, memory bandwidth, and TDP figures are from NVIDIA's [Vera CPU architecture whitepaper](https://dam-cdn.nvd.orangelogic.com/AssetLink/lptf1ea6nbw67y10wro347r4a3biqt0w.pdf).
The Xeon 6975P-C is a custom variant that is not listed on [Intel ARK](https://www.intel.com/content/www/us/en/ark/products/series/240357/intel-xeon-6-processors.html).
At the time of writing, reliable information on the TDP of the Xeon 6975P-C and the frequency of these chips is not available.

> Update DuckDB 2.1 will ship improvements for [NUMA-awarerness and many-core setups](https://github.com/duckdb/duckdb/pull/27782).

### Deviations from the Specification

Our implementation deviates from the specification in the following ways:

* The results were not audited by a TPC-certified auditor, and we did not publish a Full Disclosure Report or an Executive Summary.
* We did not price the system, so there is no price/performance figure.
* We do not list frequency data for the CPUs or power data for the Xeon 6975P-C, and we only list the configurable TDP range for Vera, as more precise information was not reliably available (see above).
* DuckDB 2.0.0-alpha was a pre-release version, not generally available at the time of the benchmark.
* We restricted DuckDB to a single socket of the dual-socket Vera server.
* We generated the base tables with `tpchgen-cli` instead of `dbgen`.
* We converted the refresh data from `dbgen`'s flat files to Parquet before the benchmark.
* The initial database load is not part of the reported results.
* We did not run the ACID tests.
* We report the runtimes of the power test and the throughput test instead of the composite metrics defined by the specification.
* We summarize three runs (after a discarded warmup run) using their mean instead of reporting the lower of two runs.

## Benchmark Runs and Results

We performed an initial warmup run and discarded its result.
Then, we conducted three complete runs in sequence.
For each run, we report two metrics, where lower values are better:

* **Power test:** the geometric mean of the runtimes of the 22 queries and the 2 refresh functions.
* **Throughput test:** the total runtime of the throughput test, which runs 7 query streams concurrently.

To summarize the three runs, we take the geometric mean of the power test results and the arithmetic mean of the throughput test results.

### Power Test

Geometric mean of the query and refresh runtimes in seconds:

| CPU                |   NVIDIA Vera |   NVIDIA Vera |  Intel Xeon 6 |  Intel Xeon 6 |
| ------------------ | ------------: | ------------: | ------------: | ------------: |
| DuckDB             |         1.5.5 |   2.0.0-alpha |         1.5.5 |   2.0.0-alpha |
| Run 1              |       1.457 s |       1.209 s |       2.319 s |       1.862 s |
| Run 2              |       1.571 s |       1.155 s |       2.302 s |       1.953 s |
| Run 3              |       1.466 s |       1.202 s |       2.243 s |       1.912 s |
| **Geometric mean** |   **1.497 s** |   **1.188 s** |   **2.288 s** |   **1.909 s** |

### Throughput Test

Total runtime of the throughput test in seconds:

| CPU                 |   NVIDIA Vera |   NVIDIA Vera |  Intel Xeon 6 |  Intel Xeon 6 |
| ------------------- | ------------: | ------------: | ------------: | ------------: |
| DuckDB              |         1.5.5 |   2.0.0-alpha |         1.5.5 |   2.0.0-alpha |
| Run 1               |      221.26 s |      174.79 s |      318.54 s |      238.30 s |
| Run 2               |      222.51 s |      176.26 s |      299.77 s |      249.76 s |
| Run 3               |      220.94 s |      178.22 s |      317.68 s |      234.49 s |
| **Arithmetic mean** |  **221.57 s** |  **176.42 s** |  **312.00 s** |  **240.85 s** |

### Findings

The run-to-run variation is small: within each configuration, the three runs differ by at most 8%.
The results show two key findings.
First, the Vera platform outperforms the x86 baseline (Intel Xeon 6) with both DuckDB versions: it is 1.53–1.61× faster in the power test and 1.37–1.41× faster in the throughput test.
Second, DuckDB 2.0.0-alpha is 1.20–1.30× faster than DuckDB 1.5.5 on both CPUs – and this is something all users will benefit from once [DuckDB 2.0.0 is out]({% link release_calendar.md %}).

> Update DuckDB 2.0.0 [is out]({% post_url 2026-10-21-announcing-duckdb-200 %})!

We attribute Vera's performance advantage compared to the x86 baseline to three key factors.
First, the high memory bandwidth enables fast scans.
Second, combined with low memory latency, it keeps the cores continuously occupied during processing.
Finally, the Olympus cores' large caches allow efficient access to the hash tables built during aggregations and joins.

We are looking forward to continuing this benchmark by using DuckDB 2.0.0's stable build, running on the full dual-socket setup, and incorporating different benchmarks.
