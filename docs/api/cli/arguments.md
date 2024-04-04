---
layout: docu
title: Command Line Arguments
---

The table below summarizes DuckDB's command line options.
To list all command line options, use the command `duckdb -help`.
Fot a list of dot commands available in the CLI shell, see the [Dot Commands page](dot_commands).

<div class="narrow_table"></div>

<!-- markdownlint-disable MD056 -->

| Argument | Description |
|---|-------|
| `-append`         | Append the database to the end of the file                                            |
| `-ascii`          | Set [output mode](output-formats) to `ascii`                                          |
| `-bail`           | Stop after hitting an error                                                           |
| `-batch`          | Force batch I/O                                                                       |
| `-box`            | Set [output mode](output-formats) to `box`                                            |
| `-column`         | Set [output mode](output-formats) to `column`                                         |
| `-cmd COMMAND`    | Run `COMMAND` before reading `stdin`                                                  |
| `-c COMMAND`      | Run `COMMAND` and exit                                                                |
| `-csv`            | Set [output mode](output-formats) to `csv`                                            |
| `-echo`           | Print commands before execution                                                       |
| `-init FILENAME`  | Run the script in `FILENAME` upon startup (instead of `~./duckdbrc`)                  |
| `-header`         | Turn headers on                                                                       |
| `-help`           | Show this message                                                                     |
| `-html`           | Set [output mode](output-formats) to HTML                                             |
| `-interactive`    | Force interactive I/O                                                                 |
| `-json`           | Set [output mode](output-formats) to `json`                                           |
| `-line`           | Set [output mode](output-formats) to `line`                                           |
| `-list`           | Set [output mode](output-formats) to `list`                                           |
| `-markdown`       | Set [output mode](output-formats) to `markdown`                                       |
| `-newline SEP`    | Set output row separator. Default: `\n`                                               |
| `-nofollow`       | Refuse to open symbolic links to database files                                       |
| `-noheader`       | Turn headers off                                                                      |
| `-no-stdin`       | Exit after processing options instead of reading stdin                                |
| `-nullvalue TEXT` | Set text string for `NULL` values. Default: empty string                              |
| `-quote`          | Set [output mode](output-formats) to `quote`                                          |
| `-readonly`       | Open the database read-only                                                           |
| `-s COMMAND`      | Run `COMMAND` and exit                                                                |
| `-separator SEP`  | Set output column separator to SEP. Default: `|`                                      |
| `-stats`          | Print memory stats before each finalize                                               |
| `-table`          | Set [output mode](output-formats) to `table`                                          |
| `-unsigned`       | Allow loading of [unsigned extensions](../../extensions/overview#unsigned-extensions) |
| `-version`        | Show DuckDB version                                                                   |

<!-- markdownlint-enable MD056 -->
