---
layout: post
title: "Parachute: Single-Pass Bi-Directional Information Passing"
author: "Mihail Stoian, Andreas Zimmerer, Skander Krid, Amadou Latyr Ngom, Jialin Ding, Tim Kraska, Andreas Kipf"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p3299-stoian.pdf)

Venue: VLDB 2025

## Abstract

Sideways information passing is a well-known technique for mitigating the impact of large build sides in a database query plan. As currently implemented in production systems, sideways information passing enables only a _uni-directional_ information flow, as opposed to instance-optimal algorithms, such as Yannakakis’. On the other hand, the latter require an additional pass over the input, which hinders adoption in production systems.

In this paper, we make a step towards enabling _single-pass bidirectional_ information passing during query execution. We achieve this by statically analyzing between which tables the information flow is blocked and by leveraging precomputed join-induced fingerprint columns on FK-tables. On the JOB benchmark, Parachute improves DuckDB v1.2’s end-to-end execution time without and with semi-join filtering by 1.54x and 1.24x, respectively, when allowed to use 15% extra space.
