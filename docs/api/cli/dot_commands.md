---
layout: docu
title: Dot Commands
redirect_from:
  - /docs/api/cli/dot-commands
---

Dot commands are available in the DuckDB CLI client. To use one of these commands, begin the line with a period (`.`) immediately followed by the name of the command you wish to execute. Additional arguments to the command are entered, space separated, after the command. If an argument must contain a space, either single or double quotes may be used to wrap that parameter. Dot commands must be entered on a single line, and no whitespace may occur before the period. No semicolon is required at the end of the line. To see available commands, use the `.help` command.

## Dot Commands

<div class="narrow_table"></div>

<!-- markdownlint-disable MD056 -->

| Command | Description |
|---|------|
| `.bail on|off`           | Stop after hitting an error.  Default: `off`                                                                 |
| `.binary on|off`         | Turn binary output on or off.  Default: `off`                                                                |
| `.cd DIRECTORY`          | Change the working directory to `DIRECTORY`                                                                  |
| `.changes on|off`        | Show number of rows changed by SQL                                                                           |
| `.check GLOB`            | Fail if output since .testcase does not match                                                                |
| `.columns`               | Column-wise rendering of query results                                                                       |
| `.constant ?COLOR?`      | Sets the syntax highlighting color used for constant values                                                  |
| `.constantcode ?CODE?`   | Sets the syntax highlighting terminal code used for constant values                                          |
| `.databases`             | List names and files of attached databases                                                                   |
| `.echo on|off`           | Turn command echo on or `off`                                                                                |
| `.excel`                 | Display the output of next command in spreadsheet                                                            |
| `.exit ?CODE?`           | Exit this program with return-code `CODE`                                                                    |
| `.explain ?on|off|auto?` | Change the `EXPLAIN` formatting mode.  Default: `auto`                                                       |
| `.fullschema ?--indent?` | Show schema and the content of `sqlite_stat` tables                                                          |
| `.headers on|off`        | Turn display of headers on or `off`                                                                          |
| `.help ?-all? ?PATTERN?` | Show help text for `PATTERN`                                                                                 |
| `.highlight [on|off]`    | Toggle syntax highlighting in the shell `on`/`off`                                                           |
| `.import FILE TABLE`     | Import data from `FILE` into `TABLE`                                                                         |
| `.indexes ?TABLE?`       | Show names of indexes                                                                                        |
| `.keyword ?COLOR?`       | Sets the syntax highlighting color used for keywords                                                         |
| `.keywordcode ?CODE?`    | Sets the syntax highlighting terminal code used for keywords                                                 |
| `.lint OPTIONS`          | Report potential schema issues.                                                                              |
| `.log FILE|off`          | Turn logging on or off.  `FILE` can be `stderr`/`stdout`                                                     |
| `.maxrows COUNT`         | Sets the maximum number of rows for display. Only for [duckbox mode](output-formats)                         |
| `.maxwidth COUNT`        | Sets the maximum width in characters. 0 defaults to terminal width. Only for [duckbox mode](output-formats)  |
| `.mode MODE ?TABLE?`     | Set [output mode](output-formats)                                                                            |
| `.nullvalue STRING`      | Use `STRING` in place of `NULL` values                                                                       |
| `.once ?OPTIONS? ?FILE?` | Output for the next SQL command only to `FILE`                                                               |
| `.open ?OPTIONS? ?FILE?` | Close existing database and reopen `FILE`                                                                    |
| `.output ?FILE?`         | Send output to `FILE` or stdout if `FILE` is omitted                                                         |
| `.parameter CMD ...`     | Manage SQL parameter bindings                                                                                |
| `.print STRING...`       | Print literal `STRING`                                                                                       |
| `.prompt MAIN CONTINUE`  | Replace the standard prompts                                                                                 |
| `.quit`                  | Exit this program                                                                                            |
| `.read FILE`             | Read input from `FILE`                                                                                       |
| `.rows`                  | Row-wise rendering of query results (default)                                                                |
| `.schema ?PATTERN?`      | Show the `CREATE` statements matching `PATTERN`                                                              |
| `.separator COL ?ROW?`   | Change the column and row separators                                                                         |
| `.sha3sum ...`           | Compute a SHA3 hash of database content                                                                      |
| `.shell CMD ARGS...`     | Run `CMD ARGS...` in a system shell                                                                          |
| `.show`                  | Show the current values for various settings                                                                 |
| `.system CMD ARGS...`    | Run `CMD ARGS...` in a system shell                                                                          |
| `.tables ?TABLE?`        | List names of tables [matching LIKE pattern](../../sql/functions/patternmatching) `TABLE`                    |
| `.testcase NAME`         | Begin redirecting output to `NAME`                                                                           |
| `.timer on|off`          | Turn SQL timer on or off                                                                                     |
| `.width NUM1 NUM2 ...`   | Set minimum column widths for columnar output                                                                |

## Using the `.help` Commmand

The `.help` text may be filtered by passing in a text string as the second argument.

```text
.help m
```

```text
.maxrows COUNT           Sets the maximum number of rows for display (default: 40). Only for duckbox mode.
.maxwidth COUNT          Sets the maximum width in characters. 0 defaults to terminal width. Only for duckbox mode.
.mode MODE ?TABLE?       Set output mode
```

