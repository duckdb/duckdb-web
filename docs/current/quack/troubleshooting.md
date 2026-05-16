---
layout: docu
title: Troubleshooting Quack
---

Quack is currently available as a beta release.
It is not ready for production and is subject to breaking changes until the release of [DuckDB v2.0]({% link release_calendar.md %}).
If you experience any issues with Quack, try upgrading all your DuckDB clients to the latest version of the `quack` extension:

```sql
FORCE INSTALL quack FROM core_nightly;
```
