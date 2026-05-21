---
layout: docu
redirect_from:
- /docs/extensions/jemalloc
- /docs/extensions/current/jemalloc 
- /docs/stable/extensions/jemalloc
- /docs/preview/core_extensions/jemalloc
- /docs/stable/core_extensions/jemalloc
- /docs/current/core_extensions/jemalloc
title: jemalloc
---

The `jemalloc` extension replaces the system's memory allocator with [jemalloc](https://jemalloc.net/).
`jemalloc` extension is statically linked and cannot be installed or loaded during runtime.

> For thechnical reasons, we used to distribute `jemalloc` as an extension. Since DuckDB v1.5.3, it is distributred as a third-party library.

## Operating System Support

The availability of the `jemalloc` extension depends on the operating system.

### Linux

Linux distributions of DuckDB ship with the `jemalloc` by default.
To disable `jemalloc`, [build DuckDB from source]({% link docs/current/dev/building/overview.md %}) and set the `SKIP_EXTENSIONS` flag as follows:

```batch
GEN=ninja SKIP_EXTENSIONS="jemalloc" make
```

### macOS

The macOS version of DuckDB does with `jemalloc` but can be [built from source]({% link docs/current/dev/building/macos.md %}) to include it:

```batch
GEN=ninja BUILD_JEMALLOC=1 make
```

### Windows

On Windows, this extension is not available.

## Configuration

### Environment Variables

The jemalloc allocator in DuckDB can be configured via the `DUCKDB_JE_MALLOC_CONF` environment variable. Setting this is equivalent to setting the [`MALLOC_CONF` environment variable](https://jemalloc.net/jemalloc.3.html#environment) for jemalloc but DuckDB uses a different environment variable name to avoid potential name clashes with other applications.

### Background Threads

By default, jemalloc's [background threads](https://jemalloc.net/jemalloc.3.html#background_thread) are disabled. To enable them, use the following configuration option:

```sql
SET allocator_background_threads = true;
```

Background threads asynchronously purge outstanding allocations so that this doesn't have to be done synchronously by the foreground threads. This improves allocation performance, and should be noticeable in allocation-heavy workloads, especially on many-core CPUs.
