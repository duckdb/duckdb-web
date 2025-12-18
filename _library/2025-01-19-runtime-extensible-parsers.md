---
layout: post
title: "Runtime-Extensible Parsers"
author: "Hannes Mühleisen, Mark Raasveldt"
thumb: "/images/library/thumbs/placeholder-duckdb.svg"
image: "/images/library/thumbs/placeholder-duckdb.jpg"
tags: ["Paper"]
thirdparty: false
excerpt: ""
pill: "CIDR"
---

[Paper (PDF)](https://vldb.org/cidrdb/papers/2025/p18-muhleisen.pdf)

Venue: CIDR 2025

## Abstract

Despite their central role in processing queries, parsers have not received any noticeable attention in the data systems space. State-of-the art systems are content with ancient old parser generators. These generators create monolithic, inflexible and unforgiving parsers that hinder innovation in query languages and frustrate users. We argue that parsers should be rewritten using modern abstractions like Parser Expression Grammars (PEG), which allow dynamic changes to the accepted query syntax and better error recovery. In this paper, we discuss how parsers could be re-designed using PEG, and validate our recommendations using experiments for both effectiveness and efficiency.

## Implementation

DuckDB's autocomplete is implemented using a PEG-based parser.
There is ongoing work to rewrite DuckDB's current PostgreSQL-based parser using a PEG-based parser.
