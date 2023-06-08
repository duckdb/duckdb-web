---
layout: docu
title: SQL on Pandas
selected: SQL on Pandas
---

# How to execute SQL on a Pandas DataFrame

Pandas DataFrames stored in local variables can be queried as if they are regular tables within DuckDB.

```py
import duckdb
import pandas

# Create a Pandas dataframe
my_df = pandas.DataFrame.from_dict({'a': [42]})

# query the Pandas DataFrame "my_df"
# Note: duckdb.sql connects to the default in-memory database connection
results = duckdb.sql("SELECT * FROM my_df").df()
```
