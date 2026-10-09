---
layout: post
title: "TurboLynx: Schemaless Graph Engine Strikes Back for General-Purpose Analytics"
authors:
  - Taesung Lee
  - Jaehyun Ha
  - Byungchul Tak
  - Wook-Shin Han
tag: paper
category: community
excerpt: ""
venue: "VLDB 2026"
---

| | |
|-------|-------|
| **Paper** | [TurboLynx: Schemaless Graph Engine Strikes Back for General-Purpose Analytics (PDF)](https://www.vldb.org/pvldb/vol19/p1250-han.pdf) |
| **Implementation** | [Code](https://github.com/turbolynx-dslab/TurboLynx) |
| **Venue** | VLDB 2026 |

## Abstract

Graph database management systems (GDBMSes) are widely adopted for their efficient handling of graph traversal queries that capture complex relationships. Recently, a class of modern GDBMSes appeared that were designed to offer explicit support for schemaless property graph models (PGMs), providing users with a high degree of flexibility. However, GDBMSes in this class often suffer from performance bottlenecks in analytical database queries—typically involving operations such as group-by and aggregation. We argue that a major cause is that schemaless processing is not treated as a primary design requirement across the storage, query-processing, and optimization layers. To address this, we propose TurboLynx, a novel graph analytics engine that holistically integrates the schemaless property at every layer of the system—from storage to query processing and optimization. TurboLynx organizes graph data into cost-based clusters, called graphlets, and stores them in a columnar format. By adopting a graphlet-aware query optimizer and processor, TurboLynx efficiently handles both graph traversal and analytical workloads in a single system. Our comprehensive evaluation on LDBC SNB Interactive, TPC-H, and DBpedia demonstrates that TurboLynx outperforms state-of-the-art GDBMSes by up to 183.9× and leading RDBMSs by up to 41.27×.
