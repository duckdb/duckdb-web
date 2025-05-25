---
github_repository: https://github.com/duckdb/ducklake
layout: docu
title: DuckLake
---

> DuckLake has been released in May 2025.
> Read the [announcement blog post]({% post_url 2025-05-27-ducklake %}).

The `ducklake` extension add support for attaching to databases stored in the [DuckLake format](http://ducklake.select/):

## Installing and Loading

To install `ducklake`, run:

```sql
INSTALL ducklake;
```

The `ducklake` extension will be transparently [autoloaded]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions) on first use in an `ATTACH clause`.``
If you would like to load it manually, run:

```sql
LOAD ducklake;
```
