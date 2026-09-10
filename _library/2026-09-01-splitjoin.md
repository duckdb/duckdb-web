---
layout: post
title: "One Join Order Does Not Fit All: Reducing Intermediate Results with Per-Split Query Plans"
author: "Yujun He, Hangdong Zhao, Simon Frisk, Yifei Yang, Kevin Kristensen, Paraschos Koutris, Xiangyao Yu"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "VLDB 2026"
---

| | |
|-------|-------|
| **Paper** | [One Join Order Does Not Fit All: Reducing Intermediate Results with Per-Split Query Plans (PDF)](https://www.vldb.org/pvldb/vol19/p2045-he.pdf) |
| **Implementation** | [Code](https://github.com/hyj2003/SplitJoin) |
| **Venue** | VLDB 2026 |

## Abstract

Minimizing intermediate results is critical for efficient multi-join query processing. Although the seminal Yannakakis algorithm offers strong guarantees for acyclic queries, cyclic queries remain an open challenge. In this paper, we propose SplitJoin, a framework that introduces split as a first-class query operator. By partitioning input tables into heavy and light parts, SplitJoin allows different data partitions to use distinct query plans with the goal of reducing intermediate sizes using existing binary join engines. We systematically explore the design space for split-based optimizations, including threshold selection, split strategies, and join ordering after splits. Implemented as a front-end to DuckDB and Umbra, SplitJoin achieves substantial improvements: on DuckDB, SplitJoin completes 66 social network queries (vs. 48 natively), achieving 1.8× faster runtime and 4.5× smaller intermediates on average (up to 14.8× and 74×, respectively); on Umbra, it completes 70 queries (vs. 56), achieving 1.3× speedups and 1.8× smaller intermediates on average (up to 11.6× and 33.1×, respectively).
