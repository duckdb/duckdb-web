---
layout: docu
redirect_from:
- /docs/operations_manual/footprint_of_duckdb/files_created_by_duckdb
title: Files Created by DuckDB
---

DuckDB creates several files and directories on disk. This page lists both the global and the local ones.

## Global Files and Directories

DuckDB creates the following global files and directories in the user's home directory (denoted with `~`):

| Location | Description | Shared between versions | Shared between clients |
|-------|-------------------|--|--|
| `~/.duckdbrc` | The content of this file is executed when starting the [DuckDB CLI client]({% link docs/stable/clients/cli/overview.md %}). The commands can be both [dot command]({% link docs/stable/clients/cli/dot_commands.md %}) and SQL statements. The naming of this file follows the `~/.bashrc` and `~/.zshrc` “run commands” files. | Yes | Only used by CLI |
| `~/.duckdb_history` | History file, similar to `~/.bash_history` and `~/.zsh_history`. Used by the [DuckDB CLI client]({% link docs/stable/clients/cli/overview.md %}). | Yes | Only used by CLI |
| `~/.duckdb/extensions` | Binaries of installed [extensions]({% link docs/stable/extensions/overview.md %}). | No | Yes |
| `~/.duckdb/stored_secrets` | [Persistent secrets]({% link docs/stable/configuration/secrets_manager.md %}#persistent-secrets) created by the [Secrets manager]({% link docs/stable/configuration/secrets_manager.md %}). | Yes | Yes |

## Local Files and Directories

DuckDB creates the following files and directories in the working directory (for in-memory connections) or relative to the database file (for persistent connections):

| Name | Description | Example |
|-------|-------------------|---|
| `⟨database_filename⟩`{:.language-sql .highlight} | Database file. Only created in on-disk mode. The file can have any extension with typical extensions being `.duckdb`, `.db`, and `.ddb`. | `weather.duckdb` |
| `.tmp/` | Temporary directory. Only created in in-memory mode. | `.tmp/` |
| `⟨database_filename⟩.tmp/`{:.language-sql .highlight} | Temporary directory. Only created in on-disk mode. | `weather.tmp/` |
| `⟨database_filename⟩.wal`{:.language-sql .highlight} | [Write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging) file. If DuckDB exits normally, the WAL file is deleted upon exit. If DuckDB crashes, the WAL file is required to recover data. | `weather.wal` |

If you are working in a Git repository and would like to disable tracking these files by Git,
see the instructions on using [`.gitignore` for DuckDB]({% link docs/stable/operations_manual/footprint_of_duckdb/gitignore_for_duckdb.md %}).
