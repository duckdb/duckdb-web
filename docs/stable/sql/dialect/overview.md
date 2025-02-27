---
layout: docu
redirect_from:
- /docs/sql/dialect/overview
title: Overview
---

DuckDB's SQL dialect is based on PostgreSQL.
DuckDB tries to closely match PostgreSQL's semantics, however, some use cases require slightly different behavior.
For example, interchangeability with data frame libraries necessitates [order preservation of inserts]({% link docs/stable/sql/dialect/order_preservation.md %}) to be supported by default.
These differences are documented in the pages below.
