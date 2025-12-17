---
layout: post
title: "Adaptive Factorization Using Linear-Chained Hash Tables"
author: "Paul Groß, Daniel ten Wolde, Peter Boncz"
thumb: "/images/library/thumbs/cidr-2025.svg"
image: "/images/library/thumbs/cidr-2025.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://vldb.org/cidrdb/papers/2025/p21-gro.pdf)

Venue: CIDR 2025

## Abstract

We introduce factorized aggregations and worst-case optimal joins in DuckDB with an adaptive mechanism that only uses them when they enhance query performance. This builds on the adoption of a new hash table design (“Linear-Chained”) for equi-joins. Our first insight is that the collision-free chains of this new design enable efficient factorized and worst-case optimal processing. We further defer the decision to use factorization and worst-case optimal joins from optimization to runtime. Our second insight is that we can obtain accurate statistics, even if the join inputs lack these (e.g. because they are sub-queries or Parquet files), by leveraging runtime heuristics and constructing efficient _on-the-fly sketches,_ during the hash join build. Finally, we show that machine learning models using these metrics can achieve close to optimal performance with a high accuracy. Furthermore, we propose heuristic-based approaches that offer comparable performance to these models, while relying on cheaper to obtain run-time statistics and being more explainable.
