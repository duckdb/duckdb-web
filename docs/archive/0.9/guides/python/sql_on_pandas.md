---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/python/sql_on_pandas
- docs/archive/0.9.1/guides/python/sql_on_pandas
- docs/archive/0.9.0/guides/python/sql_on_pandas
title: SQL on Pandas
---

Pandas DataFrames stored in local variables can be queried as if they are regular tables within DuckDB.

```python
import duckdb
import pandas

# Create a Pandas dataframe
my_df = pandas.DataFrame.from_dict({'a': [42]})

# query the Pandas DataFrame "my_df"
# Note: duckdb.sql connects to the default in-memory database connection
results = duckdb.sql("SELECT * FROM my_df").df()
```