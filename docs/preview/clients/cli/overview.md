---
layout: docu
title: Command Line Client
---

> Tip To use the DuckDB CLI client, visit the [CLI installation page]({% link install/index.html %}?environment=cli).
>
> The latest stable version of the DuckDB command line client is {{ site.current_duckdb_version }}.

## Installation

The DuckDB CLI (Command Line Interface) is a single, dependency-free executable. It is precompiled for Windows, Mac and Linux for both the stable version and for nightly builds produced by GitHub Actions. Please see the [installation page]({% link install/index.html %}) under the CLI tab for download links.

The DuckDB CLI is based on the SQLite command line shell, so CLI-client-specific functionality is similar to what is described in the [SQLite documentation](https://www.sqlite.org/cli.html) (although DuckDB's SQL syntax follows PostgreSQL conventions with a [few exceptions]({% link docs/preview/sql/dialect/postgresql_compatibility.md %})).

> DuckDB has a [tldr page](https://tldr.inbrowser.app/pages/common/duckdb), which summarizes the most common uses of the CLI client.
> If you have [tldr](https://github.com/tldr-pages/tldr) installed, you can display it by running `tldr duckdb`.

## Getting Started

Once the CLI executable has been downloaded, unzip it and save it to any directory.
Navigate to that directory in a terminal and enter the command `duckdb` to run the executable.
If in a PowerShell or POSIX shell environment, use the command `./duckdb` instead.

## Usage

The typical usage of the `duckdb` command is the following:

```batch
duckdb ⟨OPTIONS⟩ ⟨FILENAME⟩
```

### Options

The `⟨OPTIONS⟩`{:.language-sql .highlight} part encodes [arguments for the CLI client]({% link docs/preview/clients/cli/arguments.md %}). Common options include:

* `-csv`: sets the output mode to CSV
* `-json`: sets the output mode to JSON
* `-readonly`: open the database in read-only mode (see [concurrency in DuckDB]({% link docs/preview/connect/concurrency.md %}#handling-concurrency))

For a full list of options, see the [command line arguments page]({% link docs/preview/clients/cli/arguments.md %}).

### In-Memory vs. Persistent Database

When no `⟨FILENAME⟩`{:.language-sql .highlight} argument is provided, the DuckDB CLI will open a temporary [in-memory database]({% link docs/preview/connect/overview.md %}#in-memory-database).
You will see DuckDB's version number, the information on the connection and a prompt starting with a `D`.

```batch
duckdb
```

```text
DuckDB v{{ site.current_duckdb_version }} ({{ site.current_duckdb_codename }}) {{ site.current_duckdb_hash }}
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
```

To open or create a [persistent database]({% link docs/preview/connect/overview.md %}#persistent-database), simply include a path as a command line argument:

```batch
duckdb my_database.duckdb
```

### Running SQL Statements in the CLI

Once the CLI has been opened, enter a SQL statement followed by a semicolon, then hit enter and it will be executed. Results will be displayed in a table in the terminal. If a semicolon is omitted, hitting enter will allow for multi-line SQL statements to be entered.

```sql
SELECT 'quack' AS my_column;
```

| my_column |
|-----------|
| quack     |

The CLI supports all of DuckDB's rich [SQL syntax]({% link docs/preview/sql/introduction.md %}) including `SELECT`, `CREATE` and `ALTER` statements.

### Editor Features

The CLI supports [autocompletion]({% link docs/preview/clients/cli/autocomplete.md %}), and has sophisticated [editor features]({% link docs/preview/clients/cli/editing.md %}) and [syntax highlighting]({% link docs/preview/clients/cli/syntax_highlighting.md %}) on certain platforms.

### Exiting the CLI

To exit the CLI, press `Ctrl`+`D` if your platform supports it. Otherwise, press `Ctrl`+`C` or use the `.exit` command. If you used a persistent database, DuckDB will automatically checkpoint (save the latest edits to disk) and close. This will remove the `.wal` file (the [write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging)) and consolidate all of your data into the single-file database.

### Dot Commands

In addition to SQL syntax, special [dot commands]({% link docs/preview/clients/cli/dot_commands.md %}) may be entered into the CLI client. To use one of these commands, begin the line with a period (`.`) immediately followed by the name of the command you wish to execute. Additional arguments to the command are entered, space separated, after the command. If an argument must contain a space, either single or double quotes may be used to wrap that parameter. Dot commands must be entered on a single line, and no whitespace may occur before the period. No semicolon is required at the end of the line.

Frequently-used configurations can be stored in the file `~/.duckdbrc`, which will be loaded when starting the CLI client. See the [Configuring the CLI](#configuring-the-cli) section below for further information on these options.

> Tip To prevent the DuckDB CLI client from reading the `~/.duckdbrc` file, start it as follows:
> ```batch
> duckdb -init /dev/null
> ```

Below, we summarize a few important dot commands. To see all available commands, see the [dot commands page]({% link docs/preview/clients/cli/dot_commands.md %}) or use the `.help` command.

#### Opening Database Files

In addition to connecting to a database when opening the CLI, a new database connection can be made by using the `.open` command. If no additional parameters are supplied, a new in-memory database connection is created. This database will not be persisted when the CLI connection is closed.

```text
.open
```

The `.open` command optionally accepts several options, but the final parameter can be used to indicate a path to a persistent database (or where one should be created). The special string `:memory:` can also be used to open a temporary in-memory database.

```text
.open persistent.duckdb
```

> Warning `.open` closes the current database.
> To keep the current database, while adding a new database, use the [`ATTACH` statement]({% link docs/preview/sql/statements/attach.md %}).

One important option accepted by `.open` is the `--readonly` flag. This disallows any editing of the database. To open in read only mode, the database must already exist. This also means that a new in-memory database can't be opened in read only mode since in-memory databases are created upon connection.

```text
.open --readonly preexisting.duckdb
```

#### Output Formats

The `.mode` [dot command]({% link docs/preview/clients/cli/dot_commands.md %}#mode) may be used to change the appearance of the tables returned in the terminal output.
These include the default `duckbox` mode, `csv` and `json` mode for ingestion by other tools, `markdown` and `latex` for documents and `insert` mode for generating SQL statements.

#### Writing Results to a File

By default, the DuckDB CLI sends results to the terminal's standard output. However, this can be modified using either the `.output` or `.once` commands.
For details, see the documentation for the [output dot command]({% link docs/preview/clients/cli/dot_commands.md %}#output-writing-results-to-a-file).

#### Reading SQL from a File

The DuckDB CLI can read both SQL commands and dot commands from an external file instead of the terminal using the `.read` command. This allows for a number of commands to be run in sequence and allows command sequences to be saved and reused.

The `.read` command requires only one argument: the path to the file containing the SQL and/or commands to execute. After running the commands in the file, control will revert back to the terminal. Output from the execution of that file is governed by the same `.output` and `.once` commands that have been discussed previously. This allows the output to be displayed back to the terminal, as in the first example below, or out to another file, as in the second example.

In this example, the file `select_example.sql` is located in the same directory as duckdb.exe and contains the following SQL statement:

```sql
SELECT *
FROM generate_series(5);
```

To execute it from the CLI, the `.read` command is used.

```text
.read select_example.sql
```

The output below is returned to the terminal by default. The formatting of the table can be adjusted using the `.output` or `.once` commands.

```text
| generate_series |
|----------------:|
| 0               |
| 1               |
| 2               |
| 3               |
| 4               |
| 5               |
```

Multiple commands, including both SQL and dot commands, can also be run in a single `.read` command. In this example, the file `write_markdown_to_file.sql` is located in the same directory as duckdb.exe and contains the following commands:

```sql
.mode markdown
.output series.md
SELECT *
FROM generate_series(5);
```

To execute it from the CLI, the `.read` command is used as before.

```text
.read write_markdown_to_file.sql
```

In this case, no output is returned to the terminal. Instead, the file `series.md` is created (or replaced if it already existed) with the markdown-formatted results shown here:

```text
| generate_series |
|----------------:|
| 0               |
| 1               |
| 2               |
| 3               |
| 4               |
| 5               |
```

<!-- The edit function does not appear to work -->

## Configuring the CLI

Several dot commands can be used to configure the CLI.
On startup, the CLI reads and executes all commands in the file `~/.duckdbrc`, including dot commands and SQL statements.
This allows you to store the configuration state of the CLI.
You may also point to a different initialization file using the `-init` flag.

### Setting a Custom Prompt

As an example, a file in the same directory as the DuckDB CLI named `prompt.sql` will change the DuckDB prompt to be a duck head and run a SQL statement.
Note that the duck head is built with Unicode characters and does not work in all terminal environments (e.g., in Windows, unless running with WSL and using the Windows Terminal).

```text
.prompt "{color:yellow1}{sql:select current_database()} ⚫◗ "
```

Or a simpler version without colours:
```sql
.prompt "{sql:select current_database()} ⚫◗ "
```


To invoke that file on initialization, use this command:

```batch
duckdb -init prompt.sql
```

This outputs:

```text
-- Loading resources from prompt.sql
v⟨version⟩ ⟨git_hash⟩
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
⚫◗
```

## Non-Interactive Usage

To read/process a file and exit immediately, redirect the file contents in to `duckdb`:

```batch
duckdb < select_example.sql
```

To execute a command with SQL text passed in directly from the command line, call `duckdb` with two arguments: the database location (or `:memory:`), and a string with the SQL statement to execute.

```batch
duckdb :memory: "SELECT 42 AS the_answer"
```

## Loading Extensions

To load extensions, use DuckDB's SQL `INSTALL` and `LOAD` commands as you would other SQL statements.

```sql
INSTALL fts;
LOAD fts;
```

For details, see the [Extension docs]({% link docs/preview/extensions/overview.md %}).

## Reading from stdin and Writing to stdout

When in a Unix environment, it can be useful to pipe data between multiple commands.
DuckDB is able to read data from stdin as well as write to stdout using the file location of stdin (`/dev/stdin`) and stdout (`/dev/stdout`) within SQL commands, as pipes act very similarly to file handles.

This command will create an example CSV:

```sql
COPY (SELECT 42 AS woot UNION ALL SELECT 43 AS woot) TO 'test.csv' (HEADER);
```

First, read a file and pipe it to the `duckdb` CLI executable. As arguments to the DuckDB CLI, pass in the location of the database to open, in this case, an in-memory database, and a SQL command that utilizes `/dev/stdin` as a file location.

```batch
cat test.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

| woot |
|-----:|
| 42   |
| 43   |

To write back to stdout, the copy command can be used with the `/dev/stdout` file location.

```batch
cat test.csv | \
    duckdb -c "COPY (SELECT * FROM read_csv('/dev/stdin')) TO '/dev/stdout' WITH (FORMAT csv, HEADER)"
```

```csv
woot
42
43
```

## Reading Environment Variables

The `getenv` function can read environment variables.

### Examples

To retrieve the home directory's path from the `HOME` environment variable, use:

```sql
SELECT getenv('HOME') AS home;
```

|       home       |
|------------------|
| /Users/user_name |

The output of the `getenv` function can be used to set [configuration options]({% link docs/preview/configuration/overview.md %}). For example, to set the `NULL` order based on the environment variable `DEFAULT_NULL_ORDER`, use:

```sql
SET default_null_order = getenv('DEFAULT_NULL_ORDER');
```

### Restrictions for Reading Environment Variables

The `getenv` function can only be run when the [`enable_external_access`]({% link docs/preview/configuration/overview.md %}#configuration-reference) option is set to `true` (the default setting).
It is only available in the CLI client and is not supported in other DuckDB clients.

## Prepared Statements

The DuckDB CLI supports executing [prepared statements]({% link docs/preview/sql/query_syntax/prepared_statements.md %}) in addition to regular `SELECT` statements.
To create and execute a prepared statement in the CLI client, use the `PREPARE` clause and the `EXECUTE` statement.

## Query Completion ETA

DuckDB's CLI now provides intelligent time-to-completion estimates for running queries and displays total execution time upon completion.

When executing queries in the DuckDB CLI, the progress bar displays an estimated time remaining until completion. This feature employs advanced statistical modeling ([Kalman filtering](https://en.wikipedia.org/wiki/Kalman_filter)) to deliver more accurate predictions than simple linear extrapolation.

### How It Works

DuckDB calculates the estimated time to completion through the following process:

1. Progress Monitoring: DuckDB's internal progress API reports the estimated completion percentage for the running query
2. Statistical Filtering: A Kalman filter smooths noisy progress measurements and accounts for execution variability
3. Continuous Refinement: The system continuously updates predicted completion time as new progress data becomes available, improving accuracy throughout execution

The Kalman filter adapts to changing execution conditions such as memory pressure, I/O bottlenecks, or network delays. This adaptive approach means estimated completion times may not always decrease linearly—estimates can increase when query execution becomes less predictable.

### Factors Affecting The Accuracy of Query Completion ETA

Completion time estimates may be less reliable under these conditions:

System resource constraints:

* Memory pressure causing disk swapping
* High CPU load from competing processes
* Disk I/O bottlenecks

Query execution characteristics:

* Variable execution phases (initial setup versus main processing)
* Network-dependent operations with inconsistent latency
* Queries with unpredictable branching logic
* Operations on remote data sources
* External function calls
* Highly skewed data distributions
