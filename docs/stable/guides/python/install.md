---
layout: docu
redirect_from:
- /docs/guides/python/install
title: Installing the Python Client
---

## Installing via Pip

The latest release of the Python client can be installed using `pip`.

```bash
pip install duckdb
```

The pre-release Python client (known as the “preview” or “nightly” build) can be installed using `--pre`.

```bash
pip install duckdb --upgrade --pre
```

## Installing from Source

The latest Python client can be installed from source from the [`tools/pythonpkg` directory in the DuckDB GitHub repository](https://github.com/duckdb/duckdb/tree/main/tools/pythonpkg).

```batch
BUILD_PYTHON=1 GEN=ninja make
cd tools/pythonpkg
python setup.py install
```

For detailed instructions on how to compile DuckDB from source, see the [Building guide]({% link docs/stable/dev/building/python.md %}).
