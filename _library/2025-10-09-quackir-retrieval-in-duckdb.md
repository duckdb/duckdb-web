---
layout: post
title: "QuackIR: Retrieval in DuckDB and Other Relational Database Management Systems"
author: "Yijun Ge, Zijian Chen, Jimmy Lin"
thumb: "/images/science/thumbs/emnlp-2025.svg"
image: "/images/science/thumbs/emnlp-2025.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://cs.uwaterloo.ca/~jimmylin/publications/ge-etal-2025-quackir.pdf)

Venue: EMNLP 2025

## Abstract

Enterprises today are increasingly compelled to adopt dedicated vector databases for retrievalaugmented generation (RAG) in applications based on large language models (LLMs). As a potential alternative for these vector databases, we propose that organizations leverage existing relational databases for retrieval, which many have already deployed in their enterprise data lakes, thus minimizing additional complexity in their software stacks. To demonstrate the simplicity and feasibility of this approach, we present QuackIR, an information retrieval (IR) toolkit built on relational database management systems (RDBMSes), with integrations in DuckDB, SQLite, and PostgreSQL. Using QuackIR, we benchmark the sparse and dense retrieval capabilities of these popular RDBMSes and demonstrate that their effectiveness is comparable to baselines from established IR toolkits. Our results highlight the potential of relational databases as a simple option for RAG scenarios due to their established widespread usage and the easy integration of retrieval abilities. Our implementation is available at [quackir.io](https://quackir.io).
