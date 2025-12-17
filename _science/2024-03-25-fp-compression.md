---
layout: post
title: "How to Make your Duck Fly: Advanced Floating Point Compression to the Rescue"
author: "Panagiotis Liakos, Katia Papakonstantinopoulou, Thijs Bruineman, Mark Raasveldt, Yannis Kotidis"
thumb: "/images/science/thumbs/edbt-2024.svg"
image: "/images/science/thumbs/edbt-2024.png"
excerpt: ""
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://openproceedings.org/2024/conf/edbt/paper-248.pdf)

## Abstract

The massive volumes of data generated in diverse domains, such as scientific computing, finance and environmental monitoring, hinder our ability to perform multidimensional analysis at high speeds and also yield significant storage and egress costs. Applying compression algorithms to reduce these costs is particularly suitable for column-oriented DBMSs, as the values of individual columns are usually similar and thus, allow for effective compression. However, this has not been the case for binary floating point numbers, as the space savings achieved by respective compression algorithms are usually very modest. We present here two lossless compression algorithms for floating point data, termed Chimp and Patas, that attain impressive compression ratios and greatly outperform state-of-the-art approaches. We focus on how these two algorithms impact the performance of DuckDB, a purpose-built embeddable database for interactive analytics. Our demonstration will showcase how our novel compression approaches _a)_ reduce storage requirements, and _b)_ improve the time needed to load and query data using DuckDB.

## Implementation

The Chimp and Patas compression algorithms are both supported in DuckDB.
