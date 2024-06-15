---
layout: docu
title: Command Line Arguments
---

The table below summarizes DuckDB's command line options.
To list all command line options, use the command:

```bash
duckdb -help
```

For a list of dot commands available in the CLI shell, see the [Dot Commands page]({% link docs/api/cli/dot_commands.md %}).

<div class="narrow_table"></div>

<!-- markdownlint-disable MD056 -->

| Argument | Description |
|---|-------|
| `-append`         | Append the database to the end of the file                                            |
| `-ascii`          | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `ascii`                                          |
| `-bail`           | Stop after hitting an error                                                           |
| `-batch`          | Force batch I/O                                                                       |
| `-box`            | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `box`                                            |
| `-column`         | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `column`                                         |
| `-cmd COMMAND`    | Run `COMMAND` before reading `stdin`                                                  |
| `-c COMMAND`      | Run `COMMAND` and exit                                                                |
| `-csv`            | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `csv`                                            |
| `-echo`           | Print commands before execution                                                       |
| `-init FILENAME`  | Run the script in `FILENAME` upon startup (instead of `~./duckdbrc`)                  |
| `-header`         | Turn headers on                                                                       |
| `-help`           | Show this message                                                                     |
| `-html`           | Set [output mode]({% link docs/api/cli/output_formats.md %}) to HTML                                             |
| `-interactive`    | Force interactive I/O                                                                 |
| `-json`           | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `json`                                           |
| `-line`           | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `line`                                           |
| `-list`           | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `list`                                           |
| `-markdown`       | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `markdown`                                       |
| `-newline SEP`    | Set output row separator. Default: `\n`                                               |
| `-nofollow`       | Refuse to open symbolic links to database files                                       |
| `-noheader`       | Turn headers off                                                                      |
| `-no-stdin`       | Exit after processing options instead of reading stdin                                |
| `-nullvalue TEXT` | Set text string for `NULL` values. Default: empty string                              |
| `-quote`          | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `quote`                                          |
| `-readonly`       | Open the database read-only                                                           |
| `-s COMMAND`      | Run `COMMAND` and exit                                                                |
| `-separator SEP`  | Set output column separator to `SEP`. Default: `|`                                    |
| `-stats`          | Print memory stats before each finalize                                               |
| `-table`          | Set [output mode]({% link docs/api/cli/output_formats.md %}) to `table`                                          |
| `-unsigned`       | Allow loading of [unsigned extensions]({% link docs/extensions/overview.md %}#unsigned-extensions) |
| `-version`        | Show DuckDB version                                                                   |

<!-- markdownlint-enable MD056 -->
