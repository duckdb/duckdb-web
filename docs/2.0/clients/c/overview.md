---
layout: docu
redirect_from:
- /docs/api/c
- /docs/api/c/overview
- /docs/clients/c/overview
- /docs/stable/clients/c/overview
- /docs/current/clients/c/overview
- /docs/lts/clients/c/overview
- /docs/preview/clients/c/overview
title: Overview
---

> Installation To use the DuckDB C API, download the [`libduckdb` archive]({% link install/index.html %}?environment=c) for your platform.
>
> The latest stable version of the DuckDB C API is {{ site.next_major_duckdb_version }}.

DuckDB implements a custom C API modeled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown]({% link docs/2.0/clients/c/connect.md %}) to get started, or check out the [Full API overview]({% link docs/2.0/clients/c/api.md %}).

We also provide a SQLite API wrapper which means that if your application is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`shell_helpers.cpp`](https://github.com/duckdb/duckdb/tree/main/tools/shell/shell_helpers.cpp) file in our source repository for more information.

## C API v2

> Warning The C API v2 is not yet stable. Its interface may change in upcoming releases.

DuckDB 2.0 ships a revamped C API, which is considerably more powerful than its predecessor. Among others, it exposes components such as file systems and table functions to extensions.

Before marking the C API v2 as stable, we would like to test it in the field. Please give it a try and [send us your feedback](https://github.com/duckdb/duckdb/discussions/27525)!

## Installation

The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link install/index.html %}?environment=c) for details.
