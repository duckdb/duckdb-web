---
layout: docu
title: Building Instructions
---

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC).
Additionally, we recommend using the [Ninja build system](https://ninja-build.org/), which automatically parallelizes the build process.

### Linux Packages

Install the required packages with the package manager of your distribution.

Fedora, CentOS, and Red Hat:

```bash
sudo yum install -y git g++ cmake ninja-build openssl-devel
```

Ubuntu and Debian:

```bash
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build libssl-dev
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

Consult the [Windows CI workflow](https://github.com/duckdb/duckdb/blob/v0.10.2/.github/workflows/Windows.yml#L234) for a list of packages used to build DuckDB on Windows.

The DuckDB Python package requires the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) to be built and [to run](../../api/python/known_issues#error-when-importing-the-duckdb-python-package-on-windows).

## Building DuckDB

To build DuckDB we use a Makefile which in turn calls into CMake. We also advise using [Ninja](https://ninja-build.org/manual.html) as the generator for CMake.

```bash
GEN=ninja make
```

> Bestpractice It is not advised to directly call CMake, as the Makefile sets certain variables that are crucial to properly building the package.
