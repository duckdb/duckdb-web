---
layout: docu
redirect_from:
- /docs/api/python/known_issues
- /docs/clients/python/known_issues
- /docs/stable/clients/python/known_issues
- /docs/current/clients/python/known_issues
- /docs/lts/clients/python/known_issues
- /docs/preview/clients/python/known_issues
title: Troubleshooting
---

## Troubleshooting

### Running `EXPLAIN` Renders Newlines

In Python, the output of the [`EXPLAIN` statement]({% link docs/2.0/guides/meta/explain.md %}) contains hard line breaks (`\n`):

```python
In [1]: import duckdb
   ...: duckdb.sql("EXPLAIN SELECT 42 AS x")
```

```text
Out[1]:
┌───────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  explain_key  │                                            explain_value                                             │
│    varchar    │                                               varchar                                                │
├───────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ physical_plan │ ╭─ Projection ───╮\n│ Projections: x │\n│ ~1 row         │\n╰────────┬───────╯\n╭─ Dummy Scan ───╮\n │
│               │ ╰────────────────╯\n                                                                                 │
└───────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

To work around this, `print` the output of the `explain()` function:

```python
In [2]: print(duckdb.sql("SELECT 42 AS x").explain())
```

```text
Out[2]:
╭─ Projection ───╮
│ Projections: x │
│ ~1 row         │
╰────────┬───────╯
╭─ Dummy Scan ───╮
╰────────────────╯
```

In a Jupyter notebook, `explain()` displays the plan as HTML itself and returns an empty string, so printing it prints nothing.

Please also check out the [Jupyter guide]({% link docs/2.0/guides/python/jupyter.md %}) for tips on using Jupyter with JupySQL.

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

```batch
python3 -m pip install duckdb --no-binary duckdb
```

## Known Issues

Unfortunately there are some issues that are either beyond our control or are very elusive / hard to track down.
Below is a list of these issues that you might have to be aware of, depending on your workflow.

### Numpy Import Multithreading

When making use of multi threading and fetching results either directly as Numpy arrays or indirectly through a Pandas DataFrame, it might be necessary to ensure that `numpy.core.multiarray` is imported.
If this module has not been imported from the main thread, and a different thread during execution attempts to import it this causes either a deadlock or a crash.

To avoid this, it's recommended to `import numpy.core.multiarray` before starting up threads.

### Many Threads per Database

Besides its worker threads, each database starts a pool of [asynchronous I/O threads]({% link docs/2.0/data/io.md %}#thread-pools): by default four times the number of CPU cores, at most 256. Every `duckdb.connect()` to an unnamed in-memory database starts a new database, so a process that opens many of them runs many threads. To start fewer, set `async_threads` when connecting:

```python
import duckdb

con = duckdb.connect(config={"async_threads": 4})
```

### Fetching Time Zone Aware Values Needs `pytz`

Converting a `TIMESTAMP WITH TIME ZONE` value to a Python object, as `fetchone()` and `fetchall()` do, needs the [`pytz` package](https://pypi.org/project/pytz/), which is not installed with DuckDB. Without it, the fetch raises an `InvalidInputException` saying `Required module 'pytz' failed to import`. Install `pytz` with `pip install pytz`.

### `max_temp_directory_size` Is Ignored in `connect()`

The `max_temp_directory_size` setting has no effect when it is passed in the `config` dictionary of `duckdb.connect()`: `current_setting()` reports the value, but queries write temporary files beyond it. Set it with a `SET` statement after connecting instead:

```python
import duckdb

con = duckdb.connect()
con.execute("SET max_temp_directory_size = '10GB'")
```

### Arrow Readers Hang on Windows after a Subinterpreter Was Created

On Windows, once the process has created a subinterpreter, a query that scans a `pyarrow.RecordBatchReader` whose batches come from a Python generator can hang.

### DataFrame Queries or Boxplots Fail in JupySQL

With JupySQL 0.11.1, run `%sql SET python_scan_all_frames = true` to query notebook DataFrames. This is needed with both native and SQLAlchemy connections. For `%sqlplot boxplot`, use SQLAlchemy. See the [Jupyter guide]({% link docs/2.0/guides/python/jupyter.md %}) for the complete setup.

### Ibis Fails with DuckDB 2.0

Ibis 12.0.0 fails on several operations with DuckDB 2.0, such as `list_tables()`. See the [Ibis guide]({% link docs/2.0/guides/python/ibis.md %}).

### `DESCRIBE` Returns an Empty Table in JupySQL

In JupySQL, the `DESCRIBE` statement returns an empty table:

```python
%%sql
CREATE OR REPLACE TABLE tbl AS (SELECT 42 AS x);
DESCRIBE tbl;
```

To work around this, wrap it into a subquery:

```python
%%sql
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
