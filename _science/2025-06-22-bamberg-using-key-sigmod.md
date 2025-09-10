---
layout: post
title: "How DuckDB is USING KEY to Unlock Recursive Query Performance"
author: "Björn Bamberg, Denis Hirn, Torsten Grust"
thumb: "/images/science/thumbs/sigmod-2025.svg"
image: "/images/science/thumbs/sigmod-2025.png"
excerpt: ""
tags: ["Paper"]
---

[Paper (PDF)](https://db.cs.uni-tuebingen.de/publications/2025/using-key/how-duckdb-is-using-key-to-unlock-recursive-query-performance.pdf)

Venue: SIGMOD 2025

## Abstract

SQL’s _recursive common table expressions_ (CTEs) can express complex computations over tabular data. Their accumulative semantics—which collects all intermediate results in a union table—may incur substantial space and runtime overhead, however. This paper takes the recently proposed `USING KEY` variant of recursive CTEs as a starting point and demonstrates it as a production-ready feature in DuckDB. This CTE variant admits queries to selectively “overwrite” prior intermediate results, which ultimately leads to substantially smaller union tables and runtime savings. We present the changes we made to DuckDB to support this new CTE form and showcase the performance of the `USING KEY` variant using the LDBC graph instances. The demonstration features a fully functional implementation of `USING KEY` in a DuckDB instance, pre-loaded with LDBC graphs, and a large set of queries that demonstrate the benefits. The demonstration will be interactive, allowing attendees to play with sample SQL queries and data.

## Implementation

`USING KEY` is has been implemented in mainline DuckDB v1.3.0.
For details on how to use it, read the [documentation]({% link docs/stable/sql/query_syntax/with.md %}) and the [announcement blog post]({% post_url 2025-05-23-using-key %}).
