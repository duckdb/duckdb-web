---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
title: Quack Extension
---

The `quack` extension adds support for the Quack remote protocol.

## Usage

> New DuckDB v2.0.0 ships a polished version of the Quack protocol that is faster and more stable.
> Expect further improvements in upcoming patch releases.

Quack is transparently autoinstalled and [autoloaded]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) on first use.

If you would like to install Quack explicitly, run:

```sql
INSTALL quack;
```

If you would like to load Quack explicitly, run:

```sql
LOAD quack;
```

For usage details, see the [Quack remote protocol page]({% link docs/preview/quack/overview.md %}).
