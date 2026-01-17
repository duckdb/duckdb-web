---
layout: post
title: "Flexible I/O for Database Management Systems with xNVMe"
author: "Emil Houlborg, Andreas Nicolaj Tietgen, Simon A. F. Lund, Marcel Weisgut, Tilmann Rabl, Javier González, Vivek Shah, Pınar Tözün"
thumb: "/images/library/thumbs/cidr.svg"
image: "/images/library/thumbs/cidr.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "CIDR 2026"
---

[Paper (PDF)](https://vldb.org/cidrdb/papers/2026/p6-houlborg.pdf)

Venue: CIDR 2026

## Abstract

Storage hardware has undergone a sea change over the last five decades, transitioning from tape to HDDs to SSDs, with increasing capacities and bandwidth at diminishing costs. The advent of NVMe SSDs almost fifteen years ago shifted the performance cost tradeoff between memory and storage toward the storage end. In this work, we propose to leverage the xNVMe framework to offer a more flexible storage I/O backend for database systems. To evaluate this proposal, we integrate xNVMe into DuckDB by adding a new filesystem to DuckDB called nvmefs. We demonstrate that with nvmefs, DuckDB can now use state-of-the-art I/O backends such as IO Passthru and SPDK in addition to a wider variety of SSD types such as FDP SSDs, without requiring intrusive code changes.
