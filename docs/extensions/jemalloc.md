---
layout: docu
title: jemalloc Extension
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/jemalloc
---

The `jemalloc` extension replaces the system's memory allocator with [jemalloc](https://jemalloc.net/).
Unlike other DuckDB extensions, the `jemalloc` extension is statically linked and cannot be installed or loaded during runtime.

## Operating System Support

The availability of the `jemalloc` extension depends on the operating system.

### Linux

The Linux version of DuckDB ships with the `jemalloc` extension by default.

> DuckDB v0.10.1 introduced a change: on ARM64 architecture, DuckDB is shipped without `jemalloc`, while on x86_64 (AMD64) architectures, it is shipped with `jemalloc`.

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
