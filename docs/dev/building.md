---
layout: docu
title: Building From Source
selected: Documentation/Development/Building
expanded: Development
---

To build DuckDB we use a Makefile which in turn calls into CMake.  
It's not advised to directly call CMake, as the Makefile sets certain variables that are crucial to properly building the package.

When building with CMake it's possible to specify a generator, we advice using [Ninja](https://ninja-build.org/manual.html) as the generator.  
The Makefile will check the `GEN` environment variable for `'ninja'` to set this CMake flag to use Ninja.

### Build Type

DuckDB can be built in many different settings, most of these correspond directly to CMake but not all of them.

#### `release`
This build has been stripped of all the assertions and debug symbols and code, optimized for performance.

#### `debug`
This build runs with all the debug information, including symbols, assertions and DEBUG blocks.  
The special debug defines are not automatically set for this build however.

#### `relassert`
This build does not trigger the `#ifdef DEBUG` code blocks, but still has debug symbols that make it possible to step through the execution with line number information and `D_ASSERT` lines are still checked in this build.

#### `reldebug`
This build is similar to `relassert` in many ways, only assertions are also stripped in this build.

#### `benchmark`
This build is a shorthand for `release` with `BUILD_BENCHMARK=1` set.

#### `tidy-check`
This creates a build and then runs [clang tidy](https://clang.llvm.org/extra/clang-tidy/) to check for issues or style violations through static analysis.  
The CI will also run this check, causing it to fail if this check fails.

#### `format-fix` | `format-changes` | `format-master`
This doesn't actually create a build, but uses the following format checkers to check for style issues:
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) to fix format issues in the code.  
- [cmake-format](https://cmake-format.readthedocs.io/en/latest/) to fix format issues in the CMakeLists.txt files.  

The CI will also run this check, causing it to fail if this check fails.

### Package Flags

For every package that is maintained by core DuckDB, there exists a flag in the Makefile to enable building the package.  
These can be enabled by either setting them in the current `env`, through set up files like `bashrc` or `zshrc`, or by setting them before the call to `make`, for example:
```bash
BUILD_PYTHON=1 make debug
```

#### `BUILD_PYTHON`
When this flag is set, the [Python](../docs/api/python/overview) package is built.

#### `BUILD_SHELL`
When this flag is set, the [CLI](../docs/api/cli) is built, this is usually enabled by default.

#### `BUILD_BENCHMARK`
When this flag is set, our in-house Benchmark testing suite is built.  
More information about this can be found [here](https://github.com/duckdb/duckdb/blob/master/benchmark/README.md).

#### `BUILD_JDBC`
When this flag is set, the [Java](../docs/api/java) package is built.

#### `BUILD_ODBC`
When this flag is set, the [ODBC](../docs/api/odbc/overview) package is built.

#### `BUILD_R`
When this flag is set, the [R](../docs/api/r) package is built.

#### `BUILD_NODE`
When this flag is set, the [Node](../docs/api/nodejs/overview) package is built.

### Extension Flags

For every in-tree extension that is maintained by core DuckDB there exists a flag to enable building and statically linking the extension into the build.

#### `BUILD_AUTOCOMPLETE`
When this flag is set, the [AutoComplete](https://github.com/duckdb/duckdb/pull/4921) extension is built.

#### `BUILD_ICU`
When this flag is set, the [ICU](../2022/01/06/time-zones.html) extension is built.

#### `BUILD_TPCH`
When this flag is set, the [TPCH](https://www.tpc.org/tpch/) extension is built, this enables TPCH-H data generation and query support using `dbgen`.

#### `BUILD_TPCDS`
When this flag is set, the [TPCDS](https://www.tpc.org/tpcds/) extension is built, this enables TPC-DS data generation and query support using `dsdgen`.

#### `BUILD_TPCE`
When this flag is set, the [TPCE](https://www.tpc.org/tpce/) extension is built, unlike TPC-H and TPC-DS this does not enable data generation and query support, but does enable tests for TPC-E through our test suite.

#### `BUILD_FTS`
When this flag is set, the [Full Text Search](../docs/extensions/full_text_search) extension is built.

#### `BUILD_VISUALIZER`
When this flag is set, the [Visualizer](https://github.com/duckdb/duckdb/pull/1832) extension is built.

#### `BUILD_HTTPFS`
When this flag is set, the [HTTP File System](../docs/extensions/httpfs) extension is built.

#### `BUILD_JSON`
When this flag is set, the [JSON](../docs/extensions/json) extension is built.

#### `BUILD_INET`
When this flag is set, the [INET](https://github.com/duckdb/duckdb/pull/4785) extension is built.

#### `BUILD_SQLSMITH`
When this flag is set, the [SQLSmith](https://github.com/duckdb/duckdb/pull/3410) extension is built.

### Debug Flags

#### `CRASH_ON_ASSERT`
`D_ASSERT(condition)` is used all throughout the code, these will throw an InternalException in debug builds.  
With this flag enabled, when the assertion triggers it will instead directly cause a crash.

#### `DISABLE_STRING_INLINE`
In our execution format `string_t` has the feature to "inline" strings that are under a certain length (12 bytes), this means they don't require a separate allocation.  
When this flag is set, we disable this and don't inline small strings.

#### `DISABLE_MEMORY_SAFETY`
Our data structures that are used extensively throughout the non-performance-critical code have extra checks to ensure memory safety, these checks include:  
- Making sure `nullptr` is never dereferenced.  
- Making sure index out of bounds accesses don't trigger a crash.  

With this flag enabled we remove these checks, this is mostly done to check that the performance hit of these checks is negligible.

#### `DESTROY_UNPINNED_BLOCKS`
When previously pinned blocks in the BufferManager are unpinned, with this flag enabled we destroy them instantly to make sure that there aren't situations where this memory is still being used, despite not being pinned.

#### `DEBUG_STACKTRACE`
When a crash or assertion hit occurs in a test, print a stack trace.  
This is useful when debugging a crash that is hard to pinpoint with a debugger attached.

### Miscellaneous Flags

#### `DISABLE_UNITY`
To improve compilation time, we use [Unity Build](https://cmake.org/cmake/help/latest/prop_tgt/UNITY_BUILD.html) to combine translation units.  
This can however hide include bugs, this flag disables using the unity build so these errors can be detected.

#### `DISABLE_SANITIZER`
In some situations, running an executable that has been built with sanitizers enabled is not support / can cause problems. Julia is an example of this.  
With this flag enabled, the sanitizers are disabled for the build.
