---
layout: docu
title: Command Line Arguments
---

The table below summarizes DuckDB's command line options.
To list all command line options, use the command:

```batch
duckdb -help
```

For a list of dot commands available in the CLI shell, see the [Dot Commands page]({% link docs/preview/clients/cli/dot_commands.md %}).

<!-- markdownlint-disable MD056 -->

| Argument          | Description                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `-append`         | Append the database to the end of the file                                                                    |
| `-ascii`          | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `ascii`                            |
| `-bail`           | Stop after hitting an error                                                                                   |
| `-batch`          | Force batch I/O                                                                                               |
| `-box`            | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `box`                              |
| `-column`         | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `column`                           |
| `-cmd COMMAND`    | Run `COMMAND` before reading `stdin`                                                                          |
| `-c COMMAND`      | Run `COMMAND` and exit                                                                                        |
| `-csv`            | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `csv`                              |
| `-echo`           | Print commands before execution                                                                               |
| `-f FILENAME`     | Run the script in `FILENAME` and exit. Note that the `~/.duckdbrc` is read and executed first (if it exists)  |
| `-init FILENAME`  | Run the script in `FILENAME` upon startup (instead of `~/.duckdbrc`)                                          |
| `-header`         | Turn headers on                                                                                               |
| `-help`           | Show this message                                                                                             |
| `-html`           | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to HTML                               |
| `-interactive`    | Force interactive I/O                                                                                         |
| `-json`           | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `json`                             |
| `-line`           | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `line`                             |
| `-list`           | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `list`                             |
| `-markdown`       | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `markdown`                         |
| `-newline SEP`    | Set output row separator. Default: `\n`                                                                       |
| `-nofollow`       | Refuse to open symbolic links to database files                                                               |
| `-noheader`       | Turn headers off                                                                                              |
| `-no-stdin`       | Exit after processing options instead of reading stdin                                                        |
| `-nullvalue TEXT` | Set text string for `NULL` values. Default: `NULL`                                                            |
| `-quote`          | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `quote`                            |
| `-readonly`       | Open the database read-only. This option also supports attaching to remote databases via HTTPS                                                                                   |
| `-s COMMAND`      | Run `COMMAND` and exit                                                                                        |
| `-separator SEP`  | Set output column separator to `SEP`. Default: `|`                                                            |
| `-storage-version VER` | Database storage compatibility version to use.                                                           |
| `-table`          | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %}) to `table`                            |
| `-ui`             | Loads and starts the [DuckDB UI]({% link docs/preview/core_extensions/ui.md %}). If the UI is not yet installed, it installs the `ui` extension |
| `-unsigned`       | Allow loading of [unsigned extensions]({% link docs/preview/extensions/overview.md %}#unsigned-extensions). This option is intended to be used for developing extensions. Consult the [Securing DuckDB page]({% link docs/preview/operations_manual/securing_duckdb/securing_extensions.md %}) for guidelines on how to set up DuckDB in a secure manner |
| `-version`        | Show DuckDB version                                                                                           |

<!-- markdownlint-enable MD056 -->

## Passing a Sequence of Arguments

Note that the CLI arguments are processed in order, similarly to the behavior of the SQLite CLI.
For example:

```batch
duckdb -csv -c 'SELECT 42 AS hello' -json -c 'SELECT 84 AS world'
```

Returns the following:

```text
hello
42
[{"world":84}]
```
