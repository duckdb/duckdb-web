---
layout: post
title: "MacBook Pro M1 Max (2021)"
date: 2025-10-09
author: "Gábor Szárnyas"
thumb: "/images/everywhere/thumbs/macbook-pro-14.jpg"
image: "/images/everywhere/thumbs/macbook-pro-14.jpg"
excerpt: ""
tags: ["PCs"]
thirdparty: false
---

DuckDB v1.4.4 on the 2021 MacBook Pro M1 Max with 64 GB RAM can complete all queries of the [TPC-DS workload]({% link docs/current/core_extensions/tpcds.md %}) on the SF1,000 dataset (which uses 1 TiB of space when stored in CSV format).
It does not require any further configuration (i.e., it uses the default number of threads and memory) and achieves a geometric mean runtime of 7.5 seconds.
