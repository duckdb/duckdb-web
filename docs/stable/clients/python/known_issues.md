---
layout: docu
redirect_from:
- /docs/api/python/known_issues
- /docs/api/python/known_issues/
- /docs/clients/python/known_issues
title: Known Python Issues
---

## Troubleshooting

### Running `EXPLAIN` Renders Newlines

In Python, the output of the [`EXPLAIN` statement]({% link docs/stable/guides/meta/explain.md %}) contains hard line breaks (`\n`):

```python
In [1]: import duckdb
   ...: duckdb.sql("EXPLAIN SELECT 42 AS x")
```

```text
Out[1]:
┌───────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  explain_key  │                                                   explain_value                                                   │
│    varchar    │                                                      varchar                                                      │
├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ physical_plan │ ┌───────────────────────────┐\n│         PROJECTION        │\n│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │\n│             x   …  │
└───────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

To work around this, `print` the output of the `explain()` function:

```python
In [2]: print(duckdb.sql("SELECT 42 AS x").explain())
```

```text
Out[2]:
┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             x             │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         DUMMY_SCAN        │
└───────────────────────────┘
```

Please also check out the [Jupyter guide]({% link docs/stable/guides/python/jupyter.md %}) for tips on using Jupyter with JupySQL.

### Crashes and Errors on Windows

When importing DuckDB on Windows, the Python runtime may crash or return an error upon import or first use:

```python
import duckdb

duckdb.sql("...")
```

```console
ImportError: DLL load failed while importing duckdb: The specified module could not be found.
```

```console
Windows fatal exception: access violation

Current thread 0x0000311c (most recent call first):
  File "<stdin>", line 1 in <module>
```

```console
Process finished with exit code -1073741819 (0xC0000005)
```

The problem is likely caused by using an outdated Microsoft Visual C++ (MSVC) Redistributable package.
The solution is to install the [latest MSVC Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist).
Alternatively, you can instruct `pip` to compile the package from source as follows:

```bash
python3 -m pip install duckdb --no-binary duckdb
```

## Known Issues

Unfortunately there are some issues that are either beyond our control or are very elusive / hard to track down.
Below is a list of these issues that you might have to be aware of, depending on your workflow.

### Numpy Import Multithreading

When making use of multi threading and fetching results either directly as Numpy arrays or indirectly through a Pandas DataFrame, it might be necessary to ensure that `numpy.core.multiarray` is imported.
If this module has not been imported from the main thread, and a different thread during execution attempts to import it this causes either a deadlock or a crash.

To avoid this, it's recommended to `import numpy.core.multiarray` before starting up threads.

## `DESCRIBE` and `SUMMARIZE` Return Empty Tables in Jupyter

The `DESCRIBE` and `SUMMARIZE` statements return an empty table:

```python
%sql
CREATE OR REPLACE TABLE tbl AS (SELECT 42 AS x);
DESCRIBE tbl;
```

To work around this, wrap them into a subquery:

```python
%sql
CREATE OR REPLACE TABLE tbl AS (SELECT 42 AS x);
FROM (DESCRIBE tbl);
```

### Protobuf Error for JupySQL in IPython

Loading the JupySQL extension in IPython fails:

```python
In [1]: %load_ext sql
```

```console
ImportError: cannot import name 'builder' from 'google.protobuf.internal' (unknown location)
```

The solution is to fix the `protobuf` package. This may require uninstalling conflicting packages, e.g.:

```python
%pip uninstall tensorflow
%pip install protobuf
```
