---
layout: docu
title: Dot Commands
---

Dot commands are available in the DuckDB CLI client. To use one of these commands, begin the line with a period (`.`) immediately followed by the name of the command you wish to execute. Additional arguments to the command are entered, space separated, after the command. If an argument must contain a space, either single or double quotes may be used to wrap that parameter. Dot commands must be entered on a single line, and no whitespace may occur before the period. No semicolon is required at the end of the line. To see available commands, use the `.help` command.

## List of Dot Commands

<!-- markdownlint-disable MD056 -->

| Command                                                               | Description                                                                                                                                                                 |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.bail ⟨on/off⟩`{:.language-sql .highlight}                           | Stop after hitting an error. Default: `off`                                                                                                                                 |
| `.binary ⟨on/off⟩`{:.language-sql .highlight}                         | Turn binary output `on` or `off`. Default: `off`                                                                                                                            |
| `.cd ⟨DIRECTORY⟩`{:.language-sql .highlight}                          | Change the working directory to `DIRECTORY`                                                                                                                                 |
| `.changes ⟨on/off⟩`{:.language-sql .highlight}                        | Show number of rows changed by SQL                                                                                                                                          |
| `.columns`{:.language-sql .highlight}                                 | Column-wise rendering of query results                                                                                                                                      |
| `.constant ⟨COLOR⟩`{:.language-sql .highlight}                        | Sets the syntax highlighting color used for constant values                                                                                                                 |
| `.constantcode ⟨CODE⟩`{:.language-sql .highlight}                     | Sets the syntax highlighting terminal code used for constant values                                                                                                         |
| `.databases`{:.language-sql .highlight}                               | List names and files of attached databases                                                                                                                                  |
| `.echo ⟨on/off⟩`{:.language-sql .highlight}                           | Turn command echo `on` or `off`                                                                                                                                             |
| `.exit ⟨CODE⟩`{:.language-sql .highlight}                             | Exit this program with return-code `CODE`                                                                                                                                   |
| `.headers ⟨on/off⟩`{:.language-sql .highlight}                        | Turn display of headers `on` or `off`. Does not apply to duckbox mode                                                                                                       |
| `.help ⟨-all⟩ ⟨PATTERN⟩`{:.language-sql .highlight}                   | Show help text for `PATTERN`                                                                                                                                                |
| `.highlight ⟨on/off⟩`{:.language-sql .highlight}                      | Toggle syntax highlighting in the shell `on` / `off`. See the [query syntax highlighting section](#configuring-the-query-syntax-highlighter) for more details               |
| `.highlight_colors ⟨COMPONENT⟩ ⟨COLOR⟩`{:.language-sql .highlight}    | Configure the color of each component in (duckbox only). See the [result syntax highlighting section](#configuring-the-query-syntax-highlighter) for more details           |
| `.highlight_results ⟨on/off⟩`{:.language-sql .highlight}              | Toggle highlighting in result tables `on` / `off` (duckbox only). See the [result syntax highlighting section](#configuring-the-query-syntax-highlighter) for more details |
| `.import ⟨FILE⟩ ⟨TABLE⟩`{:.language-sql .highlight}                   | Import data from `FILE` into `TABLE`                                                                                                                                        |
| `.indexes ⟨TABLE⟩`{:.language-sql .highlight}                         | Show names of indexes                                                                                                                                                       |
| `.keyword ⟨COLOR⟩`{:.language-sql .highlight}                         | Sets the syntax highlighting color used for keywords                                                                                                                        |
| `.keywordcode ⟨CODE⟩`{:.language-sql .highlight}                      | Sets the syntax highlighting terminal code used for keywords                                                                                                                |
| `.large_number_rendering ⟨all/footer/off⟩`{:.language-sql .highlight} | Toggle readable rendering of large numbers (duckbox only, default: `footer`)                                                                                                |
| `.log ⟨FILE/off⟩`{:.language-sql .highlight}                          | Turn logging `on` or `off`. `FILE` can be `stderr` / `stdout`                                                                                                               |
| `.maxrows ⟨COUNT⟩`{:.language-sql .highlight}                         | Sets the maximum number of rows for display. Only for [duckbox mode]({% link docs/preview/clients/cli/output_formats.md %})                                                 |
| `.maxwidth ⟨COUNT⟩`{:.language-sql .highlight}                        | Sets the maximum width in characters. 0 defaults to terminal width. Only for [duckbox mode]({% link docs/preview/clients/cli/output_formats.md %})                          |
| `.mode ⟨MODE⟩ ⟨TABLE⟩`{:.language-sql .highlight}                     | Set [output mode]({% link docs/preview/clients/cli/output_formats.md %})                                                                                                    |
| `.multiline`{:.language-sql .highlight}                               | Set multi-line mode (default)                                                                                                                                               |
| `.nullvalue ⟨STRING⟩`{:.language-sql .highlight}                      | Use `STRING` in place of `NULL` values. Default: `NULL`                                                                                                                     |
| `.once ⟨OPTIONS⟩ ⟨FILE⟩`{:.language-sql .highlight}                   | Output for the next SQL command only to `FILE`                                                                                                                              |
| `.open ⟨OPTIONS⟩ ⟨FILE⟩`{:.language-sql .highlight}                   | Close existing database and reopen `FILE`                                                                                                                                   |
| `.output ⟨FILE⟩`{:.language-sql .highlight}                           | Send output to `FILE` or `stdout` if `FILE` is omitted                                                                                                                      |
| `.print ⟨STRING...⟩`{:.language-sql .highlight}                       | Print literal `STRING`                                                                                                                                                      |
| `.progress_bar ⟨COMPONENT⟩ `{:.language-sql .highlight}                | Set the progress bar component styles                                                                                                                                        |
| `.prompt ⟨OPTIONS⟩ ⟨CONTINUE⟩`{:.language-sql .highlight}                | Replace the standard prompts                                                                                                                                                |
| `.quit`{:.language-sql .highlight}                                    | Exit this program                                                                                                                                                           |
| `.read ⟨FILE⟩`{:.language-sql .highlight}                             | Read input from `FILE`                                                                                                                                                      |
| `.rows`{:.language-sql .highlight}                                    | Row-wise rendering of query results (default)                                                                                                                               |
| `.safe_mode`{:.language-sql .highlight}                               | Activates [safe mode]({% link docs/preview/clients/cli/safe_mode.md %})                                                                                                     |
| `.schema ⟨PATTERN⟩`{:.language-sql .highlight}                        | Show the `CREATE` statements matching `PATTERN`                                                                                                                             |
| `.separator ⟨COL⟩ ⟨ROW⟩`{:.language-sql .highlight}                   | Change the column and row separators                                                                                                                                        |
| `.shell ⟨CMD⟩ ⟨ARGS...⟩`{:.language-sql .highlight}                   | Run `CMD` with `ARGS...` in a system shell                                                                                                                                  |
| `.show`{:.language-sql .highlight}                                    | Show the current values for various settings                                                                                                                                |
| `.singleline`{:.language-sql .highlight}                              | Set single-line mode                                                                                                                                                        |
| `.system ⟨CMD⟩ ⟨ARGS...⟩`{:.language-sql .highlight}                  | Run `CMD` with `ARGS...` in a system shell                                                                                                                                  |
| `.tables ⟨TABLE⟩`{:.language-sql .highlight}                          | List names of tables [matching `LIKE` pattern]({% link docs/preview/sql/functions/pattern_matching.md %}) `TABLE`                                                           |
| `.timer ⟨on/off⟩`{:.language-sql .highlight}                          | Turn SQL timer `on` or `off`. SQL statements separated by `;` but _not_ separated via newline are measured together                                                         |
| `.width ⟨NUM1⟩ ⟨NUM2⟩ ...`{:.language-sql .highlight}                 | Set minimum column widths for columnar output                                                                                                                               |

## Using the `.help` Command

The `.help` text may be filtered by passing in a text string as the first argument.

```sql
.help m
```

```sql
.maxrows COUNT           Sets the maximum number of rows for display (default: 40). Only for duckbox mode.
.maxwidth COUNT          Sets the maximum width in characters. 0 defaults to terminal width. Only for duckbox mode.
.mode MODE ?TABLE?       Set output mode
```

## `.output`: Writing Results to a File

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

A common output format is CSV, or comma separated values. DuckDB supports [SQL syntax to export data as CSV or Parquet]({% link docs/preview/sql/statements/copy.md %}#copy-to), but the CLI-specific commands may be used to write a CSV instead if desired.

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

> Tip macOS users can copy the results to their clipboards using [`pbcopy`](https://ss64.com/mac/pbcopy.html) by using `.once` to output to `pbcopy` via a pipe: `.once |pbcopy`
>
> Combining this with the `.headers off` and `.mode lines` options can be particularly effective.

## Querying the Database Schema

All DuckDB clients support [querying the database schema with SQL]({% link docs/preview/sql/meta/information_schema.md %}), but the CLI has additional [dot commands]({% link docs/preview/clients/cli/dot_commands.md %}) that can make it easier to understand the contents of a database.
The `.tables` command will return a list of tables in the database. It has an optional argument that will filter the results according to a [`LIKE` pattern]({% link docs/preview/sql/functions/pattern_matching.md %}#like).

```sql
CREATE TABLE swimmers AS SELECT 'duck' AS animal;
CREATE TABLE fliers AS SELECT 'duck' AS animal;
CREATE TABLE walkers AS SELECT 'duck' AS animal;
.tables
```

```sql
fliers    swimmers  walkers
```

For example, to filter to only tables that contain an `l`, use the `LIKE` pattern `%l%`.

```sql
.tables %l%
```

```sql
fliers   walkers
```

The `.schema` command will show all of the SQL statements used to define the schema of the database.

```sql
.schema
```

```sql
CREATE TABLE fliers (animal VARCHAR);
CREATE TABLE swimmers (animal VARCHAR);
CREATE TABLE walkers (animal VARCHAR);
```

## Progress Bar

The DuckDB CLI client's progress bar supports customization through components.

The `.progress_bar` command supports `--add` and `--clear` parameters for adding and removing components. 

For details on specific usage, see the examples below.

### Configuring the Progress Bar Display

To check if the progress bar is enabled: 

```sql
SELECT * FROM duckdb_settings() WHERE name = 'enable_progress_bar';
```

To check the current minimum amount of time (in milliseconds) a query needs to take before displaying a progress bar: 

```sql
SELECT * FROM duckdb_settings() WHERE name = 'progress_bar_time';
```

To set the minimum amount of time that the progress bar displays to 100 milliseconds:

```sql
SET progress_bar_time = 100;
```

To set that progress bar component to a red text that displays the current time on the progress bar:

```sql
.progress_bar --add "{align:right}{min_size:20}{color:red}Time: {sql:select (current_time::varchar).split('.')[1]}{color:reset} "
```

<img src="{% link images/progress_bar/duckdb_progressbar_time.gif %}"
     alt="DuckDB progress bar with current time stamp"
     width="400"
     />


> `.progress_bar --add` commands are additive, issuing multiple `--add` calls will stack additional components on the progress bar.

To set that progress bar component to a blue text that displays the file cache RAM usage on the progress bar:

```sql
.progress_bar --add "{align:right}{min_size:20}{color:blue}External Cache Usage: {sql:select format_bytes(memory_usage_bytes) from duckdb_memory() where tag='EXTERNAL_FILE_CACHE'}{color:reset};
```

<img src="{% link images/progress_bar/duckdb_progressbar_cache_usage.gif %}"
     alt="DuckDB progress bar with cache usage"
     width="400"
     />

To reset all existing progress bar components:

```sql
.progress_bar --clear
```

## Syntax Highlighters

The DuckDB CLI client has a syntax highlighter for the SQL queries and another for the duckbox-formatted result tables.

### Configuring the Query Syntax Highlighter

By default the shell includes support for syntax highlighting.
The CLI's syntax highlighter can be configured using the following commands.

To turn off the highlighter:

```sql
.highlight off
```

To turn on the highlighter:

```sql
.highlight on
```

To configure the color used to highlight constants:

```sql
.constant [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```sql
.constantcode ⟨terminal_code⟩
```

For example:

```sql
.constantcode 033[31m
```

To configure the color used to highlight keywords:

```sql
.keyword [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```sql
.keywordcode ⟨terminal_code⟩
```

For example:

```sql
.keywordcode 033[31m
```

### Configuring the Result Syntax Highlighter

By default, the result highlighting makes a few small modifications:

* Bold column names.
* `NULL` values are greyed out.
* Layout elements are grayed out.

The highlighting of each of the components can be customized using the `.highlight_colors` command.
For example:

```sql
.highlight_colors layout red
.highlight_colors column_type yellow
.highlight_colors column_name yellow bold_underline
.highlight_colors numeric_value cyan underline
.highlight_colors temporal_value red bold
.highlight_colors string_value green bold
.highlight_colors footer gray
```

The result highlighting can be disabled using `.highlight_results off`.

## Shorthands

DuckDB's CLI allows using shorthands for dot commands.
Once a sequence of characters can be unambiguously completed to a dot command or an argument, the CLI (silently) autocompletes them.
For example:

```sql
.mo ma
```

Is equivalent to:

```sql
.mode markdown
```

> Tip Avoid using shorthands in SQL scripts to improve readability and ensure that the scripts are future-proof.

## Importing Data from CSV

> Deprecated This feature is only included for compatibility reasons and may be removed in the future.
> Use the [`read_csv` function or the `COPY` statement]({% link docs/preview/data/csv/overview.md %}) to load CSV files.

DuckDB supports [SQL syntax to directly query or import CSV files]({% link docs/preview/data/csv/overview.md %}), but the CLI-specific commands may be used to import a CSV instead if desired. The `.import` command takes two arguments and also supports several options. The first argument is the path to the CSV file, and the second is the name of the DuckDB table to create. Since DuckDB requires stricter typing than SQLite (upon which the DuckDB CLI is based), the destination table must be created before using the `.import` command. To automatically detect the schema and create a table from a CSV, see the [`read_csv` examples in the import docs]({% link docs/preview/data/csv/overview.md %}).

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
CREATE TABLE test_table (col_1 INTEGER, col_2 INTEGER);
.import import_example.csv test_table --skip 1
```

Note that the `.import` command utilizes the current `.mode` and `.separator` settings when identifying the structure of the data to import. The `--csv` option can be used to override that behavior.

```sql
.import import_example.csv test_table --skip 1 --csv
```
