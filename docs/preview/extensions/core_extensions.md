---
layout: docu
title: Core Extensions
---

## List of Core Extensions

| Name                                                              | GitHub                                                                          | Description                                                                        | Autoloadable | Aliases                 |
| :---------------------------------------------------------------- | ------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [autocomplete]({% link docs/preview/extensions/autocomplete.md %}) |                                                                                 | Adds support for autocomplete in the shell                                         | yes          |                         |
| [avro]({% link docs/preview/extensions/avro.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-avro)     | Add support for reading Avro files                                                 | yes          |                         |
| [aws]({% link docs/preview/extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)      | Provides features that depend on the AWS SDK                                       | yes          |                         |
| [azure]({% link docs/preview/extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)    | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes          |                         |
| [delta]({% link docs/preview/extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)    | Adds support for Delta Lake                                                        | yes          |                         |
| [excel]({% link docs/preview/extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)    | Adds support for reading and writing Excel files                                   | yes          |                         |
| [fts]({% link docs/preview/extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)      | Adds support for full-text search indexes                                          | yes          |                         |
| [httpfs]({% link docs/preview/extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)   | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes          | http, https, s3         |
| [iceberg]({% link docs/preview/extensions/iceberg/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)  | Adds support for Apache Iceberg                                                    | no           |                         |
| [icu]({% link docs/preview/extensions/icu.md %})                   |                                                                                 | Adds support for time zones and collations using the ICU library                   | yes          |                         |
| [inet]({% link docs/preview/extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)     | Adds support for IP-related data types and functions                               | yes          |                         |
| [jemalloc]({% link docs/preview/extensions/jemalloc.md %})         |                                                                                 | Overwrites system the allocator with jemalloc                                      | no           |                         |
| [json]({% link docs/preview/data/json/overview.md %})              |                                                                                 | Adds support for JSON operations                                                   | yes          |                         |
| [mysql]({% link docs/preview/extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)    | Adds support for reading from and writing to a MySQL database                      | no           | mysql_scanner           |
| [parquet]({% link docs/preview/data/parquet/overview.md %})        |                                                                                 | Adds support for reading and writing Parquet files                                 | (built-in)   |                         |
| [postgres]({% link docs/preview/extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres) | Adds support for reading from and writing to a PostgreSQL database                 | yes          | postgres_scanner        |
| [spatial]({% link docs/preview/extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)  | Geospatial extension that adds support for working with spatial data and functions | no           |                         |
| [sqlite]({% link docs/preview/extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)   | Adds support for reading from and writing to SQLite database files                 | yes          | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/preview/extensions/tpcds.md %})               |                                                                                 | Adds TPC-DS data generation and query support                                      | yes          |                         |
| [tpch]({% link docs/preview/extensions/tpch.md %})                 |                                                                                 | Adds TPC-H data generation and query support                                       | yes          |                         |
| [ui]({% link docs/preview/extensions/ui.md %})                     | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-ui)       | Adds local UI for DuckDB                                                           | yes          |                         |
| [vss]({% link docs/preview/extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)      | Adds support for vector similarity search queries                                  | no           |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                              | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/preview/extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/preview/extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/preview/data/json/overview.md %})              | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/preview/data/parquet/overview.md %})        | yes | yes    | yes | yes  | yes     |
| [tpch]({% link docs/preview/extensions/tpch.md %})                 |     | yes    |     |      |         |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/preview/extensions/jemalloc.md %}) for details.
