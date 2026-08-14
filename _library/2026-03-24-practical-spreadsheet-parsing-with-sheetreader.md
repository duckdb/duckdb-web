---
layout: post
title: "Practical Spreadsheet Parsing with SheetReader"
author: "Haralampos Gavriilidis, Felix Henze, Joel Ziegler, Jonas Benn, Eleni Tzirita Zacharatou, Volker Markl"
thumb: "/images/library/thumbs/edbt.svg"
image: "/images/library/thumbs/edbt.jpg"
tags: ["Paper"]
category: community
excerpt: ""
pill: "EDBT 2026"
---

| | |
|-------|-------|
| **Paper** | [Practical Spreadsheet Parsing with SheetReader (PDF)](https://heltzi.github.io/publications/SheetReader___Demo_EDBT26.pdf) |
| **Venue** | EDBT 2026 |

## Abstract

Spreadsheets remain a ubiquitous tool for data management and analysis. Since systems like Excel offer limited analytical capabilities, users routinely load spreadsheets into richer ecosystems such as Python, R, and DBMSes. However, existing spreadsheet loaders rely on general-purpose XML parsers that are ill-suited for the XLSX format, resulting in severe CPU and memory bottlenecks. In prior work, we introduced SheetReader, a specialized spreadsheet parser that leverages the structure of XLSX files and employs parallelism to significantly reduce ingestion costs, achieving up to an order of magnitude speedup and multi-gigabyte memory savings compared to state-of-the-art methods. This demonstration provides an interactive workbench where visitors can visualize XLSX internals, benchmark SheetReader against baseline parsers with live resource monitoring, and explore integrations for Python, R, PostgreSQL, and DuckDB, including running SQL directly over spreadsheets.

## Implementation

SheetReader is available as a [DuckDB community extension]({% link community_extensions/extensions/sheetreader.md %}).
