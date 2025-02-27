---
layout: docu
title: Client APIs Overview
---

DuckDB is an in-process database system and offers client APIs for several languages. These clients support the same DuckDB file format and SQL syntax. Note: DuckDB database files are portable between different clients.

| Client API | Maintainer | Support tier |
|------------|------------|--------------|
| [C]({% link docs/1.1/api/c/overview.md %})                              | DuckDB team                                                                | Primary       |
| [Command Line Interface (CLI)]({% link docs/1.1/api/cli/overview.md %}) | DuckDB team                                                                | Primary       |
| [Java]({% link docs/1.1/api/java.md %})                                 | DuckDB team                                                                | Primary       |
| [Go]({% link docs/1.1/api/go.md %})                                     | DuckDB team and [Marc Boeker](https://github.com/marcboeker)               | Primary       |
| [Node.js (deprecated)]({% link docs/1.1/api/nodejs/overview.md %})      | DuckDB team                                                                | Primary       |
| [Node.js (node-neo)]({% link docs/1.1/api/node_neo/overview.md %})      | Jeff Raymakers and Antony Courtney ([MotherDuck](https://motherduck.com/)) | Primary       |
| [Python]({% link docs/1.1/api/python/overview.md %})                    | DuckDB team                                                                | Primary       |
| [R]({% link docs/1.1/api/r.md %})                                       | DuckDB team and [Kirill Müller](https://github.com/krlmlr)                 | Primary       |
| [WebAssembly (Wasm)]({% link docs/1.1/api/wasm/overview.md %})          | DuckDB team                                                                | Primary       |
| [ADBC (Arrow)]({% link docs/1.1/api/adbc.md %})                         | DuckDB team                                                                | Secondary     |
| [C++]({% link docs/1.1/api/cpp.md %})                                   | DuckDB team                                                                | Secondary     |
| [C# (.NET)](https://duckdb.net/)                                    | [Giorgi](https://github.com/Giorgi)                                        | Secondary     |
| [Dart]({% link docs/1.1/api/dart.md %})                                 | [TigerEye](https://www.tigereye.com/)                                      | Secondary     |
| [ODBC]({% link docs/1.1/api/odbc/overview.md %})                        | DuckDB team                                                                | Secondary     |
| [Rust]({% link docs/1.1/api/rust.md %})                                 | DuckDB team                                                                | Secondary     |
| [Julia]({% link docs/1.1/api/julia.md %})                               | DuckDB team                                                                | Secondary     |
| [Swift]({% link docs/1.1/api/swift.md %})                               | DuckDB team                                                                | Secondary     |
| [Common Lisp](https://github.com/ak-coram/cl-duckdb)                | [ak-coram](https://github.com/ak-coram)                                    | Tertiary      |
| [Crystal](https://github.com/amauryt/crystal-duckdb)                | [amauryt](https://github.com/amauryt)                                      | Tertiary      |
| [Elixir](https://github.com/AlexR2D2/duckdbex)                      | [AlexR2D2](https://github.com/AlexR2D2/duckdbex)                           | Tertiary      |
| [Erlang](https://github.com/mmzeeman/educkdb)                       | [MM Zeeman](https://github.com/mmzeeman)                                   | Tertiary      |
| [Ruby](https://github.com/suketa/ruby-duckdb)                       | [suketa](https://github.com/suketa)                                        | Tertiary      |
| [Zig](https://github.com/karlseguin/zuckdb.zig)                     | [karlseguin](https://github.com/karlseguin)                                | Tertiary      |

## Support Tiers

Since there is such a wide variety of clients, the DuckDB team focuses their development effort on the most popular clients.
To reflect this, we distinguish three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://duckdblabs.com/community_support_policy).
Secondary clients receive new features but are not covered by community support.
Finally, all tertiary clients are maintained by third parties, so there are no feature or support guarantees for them.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available for the MIT license.
> For tertiary clients, please consult the repository for the license.