---
layout: docu
title: Known Python Issues
---

Unfortunately there are some issues that are either beyond our control or are very elusive / hard to track down.
Below is a list of these issues that you might have to be aware of, depending on your workflow.

## Numpy Import Multithreading

When making use of multi threading and fetching results either directly as Numpy arrays or indirectly through a Pandas DataFrame, it might be necessary to ensure that `numpy.core.multiarray` is imported.
If this module has not been imported from the main thread, and a different thread during execution attempts to import it this causes either a deadlock or a crash.

To avoid this, it's recommended to `import numpy.core.multiarray` before starting up threads.

## Running EXPLAIN Renders Newlines in Jupyter and IPython

When DuckDB is run in Jupyter notebooks or in the IPython shell, the output of the [`EXPLAIN` statement](../../guides/meta/explain) contains hard line breaks (`\n`):

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

Please also check out the [Jupyter guide](../../guides/python/jupyter) for tips on using Jupyter with JupySQL.

## Error When Importing the DuckDB Python Package on Windows

When importing DuckDB on Windows, the Python runtime may return the following error:

```python
import duckdb
```

```console
ImportError: DLL load failed while importing duckdb: The specified module could not be found.
```

The solution is to install the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist).
