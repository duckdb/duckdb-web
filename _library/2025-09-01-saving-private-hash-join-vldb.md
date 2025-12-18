---
layout: post
title: Saving Private Hash Join
author: "Laurens Kuiper, Paul Groß, Peter Boncz, Hannes Mühleisen"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: false
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p2748-kuiper.pdf)

Venue: VLDB 2025

## Abstract

Modern analytical database systems offer high-performance in-memory joins. However, if the build side of a join does not fit in RAM, performance degrades sharply due to switching to traditional external join algorithms such as sort-merge. In streaming query execution, this problem is worsened if multiple joins are evaluated simultaneously, as the database system must decide how to allocate memory to each join, which can greatly affect performance.

We revisit larger-than-memory join processing on modern hardware, aiming for robust performance that avoids a “performance cliff” when memory runs out, even in query plans with many joins. To achieve this, we propose three techniques. First, an adaptive, external hash join algorithm that stores temporary data in a unified buffer pool that oversees temporary and persistent data. Second, an optimizer that creates expressions to compress columns at runtime, reducing the size of materialized temporary data. Third, a strategy for dynamically managing the memory of concurrent operators during query execution to reduce spilling.

We integrate these techniques into DuckDB and experimentally show that when processing memory-intensive join query plans, our implementation gracefully degrades performance as the space requirement exceeds the memory limit. This greatly increases the size of datasets that can be processed on economical hardware.

## Implementation

The techniques described in this paper are integrated in DuckDB v1.2.0.
