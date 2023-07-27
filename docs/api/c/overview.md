---
layout: docu
title: C API - Overview
selected: Overview
expanded: C
---

DuckDB implements a custom C API modelled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown](connect) to get started, or check out the [Full API overview](api).

We also provide a SQLite API wrapper which means that if your applications is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`sqlite_api_wrapper`](https://github.com/duckdb/duckdb/tree/master/tools/sqlite3_api_wrapper) folder in our source repository for more information.

## Installation
The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page](../../installation?environment=cplusplus) for details.

### Pages in this Section
