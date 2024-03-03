---
layout: docu
title: jemalloc Extension
---

The `jemalloc` extension replaces the system's memory allocator with [jemalloc](https://jemalloc.net/).
Unlike other DuckDB extensions, the `jemalloc` extension is statically linked and cannot be installed or loaded during runtime.

## Operating System Support

The availability of the `jemalloc` extension depends on the operating system.

### Linux

The Linux version of DuckDB ships with the `jemalloc` extension by default.

To disable the `jemalloc` extension, [build DuckDB from source](/dev/building) and set the `SKIP_EXTENSIONS` flag as follows:

```bash
GEN=ninja SKIP_EXTENSIONS="jemalloc" make
```

### macOS

The macOS version of DuckDB does not ship with the `jemalloc` extension but can be [built from source](/dev/building) to include it:

```bash
GEN=ninja BUILD_JEMALLOC=1 make
```

### Windows

On Windows, this extension is not available.

## GitHub

The `jemalloc` extension is part of the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/extension/jemalloc).
