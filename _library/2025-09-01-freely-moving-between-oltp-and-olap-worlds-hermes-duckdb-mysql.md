---
layout: post
title: "Freely Moving Between the OLTP and OLAP Worlds: Hermes - an High-Performance OLAP Accelerator for MySQL"
author: "Tim Gubner, Rune Humborstad, Manyi Lu"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "VLDB"
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p5113-gubner.pdf)

Venue: VLDB 2025

## Abstract

Users often want to run analytics on their OLTP databases, to avoid costly and cumbersome Extract-Transform-Load (ETL) processes. Typically, analytical queries run rather slow on OLTP DBMS, making Hybrid Transaction/Analytic Processing (HTAP) solutions popular. One possible solution is to add an accelerator (for analytics) to the already existing OLTP DBMS.

Typically, analytical systems, especially for the cloud, focus on extremely large datasets ("exa-scale") and distributed query execution (across multiple machines). We argue that many customers do not have large enough datasets to justify expensive multi-node DBMSs. Compared to single-node systems, such multi-node systems typically come with a baseline drop in performance (but might scale), as they need to introduce data transfers across the network.

For this reason, we propose Hermes as cloud-native, but singlenode, accelerator for MySQL. Hermes speeds up analytical queries by, often 2-3, orders of magnitude and outperforms competing systems by up to 5× (including multi-node systems). We achieve this by keeping Hermes relatively lean and focusing on the core features required. In the paper we describe Hermes’ architecture, data storage and integration with MySQL as well as Hermes’ query engine. Importantly, Hermes provides the highest degree of data freshness. If data is not replicated yet, Hermes waits. The waiting times, however, are practically negligible (single digit vs. three digit milliseconds).

We evaluate Hermes on TPC-H as well as micro-benchmarks. Besides the aforementioned improvements, our replication mechanisms achieved high and stable throughput rates of up to 60k changes per second, leading to low waiting times.

In summary, Hermes is a lean accelerator for MySQL. Its singlenode design keeps costs for users low and performance high. Additionally, Hermes guaranteeing data freshness and compatibility with MySQL (both, Hermes and MySQL, return the same result).
