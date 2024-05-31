---
layout: docu
title: Data Import
redirect_from:
  - /docs/guides/import/overview
---

## Recommended Import Methods

When importing data from other systems to DuckDB, there are several considerations to take into account.
We recommend importing using the following order:

1. For systems which are supported by a DuckDB scanner extension, it's preferable to use the scanner. DuckDB currently offers scanners for [MySQL](../database_integration/mysql), [PostgreSQL](../database_integration/postgres), and [SQLite](../database_integration/sqlite).
2. If there is a bulk export feature in the data source system, export the data to Parquet or CSV format, then load it using DuckDB's [Parquet](../file_formats/parquet_import) or [CSV loader](../file_formats/csv_import).
3. If the approaches above are not applicable, consider using the DuckDB [appender](../../data/appender), currently available in the C, C++, Go, Java, and Rust APIs.
4. If the data source system supports Apache Arrow and the data transfer is a recurring task, consider using the DuckDB [Arrow](../../extensions/arrow) extension.

## Methods to Avoid

If possible, avoid looping row-by-row (tuple-at-a-time) in favor of bulk operations.
Performing row-by-row inserts (even with prepared statements) is detrimental to performance and will result in slow load times.

> Bestpractice Unless your data is small (<100k rows), avoid using inserts in loops.
