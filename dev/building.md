---
layout: docu
title: Building DuckDB from Source
---

> DuckDB binaries are available for stable and nightly builds on the [installation page](/docs/installation).
> You should only build DuckDB under specific circumstances, such as when running on a specific architecture or building an unmerged pull request.

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC). Additionally, we recommend using the [Ninja build system](https://ninja-build.org/).

### Linux Packages

Install the required packages with the package manager of your distribution.

Fedora, CentOS, and Red Hat:

```bash
sudo yum install -y git g++ cmake ninja-build
```

Ubuntu and Debian:

```bash
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build
```

Alpine Linux:

```bash
apk add g++ git make cmake ninja
```

### macOS

Install Xcode and [Homebrew](https://brew.sh/). Then, install the required packages with:

```bash
brew install cmake ninja
```

### Windows

Consult the [Windows CI workflow](https://github.com/duckdb/duckdb/blob/v0.9.2/.github/workflows/Windows.yml#L158) for a list of packages used to build DuckDB on Windows.

The DuckDB Python package requires the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) to be built and [to run](../docs/api/python/known_issues#error-when-importing-the-duckdb-python-package-on-windows).

## Building DuckDB

To build DuckDB we use a Makefile which in turn calls into CMake. We also advise using [Ninja](https://ninja-build.org/manual.html) as the generator for CMake.

```bash
GEN=ninja make
```

It is not advised to directly call CMake, as the Makefile sets certain variables that are crucial to properly building the package.

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

This creates a build and then runs [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/) to check for issues or style violations through static analysis.  
The CI will also run this check, causing it to fail if this check fails.

#### `format-fix` | `format-changes` | `format-main`

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
More information about this can be found [here](https://github.com/duckdb/duckdb/blob/main/benchmark/README.md).

#### `BUILD_JDBC`

When this flag is set, the [Java](../docs/api/java) package is built.

#### `BUILD_ODBC`

When this flag is set, the [ODBC](../docs/api/odbc/overview) package is built.

### Extension Flags

For every in-tree extension that is maintained by core DuckDB there exists a flag to enable building and statically linking the extension into the build.

#### `BUILD_AUTOCOMPLETE`

When this flag is set, the [`autocomplete` extension](/docs/extensions/autocomplete) is built.

#### `BUILD_ICU`

When this flag is set, the [`icu` extension](/docs/extensions/icu) is built.

#### `BUILD_TPCH`

When this flag is set, the [`tpch` extension](/docs/extensions/tpch) is built, this enables TPCH-H data generation and query support using `dbgen`.

#### `BUILD_TPCDS`

When this flag is set, the [`tpcds` extension](/docs/extensions/tpcd) is built, this enables TPC-DS data generation and query support using `dsdgen`.

#### `BUILD_TPCE`

When this flag is set, the [TPCE](https://www.tpc.org/tpce/) extension is built, unlike TPC-H and TPC-DS this does not enable data generation and query support, but does enable tests for TPC-E through our test suite.

#### `BUILD_FTS`

When this flag is set, the [`fts` (full text search) extension](/docs/extensions/full_text_search) is built.

#### `BUILD_HTTPFS`

When this flag is set, the [`httpfs` extension](/docs/extensions/httpfs) is built.

#### `BUILD_JSON`

When this flag is set, the [`json` extension](/docs/extensions/json) is built.

#### `BUILD_INET`

When this flag is set, the [`inet` extension](/docs/extensions/inet) is built.

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

## Troubleshooting

### Building the R Package on Linux aarch64

Building the R package on Linux running on an ARM64 architecture (AArch64) may result in the following error message:

```text
/usr/bin/ld: /usr/include/c++/10/bits/basic_string.tcc:206: warning: too many GOT entries for -fpic, please recompile with -fPIC
```

To work around this, create or edit the `~/.R/Makevars` file:

```text
ALL_CXXFLAGS = $(PKG_CXXFLAGS) -fPIC $(SHLIB_CXXFLAGS) $(CXXFLAGS)
```

### Building the httpfs Extension and Python Package on macOS

**Problem:** The build fails on macOS when both the [`httpfs` extension](/docs/extensions/httpfs) and the Python package are included:

```bash
GEN=ninja BUILD_PYTHON=1 BUILD_HTTPFS=1 make
```
```text
ld: library not found for -lcrypto
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command '/usr/bin/clang++' failed with exit code 1
ninja: build stopped: subcommand failed.
make: *** [release] Error 1
```

**Solution:**
In general, we recommended using the nightly builds, available under GitHub main (Bleeding Edge) on the [installation page](/docs/installation).
If you would like to build DuckDB from source, avoid using the `BUILD_PYTHON=1` flag unless you are actively developing the Python library.
Instead, first build the `httpfs` extension, then build and install the Python package separately using the `setup.py` script:

```bash
GEN=ninja BUILD_HTTPFS=1 make
python3 tools/pythonpkg/setup.py install --user
```

### Building the httpfs Extension on Linux

**Problem:** When building the [`httpfs` extension](/docs/extensions/httpfs) on Linux, the build may fail with the following error.

```text
CMake Error at /usr/share/cmake-3.22/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
  Could NOT find OpenSSL, try to set the path to OpenSSL root folder in the
  system variable OPENSSL_ROOT_DIR (missing: OPENSSL_CRYPTO_LIBRARY
  OPENSSL_INCLUDE_DIR)
```

**Solution:** Install the `libssl-dev` library.

```bash
sudo apt-get install -y libssl-dev
GEN=ninja BUILD_HTTPFS=1 make
```
