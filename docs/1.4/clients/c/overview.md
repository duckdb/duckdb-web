---
layout: docu
title: Overview
---

> The latest stable version of the DuckDB C API is {{ site.maintained_duckdb_version }}.

DuckDB implements a custom C API modeled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown]({% link docs/1.4/clients/c/connect.md %}) to get started, or check out the [Full API overview]({% link docs/1.4/clients/c/api.md %}).

We also provide a SQLite API wrapper which means that if your application is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`shell_helpers.cpp`](https://github.com/duckdb/duckdb/tree/main/tools/shell/shell_helpers.cpp) file in our source repository for more information.

## Installation

The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link docs/2.0/installation.html %}?environment=c) for details.
