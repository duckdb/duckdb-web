---
layout: docu
title: Client APIs Overview
---

DuckDB is an in-process database system and offers client APIs (also known as “drivers”) for several languages.

| Client API | Maintainer | Support tier | Latest version |
|------------|------------|--------------|---------------:|
| [C]({% link docs/api/c/overview.md %})                              | DuckDB team                                                                | Primary       | 1.2.0 |
| [Command Line Interface (CLI)]({% link docs/api/cli/overview.md %}) | DuckDB team                                                                | Primary       | 1.2.0 |
| [Java]({% link docs/api/java.md %})                                 | DuckDB team                                                                | Primary       | 1.1.3 |
| [Go]({% link docs/api/go.md %})                                     | DuckDB team and [Mark Boeker](https://github.com/marcboeker)               | Primary       | 1.1.3 |
| [Node.js (node-neo)]({% link docs/api/node_neo/overview.md %})      | Jeff Raymakers and Antony Courtney ([MotherDuck](https://motherduck.com/)) | Primary       | 1.1.3 |
| [Python]({% link docs/api/python/overview.md %})                    | DuckDB team                                                                | Primary       | 1.2.0 |
| [R]({% link docs/api/r.md %})                                       | DuckDB team and [Kirill Müller](https://github.com/krlmlr)                 | Primary       | 1.1.3 |
| [WebAssembly (Wasm)]({% link docs/api/wasm/overview.md %})          | DuckDB team                                                                | Primary       | 1.2.0 |
| [ADBC (Arrow)]({% link docs/api/adbc.md %})                         | DuckDB team                                                                | Secondary     | 1.2.0 |
| [C++]({% link docs/api/cpp.md %})                                   | DuckDB team                                                                | Secondary     | 1.2.0 |
| [C# (.NET)](https://duckdb.net/)                                    | [Giorgi](https://github.com/Giorgi)                                        | Secondary     | 1.2.0 |
| [Dart]({% link docs/api/dart.md %})                                 | [TigerEye](https://www.tigereye.com/)                                      | Secondary     | 1.1.3 |
| [ODBC]({% link docs/api/odbc/overview.md %})                        | DuckDB team                                                                | Secondary     | 1.1.0 |
| [Node.js (deprecated)]({% link docs/api/nodejs/overview.md %})      | DuckDB team                                                                | Secondary     | 1.1.3 |
| [Rust]({% link docs/api/rust.md %})                                 | DuckDB team                                                                | Secondary     | |
| [Julia]({% link docs/api/julia.md %})                               | DuckDB team                                                                | Secondary     | |
| [Swift]({% link docs/api/swift.md %})                               | DuckDB team                                                                | Secondary     | |
| [Common Lisp](https://github.com/ak-coram/cl-duckdb)                | [ak-coram](https://github.com/ak-coram)                                    | Tertiary      | |
| [Crystal](https://github.com/amauryt/crystal-duckdb)                | [amauryt](https://github.com/amauryt)                                      | Tertiary      | |
| [Elixir](https://github.com/AlexR2D2/duckdbex)                      | [AlexR2D2](https://github.com/AlexR2D2/duckdbex)                           | Tertiary      | |
| [Erlang](https://github.com/mmzeeman/educkdb)                       | [MM Zeeman](https://github.com/mmzeeman)                                   | Tertiary      | |
| [Ruby](https://github.com/suketa/ruby-duckdb)                       | [suketa](https://github.com/suketa)                                        | Tertiary      | |
| [Zig](https://github.com/karlseguin/zuckdb.zig)                     | [karlseguin](https://github.com/karlseguin)                                | Tertiary      | |

## Support Tiers

Since there is such a wide variety of clients, the DuckDB team focuses their development effort on the most popular clients.
To reflect this, we distinguish three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/news/2023/10/02/support-policy).
Secondary clients receive new features but are not covered by community support.
Finally, all tertiary clients are maintained by third parties, so there are no feature or support guarantees for them.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available for the MIT license.
> For tertiary clients, please consult the repository for the license.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/internals/storage.md %}).
[DuckDB extensions]({% link docs/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/api/wasm/extensions.md %}#list-of-officially-available-extensions)).
