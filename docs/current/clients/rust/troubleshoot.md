---
layout: docu
redirect_from:
- /docs/clients/rust/known_issues
- /docs/preview/clients/rust/known_issues
- /docs/stable/clients/rust/known_issues
title: Troubleshoot
---

## Overview

This page collects common issues encountered when using the DuckDB Rust client, together with their workarounds. If you run into a problem that is not covered here, search the [client's issue tracker](https://github.com/duckdb/duckdb-rs/issues) on GitHub.

## Linking against a System Library

The [`bundled` feature]({% link docs/current/clients/rust/overview.md %}#feature-flags) compiles DuckDB from the source shipped with the crate, so nothing else is needed to build. Without `bundled`, the underlying [`libduckdb-sys`](https://crates.io/crates/libduckdb-sys) crate links against a system DuckDB library, which it locates through `pkg-config` or, on the MSVC ABI, [Vcpkg](https://github.com/microsoft/vcpkg). If no library is found the build fails.

To link against a DuckDB library at a known location, set `DUCKDB_LIB_DIR` (and, if the header is elsewhere, `DUCKDB_INCLUDE_DIR`). For example, using the prebuilt library from a DuckDB release:

```bash
export DUCKDB_LIB_DIR=/path/to/libduckdb
export DUCKDB_INCLUDE_DIR=$DUCKDB_LIB_DIR
export LD_LIBRARY_PATH=$DUCKDB_LIB_DIR   # DYLD_FALLBACK_LIBRARY_PATH on macOS
cargo build
```

Alternatively, set `DUCKDB_DOWNLOAD_LIB=1` to have the build download a prebuilt library automatically. For most applications, enabling `bundled` is the simplest choice.

## ICU Extension Is Excluded from the Bundled Build

Because crates.io imposes a 10 MB package-size limit, the `bundled` source excludes the [ICU extension]({% link docs/current/core_extensions/icu.md %}). As a result, some collation and time-zone-aware date/time operations fail out of the box. Install and load ICU at runtime to restore them:

```rust
conn.execute_batch("INSTALL icu; LOAD icu;")?;
```

Alternatively, statically link ICU by enabling the crate's `icu` feature, which pulls it into the build.

## `open_in_memory` Panics in an Extension Build

The `loadable-extension` feature builds a DuckDB extension rather than a client application. When it is enabled, entry points such as `Connection::open_in_memory()` panic if they are called outside an extension context, because there is no host DuckDB instance to attach to.

Do not enable `loadable-extension` for a client application. Use it only when building an extension. See [Write User Defined Functions]({% link docs/current/clients/rust/functions.md %}#building-a-loadable-extension) for how loadable extensions are built and packaged.

## Cross-Compiling with `bundled`

Cross-compiling with the `bundled` feature compiles DuckDB's C++ source for the target, so it requires a working C++ cross-compiler for that target and is supported only on a best-effort basis. When cross-compilation is difficult to set up, link against a prebuilt library for the target with `DUCKDB_LIB_DIR` instead, as described in [Linking against a System Library](#linking-against-a-system-library).

## Further Reading

* [Rust Client]({% link docs/current/clients/rust/overview.md %}) — installation, the `bundled` feature, and the full list of Cargo feature flags.
* [Connect]({% link docs/current/clients/rust/connecting.md %}) — opening connections, whose failures are often build or linking problems.
* [Write User Defined Functions]({% link docs/current/clients/rust/functions.md %}) — the `loadable-extension` feature and how to package an extension correctly.
