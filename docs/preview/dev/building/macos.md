---
layout: docu
title: macOS
---

## Prerequisites

Install Xcode and [Homebrew](https://brew.sh/). Then, install the required packages with:

```bash
brew install git cmake ninja
```

## Building DuckDB

Clone and build DuckDB as follows.

```bash
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

Once the build finishes successfully, you can find the `duckdb` binary in the `build` directory:

```bash
build/release/duckdb
```

For different build configurations (`debug`, `relassert`, etc.), please consult the [Build Configurations page]({% link docs/preview/dev/building/build_configuration.md %}).

## Troubleshooting

### Build Failure: `'string' file not found`

**Problem:**
The build fails on macOS with the following error:

```console
FAILED: third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o
/Library/Developer/CommandLineTools/usr/bin/c++ -DDUCKDB_BUILD_LIBRARY -DEXT_VERSION_PARQUET=\"9cba6a2a03\" -I/Users/builder/external/duckdb/src/include -I/Users/builder/external/duckdb/third_party/fsst -I/Users/builder/external/duckdb/third_party/fmt/include -I/Users/builder/external/duckdb/third_party/hyperloglog -I/Users/builder/external/duckdb/third_party/fastpforlib -I/Users/builder/external/duckdb/third_party/skiplist -I/Users/builder/external/duckdb/third_party/fast_float -I/Users/builder/external/duckdb/third_party/re2 -I/Users/builder/external/duckdb/third_party/miniz -I/Users/builder/external/duckdb/third_party/utf8proc/include -I/Users/builder/external/duckdb/third_party/concurrentqueue -I/Users/builder/external/duckdb/third_party/pcg -I/Users/builder/external/duckdb/third_party/tdigest -I/Users/builder/external/duckdb/third_party/mbedtls/include -I/Users/builder/external/duckdb/third_party/jaro_winkler -I/Users/builder/external/duckdb/third_party/yyjson/include -I/Users/builder/external/duckdb/third_party/libpg_query/include -O3 -DNDEBUG -O3 -DNDEBUG   -std=c++11 -arch arm64 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.1.sdk -fPIC -fvisibility=hidden -fcolor-diagnostics -w -MD -MT third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o -MF third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o.d -o third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o -c /Users/builder/external/duckdb/third_party/libpg_query/src_backend_nodes_list.cpp
In file included from /Users/builder/external/duckdb/third_party/libpg_query/src_backend_nodes_list.cpp:35:
/Users/builder/external/duckdb/third_party/libpg_query/include/pg_functions.hpp:4:10: fatal error: 'string' file not found
    4 | #include <string>
```

**Solution:**
Users report that reinstalling Xcode fixed their problem.
See related discussions on the [DuckDB GitHub issues](https://github.com/duckdb/duckdb/issues/14665#issuecomment-2452679953) and on [Stack Overflow](https://stackoverflow.com/questions/78999694/cant-compile-c-hello-world-with-clang-on-mac-sequoia-15-0-and-vs-code).

> Warning Attempting to reinstall your Xcode suite may impact other applications on your system. Proceed with caution.

```bash
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

### Debug Build Prints malloc Warning

**Problem:**
The `debug` build on macOS prints a `malloc` warning, e.g.:

```text
duckdb(83082,0x205b30240) malloc: nano zone abandoned due to inability to reserve vm space.
```

**Solution:**
To prevent this, set the `MallocNanoZone` flag to 0:

```bash
MallocNanoZone=0 make debug
```

To apply this change for your future terminal sessions, you can add the following to your `~/.zshrc` file:

```bash
export MallocNanoZone=0
```
