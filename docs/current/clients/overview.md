---
layout: docu
title: Client Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.

| Client API                                                                      | Maintainer                                      | Support tier | Version                                                                                                                                                                       |
| ------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/current/clients/c/overview.md %})                              | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |
| [Command Line Interface (CLI)]({% link docs/current/clients/cli/overview.md %}) | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cli)                                                                                 |
| [Java (JDBC)]({% link docs/current/clients/java.md %})                          | Core team                                       | Primary      | [{{ site.lts_duckdb_java_short_version }}]({% link install/index.html %}?version=stable&environment=java)                                                                     |
| [Go]({% link docs/current/clients/go.md %})                                     | Core team                                       | Primary      | [{{ site.lts_duckdb_go_version }}]({% link install/index.html %}?version=stable&environment=go)                                                                               |
| [Node.js (node-neo)]({% link docs/current/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) | Primary      | [{{ site.lts_duckdb_node_neo_version }}]({% link install/index.html %}?version=stable&environment=nodejs)                                                                     |
| [ODBC]({% link docs/current/clients/odbc/overview.md %})                        | Core team                                       | Primary      | [{{ site.lts_duckdb_odbc_short_version }}]({% link install/index.html %}?version=stable&environment=odbc)                                                                     |
| [Python]({% link docs/current/clients/python/overview.md %})                    | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=python)                                                                              |
| [R]({% link docs/current/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr)      | Primary      | [{{ site.lts_duckdb_r_version }}]({% link install/index.html %}?version=stable&environment=r)                                                                                 |
| [Rust]({% link docs/current/clients/rust.md %})                                 | Core team                                       | Primary      | [{{ site.lts_duckdb_rust_version }}]({% link install/index.html %}?version=stable&environment=rust)                                                                           |
| [WebAssembly (Wasm)]({% link docs/current/clients/wasm/overview.md %})          | Core team                                       | Primary      | [{{ site.lts_duckdb_wasm_version }}](https://github.com/duckdb/duckdb-wasm#readme)                                                                                            |
| [ADBC (Arrow)]({% link docs/current/clients/adbc.md %})                         | Core team                                       | Secondary    | [{{ site.lts_duckdb_version }}]({% link docs/current/clients/adbc.md %})                                                                                                      |
| [C# (.NET)](https://duckdb.net/)                                                | [Giorgi](https://github.com/Giorgi)             | Secondary    | [{{ site.lts_duckdb_csharp_version}}](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/current/clients/cpp.md %})                                   | Core team                                       | Secondary    | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |

The table above lists the DuckDB clients with the primary and secondary [support tiers](#support-tiers).
For a list of tertiary clients, see the [“Tertiary Clients” page]({% link docs/current/clients/tertiary_clients/overview.md %}).

## Support Tiers

There are three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/community_support_policy).
Secondary clients receive new features but are not covered by community support.
Finally, there are no feature or support guarantees for tertiary clients.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available under the MIT license.
> For tertiary clients, please consult the repository for the license.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/current/internals/storage.md %}).
[DuckDB extensions]({% link docs/current/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/current/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
