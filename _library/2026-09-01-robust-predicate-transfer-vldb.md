---
layout: post
title: "Robust Predicate Transfer with Dynamic Execution"
author: "Yiming Qiao, Peter Boncz, Huanchen Zhang"
tags: ["Paper"]
category: community
excerpt: ""
pill: "VLDB 2026"
published: false
---

| | |
|-------|-------|
| **Paper** | [Robust Predicate Transfer with Dynamic Execution (PDF)](https://yimingqiao.github.io/files/rpt_plus.pdf) |
| **Implementation** | [Code](https://github.com/embryo-labs/dynamic-predicate-transfer) |
| **Venue** | VLDB 2026 |

## Abstract

Efficient join query execution remains a key challenge in modern database systems. Although a recent method, Robust Predicate Transfer (RPT), improves robustness against suboptimal join orders, it introduces significant overhead from redundant filter creation and inefficient data scanning. We present RPT+ that addresses these issues through three key improvements. First, we propose asymmetric transfer plans to reduce redundant Bloom filter constructions. Second, we design cascade filters to improve data scanning efficiency by enabling both block-level skipping and tuple-level filtering. Third, we introduce dynamic pipelines to allow runtime filter creation and transfer plan adjustment. We implemented RPT+ in DuckDB (v1.3.0) and evaluated it across multiple benchmarks, including the Join Order Benchmark (JOB), SQLStorm, TPC-H, and Appian. Compared to the baseline DuckDB, RPT+ achieves speedups of 1.47× on JOB, 1.28× on SQLStorm, 1.17× on TPC-H, and 1.01× on Appian. Importantly, it avoids the significant performance regressions observed with the original RPT. These results demonstrate that RPT+ not only improves query performance but also maintains the robustness of RPT across diverse workloads.
