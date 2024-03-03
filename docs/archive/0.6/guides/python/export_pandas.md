---
layout: docu
redirect_from:
- docs/archive/0.6.1/guides/python/export_pandas
selected: Export To Pandas
title: Export To Pandas
---

# How to export data to a Pandas DataFrame

The result of a query can be converted to a Pandas DataFrame using the `df()` function.


```py
import duckdb
import pandas

# connect to an in-memory database
con = duckdb.connect()

my_df = pandas.DataFrame.from_dict({'a': [42]})

# read the result of an arbitrary SQL query to a Pandas DataFrame
results = con.execute("SELECT 42").df()
```