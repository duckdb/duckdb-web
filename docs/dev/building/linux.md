---
layout: docu
title: Linux
---

## Prerequisites

On Linux, install the required packages with the package manager of your distribution.

### Ubuntu and Debian

```batch
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build libssl-dev
```

### Fedora, CentOS, and Red Hat

```batch
sudo yum install -y git g++ cmake ninja-build openssl-devel
```

### Alpine Linux

```batch
apk add g++ git make cmake ninja
```

Note that Alpine Linux uses the musl libc as its C standard library.
There are no official DuckDB binaries distributed for musl libc but it can be build with it manually following the instructions on this page.
Note that starting with DuckDB v1.2.0, [extensions are distributed for the `linux_amd64_musl` platform]({% post_url 2025-02-05-announcing-duckdb-120 %}#musl-extensions).

#### Python Client on Alpine Linux

To install the Python client on Alpine Linux, run:

```batch
apk add g++ py3-pip
pip3 install duckdb
```

This will compile DuckDB from source.

## Building DuckDB

Clone and build DuckDB as follows:

```batch
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

Once the build finishes successfully, you can find the `duckdb` binary in the `build` directory:

```batch
build/release/duckdb
```

For different build configurations (`debug`, `relassert`, etc.), please consult the [Build Configurations page]({% link docs/dev/building/build_configuration.md %}).

## Building Using Extension Flags

To build using extension flags, set the `CORE_EXTENSIONS` flag to the list of extensions that you want to be build. For example:

```batch
CORE_EXTENSIONS='autocomplete;httpfs;icu;json;tpch' GEN=ninja make
```

## Troubleshooting

### R Package on Linux AArch64: `too many GOT entries` Build Error

**Problem:**
Building the R package on Linux running on an ARM64 architecture (AArch64) may result in the following error message:

```console
/usr/bin/ld: /usr/include/c++/10/bits/basic_string.tcc:206:
warning: too many GOT entries for -fpic, please recompile with -fPIC
```

**Solution:**
Create or edit the `~/.R/Makevars` file. This example also contains the [flag to parallelize the build](#r-package-the-build-only-uses-a-single-thread):

```ini
ALL_CXXFLAGS = $(PKG_CXXFLAGS) -fPIC $(SHLIB_CXXFLAGS) $(CXXFLAGS)
MAKEFLAGS = -j$(nproc)
```

When making this change, also consider [making the build parallel](#r-package-the-build-only-uses-a-single-thread).

### Building the httpfs Extension Fails

**Problem:**
When building the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}) on Linux, the build may fail with the following error.

```console
CMake Error at /usr/share/cmake-3.22/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
  Could NOT find OpenSSL, try to set the path to OpenSSL root folder in the
  system variable OPENSSL_ROOT_DIR (missing: OPENSSL_CRYPTO_LIBRARY
  OPENSSL_INCLUDE_DIR)
```

**Solution:**
Install the `libssl-dev` library.

```batch
sudo apt-get install -y libssl-dev
```

Then, build with:

```batch
GEN=ninja CORE_EXTENSIONS="httpfs" make
```
