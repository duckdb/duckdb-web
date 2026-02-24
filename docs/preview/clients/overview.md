---
layout: docu
title: Client Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.

| Client API                                                                      | Maintainer                                      | Support tier | Version                                                                                                                                                                           |
| ------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/preview/clients/c/overview.md %})                              | Core team                                       | Primary      | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |
| [Command Line Interface (CLI)]({% link docs/preview/clients/cli/overview.md %}) | Core team                                       | Primary      | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cli)                                                                                 |
| [Java (JDBC)]({% link docs/preview/clients/java.md %})                          | Core team                                       | Primary      | [{{ site.current_duckdb_java_short_version }}]({% link install/index.html %}?version=stable&environment=java)                                                                     |
| [Go]({% link docs/preview/clients/go.md %})                                     | Core team                                       | Primary      | [{{ site.current_duckdb_go_version }}]({% link install/index.html %}?version=stable&environment=go)                                                                               |
| [Node.js (node-neo)]({% link docs/preview/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) | Primary      | [{{ site.current_duckdb_node_neo_version }}]({% link install/index.html %}?version=stable&environment=nodejs)                                                                     |
| [ODBC]({% link docs/preview/clients/odbc/overview.md %})                        | Core team                                       | Primary      | [{{ site.current_duckdb_odbc_short_version }}]({% link install/index.html %}?version=stable&environment=odbc)                                                                     |
| [Python]({% link docs/preview/clients/python/overview.md %})                    | Core team                                       | Primary      | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=python)                                                                              |
| [R]({% link docs/preview/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr)      | Primary      | [{{ site.current_duckdb_r_version }}]({% link install/index.html %}?version=stable&environment=r)                                                                                 |
| [Rust]({% link docs/preview/clients/rust.md %})                                 | Core team                                       | Primary      | [{{ site.current_duckdb_rust_version }}]({% link install/index.html %}?version=stable&environment=rust)                                                                           |
| [WebAssembly (Wasm)]({% link docs/preview/clients/wasm/overview.md %})          | Core team                                       | Primary      | [{{ site.current_duckdb_wasm_version }}](https://github.com/duckdb/duckdb-wasm#readme)                                                                                            |
| [ADBC (Arrow)]({% link docs/preview/clients/adbc.md %})                         | Core team                                       | Secondary    | [{{ site.current_duckdb_version }}]({% link docs/preview/clients/adbc.md %})                                                                                                      |
| [C# (.NET)](https://duckdb.net/)                                                | [Giorgi](https://github.com/Giorgi)             | Secondary    | [{{ site.current_duckdb_csharp_version}}](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/preview/clients/cpp.md %})                                   | Core team                                       | Secondary    | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |

For a list of tertiary clients, see the [“Tertiary Clients” page]({% link docs/preview/clients/tertiary.md %}).

## Support Tiers

There are three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/community_support_policy).
Secondary clients receive new features but are not covered by community support.
Finally, there are no feature or support guarantees for tertiary clients.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available under the MIT license.
> For tertiary clients, please consult the repository for the license.

We report the latest stable version for the clients in the primary and secondary support tiers.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/preview/internals/storage.md %}).
[DuckDB extensions]({% link docs/preview/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/preview/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
