---
layout: post
title: "BIRNE: Mixed-paradigm Workload Execution in SQL Engines"
author: "Tim Fischer, Denis Hirn"
thumb: "/images/library/thumbs/dbpl.svg"
image: "/images/library/thumbs/dbpl.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3735106.3736535)

Venue: DBPL at SIGMOD 2025

## Abstract

Previous work on UDF compilation strategies has proven that SQL engines can be used as efficient execution environments for imperative workloads over relational data. In this paper, we present BIRNE, a major extension of our Flummi compiler, with support for mixed-paradigm workloads, such that database-resident programs can be expressed using both imperative and functional constructs. To this end, we introduce a specialized form of control flow graphs that we call control flow plans, that allow us to express the control flow and data dependencies, such that we can use plain SQL as the target for compilation. We show that this approach allows us to compile a wide range of workloads into a single SQL query, and that it can outperform existing approaches in terms of overall runtime in many cases.
