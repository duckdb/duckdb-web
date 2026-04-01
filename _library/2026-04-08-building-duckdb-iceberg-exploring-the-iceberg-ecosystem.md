---
layout: post
title: "Building DuckDB-Iceberg: Exploring the Iceberg Ecosystem"
author: "Tom Ebergen (DuckDB Labs)"
tags: ["Talk"]
thirdparty: false
excerpt: ""
pill: "Iceberg Summit 2026"
---

## Upcoming Talk

|-------|-------|
| **Date** | {{ page.date | date: "%Y-%m-%d" }} |
| **Event** | [Iceberg Summit 2026](https://events.bizzabo.com/796372) |
| **Speaker** | Tom Ebergen (DuckDB Labs) |

## Abstract

Building DuckDB-Iceberg within the DuckDB ecosystem is challenging enough, but testing DuckDB-Iceberg interoperability with other major Iceberg engines and catalogs takes things to a whole new level.

Why? Well, ensuring DuckDB-Iceberg can integrate and operate alongside major engines and REST Catalogs in the Iceberg ecosystem requires extensive testing against the assumptions, and spec deviations of each engine.

This talk shares DuckDB's approach to testing the DuckDB-Iceberg extension against real-world catalog and engine behaviors. We will discuss the hidden interoperability challenges and edge cases discovered and outline the current testing infrastructure built to prevent regressions and catch issues before users do.
