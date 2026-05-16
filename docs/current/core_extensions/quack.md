---
github_repository: https://github.com/duckdb/duckdb-quack
layout: docu
title: Quack Extension
redirect_from:
- community_extensions/extensions/quack
---

The `quack` extension adds support for the [Quack remote protocol]({% link docs/current/quack/overview.md %}).

## Usage

Quack is currently in preview and only available from the [`core_nightly` repository]({% link docs/current/extensions/installing_extensions.md %}#extension-repositories).

To install and load `quack`, run:

```sql
FORCE INSTALL quack FROM core_nightly;
LOAD quack;
```

> Warning As of DuckDB v1.5.2, `quack` is in an experimental state. The protocol, the function names, and implementation details are all subject to change.
> Quack is expected to reach stable status in DuckDB v2.0.0, scheduled for [September 2026]({% link release_calendar.md %}#upcoming-releases).
