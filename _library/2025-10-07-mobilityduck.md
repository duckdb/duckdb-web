---
layout: post
title: "MobilityDuck: Mobility Data Management with DuckDB"
author: "Nhu Ngoc Hoang, Ngoc Hoa Pham, Viet Phuong Hoang, Esteban Zimányi"
thumb: "/images/library/thumbs/arxiv.svg"
image: "/images/library/thumbs/arxiv.jpg"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "arXiv"
---

[Paper (preprint PDF)](https://arxiv.org/pdf/2510.07963.pdf)

Published on arXiv in 2025

## Abstract

The analytics of spatiotemporal data is increasingly important for mobility analytics. Despite extensive research on moving object databases (MODs), few systems are ready on production or lightweight enough for analytics. MobilityDB is a notable system that extends PostgreSQL with spatiotemporal data, but it inherits complexity of the architecture as well. In this paper, we present MobilityDuck, a DuckDB extension that integrates the MEOS library to provide support spatiotemporal and other temporal data types in DuckDB. MobilityDuck leverages DuckDB's lightweight, columnar, in-memory executable properties to deliver efficient analytics. To the best of our knowledge, no existing in-memory or embedded analytical system offers native spatiotemporal types and continuous trajectory operators as MobilityDuck does. We evaluate MobilityDuck using the BerlinMOD-Hanoi benchmark dataset and compare its performance to MobilityDB. Our results show that MobilityDuck preserves the expressiveness of spatiotemporal queries while benefiting from DuckDB's in-memory, columnar architecture.
