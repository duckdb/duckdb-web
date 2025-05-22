---
layout: docu
redirect_from:
- /docs/1.2/extensions/official_extensions
- /docs/1.2/extensions/official_extensions/
- /docs/1.2/extensions/core_extensions
title: Core Extensions
---

## List of Core Extensions

| Name                                                              | GitHub                                                                          | Description                                                                        | Autoloadable | Aliases                 |
| :---------------------------------------------------------------- | ------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [arrow]({% link docs/1.2/extensions/arrow.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/arrow)           | A zero-copy data integration between Apache Arrow and DuckDB                       | no           |                         |
| [autocomplete]({% link docs/1.2/extensions/autocomplete.md %}) |                                                                                 | Adds support for autocomplete in the shell                                         | yes          |                         |
| [avro]({% link docs/1.2/extensions/avro.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-avro)     | Add support for reading Avro files                                                 | yes          |                         |
| [aws]({% link docs/1.2/extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)      | Provides features that depend on the AWS SDK                                       | yes          |                         |
| [azure]({% link docs/1.2/extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)    | Adds a filesystem abstraction for Azure blob storage to DuckDB                     | yes          |                         |
| [delta]({% link docs/1.2/extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)    | Adds support for Delta Lake                                                        | yes          |                         |
| [excel]({% link docs/1.2/extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)    | Adds support for reading and writing Excel files                                   | yes          |                         |
| [fts]({% link docs/1.2/extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)      | Adds support for full-text search indexes                                          | yes          |                         |
| [httpfs]({% link docs/1.2/extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)   | Adds support for reading and writing files over an HTTP(S) or S3 connection        | yes          | http, https, s3         |
| [iceberg]({% link docs/1.2/extensions/iceberg/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)  | Adds support for Apache Iceberg                                                    | no           |                         |
| [icu]({% link docs/1.2/extensions/icu.md %})                   |                                                                                 | Adds support for time zones and collations using the ICU library                   | yes          |                         |
| [inet]({% link docs/1.2/extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)     | Adds support for IP-related data types and functions                               | yes          |                         |
| [jemalloc]({% link docs/1.2/extensions/jemalloc.md %})         |                                                                                 | Overwrites system the allocator with jemalloc                                      | no           |                         |
| [json]({% link docs/1.2/data/json/overview.md %})              |                                                                                 | Adds support for JSON operations                                                   | yes          |                         |
| [mysql]({% link docs/1.2/extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)    | Adds support for reading from and writing to a MySQL database                      | no           | mysql_scanner           |
| [parquet]({% link docs/1.2/data/parquet/overview.md %})        |                                                                                 | Adds support for reading and writing Parquet files                                 | (built-in)   |                         |
| [postgres]({% link docs/1.2/extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres) | Adds support for reading from and writing to a PostgreSQL database                 | yes          | postgres_scanner        |
| [spatial]({% link docs/1.2/extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)  | Geospatial extension that adds support for working with spatial data and functions | no           |                         |
| [sqlite]({% link docs/1.2/extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)   | Adds support for reading from and writing to SQLite database files                 | yes          | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/1.2/extensions/tpcds.md %})               |                                                                                 | Adds TPC-DS data generation and query support                                      | yes          |                         |
| [tpch]({% link docs/1.2/extensions/tpch.md %})                 |                                                                                 | Adds TPC-H data generation and query support                                       | yes          |                         |
| [ui]({% link docs/1.2/extensions/ui.md %})                     | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-ui)       | Adds local UI for DuckDB                                                           | yes          |                         |
| [vss]({% link docs/1.2/extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)      | Adds support for vector similarity search queries                                  | no           |                         |

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                              | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/1.2/extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/1.2/extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/1.2/data/json/overview.md %})              | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/1.2/data/parquet/overview.md %})        | yes | yes    | yes | yes  | yes     |
| [tpch]({% link docs/1.2/extensions/tpch.md %})                 |     | yes    |     |      |         |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/1.2/extensions/jemalloc.md %}) for details.
