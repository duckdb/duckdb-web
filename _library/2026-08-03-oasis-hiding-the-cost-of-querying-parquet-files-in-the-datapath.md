---
layout: post
title: "Oasis: Hiding the Cost of Querying Parquet Files in the Datapath"
authors:
  - Jonas Dann
  - Luca Tagliavini
  - Gustavo Alonso
tag: paper
category: community
excerpt: ""
venue: "arXiv"
---

| | |
|-------|-------|
| **Paper** | [Oasis: Hiding the Cost of Querying Parquet Files in the Datapath (preprint PDF)](https://arxiv.org/pdf/2608.02268.pdf) |
| **Published** | arXiv, 2026 |

## Abstract

Cloud-native database systems disaggregate compute and storage resources to improve cost efficiency over traditional monolithic architectures through elasticity and resource pooling. Studies of production data warehouse workloads show that scans (including round trips to storage) account for roughly half of total query runtime. Data lakes and lakehouses amplify this bottleneck through per-query decoding of storage-optimized, compressed file formats such as Parquet. As storage and network bandwidth continue to outpace CPU cost-performance, the CPU cycles spent on decoding increasingly undermine the cloud's cost-efficiency promise. This has led to a wave of specialization across the stack with custom hardware at cloud-vendor scale at the extreme end. We build on this trend and present Oasis, a data-processing SmartNIC that offloads Parquet decoding into the network datapath as a custom hardware accelerator. Oasis features a hardware decoder architecture, software abstraction layer, and end-to-end integration with DuckDB. Our evaluation shows that Oasis hides the cost of Parquet decoding behind the network datapath with minimal overhead, overlapping the scan with the remainder of the query execution. In the best case, this almost doubles DuckDB query throughput.
