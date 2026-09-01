---
layout: post
title: "Workload-Aware Incremental Reclustering in Cloud Data Warehouses"
author: "Yipeng Liu, Renfei Zhou, Jiaqi Yan, Huanchen Zhang"
thumb: "/images/library/thumbs/sigmod.svg"
image: "/images/library/thumbs/sigmod.jpg"
tags: ["Paper"]
category: community
excerpt: ""
pill: "SIGMOD 2026"
---

| | |
|-------|-------|
| **Paper** | [Workload-Aware Incremental Reclustering in Cloud Data Warehouses (PDF)](https://dl.acm.org/doi/pdf/10.1145/3802127) |
| **Venue** | SIGMOD 2026 |

## Abstract

Modern cloud data warehouses store data in micro-partitions and rely on metadata (e.g., zonemaps) for efficient data pruning during query processing. Maintaining data clustering in a large-scale table is crucial for effective data pruning. Existing automatic clustering approaches lack the flexibility required in dynamic cloud environments with continuous data ingestion and evolving workloads. This paper advocates a clean separation between reclustering policy and clustering-key selection. We introduce the concept of boundary micro-partitions that sit on the boundary of query ranges. We then present WAIR, a workload-aware algorithm to identify and recluster only boundary micro-partitions most critical for pruning efficiency. WAIR achieves near-optimal (with respect to fully sorted table layouts) query performance but incurs significantly lower reclustering cost with a theoretical upper bound. We further implement the algorithm into a prototype reclustering service and evaluate on standard benchmarks (TPC-H, DSB) and a real-world workload. Results show that WAIR improves query performance and reduces the overall cost compared to existing solutions.
