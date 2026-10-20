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
> The latest stable version of the DuckDB C API is {{ site.current_duckdb_version }}.

DuckDB implements a custom C API modeled somewhat following the SQLite C API. The API is contained in the `duckdb.h` header. Continue to [Startup & Shutdown]({% link docs/2.0/clients/c/connect.md %}) to get started, or check out the [Full API overview]({% link docs/2.0/clients/c/api.md %}).

We also provide a SQLite API wrapper which means that if your application is programmed against the SQLite C API, you can re-link to DuckDB and it should continue working. See the [`shell_helpers.cpp`](https://github.com/duckdb/duckdb/tree/main/tools/shell/shell_helpers.cpp) file in our source repository for more information.

## Stable C API and C++ API

> New DuckDB 2.0 introduces a reworked C API with a stable, versioned ABI, together with a C++ API layered on top of it.

The C API now has a stable, versioned ABI: an extension built against a given DuckDB version keeps working with later releases without recompilation. DuckDB 2.0 also adds a C++ API layered on top of the C API for extension development.

If you maintain an extension built against the previous, unstable C++ API, you must rebuild it for DuckDB 2.0. For details, see the [migration guide]({% link docs/2.0/operations_manual/migration.md %}#c-and-c-extension-api) and [Versioning of Extensions]({% link docs/2.0/extensions/versioning_of_extensions.md %}).

## Installation

The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link install/index.html %}?environment=c) for details.
