---
layout: post
title: "Rethinking Analytical Processing in the GPU Era"
author: "Bobbi Yogatama, Yifei Yang, Kevin Kristensen, Devesh Sarda, Abigale Kim, Adrian Cockcroft, Yu Teng, Joshua Patterson, Gregory Kimball, Wes McKinney, Weiwei Gong, Xiangyao Yu"
thumb: "/images/library/thumbs/arxiv.svg"
image: "/images/library/thumbs/arxiv.png"
thirdparty: true
excerpt: ""
---

[Paper (preprint PDF)](https://arxiv.org/abs/2508.04701)

Published on arXiv in 2025

## Abstract

The era of GPU-powered data analytics has arrived. In this paper, we argue that recent advances in hardware (e.g., larger GPU memory, faster interconnect and IO, and declining cost) and software (e.g., composable data systems and mature libraries) have removed the key barriers that have limited the wider adoption of GPU data analytics. We present Sirius, a prototype open-source GPU-native SQL engine that offers drop-in acceleration for diverse data systems. Sirius treats GPU as the primary engine and leverages libraries like libcudf for high-performance relational operators. It provides drop-in acceleration for existing databases by leveraging the standard Substrait query representation, replacing the CPU engine without changing the user-facing interface. On TPC-H, Sirius achieves 7x speedup when integrated with DuckDB in a single node at the same hardware rental cost, and up to 12.5x speedup when integrated with Apache Doris in a distributed setting.
