---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
title: Quack Extension
redirect_from:
- community_extensions/extensions/quack
---

The `quack` extension adds support for the [Quack remote protocol]({% link docs/current/quack/overview.md %}).

## Usage

Quack is currently in a beta state. To install `quack`, run:

```sql
INSTALL quack;
```

Quack will be transparently [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extension) on first use.
If you would like to load Quack explicitly, run:

```sql
LOAD quack;
```

## Limitations

> Warning As of DuckDB v1.5.3, `quack` is in an experimental state. The protocol, the function names, and implementation details are all subject to change.
> Quack is expected to reach stable status in DuckDB v2.0.0, scheduled for [September 2026]({% link release_calendar.md %}#upcoming-releases).
