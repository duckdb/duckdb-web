---
layout: docu
title: Jupyter Notebooks
selected: Jupyter Notebooks
---

# DuckDB in Jupyter Notebooks
DuckDB's Python client can be used directly in Jupyter notebooks with no additional configration if desired. 
However, additional libraries can be used to add syntax highlighting and simplify SQL development. 
This guide will describe how to utilize those additional libraries. 
See other guides in the Python section for how to use DuckDB and Python together.  
As a small note, for maximum performance converting large output datasets to Pandas Dataframes, using DuckDB directly may be desirable. However, the difference is typically quite small.  

## Library Installation
Four additional libraries improve the DuckDB experience in Jupyter notebooks. 
1. [Pandas](https://github.com/pandas-dev/pandas)
    * Clean table visualizations and compatiblity with other analysis
2. [ipython-sql](https://github.com/catherinedevlin/ipython-sql)
    * Convert a Jupyter code cell into a SQL cell
    * SQL syntax highlighting
3. [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
    * Used by ipython-sql to connect to databases
4. [duckdb_engine (DuckDB SQLAlchemy driver)](https://github.com/Mause/duckdb_engine)
    * Allows SQLAlchemy to connect to DuckDB

```python
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

# Import ipython-sql SQL syntax highlighting Jupyter extension
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

To return query results into a variable for future usage, use `<<` as an assignment operator.
This can be used with both the `%sql` and `%%sql` Jupyter magics.
```sql
%sql my_df << SELECT 'Off and flying!' as a_duckdb_column
```

## Querying Pandas Dataframes
DuckDB is able to find and query any dataframe stored as a variable in the Jupyter notebook.
```python
test_df = pd.DataFrame.from_dict({"i":[1, 2, 3],
                                  "j":["one", "two", "three"]})
```
The dataframe can be specified just like any other table in the `FROM` clause.  
```sql
%sql output_df << SELECT sum(i) as total_i FROM test_df
```

## Total Workflow Example - Querying Pandas Dataframes
<img src="/images/guides/jupyter_querying_pandas_dfs.png" alt="Total Jupyter Workflow" title="Total Jupyter Workflow"/>
