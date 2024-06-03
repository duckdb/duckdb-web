---
layout: docu
title: Export to Numpy
---

The result of a query can be converted to a Numpy array using the `fetchnumpy()` function. For example:

```python
import duckdb
import numpy as np

my_arr = duckdb.sql("SELECT unnest([1, 2, 3]) AS x, 5.0 AS y").fetchnumpy()
my_arr
```

```text
{'x': array([1, 2, 3], dtype=int32), 'y': masked_array(data=[5.0, 5.0, 5.0],
             mask=[False, False, False],
       fill_value=1e+20)}
```

Then, the array can be processed using Numpy functions, e.g.:

```python
np.sum(my_arr['x'])
```

```text
6
```

## See Also

DuckDB also supports [importing from Numpy](import_numpy).