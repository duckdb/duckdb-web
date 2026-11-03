---
layout: docu
redirect_from:
- /docs/guides/python/import_numpy
- /docs/stable/guides/python/import_numpy
- /docs/current/guides/python/import_numpy
- /docs/lts/guides/python/import_numpy
- /docs/preview/guides/python/import_numpy
title: Import from Numpy
how_to_topic: python
---

It is possible to query Numpy arrays from DuckDB.
There is no need to register the arrays manually –
DuckDB can find them in the Python process by name thanks to [replacement scans]({% link docs/2.0/guides/glossary.md %}#replacement-scan).
For example:

```python
import duckdb
import numpy as np

columns = {
    "id": np.array([1, 2, 3]),
    "value": np.array([9.0, 8.0, 7.0]),
}
print(duckdb.sql("SELECT * FROM columns").fetchall())
```

```text
[(1, 9.0), (2, 8.0), (3, 7.0)]
```

Each array supplies one column. DuckDB also accepts a two-dimensional array, treating each outer array as a column. Transpose an array whose outer dimension represents rows before querying it.

A [masked array](https://numpy.org/doc/stable/reference/maskedarray.html) is read with its mask: masked elements become `NULL`.

```python
my_masked_arr = np.ma.masked_array([1.0, 2.0, 3.0], mask=[False, True, False])

duckdb.sql("SELECT * FROM my_masked_arr")
```

```text
┌─────────┐
│ column0 │
│ double  │
├─────────┤
│     1.0 │
│    NULL │
│     3.0 │
└─────────┘
```

## See Also

DuckDB also supports [exporting to Numpy]({% link docs/2.0/guides/python/export_numpy.md %}).
