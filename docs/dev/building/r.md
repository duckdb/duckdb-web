---
layout: docu
title: R
---

This page contains instructions for building the R client library.

## R Package: The Build Only Uses a Single Thread

**Problem:**
By default, R compiles packages using a single thread, which causes the build to be slow.

**Solution:**
To parallelize the compilation, create or edit the `~/.R/Makevars` file, and add a line like the following:

```ini
MAKEFLAGS = -j8
```

The above will parallelize the compilation using 8 threads. On Linux/macOS, you can add the following to use all of the machine's threads:

```ini
MAKEFLAGS = -j$(nproc)
```

However, note that, the more threads that are used, the higher the RAM consumption. If the system runs out of RAM while compiling, then the R session will crash.

## Python Package: `No module named 'duckdb.duckdb'` Build Error

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
