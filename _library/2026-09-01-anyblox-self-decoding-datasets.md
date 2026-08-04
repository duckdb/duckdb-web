---
layout: post
title: "AnyBlox: A Framework for Self-Decoding Datasets"
author: "Mateusz Gienieczko, Maximilian Kuschewski, Thomas Neumann, Viktor Leis, Jana Giceva"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "VLDB 2025"
---

| | |
|-------|-------|
| **Paper** | [AnyBlox: A Framework for Self-Decoding Datasets (PDF)](https://www.vldb.org/pvldb/vol18/p4017-gienieczko.pdf) |
| **Implementation** | [Code](https://github.com/AnyBlox/vldb-2025) |
| **Venue** | VLDB 2025 |

## Abstract

Research advancements in storage formats continuously produce more efficient encodings and better compression rates. Despite this, new formats are not adopted due to high implementation cost and existing formats cannot evolve because they need to maintain compatibility across systems. Can this problem be solved by introducing a new abstraction? We answer affirmatively with AnyBlox, a framework for reading arbitrary datasets using lightweight WebAssembly decoders bundled with the data. By decoupling decoders from both systems and file format specifications, AnyBlox allows transparent format evolution, instance-optimized encodings, and enables mainstream adoption of research advancements. It integrates seamlessly with modern systems like DuckDB, Spark, and Umbra, while delivering solid performance and security guarantees.
