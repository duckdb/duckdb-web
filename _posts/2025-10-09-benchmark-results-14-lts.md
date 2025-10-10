---
layout: post
title: "Benchmark Results for DuckDB v1.4 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/benchmark-results-1-4-lts.svg"
image: "/images/blog/thumbs/benchmark-results-1-4-lts.png"
excerpt: "DuckDB v1.4 LTS is both fast and scalable. In in-memory mode, it is the fastest system on ClickBench. In disk-based mode, it can run complex analytical queries on a dataset equivalent to 100 TB on a single machine."
tags: ["release"]
---

## ClickBench

Today, DuckDB hit #1 on the popular [ClickBench database benchmark](https://benchmark.clickhouse.com/):

<img src="/images/blog/clickbench-top1-light.png"
     alt="ClickBench results as of October 9, 2025"
     width="800"
     class="lightmode-img"
     />
<img src="/images/blog/clickbench-top1-dark.png"
     alt="ClickBench results as of October 9, 2025"
     width="800"
     class="darkmode-img"
     />

This result was made possible due to a long line of performance optimizations, most recently the new [sort implementation]({% post_url 2025-09-24-sorting-again %}) in DuckDB v1.4.

## TPC-H SF100,000

DuckDB is not only fast but it is also scalable. We have recently run the queries of the [TPC-H workload]({% link docs/stable/core_extensions/tpch.md %}) on the SF100,000 dataset, which is equivalent to 100,000 GB of CSV files.

We ran the experiment on an [`i8g.48xlarge` EC2 instance](https://aws.amazon.com/ec2/instance-types/i8g/), which has 1.5 TB of RAM and 192 CPU cores (AWS Graviton4, Arm64). This instance has 12 NVMe SSD disks, each 3750 GB in size. We created a RAID-0 array from them to have a single 45 TB partition and formatted it using [XFS]({% link docs/stable/guides/performance/environment.md %}#local-disk).

We generated the dataset with the [tpchgen-rs](https://github.com/clflushopt/tpchgen-rs/) tool, a pure Rust implementation of the TPC-H generator. We configured the generator to produce chunks of Parquet files and loaded them into DuckDB. The final DuckDB database was about 27 TB in size (as a single file!).

DuckDB completed all 22 queries of the benchmark using its [larger-than-memory processing]({% post_url 2024-07-09-memory-management %}). For some queries, this required spilling _about 7 terabytes of data_ to disk.
The median query runtime was 1.19 hours and the geometric mean runtime was 1.13 hours.

We will publish a detailed write-up on this experiment in the coming weeks.
