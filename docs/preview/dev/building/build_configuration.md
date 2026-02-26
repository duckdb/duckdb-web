---
layout: docu
title: Building Configuration
---

## Build Types

DuckDB can be built in many different settings, most of these correspond directly to CMake but not all of them.

### `release`

This build has been stripped of all the assertions and debug symbols and code, optimized for performance.

### `debug`

This build runs with all the debug information, including symbols, assertions and `#ifdef DEBUG` blocks.
Due to these, binaries of this build are expected to be slow.
Note: the special debug defines are not automatically set for this build.

### `relassert`

This build does not trigger the `#ifdef DEBUG` code blocks but it still has debug symbols that make it possible to step through the execution with line number information and `D_ASSERT` lines are still checked in this build.
Binaries of this build mode are significantly faster than those of the `debug` mode.

### `reldebug`

This build is similar to `relassert` in many ways, only assertions are also stripped in this build.

### `benchmark`

This build is a shorthand for `release` with `BUILD_BENCHMARK=1` set.

### `tidy-check`

This creates a build and then runs [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/) to check for issues or style violations through static analysis.
The CI will also run this check, causing it to fail if this check fails.

### `format-fix` | `format-changes` | `format-main`

This doesn't actually create a build, but uses the following format checkers to check for style issues:

* [clang-format](https://clang.llvm.org/docs/ClangFormat.html) to fix format issues in the code.
* [cmake-format](https://cmake-format.readthedocs.io/en/latest/) to fix format issues in the `CMakeLists.txt` files.

The CI will also run this check, causing it to fail if this check fails.

## Extension Selection

[Core DuckDB extensions]({% link docs/preview/core_extensions/overview.md %}) are the ones maintained by the DuckDB team. These are hosted in the `duckdb` GitHub organization and are served by the `core` extension repository.

Additional extensions can be built as part of DuckDB via the `BUILD_EXTENSIONS` flag, then listing the names of the extensions that are to be built.

```batch
BUILD_EXTENSIONS='tpch;httpfs;fts;json;parquet' make
```

More on this topic at [building DuckDB extensions]({% link docs/preview/dev/building/building_extensions.md %}).

## Package Flags

For every package that is maintained by core DuckDB, there exists a flag in the Makefile to enable building the package.
These can be enabled by either setting them in the current `env`, through set up files like `bashrc` or `zshrc`, or by setting them before the call to `make`, for example:

```batch
BUILD_PYTHON=1 make debug
```

### `BUILD_PYTHON`

When this flag is set, the [Python]({% link docs/preview/clients/python/overview.md %}) package is built.

### `BUILD_SHELL`

When this flag is set, the [CLI]({% link docs/preview/clients/cli/overview.md %}) is built, this is usually enabled by default.

### `BUILD_BENCHMARK`

When this flag is set, DuckDB's in-house benchmark suite is built.
More information about this can be found [in the README](https://github.com/duckdb/duckdb/blob/main/benchmark/README.md).

### `BUILD_JDBC`

When this flag is set, the [Java]({% link docs/preview/clients/java.md %}) package is built.

### `BUILD_ODBC`

When this flag is set, the [ODBC]({% link docs/preview/clients/odbc/overview.md %}) package is built.

## Miscellaneous Flags

### `DISABLE_UNITY`

To improve compilation time, we use [Unity Build](https://cmake.org/cmake/help/latest/prop_tgt/UNITY_BUILD.html) to combine translation units.
This can however hide include bugs, this flag disables using the unity build so these errors can be detected.

### `DISABLE_SANITIZER`

In some situations, running an executable that has been built with sanitizers enabled is not supported / can cause problems. Julia is an example of this.
With this flag enabled, the sanitizers are disabled for the build.

## Overriding Git Hash and Version

It is possible to override the Git hash and version when building from source using the `OVERRIDE_GIT_DESCRIBE` environment variable.
This is useful when building from sources that are not part of a complete Git repository (e.g., an archive file with no information on commit hashes and tags).
For example:

```batch
OVERRIDE_GIT_DESCRIBE=v0.10.0-843-g09ea97d0a9 GEN=ninja make
```

Will result in the following output when running `./build/release/duckdb`:

```text
v0.10.1-dev843 09ea97d0a9
...
```
