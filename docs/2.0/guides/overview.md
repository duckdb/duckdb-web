---
layout: docu
redirect_from:
- /docs/guides
- /docs/guides/index
- /docs/guides/overview
- /docs/stable/guides/overview
- /guides
- /docs/current/guides/overview
- /docs/lts/guides/overview
- /docs/preview/guides/overview
title: Guides
---

The guides section contains compact how-to guides that are focused on achieving a single goal.
For API references and examples, see the rest of the documentation.

Note that there are many tools using DuckDB, which are not covered in the official guides.
To find a list of these tools, check out the [Awesome DuckDB repository](https://github.com/davidgasquez/awesome-duckdb).

> Tip For a short introductory tutorial, check out the [“Analyzing Railway Traffic in the Netherlands”]({% post_url 2024-05-31-analyzing-railway-traffic-in-the-netherlands %}) tutorial.

## Data Import and Export

* [Data import overview]({% link docs/2.0/guides/file_formats/overview.md %})
* [File access with the `file:` protocol]({% link docs/2.0/guides/file_formats/file_access.md %})
* [Reading DuckDB databases]({% link docs/2.0/guides/file_formats/read_duckdb.md %})

### CSV Files

* [How to load a CSV file into a table]({% link docs/2.0/guides/file_formats/csv_import.md %})
* [How to export a table to a CSV file]({% link docs/2.0/guides/file_formats/csv_export.md %})

### Parquet Files

* [How to load a Parquet file into a table]({% link docs/2.0/guides/file_formats/parquet_import.md %})
* [How to export a table to a Parquet file]({% link docs/2.0/guides/file_formats/parquet_export.md %})
* [How to run a query directly on a Parquet file]({% link docs/2.0/guides/file_formats/query_parquet.md %})

### HTTP(S), S3 and GCP

* [Network and cloud storage overview]({% link docs/2.0/guides/network_cloud_storage/overview.md %})
* [How to authenticate to S3 / AWS]({% link docs/2.0/core_extensions/httpfs/authentication.md %})
* [How to load a Parquet file directly from HTTP(S)]({% link docs/2.0/guides/network_cloud_storage/http_import.md %})
* [How to load a CSV file directly from HTTP(S)]({% link docs/2.0/guides/network_cloud_storage/http_csv_import.md %})
* [How to load a Parquet file directly from S3]({% link docs/2.0/guides/network_cloud_storage/s3_import.md %})
* [How to export a Parquet file to S3]({% link docs/2.0/guides/network_cloud_storage/s3_export.md %})
* [How to load a Parquet file from S3 Express One]({% link docs/2.0/guides/network_cloud_storage/s3_express_one.md %})
* [How to load a Parquet file directly from GCS]({% link docs/2.0/guides/network_cloud_storage/gcs_import.md %})
* [How to load a Parquet file directly from Cloudflare R2]({% link docs/2.0/guides/network_cloud_storage/cloudflare_r2_import.md %})
* [How to load a Parquet file directly from Fastly Object Storage]({% link docs/2.0/guides/network_cloud_storage/fastly_object_storage_import.md %})
* [How to load a Parquet file directly from SeaweedFS]({% link docs/2.0/guides/network_cloud_storage/seaweedfs_import.md %})
* [How to load a Parquet file directly from Tigris]({% link docs/2.0/guides/network_cloud_storage/tigris_import.md %})
* [How to load an Iceberg table directly from S3]({% link docs/2.0/guides/network_cloud_storage/s3_iceberg_import.md %})
* [How to connect to Amazon S3 Tables]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}#amazon-s3-tables)
* [How to connect to Amazon SageMaker Lakehouse (AWS Glue)]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}#aws-glue-amazon-sagemaker-lakehouse)
* [How to share a DuckDB database that only stores views]({% link docs/2.0/guides/network_cloud_storage/duckdb_views_only.md %})
* [How to attach to a DuckDB database over HTTPS or S3]({% link docs/2.0/guides/network_cloud_storage/duckdb_over_https_or_s3.md %})

### JSON Files

