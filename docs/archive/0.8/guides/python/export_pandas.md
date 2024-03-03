---
layout: docu
redirect_from:
- docs/archive/0.8.1/guides/python/export_pandas
selected: Export To Pandas
title: Export To Pandas
---

# How to export data to a Pandas DataFrame

The result of a query can be converted to a Pandas DataFrame using the `df()` function.


```py
import duckdb

# read the result of an arbitrary SQL query to a Pandas DataFrame
results = duckdb.sql("SELECT 42").df()
```