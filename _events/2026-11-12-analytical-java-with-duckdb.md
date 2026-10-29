---
layout: post
title: "Analytical Java with DuckDB"
authors:
  - Geertjan Wielenga
excerpt: ""
tag: talk
category: community
location: "Pathé Ede, Ede"
---

Geertjan Wielenga will give a talk at [J-Fall 2026](https://jfall.nl/), the Dutch Java conference organized by the NLJUG. The talk is scheduled for 4:55 PM CET on November 12, 2026, in Room 8. See the [J-Fall timetable](https://jfall.nl/timetable-2026/) for the full program.

## Venue

Pathé Ede, [Laan der Verenigde Naties 150, 6716 JE Ede, The Netherlands](https://www.google.com/maps/search/?api=1&query=Path%C3%A9%20Ede%2C%20Laan%20der%20Verenigde%20Naties%20150%2C%20Ede).

## Abstract

Your Java service just needs to answer a few analytical questions: top products this month, p95 latency per region, a quick join between a CSV export and a Parquet dump from the data team. The usual answers are to hammer your transactional database with `GROUP BY`s it was never designed for, ship the data off to a warehouse and wait, or write the aggregation by hand in streams. But did you know that there's another option that runs inside your JVM…

DuckDB is a free open source in-process analytical database: columnar, vectorized, zero infrastructure, and available to Java through a plain JDBC driver.

In this session, we'll use it to query Parquet, CSV and JSON files directly, run analytical SQL over in-memory data, and push results straight into Java records and Apache Arrow.

Along the way, we'll look at where it beats a traditional RDBMS, where it doesn't, and how it fits into your services, batch jobs, tests and CLIs… without any new operational setup or infrastructure.
