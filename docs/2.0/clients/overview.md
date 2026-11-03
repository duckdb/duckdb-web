---
layout: docu
redirect_from:
- /apis
- /clients
- /drivers
- /docs/api
- /docs/api/overview
- /docs/clients
- /docs/clients/overview
- /docs/stable/clients
- /docs/stable/clients/overview
- /docs/current/clients/overview
- /docs/lts/clients/overview
- /docs/preview/clients/overview
title: Client Overview
---

DuckDB is primarily an in-process database system, and as such, it offers client APIs (“drivers”) for several languages.

| Client API                                                                      | Maintainer                                      | Support tier | Latest version                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/2.0/clients/c/overview.md %})                              | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="core" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=c)                                                                                                                                                                             |
| [CLI (command line interface)]({% link docs/2.0/clients/cli/overview.md %}) | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="core" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=cli)                                                                                                                                                                         |
| [Java (JDBC)]({% link docs/2.0/clients/java/overview.md %})                          | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="java" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=java)                                                                                                                                      |
| [Go]({% link docs/2.0/clients/go/overview.md %})                                     | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="go" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=go)                                                                                                                                                                  |
| [Node.js (node-neo)]({% link docs/2.0/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="nodejs" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=nodejs)                                                                                                                                        |
| [ODBC]({% link docs/2.0/clients/odbc/overview.md %})                        | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="odbc" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=odbc)                                                                                                                                      |
| [Python]({% link docs/2.0/clients/python/overview.md %})                    | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="core" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=python)                                                                                                                                                                   |
| [R]({% link docs/2.0/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr)      | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="r" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=r)                                                                                                                                                                       |
| [Rust]({% link docs/2.0/clients/rust/overview.md %})                                 | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="rust" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=rust)                                                                                                                                                        |
| [WebAssembly (Wasm)]({% link docs/2.0/clients/wasm/overview.md %})          | Core team                                       | {% include tooltip.html label="Primary" id="support_tier_primary" %}      | {% include install/latest_client.html client="wasm" %}[{{ latest_version }}](https://github.com/duckdb/duckdb-wasm#readme)                                                                                                                                                                                           |
| [ADBC (Arrow)]({% link docs/2.0/clients/adbc.md %})                         | Core team                                       | {% include tooltip.html label="Secondary" id="support_tier_secondary" %}    | {% include install/latest_client.html client="core" %}[{{ latest_version }}]({% link docs/2.0/clients/adbc.md %})                                                                                                                                                                                                                        |
| [C# (.NET)](https://duckdb.net/)                                                | [Giorgi](https://github.com/Giorgi)             | {% include tooltip.html label="Secondary" id="support_tier_secondary" %}    | {% include install/latest_client.html client="csharp" %}[{{ latest_version }}](https://www.nuget.org/packages?q=Tags%3A%22DuckDB%22+Author%3A%22Giorgi%22&includeComputedFrameworks=true&prerel=true&sortby=relevance) |
| [C++]({% link docs/2.0/clients/cpp.md %})                                   | Core team                                       | {% include tooltip.html label="Secondary" id="support_tier_secondary" %}    | {% include install/latest_client.html client="core" %}[{{ latest_version }}]({% link docs/2.0/installation.html %}?version={{ latest_release }}&environment=c)                                                                                                                                                                             |

The table above lists the DuckDB clients with the primary and secondary [support tiers](#support-tiers).
For a list of tertiary clients, see the [“Tertiary Clients” page]({% link docs/2.0/clients/tertiary_clients/overview.md %}).

## Support Tiers

There are three tiers of support for clients.
Primary clients are the first to receive new features and are covered by [community support](https://ducklabs.com/community_support_policy).
Secondary clients receive new features but are not covered by community support.
Finally, there are no feature or support guarantees for tertiary clients.

> The DuckDB clients listed above are open-source and we welcome community contributions to these libraries.
> All primary and secondary clients are available under the MIT license.
> For tertiary clients, please consult the repository for the license.

## Compatibility

All DuckDB clients support the same DuckDB SQL syntax and use the same on-disk [database format]({% link docs/2.0/internals/storage.md %}).
[DuckDB extensions]({% link docs/2.0/extensions/overview.md %}) are also portable between clients with some exceptions (see [Wasm extensions]({% link docs/2.0/clients/wasm/extensions.md %}#available-extensions)).
