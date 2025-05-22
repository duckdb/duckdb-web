---
layout: docu
redirect_from:
- /docs/operations_manual/embedding_duckdb
- /docs/1.2/operations_manual/embedding_duckdb
title: Embedding DuckDB
---

## CLI Client

The [Command Line Interface (CLI) client]({% link docs/1.2/clients/cli/overview.md %}) is intended for interactive use cases and not for embedding.
As a result, it has more features that could be abused by a malicious actor.
For example, the CLI client has the `.sh` feature that allows executing arbitrary shell commands.
This feature is only present in the CLI client and not in any other DuckDB clients.

```sql
.sh ls
```

> Tip Calling DuckDB's CLI client via shell commands is **not recommended** for embedding DuckDB. It is recommended to use one of the client libraries, e.g., [Python]({% link docs/1.2/clients/python/overview.md %}), [R]({% link docs/1.2/clients/r.md %}), [Java]({% link docs/1.2/clients/java.md %}), etc.
