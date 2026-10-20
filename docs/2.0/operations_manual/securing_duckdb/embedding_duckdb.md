---
layout: docu
redirect_from:
- /docs/stable/operations_manual/embedding_duckdb
- /docs/operations_manual/embedding_duckdb
- /docs/stable/operations_manual/securing_duckdb/embedding_duckdb
- /docs/current/operations_manual/securing_duckdb/embedding_duckdb
- /docs/lts/operations_manual/securing_duckdb/embedding_duckdb
- /docs/preview/operations_manual/securing_duckdb/embedding_duckdb
title: Embedding DuckDB
---

## CLI Client

The [Command Line Interface (CLI) client]({% link docs/2.0/clients/cli/overview.md %}) is intended for interactive use cases and not for embedding.
As a result, it has more features that could be abused by a malicious actor.
For example, the CLI client has the `.sh` feature that allows executing arbitrary shell commands.
This feature is only present in the CLI client and not in any other DuckDB clients.

```sql
.sh ls
```

> Tip Calling DuckDB's CLI client via shell commands is **not recommended** for embedding DuckDB. It is recommended to use one of the client libraries, e.g., [Python]({% link docs/2.0/clients/python/overview.md %}), [R]({% link docs/2.0/clients/r.md %}), [Java]({% link docs/2.0/clients/java/overview.md %}), etc.
