---
layout: docu
title: Jupyter Notebooks
---

DuckDB's Python client can be used directly in Jupyter notebooks with no additional configuration if desired.
However, additional libraries can be used to simplify SQL query development.
This guide will describe how to utilize those additional libraries.
See other guides in the Python section for how to use DuckDB and Python together.

In this example, we use the [JupySQL](https://github.com/ploomber/jupysql) package. This example workflow is also available as a [Google Colab notebook](https://colab.research.google.com/drive/1bNfU8xRTu8MQJnCbyyDRxvptklLb0ExH?usp=sharing).

## Library Installation

Four additional libraries improve the DuckDB experience in Jupyter notebooks.

1. [jupysql](https://github.com/ploomber/jupysql): Convert a Jupyter code cell into a SQL cell
2. [Pandas](https://github.com/pandas-dev/pandas): Clean table visualizations and compatibility with other analysis
3. [matplotlib](https://github.com/matplotlib/matplotlib): Plotting with Python
4. [duckdb-engine (DuckDB SQLAlchemy driver)](https://github.com/Mause/duckdb_engine): Used by SQLAlchemy to connect to DuckDB (optional)

Run these `pip install` commands from the command line if Jupyter Notebook is not yet installed. Otherwise, see Google Colab link above for an in-notebook example:

```batch
pip install duckdb
```

Install Jupyter Notebook:

```batch
pip install notebook
```

Or JupyterLab:

```batch
pip install jupyterlab
```

Install supporting libraries:

```batch
pip install jupysql pandas matplotlib duckdb-engine
```

## Library Import and Configuration

Open a Jupyter Notebook and import the relevant libraries.

Set configurations on jupysql to directly output data to Pandas and to simplify the output that is printed to the notebook.

```python
%config SqlMagic.autopandas = True
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
```

### Connecting to DuckDB Natively

To connect to DuckDB, run:

```python
import duckdb
import pandas as pd

%load_ext sql
conn = duckdb.connect()
%sql conn --alias duckdb
```

> Warning [Variables]({% link docs/preview/sql/statements/set_variable.md %}) are not recognized within a native DuckDB connection.

### Connecting to DuckDB via SQLAlchemy

Alternatively, you can connect to DuckDB via SQLAlchemy using `duckdb_engine`. See the [performance and feature differences](https://jupysql.ploomber.io/en/latest/tutorials/duckdb-native-sqlalchemy.html).

```python
import duckdb
import pandas as pd
# No need to import duckdb_engine
#  jupysql will auto-detect the driver needed based on the connection string!

# Import jupysql Jupyter extension to create SQL cells
%load_ext sql
```
Either connect to a new [in-memory DuckDB]({% link docs/preview/clients/python/dbapi.md %}#in-memory-connection), the [default connection]({% link docs/preview/clients/python/dbapi.md %}#default-connection), or a file-backed database:

```sql
%sql duckdb:///:memory:
```

```sql
%sql duckdb:///:default:
```

```sql
%sql duckdb:///path/to/file.db
```

> The `%sql` command and `duckdb.sql` share the same [default connection]({% link docs/preview/clients/python/dbapi.md %}) if you provide `duckdb:///:default:` as the SQLAlchemy connection string.

## Querying DuckDB

Single line SQL queries can be run using `%sql` at the start of a line. Query results will be displayed as a Pandas DataFrame.

```sql
%sql SELECT 'Off and flying!' AS a_duckdb_column;
```

An entire Jupyter cell can be used as a SQL cell by placing `%%sql` at the start of the cell. Query results will be displayed as a Pandas DataFrame.

```sql
%%sql
SELECT
    schema_name,
    function_name
FROM duckdb_functions()
ORDER BY ALL DESC
LIMIT 5;
```

To store the query results in a Python variable, use `<<` as an assignment operator.
This can be used with both the `%sql` and `%%sql` Jupyter magics.

```sql
%sql res << SELECT 'Off and flying!' AS a_duckdb_column;
```

If the `%config SqlMagic.autopandas = True` option is set, the variable is a Pandas dataframe, otherwise, it is a `ResultSet` that can be converted to Pandas with the `DataFrame()` function.

## Querying Pandas Dataframes

DuckDB is able to find and query any dataframe stored as a variable in the Jupyter notebook.

```python
input_df = pd.DataFrame.from_dict({"i": [1, 2, 3],
                                   "j": ["one", "two", "three"]})
```

The dataframe being queried can be specified just like any other table in the `FROM` clause.

```sql
%sql output_df << SELECT sum(i) AS total_i FROM input_df;
```
> Warning When using the SQLAlchemy connection, and DuckDB >= 1.1.0, make sure to run `%sql SET python_scan_all_frames=true`, to make Pandas dataframes queryable. 

## Visualizing DuckDB Data

The most common way to plot datasets in Python is to load them using Pandas and then use matplotlib or seaborn for plotting.
This approach requires loading all data into memory which is highly inefficient.
The plotting module in JupySQL runs computations in the SQL engine.
This delegates memory management to the engine and ensures that intermediate computations do not keep eating up memory, efficiently plotting massive datasets.

### Boxplot & Histogram

To create a boxplot, call `%sqlplot boxplot`, passing the name of the table and the column to plot.
In this case, the name of the table is the path of the locally stored Parquet file.

```python
from urllib.request import urlretrieve

_ = urlretrieve(
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet",
    "yellow_tripdata_2021-01.parquet",
)

%sqlplot boxplot --table yellow_tripdata_2021-01.parquet --column trip_distance
```

<img src="/images/trip-distance-boxplot.png"
     alt="Boxplot of the trip_distance column"
     width="500"
     />

### Install and Load DuckDB httpfs Extension

DuckDB's [httpfs extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) allows Parquet and CSV files to be queried remotely over http.
These examples query a Parquet file that contains historical taxi data from NYC.
Using the Parquet format allows DuckDB to only pull the rows and columns into memory that are needed rather than downloading the entire file.
DuckDB can be used to process local [Parquet files]({% link docs/preview/data/parquet/overview.md %}) as well, which may be desirable if querying the entire Parquet file, or running multiple queries that require large subsets of the file.

```sql
%%sql
INSTALL httpfs;
LOAD httpfs;
```

Now, create a query that filters by the 90th percentile.
Note the use of the `--save`, and `--no-execute` functions.
This tells JupySQL to store the query, but skips execution. It will be referenced in the next plotting call.

```sql
%%sql --save short_trips --no-execute
SELECT *
FROM 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet'
WHERE trip_distance < 6.3
```

To create a histogram, call `%sqlplot histogram` and pass the name of the table, the column to plot, and the number of bins.
This uses `--with short-trips` so JupySQL uses the query defined previously and therefore only plots a subset of the data.

```python
%sqlplot histogram --table short_trips --column trip_distance --bins 10 --with short_trips
```

<img src="/images/trip-distance-histogram.png"
     alt="Histogram of the trip_distance column"
     width="500"
     />

## Summary

You now have the ability to alternate between SQL and Pandas in a simple and highly performant way! You can plot massive datasets directly through the engine (avoiding both the download of the entire file and loading all of it into Pandas in memory). Dataframes can be read as tables in SQL, and SQL results can be output into Dataframes. Happy analyzing!

An alternative to `jupysql` is [`magic_duckdb`](https://github.com/iqmo-org/magic_duckdb).
