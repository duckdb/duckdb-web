---
layout: docu
redirect_from:
- /docs/guides/python/export_numpy
- /docs/stable/guides/python/export_numpy
- /docs/current/guides/python/export_numpy
- /docs/lts/guides/python/export_numpy
- /docs/preview/guides/python/export_numpy
title: Export to Numpy
how_to_topic: python
---

The result of a query can be converted to Numpy arrays using the `fetchnumpy()` function, which returns a dictionary that maps each column name to a Numpy array. For example:

```python
import duckdb
import numpy as np

my_arr = duckdb.sql("SELECT unnest([1, 2, 3]) AS x, 5.0 AS y").fetchnumpy()
my_arr
```

```text
{'x': array([1, 2, 3], dtype=int32), 'y': array([5., 5., 5.])}
```

Then, the array can be processed using Numpy functions, e.g.:

```python
np.sum(my_arr['x'])
```

```text
np.int64(6)
```

## See Also

DuckDB also supports [importing from Numpy]({% link docs/2.0/guides/python/import_numpy.md %}).
