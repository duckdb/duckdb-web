---
layout: post
title: "Adoption Metrics and Benchmark Results for DuckDB v1.4 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/benchmark-results-1-4-lts.svg"
image: "/images/blog/thumbs/benchmark-results-1-4-lts.png"
excerpt: "The DuckDB landing page makes some strong claims about DuckDB's popularity. In this blog post, we these claims."
tags: ["release"]
---

## #1 on ClickBench

On October 9, 2025, DuckDB's in-memory variant hit #1 on the popular [ClickBench database benchmark](https://benchmark.clickhouse.com/):

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

This result was made possible due several [performance optimizations]({% post_url 2025-09-16-announcing-duckdb-140 %}#performance-and-optimizations) in DuckDB v1.4.

## #3 Most Admired System on Stack Overflow

In Stack Overflow's 2024 Developer Survey, DuckDB was named among the [**top-3 most admired database systems**](https://survey.stackoverflow.co/2024/technology#2-databases).
In the 2025 survey, it achieved position #4 (just 0.2% behind SQLite) but it made up for this by a significant increase in usage, which jumped from 1.4% in 2024 to 3.3% in 2025.

## 20+ Fortune-100 Companies Use DuckDB

We estimated the number of Fortune-100 companies who use DuckDB by cross-checking self-reported affiliations in the [DuckDB issue tracker](https://github.com/duckdb/duckdb/issues) against a list of Fortune-100 companies.

## 25M+ Downloads / Month

DuckDB's Python packages has almost 25 million monthly downloads on [PyPI alone](https://pypistats.org/packages/duckdb). This is complemented with the downloads of other popular clients such as the CLI, Go, Node.js, Java, R, Rust and so on.

## TPC-H SF 100,000

DuckDB is not only fast but it is also scalable. We have recently run the queries of the [TPC-H workload]({% link docs/stable/core_extensions/tpch.md %}) on the scale factor 100,000 dataset, which is equivalent to 100,000 GB of CSV files. Obviously, such a data set size requires _disk-based execution._

We ran the experiment on an [`i8g.48xlarge` EC2 instance](https://aws.amazon.com/ec2/instance-types/i8g/), which has 1.5 TB of RAM and 192 CPU cores (AWS Graviton4, Arm64). This instance has 12 NVMe SSD disks, each 3750 GB in size. We created a RAID-0 array from them to have a single 45 TB partition and formatted it using [XFS]({% link docs/stable/guides/performance/environment.md %}#local-disk).

We generated the dataset with the [tpchgen-rs](https://github.com/clflushopt/tpchgen-rs/) tool, a pure Rust implementation of the TPC-H generator. We configured the generator to produce chunks of Parquet files and loaded them into DuckDB. The final DuckDB database was about 27 TB in size (as a single file!).

DuckDB completed all 22 queries of the benchmark using its [larger-than-memory processing]({% post_url 2024-07-09-memory-management %}). For some queries, this required spilling _about 7 terabytes of data_ to disk.
The median query runtime was 1.19 hours and the geometric mean runtime was 1.13 hours.

We will publish a detailed write-up on this experiment in the coming weeks.
