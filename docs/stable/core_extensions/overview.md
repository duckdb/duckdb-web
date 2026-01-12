---
layout: docu
redirect_from:
  - /docs/extensions/official_extensions
  - /docs/extensions/official_extensions/
title: Core Extensions
---

## List of Core Extensions

| Name                                                                   | Description                                                             | Maintainer  | Status       | Aliases                 |
| :--------------------------------------------------------------------- | :---------------------------------------------------------------------- | ----------- | :----------- | :---------------------- |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) | Adds support for autocomplete in the shell                              | Core team   | stable       |                         |
| [avro]({% link docs/stable/core_extensions/avro.md %})                 | Add support for reading Avro files                                      | Core team   | stable       |                         |
| [aws]({% link docs/stable/core_extensions/aws.md %})                   | Provides features that depend on the AWS SDK                            | Core team   | stable       |                         |
| [azure]({% link docs/stable/core_extensions/azure.md %})               | Adds a filesystem abstraction for Azure blob storage to DuckDB          | Core team   | stable       |                         |
| [delta]({% link docs/stable/core_extensions/delta.md %})               | Adds support for Delta Lake                                             | Core team   | experimental |                         |
| [ducklake]({% link docs/stable/core_extensions/ducklake.md %})         | Adds support for DuckLake                                               | Core team   | experimental |                         |
| [encodings]({% link docs/stable/core_extensions/encodings.md %})       | Adds support for encodings available in the ICU data repository         | Core team   | experimental |                         |
| [excel]({% link docs/stable/core_extensions/excel.md %})               | Adds support for reading and writing Excel files                        | Core team   | experimental |                         |
| [fts]({% link docs/stable/core_extensions/full_text_search.md %})      | Adds support for full-text search indexes                               | Core team   | experimental |                         |
| [httpfs]({% link docs/stable/core_extensions/httpfs/overview.md %})    | Adds support for reading/writing files over an HTTP(S) or S3 connection | Core team   | stable       | http, https, s3         |
| [iceberg]({% link docs/stable/core_extensions/iceberg/overview.md %})  | Adds support for Apache Iceberg                                         | Core team   | experimental |                         |
| [icu]({% link docs/stable/core_extensions/icu.md %})                   | Adds support for time zones and collations using the ICU library        | Core team   | stable       |                         |
| [inet]({% link docs/stable/core_extensions/inet.md %})                 | Adds support for IP-related data types and functions                    | Core team   | experimental |                         |
| [jemalloc]({% link docs/stable/core_extensions/jemalloc.md %})         | Overwrites the system allocator with jemalloc                           | Core team   | stable       |                         |
| [json]({% link docs/stable/data/json/overview.md %})                   | Adds support for JSON operations                                        | Core team   | stable       |                         |
| [motherduck]({% link docs/stable/core_extensions/motherduck.md %})     | Allows connecting to MotherDuck.                                        | Third-party | stable       | md                      |
| [mysql]({% link docs/stable/core_extensions/mysql.md %})               | Adds support for reading from and writing to a MySQL database           | Core team   | stable       | mysql_scanner           |
| [parquet]({% link docs/stable/data/parquet/overview.md %})             | Adds support for reading and writing Parquet files                      | Core team   | stable       |                         |
| [postgres]({% link docs/stable/core_extensions/postgres.md %})         | Adds support for reading from and writing to a PostgreSQL database      | Core team   | stable       | postgres_scanner        |
| [spatial]({% link docs/stable/core_extensions/spatial/overview.md %})  | Adds support for working with geospatial data and functions             | Core team   | experimental |                         |
| [sqlite]({% link docs/stable/core_extensions/sqlite.md %})             | Adds support for reading from and writing to SQLite database files      | Core team   | stable       | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/stable/core_extensions/tpcds.md %})               | Adds TPC-DS data generation and query support                           | Core team   | experimental |                         |
| [tpch]({% link docs/stable/core_extensions/tpch.md %})                 | Adds TPC-H data generation and query support                            | Core team   | stable       |                         |
| [ui]({% link docs/stable/core_extensions/ui.md %})                     | Adds local UI for DuckDB                                                | Third-party |              |                         |
| [vortex]({% link docs/stable/core_extensions/vortex.md %})             | Adds support for reading and writing Vortex files                       | Third-party |              |                         |
| [vss]({% link docs/stable/core_extensions/vss.md %})                   | Adds support for vector similarity search queries                       | Core team   | experimental |                         |

For the extensions maintained by the core DuckDB team, the **Status** column shows the lifecycle stage (`experimental`, `stable`, `deprecated`, `superseded`) following the convention of the [lifecycle stages used in tidyverse](https://lifecycle.r-lib.org/articles/stages.html).

## Default Extensions

Different DuckDB clients ship a different set of extensions.
We summarize the main distributions in the table below.

| Name                                                                   | CLI | Python | R   | Java | Node.js |
| ---------------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/stable/core_extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/stable/data/json/overview.md %})                   | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/stable/data/parquet/overview.md %})             | yes | yes    | yes | yes  | yes     |

The jemalloc extension's availability is based on the operating system.
Please check the [jemalloc page]({% link docs/stable/core_extensions/jemalloc.md %}) for details.
