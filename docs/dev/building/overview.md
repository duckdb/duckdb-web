---
layout: docu
title: Building DuckDB from Source
redirect_from:
  - /dev/building
  - /docs/dev/building
  - /docs/dev/building/build_instructions
  - /docs/dev/building/platforms
  - /docs/dev/building/supported_platforms
---

## When Should You Build DuckDB?

DuckDB binaries are available for stable and nightly builds on the [installation page]({% link docs/installation/index.html %}).
You should only build DuckDB under specific circumstances, such as when running on an experimental platform, when building an unmerged pull request, or developing your fork of DuckDB.

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC).
Additionally, we recommend using the [Ninja build system](https://ninja-build.org/), which automatically parallelizes the build process.

## Supported Platforms

DuckDB fully supports Linux, macOS and Windows. Both AMD64 (x86_64) and ARM64 (AArch64) builds are available for these platforms.

| Platform name      | Description                          |
|--------------------|--------------------------------------|
| `linux_amd64`      | Linux AMD64 (x86_64)                 |
| `linux_arm64`      | Linux ARM64 (AArch64)                |
| `osx_amd64`        | macOS 12+ AMD64 (Intel CPUs)         |
| `osx_arm64`        | macOS 12+ ARM64 (Apple Silicon CPUs) |
| `windows_amd64`    | Windows 10+ AMD64 (x86_64)           |
| `windows_arm64`    | Windows 10+ ARM64 (AArch64)          |

For instructions to build from source, see:

* [Linux]({% link docs/dev/building/linux.md %})
* [macOS]({% link docs/dev/building/macos.md %})
* [Windows]({% link docs/dev/building/windows.md %})

## Experimental Platforms

There are several additional platforms with varying levels of support.
For some platforms, DuckDB binaries and extensions (or a [subset of extensions]({% link docs/extensions/working_with_extensions.md %}#platforms)) are distributed. For others, building from source is possible.

| Platform name          | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| `freebsd_amd64`        | FreeBSD AMD64 (x86_64)                                                                               |
| `freebsd_arm64`        | FreeBSD ARM64 (AArch64)                                                                              |
| `linux_amd64_musl`     | Linux AMD64 (x86_64) with musl libc, e.g., Alpine Linux                                              |
| `linux_arm64_android`  | Android ARM64 (AArch64)                                                                              |
| `linux_arm64_gcc4`     | Linux ARM64 (AArch64) with GCC 4, e.g., CentOS 7                                                     |
| `linux_arm64_musl`     | Linux ARM64 (x86_64) with musl libc, e.g., Alpine Linux                                              |
| `wasm_eh`              | WebAssembly Exception Handling                                                                       |
| `wasm_mvp`             | WebAssembly Minimum Viable Product                                                                   |
| `windows_amd64_mingw`  | Windows 10+ AMD64 (x86_64) with MinGW                                                                |
| `windows_amd64_rtools` | Windows 10+ AMD64 (x86_64) for [RTools](https://cran.r-project.org/bin/windows/Rtools/) (deprecated) |
| `windows_arm64_mingw`  | Windows 10+ ARM64 (AArch64) with MinGW                                                               |

> These platforms are not covered by DuckDB's community support. For details on commercial support, see the [support policy blog post](https://duckdblabs.com/news/2023/10/02/support-policy#platforms).

Below, we provide detailed build instructions for some platforms:

* [Android]({% link docs/dev/building/android.md %})
* [Raspberry Pi]({% link docs/dev/building/raspberry_pi.md %})

### Outdated Platforms

DuckDB can be built for end-of-life platforms such as [macOS 11](https://endoflife.date/macos) and [CentOS 7/8](https://endoflife.date/centos) using the instructions provided for macOS and Linux.

### 32-bit Architectures

32-bit architectures are officially not supported but it is possible to build DuckDB manually for some of these platforms, e.g., for [Raspberry Pi boards]({% link docs/dev/building/raspberry_pi.md %}).
