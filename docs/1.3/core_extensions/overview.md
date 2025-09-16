---
layout: docu
title: Core Extensions
---

## List of Core Extensions

| Name                                                                    | GitHub                                                                           | Description                                                                        | Stage        | Aliases                 |
| :---------------------------------------------------------------------- | -------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [autocomplete]({% link docs/1.3/core_extensions/autocomplete.md %}) |                                                                                  | Adds support for autocomplete in the shell                                         | stable       |                         |
| [avro]({% link docs/1.3/core_extensions/avro.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-avro)      | Add support for reading Avro files                                                 | stable       |                         |
| [aws]({% link docs/1.3/core_extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)       | Provides features that depend on the AWS SDK                                       | stable       |                         |
| [azure]({% link docs/1.3/core_extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)     | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | stable       |                         |
| [delta]({% link docs/1.3/core_extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)     | Adds support for Delta Lake                                                        | experimental |                         |
| [ducklake]({% link docs/1.3/core_extensions/ducklake.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/ducklake)         | Adds support for DuckLake                                                          | experimental |                         |
| [encodings]({% link docs/1.3/core_extensions/encodings.md %})       | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-encodings) | Adds support for encodings available in the ICU data repository                    | experimental |                         |
| [excel]({% link docs/1.3/core_extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)     | Adds support for reading and writing Excel files                                   | experimental |                         |
| [fts]({% link docs/1.3/core_extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)       | Adds support for full-text search indexes                                          | experimental |                         |
| [httpfs]({% link docs/1.3/core_extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)    | Adds support for reading and writing files over an HTTP(S) or S3 connection        | stable       | http, https, s3         |
| [iceberg]({% link docs/1.3/core_extensions/iceberg/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)   | Adds support for Apache Iceberg                                                    | experimental |                         |
| [icu]({% link docs/1.3/core_extensions/icu.md %})                   |                                                                                  | Adds support for time zones and collations using the ICU library                   | stable       |                         |
| [inet]({% link docs/1.3/core_extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)      | Adds support for IP-related data types and functions                               | experimental |                         |
| [jemalloc]({% link docs/1.3/core_extensions/jemalloc.md %})         |                                                                                  | Overwrites system the allocator with jemalloc                                      | stable       |                         |
| [json]({% link docs/1.3/data/json/overview.md %})                   |                                                                                  | Adds support for JSON operations                                                   | stable       |                         |
| [mysql]({% link docs/1.3/core_extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)     | Adds support for reading from and writing to a MySQL database                      | stable       | mysql_scanner           |
| [parquet]({% link docs/1.3/data/parquet/overview.md %})             |                                                                                  | Adds support for reading and writing Parquet files                                 | stable       |                         |
| [postgres]({% link docs/1.3/core_extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres)  | Adds support for reading from and writing to a PostgreSQL database                 | stable       | postgres_scanner        |
| [spatial]({% link docs/1.3/core_extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)   | Geospatial extension that adds support for working with spatial data and functions | experimental |                         |
| [sqlite]({% link docs/1.3/core_extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)    | Adds support for reading from and writing to SQLite database files                 | stable       | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/1.3/core_extensions/tpcds.md %})               |                                                                                  | Adds TPC-DS data generation and query support                                      | experimental |                         |
| [tpch]({% link docs/1.3/core_extensions/tpch.md %})                 |                                                                                  | Adds TPC-H data generation and query support                                       | stable       |                         |
| [ui]({% link docs/1.3/core_extensions/ui.md %})                     | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-ui)        | Adds local UI for DuckDB                                                           | experimental |                         |
| [vss]({% link docs/1.3/core_extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)       | Adds support for vector similarity search queries                                  | experimental |                         |

The **Stage** column shows the lifecycle stage of the extension following the convention of the [lifecycle stages used in tidyverse](https://lifecycle.r-lib.org/articles/stages.html).

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                                    | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/1.3/core_extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/1.3/core_extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/1.3/data/json/overview.md %})                   | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/1.3/data/parquet/overview.md %})             | yes | yes    | yes | yes  | yes     |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/1.3/core_extensions/jemalloc.md %}) for details.
