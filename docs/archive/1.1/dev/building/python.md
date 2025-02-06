---
layout: docu
title: Python
---

In general, if you would like to build DuckDB from source, it's recommended to avoid using the `BUILD_PYTHON=1` flag unless you are actively developing the DuckDB Python client.

## Python Package on macOS: Building the httpfs Extension Fails

**Problem:**
The build fails on macOS when both the [`httpfs` extension]({% link docs/archive/1.1/extensions/httpfs/overview.md %}) and the Python package are included:

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
As stated above, avoid using the `BUILD_PYTHON` flag.
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