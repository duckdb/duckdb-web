---
layout: docu
title: Export to Pandas
---

The result of a query can be converted to a [Pandas](https://pandas.pydata.org/) DataFrame using the `df()` function.

```python
import duckdb

# read the result of an arbitrary SQL query to a Pandas DataFrame
results = duckdb.sql("SELECT 42").df()
results
```

```text
   42
0  42
```

## See Also

DuckDB also supports [importing from Pandas]({% link docs/guides/python/import_pandas.md %}).
