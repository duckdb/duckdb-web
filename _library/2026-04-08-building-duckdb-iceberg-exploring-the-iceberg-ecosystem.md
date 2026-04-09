---
layout: post
title: "Exploring the Iceberg Ecosystem with DuckDB-Iceberg"
author: "Tom Ebergen"
tags: ["Talk"]
thirdparty: false
highlighted: false
excerpt: ""
pill: "Iceberg Summit 2026"
---

|-------|-------|
| **Date** | {{ page.date | date: "%Y-%m-%d" }} |
| **Event** | [Iceberg Summit 2026](https://events.bizzabo.com/796372) |
| **Speaker** | Tom Ebergen (DuckDB Labs) |
| **Slide deck** | [Download](http://blobs.duckdb.org/slides/tom-ebergen-exploring-the-iceberg-ecosystem-with-duckdb-iceberg-iceberg-summit.pdf) |

## Abstract

Building DuckDB-Iceberg within the DuckDB ecosystem is challenging enough, but testing DuckDB-Iceberg interoperability with other major Iceberg engines and catalogs takes things to a whole new level.

Why? Well, ensuring DuckDB-Iceberg can integrate and operate alongside major engines and REST Catalogs in the Iceberg ecosystem requires extensive testing against the assumptions, and spec deviations of each engine.

This talk shares DuckDB's approach to testing the DuckDB-Iceberg extension against real-world catalog and engine behaviors. We will discuss the hidden interoperability challenges and edge cases discovered and outline the current testing infrastructure built to prevent regressions and catch issues before users do.
