---
layout: docu
title: Gitignore for DuckDB
---

If you work in a Git repository, you may want to configure your [gitignore](https://git-scm.com/docs/gitignore) to disable tracking the DuckDB database, write ahead log, temporary files.

The exact gitignore configuration depends on the extension you use for you DuckDB databases. For example, if your DuckDB files use the `.duckdb` extension, add the following lines to your `.gitignore` file:

```text
*.duckdb*
*.wal
*.tmp/
```