* [How to load a JSON file into a table]({% link docs/2.0/guides/file_formats/json_import.md %})
* [How to export a table to a JSON file]({% link docs/2.0/guides/file_formats/json_export.md %})

### Excel Files

* [How to load an Excel file into a table]({% link docs/2.0/guides/file_formats/excel_import.md %})
* [How to export a table to an Excel file]({% link docs/2.0/guides/file_formats/excel_export.md %})

### Querying Other Database Systems

* [Database integration overview]({% link docs/2.0/guides/database_integration/overview.md %})
* [How to directly query a MySQL database]({% link docs/2.0/guides/database_integration/mysql.md %})
* [How to directly query a PostgreSQL database]({% link docs/2.0/guides/database_integration/postgres.md %})
* [How to directly query a SQLite database]({% link docs/2.0/guides/database_integration/sqlite.md %})
* [How to connect to Amazon RDS / Aurora with IAM authentication]({% link docs/2.0/guides/database_integration/rds_iam.md %})

### Directly Reading Files

* [How to directly read a binary file]({% link docs/2.0/guides/file_formats/read_file.md %}#read_blob)
* [How to directly read a text file]({% link docs/2.0/guides/file_formats/read_file.md %}#read_text)

## Performance

* [Performance guide overview]({% link docs/2.0/guides/performance/overview.md %})
* [My workload is slow (troubleshooting guide)]({% link docs/2.0/guides/performance/my_workload_is_slow.md %})
* [How to design the schema for optimal performance]({% link docs/2.0/guides/performance/schema.md %})
* [What is the ideal hardware environment for DuckDB]({% link docs/2.0/guides/performance/environment.md %})
* [How to import data efficiently]({% link docs/2.0/guides/performance/import.md %})
* [How to use indexes and zonemaps]({% link docs/2.0/guides/performance/indexing.md %})
* [How to make join operations efficient]({% link docs/2.0/guides/performance/join_operations.md %})
* [What performance implications do Parquet files and (compressed) CSV files have]({% link docs/2.0/guides/performance/file_formats.md %})
* [How to tune workloads]({% link docs/2.0/guides/performance/how_to_tune_workloads.md %})
* [How to avoid out-of-memory issues]({% link docs/2.0/guides/performance/oom.md %})
* [How to work with huge databases]({% link docs/2.0/guides/performance/working_with_huge_databases.md %})
* [Benchmarks]({% link docs/2.0/guides/performance/benchmarks.md %})

## Meta Queries

* [How to list all tables]({% link docs/2.0/guides/meta/list_tables.md %})
* [How to view the schema of the result of a query]({% link docs/2.0/guides/meta/describe.md %})
* [How to quickly get a feel for a dataset using summarize]({% link docs/2.0/guides/meta/summarize.md %})
* [How to view the query plan of a query]({% link docs/2.0/guides/meta/explain.md %})
* [How to profile a query]({% link docs/2.0/guides/meta/explain_analyze.md %})
* [How to inspect the DuckDB environment (version, platform, extensions)]({% link docs/2.0/guides/meta/duckdb_environment.md %})

## ODBC

* [How to set up an ODBC application (and more!)]({% link docs/2.0/guides/odbc/general.md %})

## Python Client

* [How to install the Python client]({% link docs/2.0/guides/python/install.md %})
* [How to execute SQL queries]({% link docs/2.0/guides/python/execute_sql.md %})
* [How to easily query DuckDB in Jupyter Notebooks]({% link docs/2.0/guides/python/jupyter.md %})
* [How to easily query DuckDB in marimo Notebooks]({% link docs/2.0/guides/python/marimo.md %})
* [How to use Multiple Python Threads with DuckDB]({% link docs/2.0/guides/python/multiple_threads.md %})
* [How to use fsspec filesystems with DuckDB]({% link docs/2.0/guides/python/filesystems.md %})

### Pandas

* [How to execute SQL on a Pandas DataFrame]({% link docs/2.0/guides/python/sql_on_pandas.md %})
* [How to create a table from a Pandas DataFrame]({% link docs/2.0/guides/python/import_pandas.md %})
* [How to export data to a Pandas DataFrame]({% link docs/2.0/guides/python/export_pandas.md %})

### NumPy

* [How to create a table from NumPy arrays]({% link docs/2.0/guides/python/import_numpy.md %})
* [How to export data to NumPy arrays]({% link docs/2.0/guides/python/export_numpy.md %})

### Apache Arrow

* [How to execute SQL on Apache Arrow]({% link docs/2.0/guides/python/sql_on_arrow.md %})
* [How to create a DuckDB table from Apache Arrow]({% link docs/2.0/guides/python/import_arrow.md %})
* [How to export data to Apache Arrow]({% link docs/2.0/guides/python/export_arrow.md %})

### Relational API

* [How to query Pandas DataFrames with the Relational API]({% link docs/2.0/guides/python/relational_api_pandas.md %})

### Python Library Integrations

* [How to use Ibis to query DuckDB with or without SQL]({% link docs/2.0/guides/python/ibis.md %})
* [How to use DuckDB with Polars DataFrames via Apache Arrow]({% link docs/2.0/guides/python/polars.md %})
* [How to stream DuckDB query results to PyTorch via Apache Arrow]({% link docs/2.0/guides/python/pytorch.md %})

## SQL Features

* [Friendly SQL]({% link docs/2.0/sql/dialect/friendly_sql.md %})
* [As-of join]({% link docs/2.0/guides/sql_features/asof_join.md %})
* [Full-text search]({% link docs/2.0/guides/sql_features/full_text_search.md %})
* [Graph queries]({% link docs/2.0/guides/sql_features/graph_queries.md %})
* [`query` and `query_table` functions]({% link docs/2.0/guides/sql_features/query_and_query_table_functions.md %})
* [Merge statement for SCD Type 2]({% link docs/2.0/guides/sql_features/merge.md %})
* [Timestamp issues]({% link docs/2.0/guides/sql_features/timestamps.md %})

## SQL Editors and IDEs

* [How to set up the Beekeeper Studio SQL editor]({% link docs/2.0/guides/sql_editors/beekeeper_studio.md %})
* [How to set up the DBeaver SQL IDE]({% link docs/2.0/guides/sql_editors/dbeaver.md %})
* [How to set up the DBine SQL editor]({% link docs/2.0/guides/sql_editors/dbine.md %})
* [How to set up the LibreDB Studio SQL editor]({% link docs/2.0/guides/sql_editors/libredb_studio.md %})
* [How to set up the VisuaLeaf SQL editor]({% link docs/2.0/guides/sql_editors/visualeaf.md %})

## Data Viewers

* [How to visualize DuckDB databases with Tableau]({% link docs/2.0/guides/data_viewers/tableau.md %})
* [How to draw command-line plots with DuckDB and YouPlot]({% link docs/2.0/guides/data_viewers/youplot.md %})

## Snippets

* [Creating synthetic data]({% link docs/2.0/guides/snippets/create_synthetic_data.md %})
* [Dutch railway datasets]({% link docs/2.0/guides/snippets/dutch_railway_datasets.md %})
* [Sharing macros]({% link docs/2.0/guides/snippets/sharing_macros.md %})
* [Analyzing a Git repository]({% link docs/2.0/guides/snippets/analyze_git_repository.md %})
* [Importing duckbox tables]({% link docs/2.0/guides/snippets/importing_duckbox_tables.md %})
* [Copying an in-memory database to a file]({% link docs/2.0/guides/snippets/copy_in-memory_database_to_file.md %})
* [Calculating a database checksum]({% link docs/2.0/guides/snippets/database_checksum.md %})

## Troubleshooting

* [Command line]({% link docs/2.0/guides/troubleshooting/command_line.md %})
* [Crashes]({% link docs/2.0/guides/troubleshooting/crashes.md %})
* [Out of memory errors]({% link docs/2.0/guides/troubleshooting/oom_errors.md %})

## Glossary and Offline Docs

* [Glossary of terms]({% link docs/2.0/guides/glossary.md %})
* [Browsing offline]({% link docs/2.0/guides/offline-copy.md %})
