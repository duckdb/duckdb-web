---
layout: docu
title: Core Extensions
---

## List of Core Extensions

| Name                                                              | GitHub                                                                          | Description                                                                        | Autoloadable | Aliases                 |
| :---------------------------------------------------------------- | ------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [autocomplete]({% link docs/preview/core_extensions/autocomplete.md %}) |                                                                                 | Adds support for autocomplete in the shell                                         | yes          |                         |
| [avro]({% link docs/preview/core_extensions/avro.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-avro)     | Add support for reading Avro files                                                 | yes          |                         |
| [aws]({% link docs/preview/core_extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)      | Provides features that depend on the AWS SDK                                       | yes          |                         |
| [azure]({% link docs/preview/core_extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)    | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes          |                         |
| [delta]({% link docs/preview/core_extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)    | Adds support for Delta Lake                                                        | yes          |                         |
| [excel]({% link docs/preview/core_extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)    | Adds support for reading and writing Excel files                                   | yes          |                         |
| [fts]({% link docs/preview/core_extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)      | Adds support for full-text search indexes                                          | yes          |                         |
| [httpfs]({% link docs/preview/core_extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)   | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes          | http, https, s3         |
| [iceberg]({% link docs/preview/core_extensions/iceberg/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)  | Adds support for Apache Iceberg                                                    | no           |                         |
| [icu]({% link docs/preview/core_extensions/icu.md %})                   |                                                                                 | Adds support for time zones and collations using the ICU library                   | yes          |                         |
| [inet]({% link docs/preview/core_extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)     | Adds support for IP-related data types and functions                               | yes          |                         |
| [jemalloc]({% link docs/preview/core_extensions/jemalloc.md %})         |                                                                                 | Overwrites system the allocator with jemalloc                                      | no           |                         |
| [json]({% link docs/preview/data/json/overview.md %})              |                                                                                 | Adds support for JSON operations                                                   | yes          |                         |
| [mysql]({% link docs/preview/core_extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)    | Adds support for reading from and writing to a MySQL database                      | no           | mysql_scanner           |
| [parquet]({% link docs/preview/data/parquet/overview.md %})        |                                                                                 | Adds support for reading and writing Parquet files                                 | (built-in)   |                         |
| [postgres]({% link docs/preview/core_extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres) | Adds support for reading from and writing to a PostgreSQL database                 | yes          | postgres_scanner        |
| [spatial]({% link docs/preview/core_extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)  | Geospatial extension that adds support for working with spatial data and functions | no           |                         |
| [sqlite]({% link docs/preview/core_extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)   | Adds support for reading from and writing to SQLite database files                 | yes          | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/preview/core_extensions/tpcds.md %})               |                                                                                 | Adds TPC-DS data generation and query support                                      | yes          |                         |
| [tpch]({% link docs/preview/core_extensions/tpch.md %})                 |                                                                                 | Adds TPC-H data generation and query support                                       | yes          |                         |
| [ui]({% link docs/preview/core_extensions/ui.md %})                     | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-ui)       | Adds local UI for DuckDB                                                           | yes          |                         |
| [vss]({% link docs/preview/core_extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)      | Adds support for vector similarity search queries                                  | no           |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                              | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/preview/core_extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/preview/core_extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/preview/data/json/overview.md %})              | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/preview/data/parquet/overview.md %})        | yes | yes    | yes | yes  | yes     |
| [tpch]({% link docs/preview/core_extensions/tpch.md %})                 |     | yes    |     |      |         |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/preview/core_extensions/jemalloc.md %}) for details.
