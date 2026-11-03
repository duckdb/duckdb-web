---
layout: docu
redirect_from:
- /docs/guides/python/export_pandas
- /docs/stable/guides/python/export_pandas
- /docs/current/guides/python/export_pandas
- /docs/lts/guides/python/export_pandas
- /docs/preview/guides/python/export_pandas
title: Export to Pandas
how_to_topic: python
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

DuckDB also supports [importing from Pandas]({% link docs/2.0/guides/python/import_pandas.md %}).
