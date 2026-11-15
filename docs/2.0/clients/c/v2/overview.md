---
layout: docu
redirect_from:
- /docs/stable/clients/c/v2/overview
- /docs/current/clients/c/v2/overview
- /docs/lts/clients/c/v2/overview
- /docs/preview/clients/c/v2/overview
title: C API v2
---

> Warning The C API v2 is not yet stable. Its interface may change in upcoming releases.

DuckDB 2.0 ships a revamped C API, which is considerably more powerful than its predecessor. Among others, it exposes components such as file systems and table functions to extensions.

The C API v2 is declared in the `duckdb_v2.h` header. Extensions that target it include `duckdb_extension_v2.h` instead of `duckdb_extension.h`; an extension targets either the v1 or the v2 C API, never both. Every v2 function is behind the `DUCKDB_V2_API_ALLOW_UNSTABLE` switch: define it to 1 before including the header, or define the older `DUCKDB_EXTENSION_API_VERSION_UNSTABLE`, from which it defaults. An extension built with `duckdb_extension_v2.h` opts in through the `build_loadable_extension_capi_unstable` and `build_static_extension_capi_unstable` build macros instead.

Before marking the C API v2 as stable, we would like to test it in the field. Please give it a try and [send us your feedback](https://github.com/duckdb/duckdb/discussions/27525)!

## Reading the Reference

The [complete reference]({% link docs/2.0/clients/c/v2/api.md %}) lists every type and function of the API, grouped by module. Each module section opens with its types, then a quick reference of its function prototypes, then one entry per function.

Results come back through output parameters and an error slot, so the parameter list of each function tags every parameter that is not a plain input:

* No tag: an input. The callee reads it and keeps nothing.
* `(out)`: the callee writes it. When it is a handle, the caller owns what comes back and destroys it with the function the handle's description names; a plain value needs no cleanup.
* `(out, borrowed)`: the callee writes it, but the caller does not own it. It stays valid as long as the function says, usually while the owning handle lives.
* `(ownership passes to the callee)`: the caller hands the object over and must not use or destroy it afterwards.
