---
layout: docu
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

The seamless integration of Pandas DataFrames into DuckDB SQL queries is allowed by [replacement scans]({% link docs/preview/clients/c/replacement_scans.md %}), which replace instances of accessing the `my_df` table (which does not exist in DuckDB) with a table function that reads the `my_df` dataframe.
