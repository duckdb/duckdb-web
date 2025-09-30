---
layout: docu
title: Building DuckDB from Source
---

## When Should You Build DuckDB?

DuckDB binaries are available for _stable_ and _preview_ builds on the [installation page]({% link docs/installation/index.html %}).
In most cases, it's recommended to use these binaries.
When you are running on an experimental platform (e.g., [Raspberry Pi]({% link docs/preview/dev/building/raspberry_pi.md %})) or you would like to build the project for an unmerged pull request,
you can build DuckDB from source based on the [`duckdb/duckdb` repository hosted on GitHub](https://github.com/duckdb/duckdb/).
This page explains the steps for building DuckDB.

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC).
Additionally, we recommend using the [Ninja build system](https://ninja-build.org/), which automatically parallelizes the build process.

## Getting Started

A `Makefile` wraps the build process.
See [Build Configuration]({% link docs/preview/dev/building/build_configuration.md %}) for targets and configuration flags.

```bash
make
make release # same as plain make
make debug
GEN=ninja make # for use with Ninja
BUILD_BENCHMARK=1 make # build with benchmarks
```

## Platforms

### Platforms with Full Support

DuckDB fully supports Linux, macOS and Windows. Both x86_64 (amd64) and AArch64 (arm64) builds are available for these platforms, and almost all extensions are distributed for these platforms.

| Platform name      | Description                                                            |
|--------------------|------------------------------------------------------------------------|
| `linux_amd64`      | Linux x86_64 (amd64) with [glibc](https://www.gnu.org/software/libc/)  |
| `linux_arm64`      | Linux AArch64 (arm64) with [glibc](https://www.gnu.org/software/libc/) |
| `osx_amd64`        | macOS 12+ amd64 (Intel CPUs)                                           |
| `osx_arm64`        | macOS 12+ arm64 (Apple Silicon CPUs)                                   |
| `windows_amd64`    | Windows 10+ x86_64 (amd64)                                             |
| `windows_arm64`    | Windows 10+ AArch64 (arm64)                                            |

For these platforms, builds are available for both the latest stable version and the preview version (nightly build).
In some circumstances, you may still want to build DuckDB from source, e.g., to test an unmerged [pull request](https://github.com/duckdb/duckdb/pulls).
For build instructions on these platforms, see:

* [Linux]({% link docs/preview/dev/building/linux.md %})
* [macOS]({% link docs/preview/dev/building/macos.md %})
* [Windows]({% link docs/preview/dev/building/windows.md %})

### Platforms with Partial Support

There are several partially supported platforms.
For some platforms, DuckDB binaries and extensions (or a [subset of extensions]({% link docs/preview/extensions/extension_distribution.md %}#platforms)) are distributed.
For others, building from source is possible.

| Platform name          | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| `linux_amd64_musl`     | Linux x86_64 (amd64) with [musl libc](https://musl.libc.org/), e.g., Alpine Linux                    |
| `linux_arm64_musl`     | Linux AArch64 (arm64) with [musl libc](https://musl.libc.org/), e.g., Alpine Linux                   |
| `linux_arm64_android`  | Android AArch64 (arm64)                                                                              |
| `wasm_eh`              | WebAssembly Exception Handling                                                                       |

Below, we provide detailed build instructions for some platforms:

* [Android]({% link docs/preview/dev/building/android.md %})
* [Raspberry Pi]({% link docs/preview/dev/building/raspberry_pi.md %})

### Platforms with Best Effort Support

| Platform name          | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| `freebsd_amd64`        | FreeBSD x86_64 (amd64)                                                                               |
| `freebsd_arm64`        | FreeBSD AArch64 (arm64)                                                                              |
| `wasm_mvp`             | WebAssembly Minimum Viable Product                                                                   |
| `windows_amd64_mingw`  | Windows 10+ x86_64 (amd64) with MinGW                                                                |
| `windows_arm64_mingw`  | Windows 10+ AArch64 (arm64) with MinGW                                                               |

> These platforms are not covered by DuckDB's community support. For details on commercial support, see the [support policy page](https://duckdblabs.com/community_support_policy#platforms).

See also the [“Unofficial and Unsupported Platforms” page]({% link docs/preview/dev/building/unofficial_and_unsupported_platforms.md %}) for details.

### Outdated Platforms

Some platforms were supported in older DuckDB versions but are no longer supported.

| Platform name          | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| `linux_amd64_gcc4`     | Linux AMDM64 (x86_64) with GCC 4, e.g., CentOS 7                                                     |
| `linux_arm64_gcc4`     | Linux AArch64 (arm64) with GCC 4, e.g., CentOS 7                                                     |
| `windows_amd64_rtools` | Windows 10+ x86_64 (amd64) for [RTools](https://cran.r-project.org/bin/windows/Rtools/)              |

DuckDB can also be built for end-of-life platforms such as [macOS 11](https://endoflife.date/macos) and [CentOS 7/8](https://endoflife.date/centos) using the instructions provided for macOS and Linux.

## Amalgamation Build

DuckDB can be build as a single pair of C++ header and source code files (`duckdb.hpp` and `duckdb.cpp`) with approximately 0.5M lines of code.
To generate this file, run:

```bash
python scripts/amalgamation.py
```

Note that amalgamation build is provided on a best-effort basis and is not officially supported.

## Limitations

Currently, DuckDB has the following known compile-time limitations:

* The `-march=native` build flag, i.e., compiling DuckDB with the local machine's native instructions set, is not supported.

## Troubleshooting Guides

We provide troubleshooting guides for building DuckDB:

* [Generic issues]({% link docs/preview/dev/building/troubleshooting.md %})
* [Python]({% link docs/preview/dev/building/python.md %})
* [R]({% link docs/preview/dev/building/r.md %})
