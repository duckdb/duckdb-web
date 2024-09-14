---
layout: docu
title: Building Instructions
---

## Prerequisites

DuckDB needs CMake and a C++11-compliant compiler (e.g., GCC, Apple-Clang, MSVC).
Additionally, we recommend using the [Ninja build system](https://ninja-build.org/), which automatically parallelizes the build process.

## UNIX-like Systems

### macOS Packages

Install Xcode and [Homebrew](https://brew.sh/). Then, install the required packages with:

```bash
brew install git cmake ninja
```

### Linux Packages

Install the required packages with the package manager of your distribution.

Ubuntu and Debian:

```bash
sudo apt-get update && sudo apt-get install -y git g++ cmake ninja-build libssl-dev
```

Fedora, CentOS, and Red Hat:

```bash
sudo yum install -y git g++ cmake ninja-build openssl-devel
```

Alpine Linux:

```bash
apk add g++ git make cmake ninja
```

### Cloning the Repository

Clone the DuckDB repository:

```bash
git clone https://github.com/duckdb/duckdb
```

We recommend creating a full clone of the repository. Note that the directory uses approximately 1.3 GB of disk space.

### Building DuckDB

To build DuckDB, we use a Makefile which in turn calls into CMake. We also advise using [Ninja](https://ninja-build.org/manual.html) as the generator for CMake.

```bash
GEN=ninja make
```

> Bestpractice It is not advised to directly call CMake, as the Makefile sets certain variables that are crucial to properly building the package.

Once the build finishes successfully, you can find the `duckdb` binary in the `build` directory:

```bash
build/release/duckdb
```

### Linking Extensions

For testing, it can be useful to build DuckDB with statically linked core extensions. To do so, run:

```bash
CORE_EXTENSIONS='autocomplete;httpfs;icu;parquet;json' GEN=ninja make
```

This option also accepts out-of-tree extensions:

```bash
CORE_EXTENSIONS='autocomplete;httpfs;icu;parquet;json;delta' GEN=ninja make
```

For more details, see the [“Building Extensions” page]({% link docs/dev/building/building_extensions.md %}).

## Windows

On Windows, DuckDB requires the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) both as a build-time and runtime dependency.

To build DuckDB, install [MSYS2](https://www.msys2.org/) and open a MINGW64 session.
Install the required dependencies using Pacman. When prompted with `Enter a selection (default=all)`, select the default option by pressing `Enter`.
Note that unlike the build process on UNIX-like systems, the Windows build directly calls CMake.

```batch
pacman -Syu git mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DBUILD_EXTENSIONS="icu;parquet;json"
cmake --build . --config Release 
```

Once the build finishes successfully, you can find the `duckdb.exe` binary in the repository's directory:

```bash
./duckdb.exe
```

## Raspberry Pi (32-bit)

On 32-bit Raspberry Pi controllers, you need to add the [`-latomic` link flag](https://github.com/duckdb/duckdb/issues/13855#issuecomment-2341539339).
As extensions are not distributed for this platform, it's recommended to also include them in the build.
For example:

```batch
cmake .. \
    -DBUILD_EXTENSIONS="httpfs;json;parquet" \
    -DDUCKDB_EXTRA_LINK_FLAGS="-latomic"
make -j4
```

## Troubleshooting

### The Build Runs Out of Memory

Ninja parallelizes the build, which can cause out-of-memory issues on systems with limited resources. They also occur on Alpine Linux. In these cases, avoid using Ninja:

```bash
make
```
