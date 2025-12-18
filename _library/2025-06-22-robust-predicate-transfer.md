---
layout: post
title: "Debunking the Myth of Join Ordering: Toward Robust SQL Analytics"
author: "Junyi Zhao, Kai Su, Yifei Yang, Xiangyao Yu, Paraschos Koutris, Huanchen Zhang"
thumb: "/images/library/thumbs/sigmod.svg"
image: "/images/library/thumbs/sigmod.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3725283)

Venue: SIGMOD 2025

## Abstract

Join order optimization is critical in achieving good query performance. Despite decades of research and practice, modern query optimizers could still generate inferior join plans that are orders of magnitude slower than optimal. Existing research on robust query processing often lacks theoretical guarantees on join-order robustness while sacrificing query performance. In this paper, we rediscover the recent Predicate Transfer technique from a robustness point of view. We introduce two new algorithms, LargestRoot and SafeSubjoin, and then propose Robust Predicate Transfer (RPT) that is provably robust against arbitrary join orders of an acyclic query. We integrated Robust Predicate Transfer with DuckDB, a state-of-the-art analytical database, and evaluated against all the queries in TPC-H, JOB, TPC-DS, and DSB benchmarks. Our experimental results show that RPT improves join-order robustness by orders of magnitude compared to the baseline. With RPT, the largest ratio between the maximum and minimum execution time out of random join orders for a single acyclic query is only 1.6x (the ratio is close to 1 for most evaluated queries). Meanwhile, applying RPT also improves the end-to-end query performance by ≈1.5x (per-query geometric mean). We hope that this work sheds light on solving the practical join ordering problem.
