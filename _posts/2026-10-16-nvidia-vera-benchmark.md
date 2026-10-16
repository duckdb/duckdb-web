---
layout: post
title: "Benchmarking DuckDB v2.0-dev on NVIDIA Vera"
authors:
  - Gábor Szárnyas
excerpt: We put NVIDIA's new Vera CPU through its paces using the full TPC-H workload on scale factor 1,000.
tag: benchmark
thumb: "/images/blog/thumbs/nvidia-vera-benchmark.svg"
image: "/images/blog/thumbs/nvidia-vera-benchmark.png"
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

To see how this new hardware performs, we ran the full TPC-H benchmark (not just the read queries!) on scale factor 1,000.
Our setup included two server platforms: an x86 baseline (Intel Xeon 6) and NVIDIA Vera.

## Environment

### System Setup

Both machines ran Ubuntu 26.04.
Their hardware included 768 GB of memory and a single NVMe SSD with 3+ TB of storage, formatted as ext4.
At the time of writing, DuckDB v2.0 was [not released yet]({% post_url 2026-09-02-try-duckdb-20-alpha %}), so we used a [preview build]({% link install/index.html %}?version=preview), `1.6.0.dev379`.

To run the experiments, we used the [`duckdb-tpch` benchmark harness](https://github.com/duckdb/duckdb-tpch/).
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

> Tip To generate the large-scale TPC-H dataset efficiently,
> the repository uses the wonderful [`tpchgen-cli` tool](https://pypi.org/project/tpchgen-cli/),
> a parallel Rust rewrite of the TPC-H data generator.
> It also uses the old generator to produce update and query streams.

This workload is relatively large-scale (SF1,000) and highly concurrent during the throughput run.
To get the best performance out of DuckDB, we set the following flags:

```sql
SET block_allocator_memory = '500G';
SET allocator_background_threads = true;
```

### x86 Baseline: Intel Xeon 6

The x86 baseline setup used an Intel Xeon 6 CPU.
The CPU had 96 cores with [hyper-threading](https://en.wikipedia.org/wiki/Hyper-threading),
yielding 192 threads.
However, we found that DuckDB performs best when using 96 threads, so we configured it accordingly:

```sql
SET threads = 96;
```

### NVIDIA Vera

The second machine had the NVIDIA Vera CPU, which packs 88 cores with [Spatial Multithreading](https://developer.nvidia.com/blog/inside-nvidia-vera-cpu-olympus-cores-built-for-maximum-single-threaded-performance-in-agentic-ai/).
We conducted the benchmark on a dual-socket system but restricted DuckDB to a single socket using the `numactl` command:

```bash
numactl --cpunodebind=0 --membind=0 python3 benchmark.py
```

We also pinned the number of threads:

```sql
SET threads = 88;
```

## Benchmark Runs and Results

We performed an initial warmup run and discarded its result.
Then, we conducted three complete runs in sequence and took the median value of the _QphH@Size_ composite scores:

|                  | x86 QphH@Size    | Vera QphH@Size   |
| ---------------- | ---------------- | ---------------- |
| Run 1            | 2,120,588.82     | 3,073,292.99     |
| Run 2            | 2,022,795.01     | 3,131,306.27     |
| Run 3            | 2,109,782.19     | 3,052,102.87     |
| **Median score** | **2,109,782.19** | **3,073,292.99** |

The results show that the Vera platform has a 46% performance advantage on TPC-H SF1,000 over the x86 baseline (Intel Xeon 6).
In fact, if we were to audit these results through the official TPC-H channels, both would stand a chance to be in the top 3 among the [TPC-H Top Performance Results](https://www.tpc.org/tpch/results/tpch_perf_results5.asp?resulttype=noncluster&version=4) on SF1,000.

We attribute the performance advantage of Vera to three key factors.
First, the high memory bandwidth enables fast scans.
Second, combined with low memory latency, it keeps the cores continuously occupied during processing.
Finally, the Olympus cores' large caches allow efficient access to the hash tables built during aggregations and joins.

We are looking forward to continuing this benchmark by using DuckDB v2.0.0's stable build, running on the full dual-socket setup and incorporating different benchmarks.
