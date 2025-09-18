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

For different build configurations (`debug`, `relassert`, etc.), please consult the [Build Configurations page]({% link docs/1.1/dev/building/build_configuration.md %}).

## Troubleshooting

### Debug Build Prints malloc Warning

**Problem:**
The `debug` build on macOS prints a `malloc` warning, e.g.:

```text
duckdb(83082,0x205b30240) malloc: nano zone abandoned due to inability to reserve vm space.
```

To prevent this, set the `MallocNanoZone` flag to 0:

```bash
MallocNanoZone=0 make debug
```

To apply this change for your future terminal sessions, you can add the following to your `~/.zshrc` file:

```bash
export MallocNanoZone=0
```