---
layout: docu
title: Data Import Overview
---

When importing data from other systems to DuckDB, there are several considerations to take into account.
This page documents the key approaches recommended to bulk import data to DuckDB.

## Recommended Import Methods

1. For systems which are supported by a DuckDB scanner extension, it's preferable to use the scanner. DuckDB currently offers scanners for [MySQL](query_mysql), [PostgreSQL](query_postgres), and [SQLite](query_sqlite).
2. If there is a bulk export feature in the data source system, export the data to Parquet or CSV format, then load it using DuckDB's [Parquet](parquet_import) or [CSV loader](csv_import).
3. If the approaches above are not applicable, consider using the DuckDB [appender](../../data/appender), currently available in the C, C++, Go, Java, and Rust APIs.
4. If the data source system supports Apache Arrow and the data transfer is a recurring task, consider using the DuckDB [Arrow](../../extensions/arrow) extension.

## Methods to Avoid

If possible, avoid looping row-by-row (tuple-at-a-time) in favor of bulk operations.
Performing row-by-row inserts (even with prepared statements) is detrimental to performance and will result in slow load times.

> Bestpractice Unless your data is small (<100k rows), avoid using looping for inserts.

