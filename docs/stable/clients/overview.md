---
layout: docu
redirect_from:
- /docs/clients
- /docs/clients/
- /docs/api/overview
- /docs/api/overview/
- /docs/clients/overview
title: Client Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.

| Client API                                                                      | Maintainer                                                                              | Support tier | Supported DuckDB version                                                                                                 |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| [C]({% link docs/preview/clients/c/overview.md %})                              | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbversion }}]({% link docs/installation/index.html %}?version=stable&environment=cplusplus)          |
| [Command Line Interface (CLI)]({% link docs/preview/clients/cli/overview.md %}) | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbversion }}]({% link docs/installation/index.html %}?version=stable&environment=cli)                |
| [Java (JDBC)]({% link docs/preview/clients/java.md %})                          | The DuckDB team                                                                         | Primary      | [{{ site.currentjavashortversion }}](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc)                       |
| [Go]({% link docs/preview/clients/go.md %})                                     | [Marc Boeker](https://github.com/marcboeker) and the DuckDB team                        | Primary      | [{{ site.currentduckdbgoversion }}](https://github.com/marcboeker/go-duckdb?tab=readme-ov-file#go-sql-driver-for-duckdb) |
| [Node.js (node-neo)]({% link docs/preview/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) ([MotherDuck](https://motherduck.com/)) | Primary      | [{{ site.currentduckdbnodeneoversion }}](https://www.npmjs.com/package/@duckdb/node-api)                                 |
| [ODBC]({% link docs/preview/clients/odbc/overview.md %})                        | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbodbcshortversion }}]({% link docs/installation/index.html %}?version=stable&environment=odbc)      |
| [Python]({% link docs/preview/clients/python/overview.md %})                    | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbversion }}](https://pypi.org/project/duckdb/)                                                      |
| [R]({% link docs/preview/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr) and the DuckDB team                          | Primary      | [{{ site.currentrversion }}](https://cran.r-project.org/web/packages/duckdb/index.html)                                  |
| [Rust]({% link docs/preview/clients/rust.md %})                                 | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbrustversion }}](https://crates.io/crates/duckdb)                                                   |
| [WebAssembly (Wasm)]({% link docs/preview/clients/wasm/overview.md %})          | The DuckDB team                                                                         | Primary      | [{{ site.currentduckdbwasmversion }}](https://github.com/duckdb/duckdb-wasm?tab=readme-ov-file#duckdb-and-duckdb-wasm)   |
| [ADBC (Arrow)]({% link docs/preview/clients/adbc.md %})                         | The DuckDB team                                                                         | Secondary    | [{{ site.currentduckdbversion }}]({% link docs/preview/clients/adbc.md %})                                               |
| [C# (.NET)](https://duckdb.net/)                                                | [Giorgi](https://github.com/Giorgi)                                                     | Secondary    | [{{ site.currentduckdbcsharpversion}}](https://www.nuget.org/packages/DuckDB.NET.Bindings.Full)                          |
| [C++]({% link docs/preview/clients/cpp.md %})                                   | The DuckDB team                                                                         | Secondary    | [{{ site.currentduckdbversion }}]({% link docs/installation/index.html %}?version=stable&environment=cplusplus)          |
| [Dart]({% link docs/preview/clients/dart.md %})                                 | [TigerEye](https://www.tigereye.com/)                                                   | Secondary    | [{{ site.currentduckdbdartversion }}](https://pub.dev/packages/dart_duckdb)                                              |
| [Node.js (deprecated)]({% link docs/preview/clients/nodejs/overview.md %})      | The DuckDB team                                                                         | Secondary    | [{{ site.currentduckdbnodejsversion }}](https://www.npmjs.com/package/duckdb)                                            |
| [Common Lisp](https://github.com/ak-coram/cl-duckdb)                            | [ak-coram](https://github.com/ak-coram)                                                 | Tertiary     |                                                                                                                          |
| [Crystal](https://github.com/amauryt/crystal-duckdb)                            | [amauryt](https://github.com/amauryt)                                                   | Tertiary     |                                                                                                                          |
| [Elixir](https://github.com/AlexR2D2/duckdbex)                                  | [AlexR2D2](https://github.com/AlexR2D2/duckdbex)                                        | Tertiary     |                                                                                                                          |
| [Erlang](https://github.com/mmzeeman/educkdb)                                   | [MM Zeeman](https://github.com/mmzeeman)                                                | Tertiary     |                                                                                                                          |
| [Julia]({% link docs/preview/clients/julia.md %})                               | The DuckDB team                                                                         | Tertiary     |                                                                                                                          |
| [Pyodide](https://github.com/duckdb/duckdb-pyodide)                             | The DuckDB team                                                                         | Tertiary     |                                                                                                                          |
| [Ruby](https://suketa.github.io/ruby-duckdb/)                                   | [suketa](https://github.com/suketa)                                                     | Tertiary     |                                                                                                                          |
| [Swift]({% link docs/preview/clients/swift.md %})                               | The DuckDB team                                                                         | Tertiary     |                                                                                                                          |
| [Zig](https://github.com/karlseguin/zuckdb.zig)                                 | [karlseguin](https://github.com/karlseguin)                                             | Tertiary     |                                                                                                                          |

## Support Tiers

Since there is such a wide variety of clients, the DuckDB team focuses their development effort on the most popular clients.
To reflect this, we distinguish three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/community_support_policy).
Secondary clients receive new features but are not covered by community support.
Finally, there are no feature or support guarantees for tertiary clients.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available for the MIT license.
> For tertiary clients, please consult the repository for the license.

We report the latest stable version for the clients in the primary and secondary support tiers.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/preview/internals/storage.md %}).
[DuckDB extensions]({% link docs/preview/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/preview/clients/wasm/extensions.md %}#list-of-officially-available-extensions)).
