---
layout: docu
title: Import from Numpy
---

It is possible to query Numpy arrays from DuckDB.
There is no need to register the arrays manually –
DuckDB can find them in the Python process by name thanks to [replacement scans]({% link docs/archive/1.1/guides/glossary.md %}#replacement-scan).
For example:

```python
import duckdb
import numpy as np

my_arr = np.array([(1, 9.0), (2, 8.0), (3, 7.0)])

duckdb.sql("SELECT * FROM my_arr")
```

```text
┌─────────┬─────────┬─────────┐
│ column0 │ column1 │ column2 │
│ double  │ double  │ double  │
├─────────┼─────────┼─────────┤
│     1.0 │     2.0 │     3.0 │
│     9.0 │     8.0 │     7.0 │
└─────────┴─────────┴─────────┘
```

## See Also

DuckDB also supports [exporting to Numpy]({% link docs/archive/1.1/guides/python/export_numpy.md %}).