---
layout: docu
title: Building Extensions
---

[Extensions]({% link docs/preview/extensions/overview.md %}) can be built from source and installed from the resulting local binary.

## Building Extensions

To build using extension flags, set the `BUILD_EXTENSIONS` flag to the list of extensions that you want to be built. For example:

```bash
BUILD_EXTENSIONS='autocomplete;httpfs;icu;json;tpch' GEN=ninja make
```

This option also accepts out-of-tree extensions such as [`delta`]({% link docs/preview/core_extensions/delta.md %}):

```bash
BUILD_EXTENSIONS='autocomplete;httpfs;icu;json;tpch;delta' GEN=ninja make
```

In most cases, extensions will be directly linked in the resulting DuckDB executable.

## Special Extension Flags

### `BUILD_JEMALLOC`

When this flag is set, the [`jemalloc` extension]({% link docs/preview/core_extensions/jemalloc.md %}) is built.

### `BUILD_TPCE`

When this flag is set, the [TPCE](https://www.tpc.org/tpce/) library is built. Unlike TPC-H and TPC-DS this is not a proper extension and it's not distributed as such. Enabling this allows TPC-E enabled queries through our test suite.

## Debug Flags

### `CRASH_ON_ASSERT`

`D_ASSERT(condition)` is used all throughout the code, these will throw an InternalException in debug builds.
With this flag enabled, when the assertion triggers it will instead directly cause a crash.

### `DISABLE_STRING_INLINE`

In our execution format `string_t` has the feature to “inline” strings that are under a certain length (12 bytes), this means they don't require a separate allocation.
When this flag is set, we disable this and don't inline small strings.

### `DISABLE_MEMORY_SAFETY`

Our data structures that are used extensively throughout the non-performance-critical code have extra checks to ensure memory safety, these checks include:

* Making sure `nullptr` is never dereferenced.
* Making sure index out of bounds accesses don't trigger a crash.

With this flag enabled we remove these checks, this is mostly done to check that the performance hit of these checks is negligible.

### `DESTROY_UNPINNED_BLOCKS`

When previously pinned blocks in the BufferManager are unpinned, with this flag enabled we destroy them instantly to make sure that there aren't situations where this memory is still being used, despite not being pinned.

### `DEBUG_STACKTRACE`

When a crash or assertion hit occurs in a test, print a stack trace.
This is useful when debugging a crash that is hard to pinpoint with a debugger attached.

## Using a CMake Configuration File

To build using a CMake configuration file, create an extension configuration file named `extension_config.cmake` with e.g., the following content:

```cmake
duckdb_extension_load(autocomplete)
duckdb_extension_load(fts)
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
