---
layout: docu
redirect_from:
- /docs/guides/import/overview
- /docs/guides/performance/import
- /docs/stable/guides/performance/import
- /docs/current/guides/performance/import
- /docs/lts/guides/performance/import
- /docs/preview/guides/performance/import
title: Data Import
how_to_topic: performance
---

## Recommended Import Methods

When importing data from other systems to DuckDB, there are several considerations to take into account.
We recommend importing using the following order:

1. For systems which are supported by a DuckDB scanner extension, it's preferable to use the scanner. DuckDB currently offers scanners for [MySQL]({% link docs/2.0/guides/database_integration/mysql.md %}), [PostgreSQL]({% link docs/2.0/guides/database_integration/postgres.md %}) and [SQLite]({% link docs/2.0/guides/database_integration/sqlite.md %}), as well as a generic [ODBC scanner]({% link docs/2.0/core_extensions/odbc/overview.md %}).
2. If there is a bulk export feature in the data source system, export the data to Parquet or CSV format, then load it using DuckDB's [Parquet]({% link docs/2.0/guides/file_formats/parquet_import.md %}) or [CSV loader]({% link docs/2.0/guides/file_formats/csv_import.md %}).
3. If the approaches above are not applicable, consider using the DuckDB [appender]({% link docs/2.0/data/appender.md %}), currently available in the C, C++, Go, Java, Julia, Node.js, Python and Rust APIs.

## Methods to Avoid

If possible, avoid looping row-by-row (tuple-at-a-time) in favor of bulk operations.
Performing row-by-row inserts (even with prepared statements) is detrimental to performance and will result in slow load times.

> Bestpractice Unless your data is small (<100k rows), avoid using inserts in loops.
