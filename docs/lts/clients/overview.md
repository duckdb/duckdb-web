---
layout: docu
title: Client Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.
Visit the [installation page]({% link install/index.html %}) for instructions on how to install a given DuckDB client.

| Client API                                                                     | Maintainer                                      | Support tier | LTS version                                                                                                                                                                   |
| ------------------------------------------------------------------------------ | ----------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/lts/clients/c/overview.md %})                              | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |
| [Command Line Interface (CLI)]({% link docs/lts/clients/cli/overview.md %}) | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=cli)                                                                                 |
| [Java (JDBC)]({% link docs/lts/clients/java.md %})                          | Core team                                       | Primary      | [{{ site.lts_duckdb_java_short_version }}](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc)                                                                      |
| [Go]({% link docs/lts/clients/go.md %})                                     | Core team                                       | Primary      | [{{ site.lts_duckdb_go_version }}](https://github.com/duckdb/duckdb-go#readme)                                                                                                |
| [Node.js (node-neo)]({% link docs/lts/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) | Primary      | [{{ site.lts_duckdb_node_neo_version }}](https://www.npmjs.com/package/@duckdb/node-api)                                                                                      |
| [ODBC]({% link docs/lts/clients/odbc/overview.md %})                        | Core team                                       | Primary      | [{{ site.lts_duckdb_odbc_short_version }}]({% link install/index.html %}?version=stable&environment=odbc)                                                                     |
| [Python]({% link docs/lts/clients/python/overview.md %})                    | Core team                                       | Primary      | [{{ site.lts_duckdb_version }}](https://pypi.org/project/duckdb/)                                                                                                             |
| [R]({% link docs/lts/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr)      | Primary      | [{{ site.lts_duckdb_r_version }}](https://cran.r-project.org/web/packages/duckdb/index.html)                                                                                  |
| [Rust]({% link docs/lts/clients/rust.md %})                                 | Core team                                       | Primary      | [{{ site.lts_duckdb_rust_version }}](https://crates.io/crates/duckdb)                                                                                                         |
| [WebAssembly (Wasm)]({% link docs/lts/clients/wasm/overview.md %})          | Core team                                       | Primary      | [{{ site.lts_duckdb_wasm_version }}](https://github.com/duckdb/duckdb-wasm#readme)                                                                                            |
| [ADBC (Arrow)]({% link docs/lts/clients/adbc.md %})                         | Core team                                       | Secondary    | [{{ site.lts_duckdb_version }}]({% link docs/lts/clients/adbc.md %})                                                                                                       |
| [C# (.NET)](https://duckdb.net/)                                               | [Giorgi](https://github.com/Giorgi)             | Secondary    | [{{ site.lts_duckdb_csharp_version}}](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/lts/clients/cpp.md %})                                   | Core team                                       | Secondary    | [{{ site.lts_duckdb_version }}]({% link install/index.html %}?version=stable&environment=c)                                                                                   |
| [Node.js (deprecated)]({% link docs/lts/clients/nodejs/overview.md %})      | Core team                                       | Secondary    | [{{ site.lts_duckdb_nodejs_version }}](https://www.npmjs.com/package/duckdb)                                                                                                  |

For a list of tertiary clients, see the [“Tertiary Clients” page]({% link docs/lts/clients/tertiary.md %}).

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

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/lts/internals/storage.md %}).
[DuckDB extensions]({% link docs/lts/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/lts/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
