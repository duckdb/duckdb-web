---
layout: docu
title: Python
---

In general, if you would like to build DuckDB from source, it's recommended to avoid using the `BUILD_PYTHON=1` flag unless you are actively developing the DuckDB Python client.

## Python Package on macOS: Building the httpfs Extension Fails

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

## `No module named 'duckdb.duckdb'` Build Error

**Problem:**
Building the Python package succeeds but the package cannot be imported:

```batch
cd tools/pythonpkg/
python3 -m pip install .
python3 -c "import duckdb"
```

This returns the following error message:

```console
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/duckdb/tools/pythonpkg/duckdb/__init__.py", line 4, in <module>
    import duckdb.functional as functional
  File "/duckdb/tools/pythonpkg/duckdb/functional/__init__.py", line 1, in <module>
    from duckdb.duckdb.functional import (
ModuleNotFoundError: No module named 'duckdb.duckdb'
```

**Solution:**
The problem is caused by Python trying to import from the current working directory.
To work around this, navigate to a different directory (e.g., `cd ..`) and try running Python import again.
