---
layout: post
title: "Analytical Java with DuckDB"
authors:
  - Geertjan Wielenga
thumb: "/images/events/thumbs/jfall-2026.svg"
image: "/images/events/thumbs/jfall-2026.png"
excerpt: ""
tag: talk
category: core
venue: "J-Fall 2026"
redirect_from:
- /events/2026/11/12/analytical-java-with-duckdb/
---

|-------|-------|
| **Event** | [J-Fall 2026](https://jfall.nl/) |
| **Speaker** | Geertjan Wielenga |
| **Slide deck** | [Download](https://blobs.duckdb.org/slides/geertjan-wielenga-duckdb-jfall-2026.pdf) |

## Abstract

Your Java service just needs to answer a few analytical questions: top products this month, p95 latency per region, a quick join between a CSV export and a Parquet dump from the data team. The usual answers are to hammer your transactional database with `GROUP BY`s it was never designed for, ship the data off to a warehouse and wait, or write the aggregation by hand in streams. But did you know that there’s another option that runs inside your JVM…

DuckDB is a free open source in-process analytical database: columnar, vectorized, zero infrastructure, and available to Java through a plain JDBC driver.

In this session, we’ll use it to query Parquet, CSV, and JSON files directly, run analytical SQL over in-memory data, and push results straight into Java records and Apache Arrow.

Along the way, we’ll look at where it beats a traditional RDBMS, where it doesn’t, and how it fits into your services, batch jobs, tests, and CLIs… without any new operational setup or infrastructure.
