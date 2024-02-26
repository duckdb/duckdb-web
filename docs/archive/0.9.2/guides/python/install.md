---
layout: docu
title: Install the Python Client
---

The latest release of the Python client can be installed using `pip`.

```bash
pip install duckdb
```

The pre-release Python client can be installed using `--pre`.

```bash
pip install duckdb --upgrade --pre
```

The latest Python client can be installed from source from the [`tools/pythonpkg` directory in the DuckDB GitHub repository](https://github.com/duckdb/duckdb/tree/main/tools/pythonpkg).

```bash
BUILD_PYTHON=1 GEN=ninja make
cd tools/pythonpkg
python setup.py install
```