---
layout: docu
title: Export to Pandas
---

The result of a query can be converted to a Pandas DataFrame using the `df()` function.


```python
import duckdb

# read the result of an arbitrary SQL query to a Pandas DataFrame
results = duckdb.sql("SELECT 42").df()
```