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

## 'object' columns

pandas.DataFrame columns of an `object` dtype require some special care, since this stores values of arbitrary type.

To convert these columns to DuckDB, we first go through an analyze phase before converting the values.

In this analyze phase a sample of all the rows of the column are analyzed to determine the target type.

This sample size is by default set to 1000.

If the type picked during the analyze step is wrong, this will result in a "Failed to cast value:" error, in which case you will need to increase the sample size.

The sample size can be changed by setting the `pandas_analyze_sample` config option.
```py
# example setting the sample size to 100000
duckdb.default_connection.execute("SET GLOBAL pandas_analyze_sample=100000")
```
