---
layout: docu
title: Overview
---

> Tip To use the DuckDB C API, download the [`libduckdb` archive]({% link install/index.html %}?environment=c) for your platform.
>
> The latest stable version of the DuckDB C API is {{ site.current_duckdb_version }}.

DuckDB implements a custom C API modeled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown]({% link docs/preview/clients/c/connect.md %}) to get started, or check out the [Full API overview]({% link docs/preview/clients/c/api.md %}).

We also provide a SQLite API wrapper which means that if your application is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`sqlite_api_wrapper`](https://github.com/duckdb/duckdb/tree/main/tools/sqlite3_api_wrapper) folder in our source repository for more information.

## Installation

The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link install/index.html %}?environment=cplusplus) for details.
