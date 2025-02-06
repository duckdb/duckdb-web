---
layout: docu
redirect_from:
- /docs/archive/1.1/api/c
- /docs/archive/1.1/api/c/
title: Overview
---

DuckDB implements a custom C API modelled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown]({% link docs/archive/1.1/api/c/connect.md %}) to get started, or check out the [Full API overview]({% link docs/archive/1.1/api/c/api.md %}).

We also provide a SQLite API wrapper which means that if your applications is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`sqlite_api_wrapper`](https://github.com/duckdb/duckdb/tree/main/tools/sqlite3_api_wrapper) folder in our source repository for more information.

## Installation

The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page](../../installation?environment=cplusplus) for details.