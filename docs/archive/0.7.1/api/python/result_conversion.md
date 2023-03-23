---
layout: docu
title: Result Conversion
selected: Client APIs
---
DuckDB's Python client provides multiple additional methods that can be used to efficiently retrieve data.
### NumPy
* `fetchnumpy()` fetches the data as a dictionary of NumPy arrays

### Pandas
* `df()` fetches the data as a Pandas DataFrame
* `fetchdf()` is an alias of `df()`
* `fetch_df()` is an alias of `df()`
* `fetch_df_chunk(vector_multiple)` fetches a portion of the results into a DataFrame. The number of rows returned in each chunk is the vector size (2048 by default) * vector_multiple (1 by default).

### Apache Arrow
* `arrow()` fetches the data as an [Arrow table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* `fetch_arrow_table()` is an alias of `arrow()`
* `fetch_record_batch(chunk_size)` returns an [Arrow record batch reader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) with `chunk_size` rows per batch

### Polars
* `pl()` fetches the data as a Polars DataFrame

Below are some examples using this functionality. See the Python [guides](../../guides/index#python-client) for more examples.

```python
# fetch as Pandas DataFrame
df = con.execute("SELECT * FROM items").fetchdf()
print(df)
#        item   value  count
# 0     jeans    20.0      1
# 1    hammer    42.2      2
# 2    laptop  2000.0      1
# 3  chainsaw   500.0     10
# 4    iphone   300.0      2

# fetch as dictionary of numpy arrays
arr = con.execute("SELECT * FROM items").fetchnumpy()
print(arr)
# {'item': masked_array(data=['jeans', 'hammer', 'laptop', 'chainsaw', 'iphone'],
#              mask=[False, False, False, False, False],
#        fill_value='?',
#             dtype=object), 'value': masked_array(data=[20.0, 42.2, 2000.0, 500.0, 300.0],
#              mask=[False, False, False, False, False],
#        fill_value=1e+20), 'count': masked_array(data=[1, 2, 1, 10, 2],
#              mask=[False, False, False, False, False],
#        fill_value=999999,
#             dtype=int32)}

# fetch as an Arrow table. Converting to Pandas afterwards just for pretty printing
tbl = con.execute("SELECT * FROM items").fetch_arrow_table()
print(tbl.to_pandas())
#        item    value  count
# 0     jeans    20.00      1
# 1    hammer    42.20      2
# 2    laptop  2000.00      1
# 3  chainsaw   500.00     10
# 4    iphone   300.00      2
```
