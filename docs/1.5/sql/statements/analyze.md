---
layout: docu
title: ANALYZE Statement
---

The `ANALYZE` statement recomputes the statistics on DuckDB's tables.

## Usage

The statistics recomputed by the `ANALYZE` statement are only used for [join order optimization](https://blobs.duckdb.org/papers/tom-ebergen-msc-thesis-join-order-optimization-with-almost-no-statistics.pdf). It is therefore recommended to recompute these statistics for improved join orders, especially after performing large updates (inserts and/or deletes).

To recompute the statistics, run:

```sql
ANALYZE;
```
