---
layout: docu
title: Client Overview
redirect_from:
  - /docs/clients
  - /docs/clients/
  - /docs/api/overview
  - /docs/api/overview/
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.

| Client API                                                              | Maintainer                                                                                                                                       | Support tier |                                                                                                                                  Latest version |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------: |
| [C]({% link docs/clients/c/overview.md %})                              | The DuckDB team                                                                                                                                  | Primary      |                                 [{{ site.currentduckdbversion }}]({% link docs/installation/index.html %}?version=stable&environment=cplusplus) |
| [Command Line Interface (CLI)]({% link docs/clients/cli/overview.md %}) | The DuckDB team                                                                                                                                  | Primary      |                                       [{{ site.currentduckdbversion }}]({% link docs/installation/index.html %}?version=stable&environment=cli) |
| [Java (JDBC)]({% link docs/clients/java.md %})                          | The DuckDB team                                                                                                                                  | Primary      |                                                [{{ site.currentjavaversion }}](https://mvnrepository.com/artifact/org.duckdb/duckdb_jdbc/1.2.0) |
| [Go]({% link docs/clients/go.md %})                                     | [Marc Boeker](https://github.com/marcboeker) and the DuckDB team                                                                                 | Primary      |                                                    [1.1.3](https://github.com/marcboeker/go-duckdb?tab=readme-ov-file#go-sql-driver-for-duckdb) |
| [Node.js (node-neo)]({% link docs/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) and [Antony Courtney](https://github.com/antonycourtney) ([MotherDuck](https://motherduck.com/)) | Primary      |                                                                                         [1.2.0](https://www.npmjs.com/package/@duckdb/node-api) |
| [Python]({% link docs/clients/python/overview.md %})                    | The DuckDB team                                                                                                                                  | Primary      |                                                                             [{{ site.currentduckdbversion }}](https://pypi.org/project/duckdb/) |
| [R]({% link docs/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr) and the DuckDB team                                                                                   | Primary      |                                                                              [1.1.3](https://cran.r-project.org/web/packages/duckdb/index.html) |
| [WebAssembly (Wasm)]({% link docs/clients/wasm/overview.md %})          | The DuckDB team                                                                                                                                  | Primary      |                                                        [1.2.0](https://github.com/duckdb/duckdb-wasm?tab=readme-ov-file#duckdb-and-duckdb-wasm) |
| [ADBC (Arrow)]({% link docs/clients/adbc.md %})                         | The DuckDB team                                                                                                                                  | Secondary    |                                                                          [{{ site.currentduckdbversion }}]({% link docs/extensions/arrow.md %}) |
| [C# (.NET)](https://duckdb.net/)                                        | [Giorgi](https://github.com/Giorgi)                                                                                                              | Secondary    | [1.2.0](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/clients/cpp.md %})                                   | The DuckDB team                                                                                                                                  | Secondary    |                                                           [1.2.0]({% link docs/installation/index.html %}?version=stable&environment=cplusplus) |
| [Dart]({% link docs/clients/dart.md %})                                 | [TigerEye](https://www.tigereye.com/)                                                                                                            | Secondary    |                                                                                                   [1.1.3](https://pub.dev/packages/dart_duckdb) |
| [Julia]({% link docs/clients/julia.md %})                               | The DuckDB team                                                                                                                                  | Secondary    |                                                                                        [1.2.0](https://juliahub.com/ui/Packages/General/DuckDB) |
| [Node.js (deprecated)]({% link docs/clients/nodejs/overview.md %})      | The DuckDB team                                                                                                                                  | Secondary    |                                                                                                   [1.2.0](https://www.npmjs.com/package/duckdb) |
| [ODBC]({% link docs/clients/odbc/overview.md %})                        | The DuckDB team                                                                                                                                  | Secondary    |                                                                [1.1.0]({% link docs/installation/index.html %}?version=stable&environment=odbc) |
| [Rust]({% link docs/clients/rust.md %})                                 | The DuckDB team                                                                                                                                  | Secondary    |                                                                                                        [1.2.0](https://crates.io/crates/duckdb) |
| [Swift]({% link docs/clients/swift.md %})                               | The DuckDB team                                                                                                                                  | Secondary    |                                                                                                [1.2.0](https://github.com/duckdb/duckdb-swift/) |
| [Common Lisp](https://github.com/ak-coram/cl-duckdb)                    | [ak-coram](https://github.com/ak-coram)                                                                                                          | Tertiary     |                                                                                                                                                 |
| [Crystal](https://github.com/amauryt/crystal-duckdb)                    | [amauryt](https://github.com/amauryt)                                                                                                            | Tertiary     |                                                                                                                                                 |
| [Elixir](https://github.com/AlexR2D2/duckdbex)                          | [AlexR2D2](https://github.com/AlexR2D2/duckdbex)                                                                                                 | Tertiary     |                                                                                                                                                 |
| [Erlang](https://github.com/mmzeeman/educkdb)                           | [MM Zeeman](https://github.com/mmzeeman)                                                                                                         | Tertiary     |                                                                                                                                                 |
| [Ruby](https://github.com/suketa/ruby-duckdb)                           | [suketa](https://github.com/suketa)                                                                                                              | Tertiary     |                                                                                                                                                 |
| [Zig](https://github.com/karlseguin/zuckdb.zig)                         | [karlseguin](https://github.com/karlseguin)                                                                                                      | Tertiary     |                                                                                                                                                 |

## Support Tiers

Since there is such a wide variety of clients, the DuckDB team focuses their development effort on the most popular clients.
To reflect this, we distinguish three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/news/2023/10/02/support-policy).
Secondary clients receive new features but are not covered by community support.
Finally, all tertiary clients are maintained by third parties, so there are no feature or support guarantees for them.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available for the MIT license.
> For tertiary clients, please consult the repository for the license.

We report the latest stable version for the clients in the primary and secondary support tiers.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/internals/storage.md %}).
[DuckDB extensions]({% link docs/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
