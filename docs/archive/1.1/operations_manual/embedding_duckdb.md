---
layout: docu
title: Embedding DuckDB
---

## CLI Client

The [Command Line Interface (CLI) client]({% link docs/archive/1.1/api/cli/overview.md %}) is intended for interactive use cases and not for embedding.
As a result, it has more features that could be abused by a malicious actor.
For example, the CLI client has the `.sh` feature that allows executing arbitrary shell commands.
This feature is only present in the CLI client and not in any other DuckDB clients.

```sql
.sh ls
```

> Tip Calling DuckDB's CLI client via shell commands is **not recommended** for embedding DuckDB. It is recommended to use one of the client libraries, e.g., [Python]({% link docs/archive/1.1/api/python/overview.md %}), [R]({% link docs/archive/1.1/api/r.md %}), [Java]({% link docs/archive/1.1/api/java.md %}), etc.