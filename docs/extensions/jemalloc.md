---
layout: docu
title: jemalloc Extension
---

The `jemalloc` extension replaces the system's memory allocator with [jemalloc](https://jemalloc.net/). Unlike other DuckDB extensions, the `jemalloc` extension is statically linked and cannot be installed or loaded during runtime.

## Availability

The Linux and macOS versions of DuckDB ship with the `jemalloc` extension by default.
On Windows, this extension is not available.

## GitHub

The `jemalloc` extension is part of the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/extension/jemalloc).
