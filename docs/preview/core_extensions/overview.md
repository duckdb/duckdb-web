---
layout: docu
title: Core Extensions
---

## List of Core Extensions

<div class="sticky_header_table"></div>

| Name                                                                      | Description                                     | Maintainer       | Support&nbsp;tier                                                                  | Aliases                 |
| :------------------------------------------------------------------------ | :---------------------------------------------- | ---------------- | :--------------------------------------------------------------------------------- | :---------------------- |
| [autocomplete]({% link docs/preview/core_extensions/autocomplete.md %})   | Autocompletion for CLI client                   | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [avro]({% link docs/preview/core_extensions/avro.md %})                   | Avro files reading                              | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [aws]({% link docs/preview/core_extensions/aws.md %})                     | AWS S3 functionality                            | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [azure]({% link docs/preview/core_extensions/azure.md %})                 | Filesystem abstraction for Azure Blob Storage   | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [delta]({% link docs/preview/core_extensions/delta.md %})                 | Delta Lake format                               | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [ducklake]({% link docs/preview/core_extensions/ducklake.md %})           | DuckLake format                                 | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [encodings]({% link docs/preview/core_extensions/encodings.md %})         | Read CSVs in 1000+ encodings                    | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [excel]({% link docs/preview/core_extensions/excel.md %})                 | Excel (`.xlsx`) read/write                      | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [fts]({% link docs/preview/core_extensions/full_text_search.md %})        | Full-text search                                | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [httpfs]({% link docs/preview/core_extensions/httpfs/overview.md %})      | HTTP(S) and S3 - file read/write operations     | DuckDB&nbsp;team | {% include tooltip.html label="Primary" id="support_tier_primary_extension" %}     | http, https, s3         |
| [iceberg]({% link docs/preview/core_extensions/iceberg/overview.md %})    | Apache Iceberg table format                     | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [icu]({% link docs/preview/core_extensions/icu.md %})                     | Time zones and collations using the ICU library | DuckDB&nbsp;team | {% include tooltip.html label="Primary" id="support_tier_primary_extension" %}     |                         |
| [inet]({% link docs/preview/core_extensions/inet.md %})                   | IP-related data types and functions             | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [json]({% link docs/preview/data/json/overview.md %})                     | JSON operations                                 | DuckDB&nbsp;team | {% include tooltip.html label="Primary" id="support_tier_primary_extension" %}     |                         |
| [lance]({% link docs/preview/core_extensions/lance.md %})                 | Lance tables read/write                         | Third party      |                                                                                    |                         |
| [motherduck]({% link docs/preview/core_extensions/motherduck.md %})       | MotherDuck connectivity                         | Third party      |                                                                                    | md                      |
| [mysql]({% link docs/preview/core_extensions/mysql.md %})                 | MySQL database read/write operations            | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} | mysql_scanner           |
| [odbc]({% link docs/preview/core_extensions/odbc/overview.md %})          | ODBC connectivity                               | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} | odbc_scanner            |
| [parquet]({% link docs/preview/data/parquet/overview.md %})               | Parquet files read/write                        | DuckDB&nbsp;team | {% include tooltip.html label="Primary" id="support_tier_primary_extension" %}     |                         |
| [postgres]({% link docs/preview/core_extensions/postgres/overview.md %})  | PostgreSQL database read/write operations       | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} | postgres_scanner        |
| [quack]({% link docs/preview/core_extensions/quack.md %})                 | DuckDB-Quack protocol for remote access         | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [spatial]({% link docs/preview/core_extensions/spatial/overview.md %})    | Geospatial data and functions                   | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [sqlite]({% link docs/preview/core_extensions/sqlite.md %})               | SQLite database read/write operations           | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/preview/core_extensions/tpcds.md %})                 | TPC-DS data generation and query                | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [tpch]({% link docs/preview/core_extensions/tpch.md %})                   | TPC-H data generation and query                 | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |
| [unity_catalog]({% link docs/preview/core_extensions/unity_catalog.md %}) | Unity Catalog connectivity                      | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} | uc_catalog              |
| [ui]({% link docs/preview/core_extensions/ui.md %})                       | Local UI for DuckDB                             | Third party      |                                                                                    |                         |
| [vortex]({% link docs/preview/core_extensions/vortex.md %})               | Vortex files read/write                         | Third party      |                                                                                    |                         |
| [vss]({% link docs/preview/core_extensions/vss.md %})                     | Vector similarity search queries                | DuckDB&nbsp;team | {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} |                         |

The **Maintainer** column denotes whether the extension is maintained by the DuckDB team or by a third party.
For the extensions maintained by the DuckDB team, the **Support tier** column denotes the extension's support status.
_Primary extensions_ are covered by [community support](https://ducklabs.com/community_support_policy/).
_Secondary extensions_ are supported on a best-effort basis. That said, they still receive frequent bugfixes/updates and are shipped with new DuckDB releases.
