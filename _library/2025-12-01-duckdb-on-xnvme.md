---
layout: post
title: "DuckDB on xNVMe"
author: "Marius Ottosen, Magnus Keinicke Parlo, Philippe Bonnet"
thumb: "/images/library/thumbs/arxiv.svg"
image: "/images/library/thumbs/arxiv.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (preprint PDF)](https://arxiv.org/abs/2512.01490)

[Implementation (fork)](https://github.com/Ma-Master-DK/duckdb)

Published on arXiv in 2025

## Abstract

DuckDB is designed for portability. It is also designed to run anywhere, and possibly in contexts where it can be specialized for performance, e.g., as a cloud service or on a smart device. In this paper, we consider the way DuckDB interacts with local storage. Our long term research question is whether and how SSDs could be co-designed with DuckDB. As a first step towards vertical integration of DuckDB and programmable SSDs, we consider whether and how DuckDB can access NVMe SSDs directly. By default, DuckDB relies on the POSIX file interface. In contrast, we rely on the xNVMe library and explore how it can be leveraged in DuckDB. We leverage the block-based nature of the DuckDB buffer manager to bypass the synchronous POSIX I/O interface, the file system and the block manager. Instead, we directly issue asynchronous I/Os against the SSD logical block address space. Our preliminary experimental study compares different ways to manage asynchronous I/Os atop xNVMe. The speed-up we observe over the DuckDB baseline is significant, even for the simplest scan query over a TPC-H table. As expected, the speed-up increases with the scale factor, and the Linux NVMe passthru improves performance. Future work includes a more thorough experimental study, a flexible solution that combines raw NVMe access and legacy POSIX file interface as well the co-design of DuckDB and SSDs.
