---
layout: docu
redirect_from:
- docs/archive/1.1/extensions/official_extensions
title: Core Extensions
---

## List of Core Extensions

| Name                                                       | GitHub                                                                                           | Description                                                                        | Autoloadable  | Aliases                 |
|:-----------------------------------------------------------|--------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:--------------|:------------------------|
| [arrow]({% link docs/archive/1.1/extensions/arrow.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)                            | A zero-copy data integration between Apache Arrow and DuckDB                       | no            |                         |
| [autocomplete]({% link docs/archive/1.1/extensions/autocomplete.md %}) |                                                                                                  | Adds support for autocomplete in the shell                                         | yes           |                         |
| [aws]({% link docs/archive/1.1/extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)                       | Provides features that depend on the AWS SDK                                       | yes           |                         |
| [azure]({% link docs/archive/1.1/extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)                     | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes           |                         |
| [delta]({% link docs/archive/1.1/extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)                     | Adds support for Delta Lake                                                        | yes           |                         |
| [excel]({% link docs/archive/1.1/extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)                     | Adds support for Excel-like format strings                                         | yes           |                         |
| [fts]({% link docs/archive/1.1/extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)                       | Adds support for Full-Text Search Indexes                                          | yes           |                         |
| [httpfs]({% link docs/archive/1.1/extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)                    | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes           | http, https, s3         |
| [iceberg]({% link docs/archive/1.1/extensions/iceberg.md %})           | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)                   | Adds support for Apache Iceberg                                                    | no            |                         |
| [icu]({% link docs/archive/1.1/extensions/icu.md %})                   |                                                                                                  | Adds support for time zones and collations using the ICU library                   | yes           |                         |
| [inet]({% link docs/archive/1.1/extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)                      | Adds support for IP-related data types and functions                               | yes           |                         |
| [jemalloc]({% link docs/archive/1.1/extensions/jemalloc.md %})         |                                                                                                  | Overwrites system allocator with jemalloc                                          | no            |                         |
| [json]({% link docs/archive/1.1/data/json/overview.md %})              |                                                                                                  | Adds support for JSON operations                                                   | yes           |                         |
| [mysql]({% link docs/archive/1.1/extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)                     | Adds support for reading from and writing to a MySQL database                      | no            |                         |
| [parquet]({% link docs/archive/1.1/data/parquet/overview.md %})        |                                                                                                  | Adds support for reading and writing Parquet files                                 | (built-in)    |                         |
| [postgres]({% link docs/archive/1.1/extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres)                  | Adds support for reading from and writing to a PostgreSQL database                 | yes           | postgres_scanner        |
| [spatial]({% link docs/archive/1.1/extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)                   | Geospatial extension that adds support for working with spatial data and functions | no            |                         |
| [sqlite]({% link docs/archive/1.1/extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)                    | Adds support for reading from and writing to SQLite database files                 | yes           | sqlite_scanner, sqlite3 |
| [substrait]({% link docs/archive/1.1/extensions/substrait.md %})       | [<span class="github">GitHub</span>](https://github.com/substrait-io/duckdb-substrait-extension) | Adds support for the Substrait integration                                         | no            |                         |
| [tpcds]({% link docs/archive/1.1/extensions/tpcds.md %})               |                                                                                                  | Adds TPC-DS data generation and query support                                      | yes           |                         |
| [tpch]({% link docs/archive/1.1/extensions/tpch.md %})                 |                                                                                                  | Adds TPC-H data generation and query support                                       | yes           |                         |
| [vss]({% link docs/archive/1.1/extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)                       | Adds support for vector similarity search queries                                  | no            |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name | CLI (duckdb.org) | CLI (Homebrew) | Python | R | Java | Node.js |
|------|------|------|---|---|---|---|---|
| [autocomplete]({% link docs/archive/1.1/extensions/autocomplete.md %}) | yes | yes |     |     |     |     |
| [excel]({% link docs/archive/1.1/extensions/excel.md %})               | yes |     |     |     |     |     |
| [fts]({% link docs/archive/1.1/extensions/full_text_search.md %})      | yes |     | yes |     |     |     |
| [httpfs]({% link docs/archive/1.1/extensions/httpfs/overview.md %})    |     |     |     |     |     |     |
| [icu]({% link docs/archive/1.1/extensions/icu.md %})                   | yes | yes | yes |     | yes | yes |
| [json]({% link docs/archive/1.1/data/json/overview.md %})              | yes | yes | yes |     | yes | yes |
| [parquet]({% link docs/archive/1.1/data/parquet/overview.md %})        | yes | yes | yes | yes | yes | yes |
| [tpcds]({% link docs/archive/1.1/extensions/tpcds.md %})               |     |     | yes |     |     |     |
| [tpch]({% link docs/archive/1.1/extensions/tpch.md %})                 | yes |     | yes |     |     |     |

The [jemalloc]({% link docs/archive/1.1/extensions/jemalloc.md %}) extension's availability is based on the operating system.
Starting with version 0.10.1, `jemalloc` is a built-in extension on Linux x86_64 (AMD64) distributions, while it will be optionally available on Linux ARM64 distributions and on macOS (via compiling from source).
On Windows, it is not available.