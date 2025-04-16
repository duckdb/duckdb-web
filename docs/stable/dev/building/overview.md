---
layout: docu
redirect_from:
- /dev/building
- /dev/building/
- /docs/dev/building
- /docs/dev/building/
- /docs/dev/building/build_instructions
- /docs/dev/building/build_instructions/
- /docs/dev/building/platforms
- /docs/dev/building/platforms/
- /docs/dev/building/supported_platforms
- /docs/dev/building/supported_platforms/
- /docs/dev/building/overview
title: Building DuckDB from Source
---

## When Should You Build DuckDB?

DuckDB binaries are available for _stable_ and _preview_ builds on the [installation page]({% link docs/installation/index.html %}).
In most cases, it's recommended to use these binaries.
When you are running on an experimental platform (e.g., [Raspberry Pi]({% link docs/stable/dev/building/raspberry_pi.md %})) or you would like to build the project for an unmerged pull request,
you can build DuckDB from source based on the [`duckdb/duckdb` repository hosted on GitHub](https://github.com/duckdb/duckdb/).
This page explains the steps for building DuckDB.

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC).
Additionally, we recommend using the [Ninja build system](https://ninja-build.org/), which automatically parallelizes the build process.

## Platforms

### Supported Platforms

DuckDB fully supports Linux, macOS and Windows. Both AMD64 (x86_64) and ARM64 (AArch64) builds are available for these platforms.

| Platform name      | Description                                                            |
|--------------------|------------------------------------------------------------------------|
| `linux_amd64`      | Linux AMD64 (x86_64) with [glibc](https://www.gnu.org/software/libc/)  |
| `linux_arm64`      | Linux ARM64 (AArch64) with [glibc](https://www.gnu.org/software/libc/) |
| `osx_amd64`        | macOS 12+ AMD64 (Intel CPUs)                                           |
| `osx_arm64`        | macOS 12+ ARM64 (Apple Silicon CPUs)                                   |
| `windows_amd64`    | Windows 10+ AMD64 (x86_64)                                             |
| `windows_arm64`    | Windows 10+ ARM64 (AArch64)                                            |

For instructions to build from source, see:

* [Linux]({% link docs/stable/dev/building/linux.md %})
* [macOS]({% link docs/stable/dev/building/macos.md %})
* [Windows]({% link docs/stable/dev/building/windows.md %})

### Experimental Platforms

There are several additional platforms with varying levels of support.
For some platforms, DuckDB binaries and extensions (or a [subset of extensions]({% link docs/stable/extensions/extension_distribution.md %}#platforms)) are distributed. For others, building from source is possible.

| Platform name          | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| `freebsd_amd64`        | FreeBSD AMD64 (x86_64)                                                                               |
| `freebsd_arm64`        | FreeBSD ARM64 (AArch64)                                                                              |
| `linux_amd64_musl`     | Linux AMD64 (x86_64) with [musl libc](https://musl.libc.org/), e.g., Alpine Linux                    |
| `linux_arm64_android`  | Android ARM64 (AArch64)                                                                              |
| `linux_arm64_gcc4`     | Linux ARM64 (AArch64) with GCC 4, e.g., CentOS 7                                                     |
| `linux_arm64_musl`     | Linux ARM64 (AArch64) with [musl libc](https://musl.libc.org/), e.g., Alpine Linux                   |
| `wasm_eh`              | WebAssembly Exception Handling                                                                       |
| `wasm_mvp`             | WebAssembly Minimum Viable Product                                                                   |
| `windows_amd64_mingw`  | Windows 10+ AMD64 (x86_64) with MinGW                                                                |
| `windows_amd64_rtools` | Windows 10+ AMD64 (x86_64) for [RTools](https://cran.r-project.org/bin/windows/Rtools/) (deprecated) |
| `windows_arm64_mingw`  | Windows 10+ ARM64 (AArch64) with MinGW                                                               |

> These platforms are not covered by DuckDB's community support. For details on commercial support, see the [support policy page](https://duckdblabs.com/community_support_policy#platforms).

Below, we provide detailed build instructions for some platforms:

* [Android]({% link docs/stable/dev/building/android.md %})
* [Raspberry Pi]({% link docs/stable/dev/building/raspberry_pi.md %})

### Outdated Platforms

DuckDB can be built for end-of-life platforms such as [macOS 11](https://endoflife.date/macos) and [CentOS 7/8](https://endoflife.date/centos) using the instructions provided for macOS and Linux.

### Unofficial and Unsupported Platforms

Several platforms are not supported or supported on a best-effort basis.
See the [“Unofficial and Unsupported Platforms” page]({% link docs/stable/dev/building/unofficial_and_unsupported_platforms.md %}) for details.

## Limitations

Currently, DuckDB has the following limitations:

* The DuckDB codebase is not compatible with [C++23](https://en.wikipedia.org/wiki/C%2B%2B23). Therefore, trying to compile DuckDB with `-std=c++23` will fail.
* The `-march=native` build flag, i.e., compiling DuckDB with the local machine's native instructions set, is not supported.

## Troubleshooting Guides

We provide troubleshooting guides for building DuckDB:

* [Generic issues]({% link docs/stable/dev/building/troubleshooting.md %})
* [Python]({% link docs/stable/dev/building/python.md %})
* [R]({% link docs/stable/dev/building/r.md %})
