---
layout: docu
title: Jupyter Notebooks
selected: Jupyter Notebooks
---

# DuckDB in Jupyter Notebooks
DuckDB's Python client can be used directly in Jupyter notebooks with no additional configration if desired. 
However, additional libraries can be used to simplify SQL query development. 
This guide will describe how to utilize those additional libraries.
See other guides in the Python section for how to use DuckDB and Python together.  
  
As a small note, for maximum performance converting large output datasets to Pandas Dataframes, using DuckDB directly may be desirable. However, the difference is typically quite small.  

This example workflow is also available as a [Google Collab notebook](https://colab.research.google.com/drive/1eOA2FYHqEfZWLYssbUxdIpSL3PFxWVjk?usp=sharing).

## Library Installation
Four additional libraries improve the DuckDB experience in Jupyter notebooks. 
1. [Pandas](https://github.com/pandas-dev/pandas)
    * Clean table visualizations and compatibility with other analysis
2. [ipython-sql](https://github.com/catherinedevlin/ipython-sql)
    * Convert a Jupyter code cell into a SQL cell
3. [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
    * Used by ipython-sql to connect to databases
4. [duckdb_engine (DuckDB SQLAlchemy driver)](https://github.com/Mause/duckdb_engine)
    * Used by SQLAlchemy to connect to DuckDB

```python
# Run these pip install commands from the command line if Jupyter Notebook is not yet installed.
# Otherwise, see Google Collab link above for an in-notebook example
pip install duckdb

# Install Jupyter Notebook
pip install notebook

# Install supporting libraries
pip install pandas       # conda install pandas
pip install ipython-sql 
pip install SQLAlchemy
pip install duckdb-engine
```

## Library Import and Configuration
Next, open a Jupyter Notebook and import the relevant libraries. 
```python
import duckdb
import pandas as pd
import sqlalchemy
# No need to import duckdb_engine
#  SQLAlchemy will auto-detect the driver needed based on your connection string!

# Import ipython-sql Jupyter extension to create SQL cells
%load_ext sql
```

Set configrations on ipython-sql to directly output data to Pandas and to simplify the output that is printed to the notebook.  
```python
%config SqlMagic.autopandas = True
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
```

Connect ipython-sql to DuckDB using a SQLAlchemy-style connection string. 
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

## Summary
You now have the ability to alternate between SQL and Pandas in a simple and highly performant way! Dataframes can be read as tables in SQL, and SQL results can be output into Dataframes. Happy analyzing!