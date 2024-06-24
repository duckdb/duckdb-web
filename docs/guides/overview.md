---
layout: docu
title: Guides
redirect_from:
- /docs/guides
- /docs/guides/index
---

The guides section contains compact how-to guides that are focused on achieving a single goal. For an API references and examples, see the rest of the documentation.

Note that there are many tools using DuckDB, which are not covered in the official guides. To find a list of these tools, check out the [Awesome DuckDB repository](https://github.com/davidgasquez/awesome-duckdb).

> Tip For a short introductory tutorial, check out the [Analyzing Railway Traffic in the Netherlands]({% link _posts/2024-05-31-analyzing-railway-traffic-in-the-netherlands.md %}) tutorial.

## Data Import and Export

* [Data import overview]({% link docs/guides/file_formats/overview.md %})

### CSV Files

* [How to load a CSV file into a table]({% link docs/guides/file_formats/csv_import.md %})
* [How to export a table to a CSV file]({% link docs/guides/file_formats/csv_export.md %})

### Parquet Files

* [How to load a Parquet file into a table]({% link docs/guides/file_formats/parquet_import.md %})
* [How to export a table to a Parquet file]({% link docs/guides/file_formats/parquet_export.md %})
* [How to run a query directly on a Parquet file]({% link docs/guides/file_formats/query_parquet.md %})

### HTTP(S), S3 and GCP

* [How to load a Parquet file directly from HTTP(S)]({% link docs/guides/network_cloud_storage/http_import.md %})
* [How to load a Parquet file directly from S3]({% link docs/guides/network_cloud_storage/s3_import.md %})
* [How to export a Parquet file to S3]({% link docs/guides/network_cloud_storage/s3_export.md %})
* [How to load a Parquet file from S3 Express One]({% link docs/guides/network_cloud_storage/s3_express_one.md %})
* [How to load a Parquet file directly from GCS]({% link docs/guides/network_cloud_storage/gcs_import.md %})
* [How to load a Parquet file directly from Cloudflare R2]({% link docs/guides/network_cloud_storage/cloudflare_r2_import.md %})
* [How to load an Iceberg table directly from S3]({% link docs/guides/network_cloud_storage/s3_iceberg_import.md %})

### JSON Files

* [How to load a JSON file into a table]({% link docs/guides/file_formats/json_import.md %})
* [How to export a table to a JSON file]({% link docs/guides/file_formats/json_export.md %})

### Excel Files with the Spatial Extension

* [How to load an Excel file into a table]({% link docs/guides/file_formats/excel_import.md %})
* [How to export a table to an Excel file]({% link docs/guides/file_formats/excel_export.md %})

### Querying Other Database Systems

* [How to directly query a MySQL database]({% link docs/guides/database_integration/mysql.md %})
* [How to directly query a PostgreSQL database]({% link docs/guides/database_integration/postgres.md %})
* [How to directly query a SQLite database]({% link docs/guides/database_integration/sqlite.md %})

### Directly Reading Files

* [How to directly read a binary file]({% link docs/guides/file_formats/read_file.md %}#read_blob)
* [How to directly read a text file]({% link docs/guides/file_formats/read_file.md %}#read_text)

## Performance

* [My workload is slow (troubleshooting guide)]({% link docs/guides/performance/my_workload_is_slow.md %})
* [How to design the schema for optimal performance]({% link docs/guides/performance/schema.md %})
* [What is the ideal hardware environment for DuckDB]({% link docs/guides/performance/environment.md %})
* [What performance implications do Parquet files and (compressed) CSV files have]({% link docs/guides/performance/file_formats.md %})
* [How to tune workloads]({% link docs/guides/performance/how_to_tune_workloads.md %})
* [Benchmarks]({% link docs/guides/performance/benchmarks.md %})

## Meta Queries

* [How to list all tables]({% link docs/guides/meta/list_tables.md %})
* [How to view the schema of the result of a query]({% link docs/guides/meta/describe.md %})
* [How to quickly get a feel for a dataset using summarize]({% link docs/guides/meta/summarize.md %})
* [How to view the query plan of a query]({% link docs/guides/meta/explain.md %})
* [How to profile a query]({% link docs/guides/meta/explain_analyze.md %})

## ODBC

* [How to set up an ODBC application (and more!)]({% link docs/guides/odbc/general.md %})

## Python Client

* [How to install the Python client]({% link docs/guides/python/install.md %})
* [How to execute SQL queries]({% link docs/guides/python/execute_sql.md %})
* [How to easily query DuckDB in Jupyter Notebooks]({% link docs/guides/python/jupyter.md %})
* [How to use Multiple Python Threads with DuckDB]({% link docs/guides/python/multiple_threads.md %})
* [How to use fsspec filesystems with DuckDB]({% link docs/guides/python/filesystems.md %})

### Pandas

* [How to execute SQL on a Pandas DataFrame]({% link docs/guides/python/sql_on_pandas.md %})
* [How to create a table from a Pandas DataFrame]({% link docs/guides/python/import_pandas.md %})
* [How to export data to a Pandas DataFrame]({% link docs/guides/python/export_pandas.md %})

### Apache Arrow

* [How to execute SQL on Apache Arrow]({% link docs/guides/python/sql_on_arrow.md %})
* [How to create a DuckDB table from Apache Arrow]({% link docs/guides/python/import_arrow.md %})
* [How to export data to Apache Arrow]({% link docs/guides/python/export_arrow.md %})

### Relational API

* [How to query Pandas DataFrames with the Relational API]({% link docs/guides/python/relational_api_pandas.md %})

### Python Library Integrations

* [How to use Ibis to query DuckDB with or without SQL]({% link docs/guides/python/ibis.md %})
* [How to use DuckDB with Polars DataFrames via Apache Arrow]({% link docs/guides/python/polars.md %})

## SQL Features

* [Friendly SQL]({% link docs/guides/sql_features/friendly_sql.md %})
* [As-of join]({% link docs/guides/sql_features/asof_join.md %})
* [Full-text search]({% link docs/guides/sql_features/full_text_search.md %})

## SQL Editors and IDEs

* [How to set up the DBeaver SQL IDE]({% link docs/guides/sql_editors/dbeaver.md %})

## Data Viewers

* [How to visualize DuckDB databases with Tableau]({% link docs/guides/data_viewers/tableau.md %})
* [How to draw command-line plots with DuckDB and YouPlot]({% link docs/guides/data_viewers/youplot.md %})
