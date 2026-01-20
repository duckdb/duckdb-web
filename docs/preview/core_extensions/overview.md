---
layout: docu
title: Core Extensions
---

## List of Core Extensions

| Name                                                                     | Description                                                             | Maintainer  | Support&nbsp;tier | Aliases                 |
| :----------------------------------------------------------------------- | :---------------------------------------------------------------------- | ----------- | :---------------- | :---------------------- |
| [autocomplete]({% link docs/preview/core_extensions/autocomplete.md %})   | Adds support for autocomplete in the shell                              | DuckDB team | Secondary         |                         |
| [avro]({% link docs/preview/core_extensions/avro.md %})                   | Add support for reading Avro files                                      | DuckDB team | Secondary         |                         |
| [aws]({% link docs/preview/core_extensions/aws.md %})                     | Provides features that depend on the AWS SDK                            | DuckDB team | Secondary         |                         |
| [azure]({% link docs/preview/core_extensions/azure.md %})                 | Adds a filesystem abstraction for Azure blob storage to DuckDB          | DuckDB team | Secondary         |                         |
| [delta]({% link docs/preview/core_extensions/delta.md %})                 | Adds support for Delta Lake                                             | DuckDB team | Secondary         |                         |
| [ducklake]({% link docs/preview/core_extensions/ducklake.md %})           | Adds support for DuckLake                                               | DuckDB team | Secondary         |                         |
| [encodings]({% link docs/preview/core_extensions/encodings.md %})         | Adds support for encodings available in the ICU data repository         | DuckDB team | Secondary         |                         |
| [excel]({% link docs/preview/core_extensions/excel.md %})                 | Adds support for reading and writing Excel files                        | DuckDB team | Secondary         |                         |
| [fts]({% link docs/preview/core_extensions/full_text_search.md %})        | Adds support for full-text search indexes                               | DuckDB team | Secondary         |                         |
| [httpfs]({% link docs/preview/core_extensions/httpfs/overview.md %})      | Adds support for reading/writing files over an HTTP(S) or S3 connection | DuckDB team | Primary           | http, https, s3         |
| [iceberg]({% link docs/preview/core_extensions/iceberg/overview.md %})    | Adds support for Apache Iceberg                                         | DuckDB team | Secondary         |                         |
| [icu]({% link docs/preview/core_extensions/icu.md %})                     | Adds support for time zones and collations using the ICU library        | DuckDB team | Primary           |                         |
| [inet]({% link docs/preview/core_extensions/inet.md %})                   | Adds support for IP-related data types and functions                    | DuckDB team | Secondary         |                         |
| [jemalloc]({% link docs/preview/core_extensions/jemalloc.md %})           | Overwrites the system allocator with jemalloc                           | DuckDB team | Secondary         |                         |
| [json]({% link docs/preview/data/json/overview.md %})                     | Adds support for JSON operations                                        | DuckDB team | Primary           |                         |
| [motherduck]({% link docs/preview/core_extensions/motherduck.md %})       | Allows connecting to MotherDuck                                         | Third party |                   | md                      |
| [mysql]({% link docs/preview/core_extensions/mysql.md %})                 | Adds support for reading from and writing to a MySQL database           | DuckDB team | Secondary         | mysql_scanner           |
| [parquet]({% link docs/preview/data/parquet/overview.md %})               | Adds support for reading and writing Parquet files                      | DuckDB team | Primary           |                         |
| [postgres]({% link docs/preview/core_extensions/postgres.md %})           | Adds support for reading from and writing to a PostgreSQL database      | DuckDB team | Secondary         | postgres_scanner        |
| [spatial]({% link docs/preview/core_extensions/spatial/overview.md %})    | Adds support for working with geospatial data and functions             | DuckDB team | Secondary         |                         |
| [sqlite]({% link docs/preview/core_extensions/sqlite.md %})               | Adds support for reading from and writing to SQLite database files      | DuckDB team | Secondary         | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/preview/core_extensions/tpcds.md %})                 | Adds TPC-DS data generation and query support                           | DuckDB team | Secondary         |                         |
| [tpch]({% link docs/preview/core_extensions/tpch.md %})                   | Adds TPC-H data generation and query support                            | DuckDB team | Secondary         |                         |
| [unity_catalog]({% link docs/preview/core_extensions/unity_catalog.md %}) | Adds support for connecting to Unity Catalog                            | DuckDB team | Secondary         | uc_catalog              |
| [ui]({% link docs/preview/core_extensions/ui.md %})                       | Adds local UI for DuckDB                                                | Third party |                   |                         |
| [vortex]({% link docs/preview/core_extensions/vortex.md %})               | Adds support for reading and writing Vortex files                       | Third party |                   |                         |
| [vss]({% link docs/preview/core_extensions/vss.md %})                     | Adds support for vector similarity search queries                       | DuckDB team | Secondary         |                         |

The **Maintainer** column denotes whether the extension is maintained by the DuckDB team or by a third party.
For the extensions maintained by the DuckDB team, the **Support tier** column denotes whether the extension's support status.
_Primary extension_ are covered by [community support](https://duckdblabs.com/community_support_policy/).
_Secondary extensions_ are supported on a best-effort basis. That said, they still receive frequent bugfixes/updates and are shipped with new DuckDB releases.
