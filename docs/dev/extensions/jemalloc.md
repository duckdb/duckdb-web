---
layout: docu
redirect_from:
- /docs/extensions/jemalloc
title: jemalloc Extension
---

The `jemalloc` extension replaces the system's memory allocator with [jemalloc](https://jemalloc.net/). Unlike other DuckDB extensions, the `jemalloc` extension is statically linked and cannot be installed or loaded during runtime.

## Availability

The Linux and macOS versions of DuckDB ship with the `jemalloc` extension by default.
On Windows, this extension is not available.
