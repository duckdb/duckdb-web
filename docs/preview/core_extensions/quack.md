---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
title: Quack Extension
---

The `quack` extension adds support for the [Quack remote protocol]({% link docs/preview/quack/overview.md %}).

## Usage

> New The `quack` extension graduates to stable status in DuckDB 2.0. It was previously released as a preview.

Quack is transparently autoinstalled and [autoloaded]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) on first use.

If you would like to install Quack explicitly, run:

```sql
INSTALL quack;
```

If you would like to load Quack explicitly, run:

```sql
LOAD quack;
```
