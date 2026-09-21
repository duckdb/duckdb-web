---
layout: docu
title: Gitignore for DuckDB
---

If you work in a Git repository, you may want to configure your [Gitignore](https://git-scm.com/docs/gitignore) to disable tracking [files created by DuckDB]({% link docs/preview/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md %}).
These potentially include the DuckDB database, write-ahead log, and temporary files.

## Sample Gitignore Files

In the following, we present sample Gitignore configuration snippets for DuckDB.

### Ignore Temporary Files but Keep Database

This configuration is useful if you would like to keep the database file in the version control system:

```text
*.wal
*.tmp/
```

### Ignore Database and Temporary Files

If you would like to ignore both the database and the temporary files, extend the Gitignore file to include the database file.
The exact Gitignore configuration to achieve this depends on the extension you use for your DuckDB databases (`.duckdb`, `.db`, `.ddb`, etc.).
For example, if your DuckDB files use the `.duckdb` extension, add the following lines to your `.gitignore` file:

```text
*.duckdb*
*.wal
*.tmp/
```
