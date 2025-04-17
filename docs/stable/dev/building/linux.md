---
layout: docu
redirect_from:
- /docs/dev/building/linux
title: Linux
---

## Prerequisites

On Linux, install the required packages with the package manager of your distribution.

### Ubuntu and Debian

#### CLI Client

On Ubuntu and Debian (and also MX Linux, Linux Mint, etc.), the requirements for building the DuckDB CLI client are the following:

```batch
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build libssl-dev
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

### Fedora, CentOS and Red Hat

#### CLI Client

The requirements for building the DuckDB CLI client on Fedora, CentOS, Red Hat, AlmaLinux, Rocky Linux, etc. are the following:

```batch
sudo yum install -y git g++ cmake ninja-build openssl-devel
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

### Alpine Linux

#### CLI Client

The requirements for building the DuckDB CLI client on Alpine Linux are the following:

```batch
apk add g++ git make cmake ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

#### Performance with musl libc

Note that Alpine Linux uses [musl libc](https://musl.libc.org/) as its C standard library.
DuckDB binaries built with musl libc have lower performance compared to the glibc variants: for some workloads, the slowdown can be more than 5×.
Therefore, it's recommended to use glibc for performance-oriented workloads.

#### Distribution for the `linux_*_musl` platforms

Starting with DuckDB v1.2.0, [_extensions_ are distributed for the `linux_amd64_musl` platform]({% post_url 2025-02-05-announcing-duckdb-120 %}#musl-extensions) (but not yet for the `linux_amd64_musl` platform).
However, there are no official _DuckDB binaries_ distributed for musl libc but it can be build with it manually following the instructions on this page.

#### Python Client on Alpine Linux

Currently, installing the DuckDB Python on Alpine Linux requires compilation from source.
To do so, install the required packages before running `pip`:

```batch
apk add g++ py3-pip python3-dev
pip install duckdb
```

## Using the DuckDB CLI Client on Linux

Once the build finishes successfully, you can find the `duckdb` binary in the `build` directory:

```batch
build/release/duckdb
```

For different build configurations (`debug`, `relassert`, etc.), please consult the [“Build Configurations” page]({% link docs/stable/dev/building/build_configuration.md %}).

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
Create or edit the `~/.R/Makevars` file. This example also contains the [`MAKEFLAGS` setting to parallelize the build]({% link docs/stable/dev/building/r.md %}#the-build-only-uses-a-single-thread ):

```ini
ALL_CXXFLAGS = $(PKG_CXXFLAGS) -fPIC $(SHLIB_CXXFLAGS) $(CXXFLAGS)
MAKEFLAGS = -j$(nproc)
```

### Building the httpfs Extension Fails

**Problem:**
When building the [`httpfs` extension]({% link docs/stable/extensions/httpfs/overview.md %}) on Linux, the build may fail with the following error.

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
