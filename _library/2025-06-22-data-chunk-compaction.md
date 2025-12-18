---
layout: post
title: "Data Chunk Compaction in Vectorized Execution"
author: "Yiming Qiao, Huanchen Zhang"
thumb: "/images/library/thumbs/sigmod.svg"
image: "/images/library/thumbs/sigmod.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
---

[Paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3709676)

Venue: SIGMOD 2025

## Abstract

Modern analytical database management systems often adopt vectorized query execution engines that process columnar data in batches (i.e., data chunks) to minimize the interpretation overhead and improve CPU parallelism. However, certain database operators, especially hash joins, can drastically reduce the number of valid entries in a data chunk, resulting in numerous small chunks in an execution pipeline. These small chunks cannot fully enjoy the benefits of vectorized query execution, causing significant performance degradation. The key research question is when and how to compact these small data chunks during query execution. In this paper, we first model the chunk compaction problem and analyze the trade-offs between different compaction strategies. We then propose a learning-based algorithm that can adjust the compaction threshold dynamically at run time. To answer the ''how'' question, we propose a compaction method for the hash join operator, called logical compaction, that minimizes data movements when compacting data chunks. We implemented the proposed techniques in the state-of-the-art DuckDB and observed up to 63% speedup when evaluated using the Join Order Benchmark, TPC-H, and TPC-DS.
