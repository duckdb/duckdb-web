---
layout: post
title: "Selective Late Materialization in Modern Analytical Databases"
author: "Yihao Liu, Shaoxuan Tang, Yulong Hui, Hangrui Zhou, Huanchen Zhang"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "VLDB 2025"
---

|-------|-------|
| **Paper** | [Selective Late Materialization in Modern Analytical Databases (PDF)](https://people.iiis.tsinghua.edu.cn/~huanchen/publications/slm-vldb25.pdf) |
| **Implementation** | [Code](https://github.com/yhliu918/duckdb/tree/latest) |
| **Venue** | VLDB 2025 |

## Abstract

Late Materialization (LM) is a critical technique applied in traditional column stores to speed up analytical queries. However, with modern analytical databases evolved to incorporate a vectorized columnar execution engine, LM's benefits in I/O reduction and fast columnar query processing have diminished. In this paper, we redefine the concept of Late Materialization in the context of modern analytical databases and propose Selective Late Materialization (SLM) to allow each attribute in a query to choose its own materialization point that yields the minimum cost. SLM expands the solution space of the traditional materialization problem from one unified hard-coded binary decision (i.e., early or late) for all attributes to per attribute per query decisions. By integrating SLM into DuckDB, we show that SLM consistently outperforms the baselines of Early Materialization and Late Materialization by 14.7% and 8.9%, respectively, on average using the Join Order Benchmark (JOB), with up to 76.7% latency reduction for individual queries. We observe similar results for the TPC-DS benchmark.
