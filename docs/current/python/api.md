---
layout: default
title: Python API
selected: Documentation/Python API
---
# Python Installation
DuckDB can be installed for Python using the following command:

```bash
pip install duckdb
```

# Simple Usage
The standard DuckDB Python API provides a SQL interface compliant with the DB-API 2.0 specification described by PEP 249. It is based on the SQLite Python API.

To use the module, you must first create a `Connection` object that represents the database. The connection object takes as parameter the database file to read and write from. The special value `:memory:` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the Python process).

```python
import duckdb
con = duckdb.connect(':memory:')
```

Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL commands:

```python
c = con.cursor()

# create a table
c.execute("CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
# insert an item into the table
c.execute("INSERT INTO items VALUES ('jeans', 20.0, 1)")

# retrieve the item again
c.execute("SELECT * FROM items")
print(c.fetchall())
# [['jeans', 20.0, 1]]
```

# Efficient Retrieval
When retrieving the data from DuckDB back into Python, the standard method of calling `fetchall()` is inefficient as individual Python objects need to be created for every value in the result set. When retrieving a lot of data, this can become very costly.

In DuckDB, there are two additional methods that can be used to efficiently retrieve dat: `fetchnumpy()` and `fetchdf()`. `fetchnumpy()` fetches the data as a dictionary of `NumPy` arrays. `fetchdf()` fetches the data as a Pandas DataFrame.

Below is an example of using this functionality:

```python
# fetch as pandas data frame
df = c.execute("SELECT * FROM items").fetchdf()
print(df)
#    item  value  count
# 0  jeans   20.0      1

# fetch as dictionary of numpy arrays
arr = c.execute("SELECT * FROM items").fetchnumpy()
print(arr)
# {'item': masked_array(data=['jeans'], mask=False, fill_value='?', dtype=object),
#  'value': masked_array(data=[20.], mask=False, fill_value=1e+20),
#  'count': masked_array(data=[1], mask=False, fill_value=999999, dtype=int32)}

```