---
layout: docu
redirect_from:
  - /clients
  - /docs/clients
  - /docs/api/overview
  - /docs/clients/overview
title: Client Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.
Visit the [installation page]({% link install/index.html %}) for instructions on how to install a given DuckDB client.

| Client API                                                                     | Maintainer                                      | Support tier | Version                                                                                                                                                                           |
| ------------------------------------------------------------------------------ | ----------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/stable/clients/c/overview.md %})                              | Core team                                       | Primary      | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cplusplus)                                                                           |
| [Command Line Interface (CLI)]({% link docs/stable/clients/cli/overview.md %}) | Core team                                       | Primary      | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cli)                                                                                 |
| [Java (JDBC)]({% link docs/stable/clients/java.md %})                          | Core team                                       | Primary      | [{{ site.current_duckdb_java_short_version }}](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc)                                                                      |
| [Go]({% link docs/stable/clients/go.md %})                                     | Core team                                       | Primary      | [{{ site.current_duckdb_go_version }}](https://github.com/duckdb/duckdb-go#readme)                                                                                                |
| [Node.js (node-neo)]({% link docs/stable/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) | Primary      | [{{ site.current_duckdb_node_neo_version }}](https://www.npmjs.com/package/@duckdb/node-api)                                                                                      |
| [ODBC]({% link docs/stable/clients/odbc/overview.md %})                        | Core team                                       | Primary      | [{{ site.current_duckdb_odbc_short_version }}]({% link install/index.html %}?version=stable&environment=odbc)                                                                     |
| [Python]({% link docs/stable/clients/python/overview.md %})                    | Core team                                       | Primary      | [{{ site.current_duckdb_version }}](https://pypi.org/project/duckdb/)                                                                                                             |
| [R]({% link docs/stable/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr)      | Primary      | [{{ site.current_duckdb_r_version }}](https://cran.r-project.org/web/packages/duckdb/index.html)                                                                                  |
| [Rust]({% link docs/stable/clients/rust.md %})                                 | Core team                                       | Primary      | [{{ site.current_duckdb_rust_version }}](https://crates.io/crates/duckdb)                                                                                                         |
| [WebAssembly (Wasm)]({% link docs/stable/clients/wasm/overview.md %})          | Core team                                       | Primary      | [{{ site.current_duckdb_wasm_version }}](https://github.com/duckdb/duckdb-wasm#readme)                                                                                            |
| [ADBC (Arrow)]({% link docs/stable/clients/adbc.md %})                         | Core team                                       | Secondary    | [{{ site.current_duckdb_version }}]({% link docs/stable/clients/adbc.md %})                                                                                                       |
| [C# (.NET)](https://duckdb.net/)                                               | [Giorgi](https://github.com/Giorgi)             | Secondary    | [{{ site.current_duckdb_csharp_version}}](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/stable/clients/cpp.md %})                                   | Core team                                       | Secondary    | [{{ site.current_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cplusplus)                                                                           |
| [Node.js (deprecated)]({% link docs/stable/clients/nodejs/overview.md %})      | Core team                                       | Secondary    | [{{ site.current_duckdb_nodejs_version }}](https://www.npmjs.com/package/duckdb)                                                                                                  |

For a list of tertiary clients, see the [“Tertiary Clients” page]({% link docs/stable/clients/tertiary.md %}).

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

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/stable/internals/storage.md %}).
[DuckDB extensions]({% link docs/stable/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/stable/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
