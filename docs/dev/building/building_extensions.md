---
layout: docu
title: Building Extensions
---

[Extensions]({% link docs/extensions/overview.md %}) can be built from source and installed from the resulting local binary.

## Building Extensions using Build Flags

To build using extension flags, set the corresponding [`BUILD_[EXTENSION_NAME]` extension flag](#extension-flags) when running the build, then use the `INSTALL` command.

For example, to install the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}), run the following script:

```bash
GEN=ninja BUILD_HTTPFS=1 make
```

For release builds:

```bash
build/release/duckdb -c "INSTALL 'build/release/extension/httpfs/httpfs.duckdb_extension';"
```

For debug builds:

```bash
build/debug/duckdb -c "INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension';"
```

### Extension Flags

For every in-tree extension that is maintained by core DuckDB there exists a flag to enable building and statically linking the extension into the build.

#### `BUILD_AUTOCOMPLETE`

When this flag is set, the [`autocomplete` extension]({% link docs/extensions/autocomplete.md %}) is built.

#### `BUILD_ICU`

When this flag is set, the [`icu` extension]({% link docs/extensions/icu.md %}) is built.

#### `BUILD_TPCH`

When this flag is set, the [`tpch` extension]({% link docs/extensions/tpch.md %}) is built, this enables TPCH-H data generation and query support using `dbgen`.

#### `BUILD_TPCDS`

When this flag is set, the [`tpcds` extension]({% link docs/extensions/tpcds.md %}) is built, this enables TPC-DS data generation and query support using `dsdgen`.

#### `BUILD_TPCE`

When this flag is set, the [TPCE](https://www.tpc.org/tpce/) extension is built. Unlike TPC-H and TPC-DS this does not enable data generation and query support. Instead, it enables tests for TPC-E through our test suite.

#### `BUILD_FTS`

When this flag is set, the [`fts` (full text search) extension]({% link docs/extensions/full_text_search.md %}) is built.

#### `BUILD_HTTPFS`

When this flag is set, the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}) is built.

#### `BUILD_JEMALLOC`

When this flag is set, the [`jemalloc` extension]({% link docs/extensions/jemalloc.md %}) is built.

#### `BUILD_JSON`

When this flag is set, the [`json` extension]({% link docs/extensions/json.md %}) is built.

#### `BUILD_INET`

When this flag is set, the [`inet` extension]({% link docs/extensions/inet.md %}) is built.

#### `BUILD_SQLSMITH`

When this flag is set, the [SQLSmith extension](https://github.com/duckdb/duckdb/pull/3410) is built.

### Debug Flags

#### `CRASH_ON_ASSERT`

`D_ASSERT(condition)` is used all throughout the code, these will throw an InternalException in debug builds.  
With this flag enabled, when the assertion triggers it will instead directly cause a crash.

#### `DISABLE_STRING_INLINE`

In our execution format `string_t` has the feature to "inline" strings that are under a certain length (12 bytes), this means they don't require a separate allocation.  
When this flag is set, we disable this and don't inline small strings.

#### `DISABLE_MEMORY_SAFETY`

Our data structures that are used extensively throughout the non-performance-critical code have extra checks to ensure memory safety, these checks include:  

* Making sure `nullptr` is never dereferenced.
* Making sure index out of bounds accesses don't trigger a crash.

With this flag enabled we remove these checks, this is mostly done to check that the performance hit of these checks is negligible.

#### `DESTROY_UNPINNED_BLOCKS`

When previously pinned blocks in the BufferManager are unpinned, with this flag enabled we destroy them instantly to make sure that there aren't situations where this memory is still being used, despite not being pinned.

#### `DEBUG_STACKTRACE`

When a crash or assertion hit occurs in a test, print a stack trace.  
This is useful when debugging a crash that is hard to pinpoint with a debugger attached.

## Using a CMake Configuration File

To build using a CMake configuration file, create an extension configuration file named `extension_config.cmake` with e.g., the following content:

```cmake
duckdb_extension_load(autocomplete)
duckdb_extension_load(fts)
duckdb_extension_load(httpfs/overview)
duckdb_extension_load(inet)
duckdb_extension_load(icu)
duckdb_extension_load(json)
duckdb_extension_load(parquet)
```

Build DuckDB as follows:

```bash
GEN=ninja EXTENSION_CONFIGS="extension_config.cmake" make
```

Then, to install the extensions in one go, run:

```bash
# for release builds
cd build/release/extension/
# for debug builds
cd build/debug/extension/
# install extensions
for EXTENSION in *; do
    ../duckdb -c "INSTALL '${EXTENSION}/${EXTENSION}.duckdb_extension';"
done
```
