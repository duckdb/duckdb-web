---
layout: docu
title: Import From Pandas
selected: Import From Pandas
---

# How to create a table from a Pandas DataFrame

`CREATE TABLE AS` and `INSERT INTO` can be used to create a table from any query. We can then create tables or insert into existing tables by referring to referring to the Pandas DataFrame in the query.

```py
import duckdb
import pandas

# connect to an in-memory database
con = duckdb.connect()

my_df = pandas.DataFrame.from_dict({'a': [42]})

# create the table "my_table" from the DataFrame "my_df"
con.execute("CREATE TABLE my_table AS SELECT * FROM my_df")

# insert into the table "my_table" from the DataFrame "my_df"
con.execute("INSERT INTO my_table SELECT * FROM my_df")
```
