---
layout: docu
title: Official Extensions
---

## List of Official Extensions

| Extension Name | Description | Aliases |
|---|-----|--|
| [arrow](arrow) [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)                                  | A zero-copy data integration between Apache Arrow and DuckDB                       |                 |
| [autocomplete](autocomplete)                                                                                          | Adds support for autocomplete in the shell                                         |                 |
| [aws](aws) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_aws)                                 | Provides features that depend on the AWS SDK                                       |                 |
| [azure](azure) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_azure)                           | Adds a filesystem abstraction for Azure blob storage to DuckDB                     |                 |
| [excel](excel)                                                                                                        | Adds support for Excel-like format strings                                         |                 |
| [fts](full_text_search)                                                                                               | Adds support for Full-Text Search Indexes                                          |                 |
| [httpfs](httpfs)                                                                                                      | Adds support for reading and writing files over a HTTP(S) connection               | http, https, s3 |
| [iceberg](iceberg) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_iceberg)                     | Adds support for Apache Iceberg                                                    |                 |
| [icu](icu)                                                                                                            | Adds support for time zones and collations using the ICU library                   |                 |
| [inet](inet)                                                                                                          | Adds support for IP-related data types and functions                               |                 |
| [jemalloc](jemalloc)                                                                                                  | Overwrites system allocator with jemalloc                                          |                 |
| [json](json)                                                                                                          | Adds support for JSON operations                                                   |                 |
| [mysql](mysql) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_mysql)                           | Adds support for reading from and writing to a MySQL database                      |                 |
| [parquet](parquet)                                                                                                    | Adds support for reading and writing Parquet files                                 |                 |
| [postgres_scanner](postgres_scanner) [<span class="github">GitHub</span>](https://github.com/duckdb/postgres_scanner) | Adds support for reading from a Postgres database                                  | postgres        |
| [spatial](spatial) [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_spatial)                     | Geospatial extension that adds support for working with spatial data and functions |                 |
| [sqlite_scanner](sqlite_scanner) [<span class="github">GitHub</span>](https://github.com/duckdb/sqlite_scanner)       | Adds support for reading SQLite database files                                     | sqlite, sqlite3 |
| [substrait](substrait) [<span class="github">GitHub</span>](https://github.com/duckdb/substrait)                      | Adds support for the Substrait integration                                         |                 |
| [tpcds](tpcds)                                                                                                        | Adds TPC-DS data generation and query support                                      |                 |
| [tpch](tpch)                                                                                                          | Adds TPC-H data generation and query support                                       |                 |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

<div class="narrow_table"></div>

| Extension Name | CLI (duckdb.org) | CLI (Homebrew) | Python | R | Java | Julia | Node.JS
|------|------|------|---|---|---|---|---|
| [autocomplete](autocomplete) | yes | yes |     |     |     |     |     |
| [excel](excel)               | yes |     |     |     |     |     |     |
| [fts](full_text_search)      | yes |     | yes |     |     |     |     |
| [httpfs](httpfs)             |     |     | yes |     |     |     |     |
| [icu](icu)                   | yes | yes | yes |     | yes | yes | yes |
| [json](json)                 | yes | yes | yes |     | yes | yes | yes |
| [parquet](parquet)           | yes | yes | yes | yes | yes | yes | yes |
| [tpcds](tpcds)               |     |     | yes |     |     |     |     |
| [tpch](tpch)                 | yes |     | yes |     |     |     |     |

The [json](json) and [parquet](parquet) extensions are central pieces of
infrastructure and are always built-in.

The [jemalloc](jemalloc) extension's availability is based on the operating system.
It is a built-in extension on Linux and macOS versions, while on Windows, it is not available.
