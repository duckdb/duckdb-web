---
layout: post
title: "Robust External Hash Aggregation in the Solid State Age"
author: "Laurens Kuiper, Peter A. Boncz, Hannes Mühleisen"
tags: ["Paper"]
thirdparty: false
excerpt: ""
pill: "ICDE 2024"
---

[Paper (PDF)](https://duckdb.org/pdf/ICDE2024-kuiper-boncz-muehleisen-out-of-core.pdf)

Venue: ICDE 2024

## Abstract

Analytical database systems offer high-performance in-memory aggregation. If there are many unique groups, temporary query intermediates may not fit RAM, requiring the use of external storage. However, switching from an in-memory to an external algorithm can degrade performance sharply. We revisit external hash aggregation on modern hardware, aiming instead for robust performance that avoids a “performance cliff” when memory runs out. To achieve this, we introduce two techniques for handling temporary query intermediates. First, we propose unifying the memory management of temporary and persistent data. Second, we propose using a page layout that can be spilled to disk despite being optimized for main memory performance. These two techniques allow operator implementations to process largerthan-memory query intermediates with only minor modifications. We integrate these into DuckDB’s parallel hash aggregation. Experimental results show that our implementation gracefully degrades performance as query intermediates exceed the available memory limit, while main memory performance is competitive with other analytical database systems.
