---
layout: post
title: "Beyond Quacking: Deep Integration of Language Models and RAG into DuckDB"
author: "Anas Dorbani, Sunny Yasser, Jimmy Lin, Amine Mhedhbi"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p5415-mhedhbi.pdf)

Venue: VLDB 2025

## Abstract

Knowledge-intensive analytical applications retrieve context from both structured tabular data and unstructured free text documents for effective decision-making. Large language models (LLMs) have significantly simplified the prototyping of such retrieval and reasoning data pipelines. However, implementing them efficiently remains challenging and demands significant effort. Developers must often orchestrate heterogeneous systems, manage data movement, and handle low-level concerns such as LLM context management. To address these challenges, we introduce FlockMTL: an extension for DBMSs that integrates LLM capabilities and enables retrieval-augmented generation (RAG) within SQL. FlockMTL provides LLM-powered scalar and aggregate functions, enabling chained predictions over tuples. It further provides data fusion functions to support hybrid search. Drawing inspiration from the relational model, FlockMTL incorporates: (i) seamless optimizations such as batching and meta-prompting; and (ii) resource independence through novel SQL DDL abstractions: PROMPT and MODEL, introduced as first-class schema objects alongside TABLE.

## Implementation

FlockMTL is available as a [DuckDB community extension]({% link community_extensions/extensions/flockmtl.md %}).
