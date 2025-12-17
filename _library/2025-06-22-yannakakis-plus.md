---
layout: post
title: "Yannakakis+: Practical Acyclic Query Evaluation with Theoretical Guarantees"
author: "Qichen Wang, Bingnan Chen, Binyang Dai, Ke Yi, Feifei Li, Liang Lin"
thumb: "/images/library/thumbs/sigmod-2025.svg"
image: "/images/library/thumbs/sigmod-2025.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3725423)

Venue: SIGMOD 2025

## Abstract

Acyclic conjunctive queries form the backbone of most analytical workloads, and have been extensively studied in the literature from both theoretical and practical angles. However, there is still a large divide between theory and practice. While the 40-year-old Yannakakis algorithm has strong theoretical running time guarantees, it has not been adopted in real systems due to its high hidden constant factor. In this paper, we strive to close this gap by proposing Yannakakis+, an improved version of the Yannakakis algorithm, which is more practically efficient while preserving its theoretical guarantees. Our experiments demonstrate that Yannakakis+ consistently outperforms the original Yannakakis algorithm by 2x to 5x across a wide range of queries and datasets.

Another nice feature of our new algorithm is that it generates a traditional DAG query plan consisting of standard relational operators, allowing Yannakakis+ to be easily plugged into any standard SQL engine. Our system prototype currently supports four different SQL engines (DuckDB, PostgreSQL, SparkSQL, and AnalyticDB from Alibaba Cloud), and our experiments show that Yannakakis+ is able to deliver better performance than their native query plans on 160 out of the 162 queries tested, with an average speedup of 2.41x and a maximum speedup of 47,059x.
