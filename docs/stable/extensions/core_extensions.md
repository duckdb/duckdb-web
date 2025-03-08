---
layout: docu
redirect_from:
- /docs/extensions/official_extensions
- /docs/extensions/official_extensions/
- /docs/extensions/core_extensions
title: Core Extensions
---

## List of Core Extensions

| Name                                                              | GitHub                                                                          | Description                                                                        | Autoloadable | Aliases                 |
| :---------------------------------------------------------------- | ------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [arrow]({% link docs/stable/extensions/arrow.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)           | A zero-copy data integration between Apache Arrow and DuckDB                       | no           |                         |
| [autocomplete]({% link docs/stable/extensions/autocomplete.md %}) |                                                                                 | Adds support for autocomplete in the shell                                         | yes          |                         |
| [aws]({% link docs/stable/extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)      | Provides features that depend on the AWS SDK                                       | yes          |                         |
| [azure]({% link docs/stable/extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)    | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes          |                         |
| [delta]({% link docs/stable/extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)    | Adds support for Delta Lake                                                        | yes          |                         |
| [excel]({% link docs/stable/extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)    | Adds support for Excel-like format strings                                         | yes          |                         |
| [fts]({% link docs/stable/extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)      | Adds support for Full-Text Search Indexes                                          | yes          |                         |
| [httpfs]({% link docs/stable/extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)   | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes          | http, https, s3         |
| [iceberg]({% link docs/stable/extensions/iceberg.md %})           | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)  | Adds support for Apache Iceberg                                                    | no           |                         |
| [icu]({% link docs/stable/extensions/icu.md %})                   |                                                                                 | Adds support for time zones and collations using the ICU library                   | yes          |                         |
| [inet]({% link docs/stable/extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)     | Adds support for IP-related data types and functions                               | yes          |                         |
| [jemalloc]({% link docs/stable/extensions/jemalloc.md %})         |                                                                                 | Overwrites system allocator with jemalloc                                          | no           |                         |
| [json]({% link docs/stable/data/json/overview.md %})              |                                                                                 | Adds support for JSON operations                                                   | yes          |                         |
| [mysql]({% link docs/stable/extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)    | Adds support for reading from and writing to a MySQL database                      | no           | mysql_scanner           |
| [parquet]({% link docs/stable/data/parquet/overview.md %})        |                                                                                 | Adds support for reading and writing Parquet files                                 | (built-in)   |                         |
| [postgres]({% link docs/stable/extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres) | Adds support for reading from and writing to a PostgreSQL database                 | yes          | postgres_scanner        |
| [spatial]({% link docs/stable/extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)  | Geospatial extension that adds support for working with spatial data and functions | no           |                         |
| [sqlite]({% link docs/stable/extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)   | Adds support for reading from and writing to SQLite database files                 | yes          | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/stable/extensions/tpcds.md %})               |                                                                                 | Adds TPC-DS data generation and query support                                      | yes          |                         |
| [tpch]({% link docs/stable/extensions/tpch.md %})                 |                                                                                 | Adds TPC-H data generation and query support                                       | yes          |                         |
| [vss]({% link docs/stable/extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)      | Adds support for vector similarity search queries                                  | no           |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                              | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/stable/extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/stable/extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/stable/data/json/overview.md %})              | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/stable/data/parquet/overview.md %})        | yes | yes    | yes | yes  | yes     |
| [tpch]({% link docs/stable/extensions/tpch.md %})                 |     | yes    |     |      |         |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/stable/extensions/jemalloc.md %}) for details.
