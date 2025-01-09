---
layout: docu
title: macOS
---

## Prerequisites

Install Xcode and [Homebrew](https://brew.sh/). Then, install the required packages with:

```batch
brew install git cmake ninja
```

## Building DuckDB

Clone and build DuckDB as follows.

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

## Troubleshooting

### Debug Build Prints malloc Warning

**Problem:**
The `debug` build on macOS prints a `malloc` warning, e.g.:

```text
duckdb(83082,0x205b30240) malloc: nano zone abandoned due to inability to reserve vm space.
```

To prevent this, set the `MallocNanoZone` flag to 0:

```batch
MallocNanoZone=0 make debug
```

To apply this change for your future terminal sessions, you can add the following to your `~/.zshrc` file:

```batch
export MallocNanoZone=0
```

### Python Package on macOS: Building the httpfs Extension Fails

**Problem:**
The build fails on macOS when both the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}) and the Python package are included:

```batch
GEN=ninja BUILD_PYTHON=1 CORE_EXTENSIONS="httpfs" make
```

```console
ld: library not found for -lcrypto
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command '/usr/bin/clang++' failed with exit code 1
ninja: build stopped: subcommand failed.
make: *** [release] Error 1
```

**Solution:**
If you would like to build DuckDB from source, avoid using the `BUILD_PYTHON=1` flag unless you are actively developing the Python library.
Instead, first build the `httpfs` extension (if required), then build and install the Python package separately using pip:

```batch
GEN=ninja CORE_EXTENSIONS="httpfs" make
python3 -m pip install tools/pythonpkg --use-pep517 --user
```

If the second line complains about pybind11 being missing, or `--use-pep517` not being supported, make sure you're using a modern version of pip and setuptools.
The default `python3-pip` on your OS may not be modern, so you may need to update it using:

```batch
python3 -m pip install pip -U
```
