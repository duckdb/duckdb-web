---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
redirect_from:
- /community_extensions/extensions/quack
- /docs/current/core_extensions/quack
- /docs/lts/core_extensions/quack
- /docs/preview/core_extensions/quack
- /docs/stable/core_extensions/quack
title: Quack Extension
---

The `quack` extension adds support for the Quack remote protocol.

## Usage

> New DuckDB 2.0.0 shipped a polished version of the Quack protocol that is faster and more stable.
> Expect further improvements in upcoming patch releases.

Quack is transparently autoinstalled and [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use.

If you would like to install Quack explicitly, run:

```sql
INSTALL quack;
```

If you would like to load Quack explicitly, run:

```sql
LOAD quack;
```

For usage details, see the [Quack remote protocol page]({% link docs/2.0/quack/overview.md %}).
