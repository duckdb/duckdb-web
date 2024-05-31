---
layout: docu
redirect_from:
- docs/archive/0.7.1/guides/python/sql_on_pandas
selected: SQL on Pandas
title: SQL on Pandas
---

# How to execute SQL on a Pandas DataFrame

Pandas DataFrames stored in local variables can be queried as if they are regular tables within DuckDB.

```py
import duckdb
import pandas

# connect to an in-memory database
my_df = pandas.DataFrame.from_dict({'a': [42]})

# query the Pandas DataFrame "my_df"
results = duckdb.sql("SELECT * FROM my_df").df()
```