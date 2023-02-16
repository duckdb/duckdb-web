---
layout: docu
title: Relational API and Pandas
selected: Relational API and Pandas
---

# How to use the Relational API to query Pandas

DuckDB offers a relational API that can be used to chain together query operations. These are lazily evaluated so that DuckDB can optimize their execution. These operators can act on Pandas DataFrames, DuckDB tables or views (which can point to any underlying storage format that DuckDB can read, such as csv or parquet files, etc.). Here we show a simple example of reading from a Pandas DataFrame and returning a DataFrame.

```python
import duckdb
import pandas

# connect to an in-memory database
con = duckdb.connect()

input_df = pandas.DataFrame.from_dict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})

# create a DuckDB relation from a dataframe
rel = con.from_df(input_df)

# chain together relational operators (this is a lazy operation, so the operations are not yet executed)
# equivalent to: SELECT i, j, i*2 as two_i FROM input_df ORDER BY i desc limit 2
transformed_rel = rel.filter('i >= 2').project('i, j, i*2 as two_i').order('i desc').limit(2)

# trigger execution by requesting .df() of the relation
# .df() could have been added to the end of the chain above - it was separated for clarity
output_df = transformed_rel.df()
```

Relational operators can also be used to group rows, aggregate, find distinct combinations of values, join, union, and more! They are also able to directly insert results into a DuckDB table or write to a csv.  

Please see [these additional examples](https://github.com/duckdb/duckdb/blob/master/examples/python/duckdb-python.py), and [the available relational methods on the DuckDBPyRelation class](https://duckdb.org/docs/api/python/reference/#duckdb.DuckDBPyRelation).
