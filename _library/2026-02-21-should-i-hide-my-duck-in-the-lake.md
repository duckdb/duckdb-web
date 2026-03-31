---
layout: post
title: "Should I Hide My Duck in the Lake?"
author: "Jonas Dann, Gustavo Alonso"
thumb: "/images/library/thumbs/arxiv.svg"
image: "/images/library/thumbs/arxiv.jpg"
tags: ["Paper"]
category: community
excerpt: ""
pill: "arXiv"
---

| | |
|-------|-------|
| **Paper** | [Should I Hide My Duck in the Lake? (preprint PDF)](https://arxiv.org/pdf/2602.18775.pdf) |
| **Published** | arXiv, 2026 |

## Abstract

Data lakes spend a significant fraction of query execution time on scanning data from remote storage. Decoding alone accounts for 46% of runtime when running TPC-H directly on Parquet files. To address this bottleneck, we propose a vision for a data processing SmartNIC for the cloud that sits on the network datapath of compute nodes to offload decoding and pushed-down operators, effectively hiding the cost of querying raw files. Our experimental estimations with DuckDB suggest that by operating directly on pre-filtered data as delivered by a SmartNIC, significantly smaller CPUs can still match query throughput of traditional setups.
