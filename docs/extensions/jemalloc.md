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

Linux distributions of DuckDB ships with the `jemalloc` extension.
To disable the `jemalloc` extension, [build DuckDB from source]({% link docs/dev/building/overview.md %}) and set the `SKIP_EXTENSIONS` flag as follows:

```bash
GEN=ninja SKIP_EXTENSIONS="jemalloc" make
```

### macOS

The macOS version of DuckDB does not ship with the `jemalloc` extension but can be [built from source]({% link docs/dev/building/macos.md %}) to include it:

```bash
GEN=ninja BUILD_JEMALLOC=1 make
```

### Windows

On Windows, this extension is not available.

## Configuration

### Environment Variables

The jemalloc allocator in DuckDB can be configured via the [`MALLOC_CONF` environment variable](https://jemalloc.net/jemalloc.3.html#environment).

### Background Threads

By default, jemalloc's [background threads](https://jemalloc.net/jemalloc.3.html#background_thread) are disabled. To enable them, use the following configuration option:

```sql
SET allocator_background_threads = true;
```

Background threads asynchronously purge outstanding allocations so that this doesn't have to be done synchronously by the foreground threads. This improves allocation performance, and should be noticeable in allocation-heavy workloads, especially on many-core CPUs.
