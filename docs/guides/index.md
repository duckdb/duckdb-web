---
layout: docu
title: Guides
selected: Guides
---

The guides section contains compact how-to guides that are focused on achieving a single goal. For an in-depth reference see the Documentation section.

## DuckDB SQL

* [ASOF Join](../guides/sql_features/asof_join)
* [Full Text Search](../guides/sql_features/full_text_search)

## SQL: Data Import & Export

##### CSV Files

* [How to load a CSV file into a table](../guides/import/csv_import)
* [How to export a table to a CSV file](../guides/import/csv_export)

##### Parquet Files

* [How to load a Parquet file into a table](../guides/import/parquet_import)
* [How to export a table to a Parquet file](../guides/import/parquet_export)
* [How to run a query directly on a Parquet file](../guides/import/query_parquet)

##### JSON Files

* [How to load a JSON file into a table](../guides/import/json_import)
* [How to export a table to a JSON file](../guides/import/json_export)

##### Excel Files with the Spatial Extension
* [How to load an Excel file into a table](../guides/import/excel_import)
* [How to export a table to an Excel file](../guides/import/excel_export)

##### HTTP, S3 and GCP

* [How to load a Parquet file directly from HTTP(s)](../guides/import/http_import)
* [How to load a Parquet file directly from S3 or GCS](../guides/import/s3_import)

## SQL: Meta Queries

* [How to list all tables](../guides/meta/list_tables)
* [How to view the schema of the result of a query](../guides/meta/describe)
* [How to quickly get a feel for a dataset using summarize](../guides/meta/summarize)
* [How to view the query plan of a query](../guides/meta/explain)
* [How to profile a query](../guides/meta/explain_analyze)

## Python Client

* [How to install the Python client](../guides/python/install)
* [How to execute SQL queries](../guides/python/execute_sql)
* [How to easily query DuckDB in Jupyter Notebooks](../guides/python/jupyter)
* [How to use Multiple Python Threads with DuckDB](../guides/python/multiple_threads)
* [How to use fsspec filesystems with DuckDB](../guides/python/filesystems)

### Pandas

* [How to execute SQL on a Pandas DataFrame](../guides/python/sql_on_pandas)
* [How to create a table from a Pandas DataFrame](../guides/python/import_pandas)
* [How to export data to a Pandas DataFrame](../guides/python/export_pandas)

### Apache Arrow

* [How to execute SQL on Apache Arrow](../guides/python/sql_on_arrow)
* [How to create a DuckDB table from Apache Arrow](../guides/python/import_arrow)
* [How to export data to Apache Arrow](../guides/python/export_arrow)

### Relational API

* [How to query Pandas DataFrames with the Relational API](../guides/python/relational_api_pandas)

### Python Library Integrations

* [How to use Ibis to query DuckDB with or without SQL](../guides/python/ibis)
* [How to use FugueSQL to use DuckDB with Python/Pandas functions](../guides/python/fugue)
* [How to use DuckDB with Polars DataFrames via Apache Arrow](../guides/python/polars)
* [How to use DuckDB with Vaex DataFrames via Apache Arrow](../guides/python/vaex)
* [How to use DuckDB with DataFusion via Apache Arrow](../guides/python/datafusion)

## SQL Editors / IDE's

* [How to set up the DBeaver SQL IDE](../guides/sql_editors/dbeaver)
* [How to use the Harlequin terminal-based SQL IDE](../guides/sql_editors/harlequin)
* [How to use qStudio SQL IDE](../guides/sql_editors/qstudio)
* [How to set up Rill Data Developer](../guides/sql_editors/rill)


## Data Viewers

* [How to use Tad to view tabular data files and DuckDB databases](../guides/data_viewers/tad)
* [How to Visualise DuckDB databases with Tableau](../guides/data_viewers/tableau)
* [How to draw command-line plots with DuckDB and YouPlot](../guides/data_viewers/youplot)
