---
layout: docu
title: Files Created by DuckDB
---

<div class="narrow_table"></div>

DuckDB creates several files and directories on disk. This page lists both the global and the local ones.

## Global Files and Directories

DuckDB creates the following global files and directories in the user's home directory (denoted with `~`):

| Location | Description | Shared between versions | Shared between clients |
|-------|-------------------|--|--|
| `~/.duckdbrc` | The content of this file is executed when starting the [DuckDB CLI client]({% link docs/api/cli/overview.md %}). The commands can be both [dot commmand]({% link docs/api/cli/dot_commands.md %}) and SQL statements. The naming of this file follows the `~/.bashrc` and `~/.zshrc` "run commands" files. | Yes | Only used by CLI |
| `~/.duckdb_history` | History file, similar to `~/.bash_history` and `~/.zsh_history`. Used by the [DuckDB CLI client]({% link docs/api/cli/overview.md %}). | Yes | Only used by CLI |
| `~/duckdb/extensions` | Binaries of installed [extensions]({% link docs/extensions/overview.md %}). | No | Yes |
| `~/duckdb/secrets` | [Persistent secrets]({% link docs/configuration/secrets_manager.md %}#persistent-secrets) created by the [Secrets manager]({% link docs/configuration/secrets_manager.md %}) | Yes | Yes |

## Local Files and Directories

DuckDB creates the following files and directories in the working directory (for in-memory connections) or relative to the database file (for pesistent connections):

| Name | Description | Example | Deleted upon exit |
|-------|-------------------|---|--|
| `⟨database_filename⟩` | Database file. Only created in on-disk mode. The file can have any extension with typical extensions being `.duckdb`, `.db`, and `.ddb`. | `weather.duckdb` |  No |
| `.tmp/` | Temporary directory. Only created in in-memory mode. | `.tmp/` | Yes |
| `⟨database_filename⟩.tmp/` | Temporary directory. Only created in on-disk mode. | `weather.tmp/` | Yes |
| `⟨database_filename⟩.wal` | [Write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging) file. | `weather.wal` | Yes |

If you are working in a Git repository and would like to disable tracking these files by Git,
see the instructions on using [`.gitignore` for DuckDB]({% link docs/guides/using_duckdb/gitignore_for_duckdb.md %}).
