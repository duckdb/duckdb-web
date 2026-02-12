---
layout: post
title: "RISC-V Meets RDBMS: An Experimental Study of Database Performance on an Open Instruction Set Architecture"
author: "Yizhe Zhang, Zhengyi Yang, Bocheng Han, Haoran Ning, Xin Cao, John Shepherd, Guanfeng Liu"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "ADMS 2025"
---

[Paper (PDF)](https://www.vldb.org/2025/Workshops/VLDB-Workshops-2025/ADMS/ADMS25-06.pdf)

Venue: ADMS 2025 (Accelerating Analytics and Data Management Systems Using Modern Processor and Storage Architectures)

## Abstract

RISC-V, an open and extensible instruction set architecture, has gained significant attention in both academia and industry for its potential to reshape processor design. Among its numerous instruction set architecture (ISA) extensions, RISC-V Vector Extension (RVV) Version 1.0 introduces a novel approach to scalable and flexible vector computation, which holds particular promise for data-intensive workloads such as those found in modern database systems. In this paper, we systematically explore the implications of RISC-V architectural features, especially RVV 1.0, for database execution engines. We begin with an overview of the RISC-V ISA and its vector and scalar extensions relevant to data processing, then evaluate open source database systems compiled and executed on RISC-V platforms using industry-standard benchmarks such as TPC-H to measure performance and identify bottlenecks. Our experiments span various RISC-V ISA extensions, including the V, Zfh, Zknd, and compressed instruction sets, and assess their impact on execution speed, memory usage, and binary size. Our results demonstrate that mature existing database systems do not effectively leverage RISC-V ISA capabilities, with most extensions providing minimal performance improvements through change of database compilation parameters: the Vector Extension yields a performance improvement of less than 5%, while some extensions like Zknd can reduce performance by up to 32%. However, manually optimized RVV implementations achieve up to 10× speedups for specific query types, indicating substantial untapped potential. These findings reveal both the current limitations and future opportunities of RISC-V for database workloads, demonstrating that realizing the architecture’s full potential requires hardware-aware optimization beyond current compiler capabilities and providing guidance for future system designs and hardware-software co-optimization.
