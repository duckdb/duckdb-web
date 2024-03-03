---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/python/export_pandas
- docs/archive/0.9.1/guides/python/export_pandas
title: Export to Pandas
---

The result of a query can be converted to a Pandas DataFrame using the `df()` function.


```python
import duckdb

# read the result of an arbitrary SQL query to a Pandas DataFrame
results = duckdb.sql("SELECT 42").df()
```