---
layout: docu
title: Troubleshooting Quack
---

Quack was released as a stable extension in [DuckDB v2.0]({% link release_calendar.md %}), having previously been available as a preview since DuckDB v1.5.3.
The protocol continues to be refined as the team works toward full production readiness.
If you experience any issues with Quack, try upgrading all your DuckDB clients to the latest version of the `quack` extension:

```sql
FORCE INSTALL quack;
```
