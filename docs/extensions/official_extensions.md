---
layout: docu
title: Official Extensions
---

## List of Official Extensions

| Name                         | GitHub                                                                           | Description                                                                        | Autoloadable  | Aliases                 |
|:-----------------------------|----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:--------------|:------------------------|
| [arrow]({% link docs/extensions/arrow.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)            | A zero-copy data integration between Apache Arrow and DuckDB                       | no            |                         |
| [autocomplete]({% link docs/extensions/autocomplete.md %}) |                                                                                  | Adds support for autocomplete in the shell                                         | yes           |                         |
| [aws]({% link docs/extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_aws)       | Provides features that depend on the AWS SDK                                       | yes           |                         |
| [azure]({% link docs/extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_azure)     | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes           |                         |
| [excel]({% link docs/extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_excel)     | Adds support for Excel-like format strings                                         | yes           |                         |
| [fts]({% link docs/extensions/full_text_search.md %})      |                                                                                  | Adds support for Full-Text Search Indexes                                          | yes           |                         |
| [httpfs]({% link docs/extensions/httpfs/overview.md %})             |                                                                                  | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes           | http, https, s3         |
| [iceberg]({% link docs/extensions/iceberg.md %})           | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_iceberg)   | Adds support for Apache Iceberg                                                    | no            |                         |
| [icu]({% link docs/extensions/icu.md %})                   |                                                                                  | Adds support for time zones and collations using the ICU library                   | yes           |                         |
| [inet]({% link docs/extensions/inet.md %})                 |                                                                                  | Adds support for IP-related data types and functions                               | yes           |                         |
| [jemalloc]({% link docs/extensions/jemalloc.md %})         |                                                                                  | Overwrites system allocator with jemalloc                                          | no            |                         |
| [json]({% link docs/extensions/json.md %})                 |                                                                                  | Adds support for JSON operations                                                   | yes           |                         |
| [mysql]({% link docs/extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_mysql)     | Adds support for reading from and writing to a MySQL database                      | no            |                         |
| [parquet]({% link docs/data/parquet/overview.md %})           |                                                                                  | Adds support for reading and writing Parquet files                                 | (built-in)    |                         |
| [postgres]({% link docs/extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/postgres_scanner) | Adds support for reading from and writing to a Postgres database                   | yes           | postgres_scanner        |
| [spatial]({% link docs/extensions/spatial.md %})           | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_spatial)   | Geospatial extension that adds support for working with spatial data and functions | no            |                         |
| [sqlite]({% link docs/extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/sqlite_scanner)   | Adds support for reading from and writing to SQLite database files                 | yes           | sqlite_scanner, sqlite3 |
| [substrait]({% link docs/extensions/substrait.md %})       | [<span class="github">GitHub</span>](https://github.com/duckdb/substrait)        | Adds support for the Substrait integration                                         | no            |                         |
| [tpcds]({% link docs/extensions/tpcds.md %})               |                                                                                  | Adds TPC-DS data generation and query support                                      | yes           |                         |
| [tpch]({% link docs/extensions/tpch.md %})                 |                                                                                  | Adds TPC-H data generation and query support                                       | yes           |                         |
| [vss]({% link docs/extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_vss)       | Adds support for vector similarity search queries                                  | no            |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

<div class="narrow_table"></div>

| Name | CLI (duckdb.org) | CLI (Homebrew) | Python | R | Java | Node.js |
|------|------|------|---|---|---|---|---|
| [autocomplete]({% link docs/extensions/autocomplete.md %}) | yes | yes |     |     |     |     |
| [excel]({% link docs/extensions/excel.md %})               | yes |     |     |     |     |     |
| [fts]({% link docs/extensions/full_text_search.md %})      | yes |     | yes |     |     |     |
| [httpfs]({% link docs/extensions/httpfs/overview.md %})             |     |     | yes |     |     |     |
| [icu]({% link docs/extensions/icu.md %})                   | yes | yes | yes |     | yes | yes |
| [json]({% link docs/extensions/json.md %})                 | yes | yes | yes |     | yes | yes |
| [parquet]({% link docs/data/parquet/overview.md %})           | yes | yes | yes | yes | yes | yes |
| [tpcds]({% link docs/extensions/tpcds.md %})               |     |     | yes |     |     |     |
| [tpch]({% link docs/extensions/tpch.md %})                 | yes |     | yes |     |     |     |

The [jemalloc]({% link docs/extensions/jemalloc.md %}) extension's availability is based on the operating system.
Starting with version 0.10.1, `jemalloc` is a built-in extension on Linux x86_64 (AMD64) distributions, while it will be optionally available on Linux ARM64 distributions and on macOS (via compiling from source).
On Windows, it is not available.
