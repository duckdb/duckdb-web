---
layout: docu
redirect_from:
- /docs/clients/rust/known_issues
- /docs/stable/clients/rust/known_issues
- /docs/current/clients/rust/troubleshoot
- /docs/lts/clients/rust/troubleshoot
- /docs/preview/clients/rust/troubleshoot
- /docs/stable/clients/rust/troubleshoot
title: Troubleshoot
---

## Overview

This page collects common issues encountered when using the DuckDB Rust client, together with their workarounds. If you run into a problem that is not covered here, search the [client's issue tracker](https://github.com/duckdb/duckdb-rs/issues) on GitHub.

## Linking against a System Library

The [`bundled` feature]({% link docs/2.0/clients/rust/overview.md %}#feature-flags) compiles DuckDB from the source shipped with the crate, so nothing else is needed to build, and it is the simplest choice for most applications. Without `bundled`, the underlying [`libduckdb-sys`](https://crates.io/crates/libduckdb-sys) crate links against a DuckDB library already on the system, which it locates through `pkg-config` or, on the MSVC ABI, [Vcpkg](https://github.com/microsoft/vcpkg). If no library is found, the build fails. There are three ways to build without `bundled`.

### Point at a Library You Already Have

Set `DUCKDB_LIB_DIR` to the directory containing the library, and `DUCKDB_INCLUDE_DIR` to the directory containing `duckdb.h` if it is elsewhere. For example, using a prebuilt library from a [DuckDB release](https://github.com/duckdb/duckdb/releases):

```bash
wget https://github.com/duckdb/duckdb/releases/download/v{{ site.latest_duckdb_version }}/duckdb-shared-libs-osx-universal.tar.gz
mkdir libduckdb && tar -xzf duckdb-shared-libs-osx-universal.tar.gz -C libduckdb

export DUCKDB_LIB_DIR=$PWD/libduckdb
export DUCKDB_INCLUDE_DIR=$DUCKDB_LIB_DIR
export DYLD_FALLBACK_LIBRARY_PATH=$DUCKDB_LIB_DIR   # LD_LIBRARY_PATH on Linux
cargo build
```

On Linux, use the matching `duckdb-shared-libs-linux-amd64.tar.gz` or `duckdb-shared-libs-linux-arm64.tar.gz` archive and set `LD_LIBRARY_PATH` instead.

### Let the Build Download a Library

Set `DUCKDB_DOWNLOAD_LIB=1` and the build script downloads the prebuilt DuckDB library matching the crate's version from GitHub Releases, caches it under `target/`, and adds it to the linker search path. Leave `DUCKDB_STATIC` unset, because the downloaded archives contain only the dynamic library:

```bash
DUCKDB_DOWNLOAD_LIB=1 cargo build
```

### Use a Package Manager

If DuckDB is installed through `pkg-config` or Vcpkg, the build finds it automatically. `vcpkg` uses static libraries by default; set `VCPKGRS_DYNAMIC=1` to link dynamically instead.

## ICU Extension Missing from the Bundled Build

Because crates.io imposes a 10 MB package-size limit, the `bundled` source of earlier crate versions excluded the [`icu` extension]({% link docs/2.0/core_extensions/icu.md %}). In DuckDB 2.0, the `icu` extension no longer depends on the ICU library and implements time zones, calendars and collations natively. If some collation or time-zone-aware date/time operations still fail out of the box with your crate version, install and load the extension at runtime:

```rust
conn.execute_batch("INSTALL icu; LOAD icu;")?;
```

Alternatively, statically link the extension by enabling the crate's `icu` feature, which pulls it into the build.

## `open_in_memory` Panics in an Extension Build

The `loadable-extension` feature builds a DuckDB extension rather than a client application. When it is enabled, entry points such as `Connection::open_in_memory()` panic if they are called outside an extension context, because there is no host DuckDB instance to attach to.

Do not enable `loadable-extension` for a client application. Use it only when building an extension. See [Write User Defined Functions]({% link docs/2.0/clients/rust/functions.md %}#building-a-loadable-extension) for how loadable extensions are built and packaged.

## Cross-Compiling with `bundled`

Cross-compiling with the `bundled` feature compiles DuckDB's C++ source for the target, so it requires a working C++ cross-compiler for that target and is supported only on a best-effort basis. When cross-compilation is difficult to set up, link against a prebuilt library for the target with `DUCKDB_LIB_DIR` instead, as described in [Linking against a System Library](#linking-against-a-system-library).

## Further Reading

* [Rust Client]({% link docs/2.0/clients/rust/overview.md %}) — installation, the `bundled` feature, and the full list of Cargo feature flags.
* [Connect]({% link docs/2.0/clients/rust/connecting.md %}) — opening connections, whose failures are often build or linking problems.
* [Write User Defined Functions]({% link docs/2.0/clients/rust/functions.md %}) — the `loadable-extension` feature and how to package an extension correctly.
