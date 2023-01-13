---
layout: docu
title: Jupyter Notebooks
selected: Jupyter Notebooks
---

# DuckDB in Jupyter Notebooks
DuckDB's Python client can be used directly in Jupyter notebooks with no additional configuration if desired. 
However, additional libraries can be used to simplify SQL query development. 
This guide will describe how to utilize those additional libraries.
See other guides in the Python section for how to use DuckDB and Python together.  

In this example, we used the [jupysql](https://github.com/ploomber/jupysql) package which is a direct fork of [ipython-sql](https://github.com/catherinedevlin/ipython-sql).
The main difference is that `Jupysql` is well maintained, has newer features and bug fixes.
  
As a small note, for maximum performance converting large output datasets to Pandas Dataframes, using DuckDB directly may be desirable. However, the difference is typically quite small.  

This example workflow is also available as a [Google Collab notebook](https://colab.research.google.com/drive/1eOA2FYHqEfZWLYssbUxdIpSL3PFxWVjk?usp=sharing).

## Library Installation
Four additional libraries improve the DuckDB experience in Jupyter notebooks. 
1. [jupysql](https://github.com/ploomber/jupysql)
    * Convert a Jupyter code cell into a SQL cell
2. [duckdb_engine (DuckDB SQLAlchemy driver)](https://github.com/Mause/duckdb_engine)
    * Used by SQLAlchemy to connect to DuckDB
3. [Pandas](https://github.com/pandas-dev/pandas)
    * Clean table visualizations and compatibility with other analysis
4. [matplotlib](https://github.com/matplotlib/matplotlib)
    * Plotting with Python

```python
# Run these pip install commands from the command line if Jupyter Notebook is not yet installed.
# Otherwise, see Google Collab link above for an in-notebook example
pip install duckdb

# Install Jupyter Notebook (Note: you can also install JupyterLab: pip install jupyterlab) 
pip install notebook

# Install supporting libraries
pip install jupysql
pip install duckdb-engine
pip install pandas       # conda install pandas (in case pip fails)
pip install matplotlib
```

## Library Import and Configuration
Next, open a Jupyter Notebook and import the relevant libraries. 
```python
import duckdb
import pandas as pd
# No need to import duckdb_engine
#  SQLAlchemy will auto-detect the driver needed based on your connection string!

# Import jupysql Jupyter extension to create SQL cells
%load_ext sql
```

Set configrations on jupysql to directly output data to Pandas and to simplify the output that is printed to the notebook.  
```python
%config SqlMagic.autopandas = True
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
```

Connect jupysql to DuckDB using a SQLAlchemy-style connection string. 
You may either connect to an in memory DuckDB, or a file backed db.
```python
%sql duckdb:///:memory:
# %sql duckdb:///path/to/file.db
```

## Querying DuckDB
Single line SQL queries can be run using `%sql` at the start of a line. Query results will be displayed as a Pandas DF.
```sql
%sql SELECT 'Off and flying!' as a_duckdb_column
```
An entire Jupyter cell can be used as a SQL cell by placing `%%sql` at the start of the cell. Query results will be displayed as a Pandas DF.
```sql
%%sql
SELECT
    schema_name,
    function_name
FROM duckdb_functions()
ORDER BY ALL DESC
LIMIT 5
```

To return query results into a Pandas dataframe for future usage, use `<<` as an assignment operator.
This can be used with both the `%sql` and `%%sql` Jupyter magics.
```sql
%sql my_df << SELECT 'Off and flying!' as a_duckdb_column
```

## Querying Pandas Dataframes
DuckDB is able to find and query any dataframe stored as a variable in the Jupyter notebook.
```python
input_df = pd.DataFrame.from_dict({"i":[1, 2, 3],
                                  "j":["one", "two", "three"]})
```
The dataframe being queried can be specified just like any other table in the `FROM` clause.  
```sql
%sql output_df << SELECT sum(i) as total_i FROM input_df
```

## Visualizing DuckDB Data
The most common way for plotting datasets in Python is to load them using pandas and then use matplotlib or seaborn for plotting.
This approach requires loading all your data into memory which is highly inefficient.
The plotting module in JupySQL runs computations in the SQL engine. 
This delegates memory management to the engine and ensures that intermediate computations do not keep eating up memory, allowing you to efficiently plot massive datasets. 

### Download data
In this example, we will query a .parquet file using DuckDB.

```python
from pathlib import Path
from urllib.request import urlretrieve

if not Path("yellow_tripdata_2021-01.parquet").is_file():
    urlretrieve("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet",
                "yellow_tripdata_2021-01.parquet")
```

Load the extension and connect to an in-memory DuckDB database:
```python
%sql duckdb://
```
Note: We’ll be using a sample dataset that contains historical taxi data from NYC (from the above cell).

### Boxplot & Histogram
To create a boxplot, call `%sqlplot boxplot`, and pass the name of the table, 
and the column you want to plot.

```python
%sqlplot boxplot --table yellow_tripdata_2021-01.parquet --column trip_distance
```

Now, let’s create a query that filters by the 90th percentile. 
Note that we’re using the --save, and --no-execute functions. 
This tells JupySQL to store the query, but skips execution. We’ll reference it in our next plotting call.


```python
%%sql --save short-trips --no-execute
SELECT *
FROM "yellow_tripdata_2021-01.parquet"
WHERE trip_distance < 6.3
```

To create a histogram, call %sqlplot histogram, and pass the name of the table, the column you want to plot, and the number of bins. 
We’re using --with short-trips so JupySQL uses the query we defined and only plots such data subset.

```python
%sqlplot histogram --table short-trips --column trip_distance --bins 10 --with short-trips
```

## Summary
You now have the ability to alternate between SQL and Pandas in a simple and highly performant way! You can plot massive datasets directly through the engine (avoiding pandas inefficiency). Dataframes can be read as tables in SQL, and SQL results can be output into Dataframes. Happy analyzing!
