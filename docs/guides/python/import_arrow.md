---
layout: docu
title: Import From Apache Arrow
selected: Import From Apache Arrow
---

# How to create a table from Apache Arrow

`CREATE TABLE AS` and `INSERT INTO` can be used to create a table from any query. We can then create tables or insert into existing tables by referring to referring to the Apache Arrow object in the query. DuckDB can query different Apache Arrow formats, as seen below.

## Arrow Table

```py
import duckdb
import pyarrow

# connect to an in-memory database
con = duckdb.connect()

my_arrow = 

# create the table "my_table" from the DataFrame "my_df"
con.execute("CREATE TABLE my_table AS SELECT * FROM my_arrow")

# insert into the table "my_table" from the DataFrame "my_df"
con.execute("INSERT INTO my_table SELECT * FROM my_arrow")
```
## Arrow RecordBatch