### `.output`: Writing Results to a File

By default, the DuckDB CLI sends results to the terminal's standard output. However, this can be modified using either the `.output` or `.once` commands. Pass in the desired output file location as a parameter. The `.once` command will only output the next set of results and then revert to standard out, but `.output` will redirect all subsequent output to that file location. Note that each result will overwrite the entire file at that destination. To revert back to standard output, enter `.output` with no file parameter.

In this example, the output format is changed to `markdown`, the destination is identified as a Markdown file, and then DuckDB will write the output of the SQL statement to that file. Output is then reverted to standard output using `.output` with no parameter.

```sql
.mode markdown
.output my_results.md
SELECT 'taking flight' AS output_column;
.output
SELECT 'back to the terminal' AS displayed_column;
```

The file `my_results.md` will then contain:

```text
| output_column |
|---------------|
| taking flight |
```

The terminal will then display:

```text
|   displayed_column   |
|----------------------|
| back to the terminal |
```

A common output format is CSV, or comma separated values. DuckDB supports [SQL syntax to export data as CSV or Parquet](../../sql/statements/copy#copy-to), but the CLI-specific commands may be used to write a CSV instead if desired.

```sql
.mode csv
.once my_output_file.csv
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

The file `my_output_file.csv` will then contain:

```csv
col_1,col_2
1,2
10,20
```

By passing special options (flags) to the `.once` command, query results can also be sent to a temporary file and automatically opened in the user's default program. Use either the `-e` flag for a text file (opened in the default text editor), or the `-x` flag for a CSV file (opened in the default spreadsheet editor). This is useful for more detailed inspection of query results, especially if there is a relatively large result set. The `.excel` command is equivalent to `.once -x`.

```sql
.once -e
SELECT 'quack' AS hello;
```

The results then open in the default text file editor of the system, for example:

<img src="/images/cli_docs_output_to_text_editor.jpg" alt="cli_docs_output_to_text_editor" title="Output to text editor" style="width:293px;"/>

## Querying the Database Schema

All DuckDB clients support [querying the database schema with SQL](../../sql/information_schema), but the CLI has additional [dot commands](dot_commands) that can make it easier to understand the contents of a database.
The `.tables` command will return a list of tables in the database. It has an optional argument that will filter the results according to a [`LIKE` pattern](../../sql/functions/patternmatching#like).

```sql
CREATE TABLE swimmers AS SELECT 'duck' AS animal;
CREATE TABLE fliers AS SELECT 'duck' AS animal;
CREATE TABLE walkers AS SELECT 'duck' AS animal;
.tables
```

```text
fliers    swimmers  walkers
```

For example, to filter to only tables that contain an "l", use the `LIKE` pattern `%l%`.

```sql
.tables %l%
```

```text
fliers   walkers
```

The `.schema` command will show all of the SQL statements used to define the schema of the database.

```text
.schema
```

```sql
CREATE TABLE fliers (animal VARCHAR);
CREATE TABLE swimmers (animal VARCHAR);
CREATE TABLE walkers (animal VARCHAR);
```

## Configuring the Syntax Highlighter

By default the shell includes support for syntax highlighting.
The CLI's syntax highlighter can be configured using the following commands.

To turn off the highlighter:

```text
.highlight on
```

To turn on the highlighter:

```text
.highlight off
```

To configure the color used to highlight constants:

```text
.constant [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```text
.constantcode [terminal_code]
```

To configure the color used to highlight keywords:

```text
.keyword [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```text
.keywordcode [terminal_code]
```

## Importing Data from CSV

> Deprecated This feature is only included for compatibility reasons and may be removed in the future.
> Use the [`read_csv` function or the `COPY` statement](../../data/csv) to load CSV files.

DuckDB supports [SQL syntax to directly query or import CSV files](../../data/csv), but the CLI-specific commands may be used to import a CSV instead if desired. The `.import` command takes two arguments and also supports several options. The first argument is the path to the CSV file, and the second is the name of the DuckDB table to create. Since DuckDB requires stricter typing than SQLite (upon which the DuckDB CLI is based), the destination table must be created before using the `.import` command. To automatically detect the schema and create a table from a CSV, see the [`read_csv` examples in the import docs](../../data/csv).

In this example, a CSV file is generated by changing to CSV mode and setting an output file location:

```sql
.mode csv
.output import_example.csv
SELECT 1 AS col_1, 2 AS col_2 UNION ALL SELECT 10 AS col1, 20 AS col_2;
```

Now that the CSV has been written, a table can be created with the desired schema and the CSV can be imported. The output is reset to the terminal to avoid continuing to edit the output file specified above. The `--skip N` option is used to ignore the first row of data since it is a header row and the table has already been created with the correct column names.

```sql
.mode csv
.output
CREATE TABLE test_table (col_1 INT, col_2 INT);
.import import_example.csv test_table --skip 1
```

Note that the `.import` command utilizes the current `.mode` and `.separator` settings when identifying the structure of the data to import. The `--csv` option can be used to override that behavior.

```sql
.import import_example.csv test_table --skip 1 --csv
```
