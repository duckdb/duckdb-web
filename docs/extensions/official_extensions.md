---
layout: docu
title: Official Extensions
---

## List of Official Extensions

| Extension name                                                                                        | Description                                                                        | Auto-loadable | Aliases                 |
|:------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:--------------|:------------------------|
| [arrow](arrow) [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)                  | A zero-copy data integration between Apache Arrow and DuckDB                       | no            |                         |
| [autocomplete](autocomplete)                                                                          | Adds support for autocomplete in the shell                                         | yes           |                         |
| [aws](aws) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_aws)                 | Provides features that depend on the AWS SDK                                       | yes           |                         | 
| [azure](azure) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_azure)           | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes           |                         | 
| delta [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_delta)                    | Adds support for Delta Lake                                                        |               |                         |
| [excel](excel)                                                                                        | Adds support for Excel-like format strings                                         | yes           |                         |
| [fts](full_text_search)                                                                               | Adds support for Full-Text Search Indexes                                          | yes           |                         |
| [httpfs](httpfs)                                                                                      | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes           | http, https, s3         |
| [iceberg](iceberg) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_iceberg)     | Adds support for Apache Iceberg                                                    | no            |                         |
| [icu](icu)                                                                                            | Adds support for time zones and collations using the ICU library                   | yes           |                         |
| [inet](inet)                                                                                          | Adds support for IP-related data types and functions                               | yes           |                         |
| [jemalloc](jemalloc)                                                                                  | Overwrites system allocator with jemalloc                                          | no            |                         |
| [json](json)                                                                                          | Adds support for JSON operations                                                   | yes           |                         |
| [mysql](mysql) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_mysql)           | Adds support for reading from and writing to a MySQL database                      | no            |                         |
| [parquet](parquet)                                                                                    | Adds support for reading and writing Parquet files                                 | (built-in)    |                         |
| [postgres](postgres) [<span class="github">GitHub</span>](https://github.com/duckdb/postgres_scanner) | Adds support for reading from and writing to a Postgres database                   | yes           | postgres_scanner        |
| [spatial](spatial) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_spatial)     | Geospatial extension that adds support for working with spatial data and functions | no            |                         |
| [sqlite](sqlite) [<span class="github">GitHub</span>](https://github.com/duckdb/sqlite_scanner)       | Adds support for reading from and writing to SQLite database files                 | yes           | sqlite_scanner, sqlite3 |
| [substrait](substrait) [<span class="github">GitHub</span>](https://github.com/duckdb/substrait)      | Adds support for the Substrait integration                                         | no            |                         |
| [tpcds](tpcds)                                                                                        | Adds TPC-DS data generation and query support                                      | yes           |                         |
| [tpch](tpch)                                                                                          | Adds TPC-H data generation and query support                                       | yes           |                         |
| [vss](vss) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_vss)                 | Adds support for vector similarity search queries                                  | no            |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

<div class="narrow_table"></div>

| Extension name | CLI (duckdb.org) | CLI (Homebrew) | Python | R | Java | Node.js |
|------|------|------|---|---|---|---|---|
| [autocomplete](autocomplete) | yes | yes |     |     |     |     |
| [excel](excel)               | yes |     |     |     |     |     |
| [fts](full_text_search)      | yes |     | yes |     |     |     |
| [httpfs](httpfs)             |     |     | yes |     |     |     |
| [icu](icu)                   | yes | yes | yes |     | yes | yes |
| [json](json)                 | yes | yes | yes |     | yes | yes |
| [parquet](parquet)           | yes | yes | yes | yes | yes | yes |
| [tpcds](tpcds)               |     |     | yes |     |     |     |
| [tpch](tpch)                 | yes |     | yes |     |     |     |

The [jemalloc](jemalloc) extension's availability is based on the operating system.
Starting with version 0.10.1, `jemalloc` is a built-in extension on Linux x86_64 (AMD64) distributions, while it will be optionally available on Linux ARM64 distributions and on macOS (via compiling from source).
On Windows, it is not available.
