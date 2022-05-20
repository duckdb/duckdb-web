---
layout: docu
title: CLI API
selected: CLI
---
## Installation
The DuckDB CLI (Command Line Interface) is a single, dependency free executable. It is precompiled for Windows, Mac, and Linux. Please see the [installation page](/docs/installation/index) under the CLI tab, or download the version for your environment from the [DuckDB GitHub releases page](https://github.com/duckdb/duckdb/releases/) (in the "Assets" section). For pre-release versions, download the executable file that is produced from GitHub Actions ([Mac](https://github.com/duckdb/duckdb/actions?query=workflow%3AOSX+is%3Asuccess+branch%3Amaster), [Linux](https://github.com/duckdb/duckdb/actions?query=workflow%3ALinuxRelease+is%3Asuccess+branch%3Amaster), or [Windows](https://github.com/duckdb/duckdb/actions?query=workflow%3AWindows+is%3Asuccess+branch%3Amaster++)) or compile DuckDB from source.

The DuckDB CLI is based on the SQLite command line shell, so CLI-client-specific functionality is similar to what is described in the [SQLite documentation](https://www.sqlite.org/cli.html) (although DuckDB's SQL syntax follows PostgreSQL conventions).

## Getting Started
Once the CLI executable has been downloaded, unzip it and save it to any directory. Navigate to that directory in a terminal and enter the command `duckdb` to run the executable. If in a PowerShell environment, use the command `./duckdb` instead. By default, this will open a temporary in-memory database. To open or create a persistent database, simply include a path as a command line argument like `duckdb path/to/my_database.duckdb`. This path can point to an existing database or to a file that does not yet exist and DuckDB will open or create a database at that location as needed. The file may have any arbitrary extension, but `.db` or `.duckdb` are two common choices. You will see a prompt like the below, with a D on the final line.

```command
v0.3.4 662041e2b
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
```

Once the CLI has been opened, enter a SQL statement followed by a semicolon, then hit enter and it will be executed. Results will be displayed in a table in the terminal. If a semicolon is omitted, hitting enter will allow for multi-line SQL statements to be entered. 

```sql
D SELECT 'quack' AS my_column;
```

| my_column |
|-----------|
| quack     |

```sql
D SELECT
>     'nicely formatted quack' AS my_column,
>     'excited quacking' AS another_column;
```

|       my_column        |  another_column  |
|------------------------|------------------|
| nicely formatted quack | excited quacking |

The CLI supports all of DuckDB's rich SQL syntax including `SELECT`, `CREATE`, and `ALTER` statements, etc. 

To exit the CLI, press Ctrl-C. If using a persistent database, it will automatically checkpoint (save the latest edits to disk) and close. This will remove the .WAL file (the Write-Ahead-Log) and consolidate all of your data into the single file database.

## Special Commands (Dot Commands)
In addition to SQL syntax, special dot commands may be entered that are specific to the CLI client. To use one of these commands, begin the line with a period (`.`) immediately followed by the name of the command you wish to execute. Additional arguments to the command are entered, space separated, after the command. If an argument must contain a space, either single or double quotes may be used to wrap that parameter. Dot commands must be entered on a single line, and no whitespace may occur before the period. No semicolon is required at the end of the line. To see available commands, use the `.help` command:

```command
D .help
```
```command
.auth ON|OFF             Show authorizer callbacks
.backup ?DB? FILE        Backup DB (default "main") to FILE
.bail on|off             Stop after hitting an error.  Default OFF
.binary on|off           Turn binary output on or off.  Default OFF
.cd DIRECTORY            Change the working directory to DIRECTORY
.changes on|off          Show number of rows changed by SQL
.check GLOB              Fail if output since .testcase does not match
.clone NEWDB             Clone data into NEWDB from the existing database
.databases               List names and files of attached databases
.dbconfig ?op? ?val?     List or change sqlite3_db_config() options
.dbinfo ?DB?             Show status information about the database
.dump ?TABLE?            Render database content as SQL
.echo on|off             Turn command echo on or off
.eqp on|off|full|...     Enable or disable automatic EXPLAIN QUERY PLAN
.excel                   Display the output of next command in spreadsheet
.exit ?CODE?             Exit this program with return-code CODE
.expert                  EXPERIMENTAL. Suggest indexes for queries
.explain ?on|off|auto?   Change the EXPLAIN formatting mode.  Default: auto
.filectrl CMD ...        Run various sqlite3_file_control() operations
.fullschema ?--indent?   Show schema and the content of sqlite_stat tables
.headers on|off          Turn display of headers on or off
.help ?-all? ?PATTERN?   Show help text for PATTERN
.import FILE TABLE       Import data from FILE into TABLE
.imposter INDEX TABLE    Create imposter table TABLE on index INDEX
.indexes ?TABLE?         Show names of indexes
.limit ?LIMIT? ?VAL?     Display or change the value of an SQLITE_LIMIT
.lint OPTIONS            Report potential schema issues.
.log FILE|off            Turn logging on or off.  FILE can be stderr/stdout
.mode MODE ?TABLE?       Set output mode
.nullvalue STRING        Use STRING in place of NULL values
.once ?OPTIONS? ?FILE?   Output for the next SQL command only to FILE
.open ?OPTIONS? ?FILE?   Close existing database and reopen FILE
.output ?FILE?           Send output to FILE or stdout if FILE is omitted
.parameter CMD ...       Manage SQL parameter bindings
.print STRING...         Print literal STRING
.progress N              Invoke progress handler after every N opcodes
.prompt MAIN CONTINUE    Replace the standard prompts
.quit                    Exit this program
.read FILE               Read input from FILE
.restore ?DB? FILE       Restore content of DB (default "main") from FILE
.save FILE               Write in-memory database into FILE
.scanstats on|off        Turn sqlite3_stmt_scanstatus() metrics on or off
.schema ?PATTERN?        Show the CREATE statements matching PATTERN
.selftest ?OPTIONS?      Run tests defined in the SELFTEST table
.separator COL ?ROW?     Change the column and row separators
.sha3sum ...             Compute a SHA3 hash of database content
.shell CMD ARGS...       Run CMD ARGS... in a system shell
.show                    Show the current values for various settings
.stats ?on|off?          Show stats or turn stats on or off
.system CMD ARGS...      Run CMD ARGS... in a system shell
.tables ?TABLE?          List names of tables matching LIKE pattern TABLE
.testcase NAME           Begin redirecting output to 'testcase-out.txt'
.testctrl CMD ...        Run various sqlite3_test_control() operations
.timeout MS              Try opening locked tables for MS milliseconds
.timer on|off            Turn SQL timer on or off
.trace ?OPTIONS?         Output each SQL statement as it is run
.vfsinfo ?AUX?           Information about the top-level VFS
.vfslist                 List all available VFSes
.vfsname ?AUX?           Print the name of the VFS stack
.width NUM1 NUM2 ...     Set minimum column widths for columnar output
```

Note that the above list of methods is extensive, and DuckDB supports only a subset of the commands that are displayed. Please file a [GitHub issue](https://github.com/duckdb/duckdb/issues) if a command that is central to your workflow is not yet supported.

As an example of passing an argument to a dot command, the `.help` text may be filtered by passing in a text string as the second argument.

```command
D .help sh
```
```command
.sha3sum ...             Compute a SHA3 hash of database content
.shell CMD ARGS...       Run CMD ARGS... in a system shell
.show                    Show the current values for various settings
```

## Output Formats
The `.mode` command may be used to change the appearance of the tables returned in the terminal output. In addition to customizing the appearance, these modes have additional benefits. This can be useful for presenting DuckDB output elsewhere by redirecting the terminal output to a file, for example (see "Writing Results to a File" section below). Using the `insert` mode will build a series of SQL statements that can be used to insert the data at a later point. The `markdown` mode is particularly useful for building documentation!
* ascii
* box
* csv
* column
* html
* insert
* json
* line
* list
* markdown
* quote
* table
* tabs
* tcl

```sql
D .mode markdown
D SELECT 'quacking intensifies' AS incoming_ducks;
```
```
|    incoming_ducks    |
|----------------------|
| quacking intensifies |
```

The output appearance can also be adjusted with the `.separator` command. If using an export mode that relies on a separator (`csv` or `tabs` for example), the separator will be reset when the mode is changed. For example, `.mode csv` will set the separator to a comma (`,`). Using `.separator "|"` will then convert the output to be pipe separated.
```sql
D .mode csv
D SELECT 1 AS col_1, 2 AS col_2
> UNION ALL
> SELECT 10 AS col1, 20 AS col_2;
```
```
col_1,col_2
1,2
10,20
```
```sql
D .separator "|"
D SELECT 1 AS col_1, 2 AS col_2
> UNION ALL
> SELECT 10 AS col1, 20 AS col_2;
```
```
col_1|col_2
1|2
10|20
```

## Querying the Database Schema
All DuckDB clients support [querying the database schema with SQL](/docs/sql/information_schema), but the CLI has additional dot commands that can make it easier to understand the contents of a database.
The `.tables` command will return a list of tables in the database. It has an optional argument that will filter the results according to a [`LIKE` pattern](/docs/sql/functions/patternmatching#like).

```sql
D CREATE TABLE swimmers AS SELECT 'duck' as animal;
D CREATE TABLE fliers AS SELECT 'duck' as animal;
D CREATE TABLE walkers AS SELECT 'duck' as animal;
D .tables
```
```command
fliers    swimmers  walkers
```

For example, to filter to only tables that contain an "l", use the `LIKE` pattern `%l%`.
```sql
D .tables %l%
```
```command
fliers   walkers
```

The `.schema` command will show all of the SQL statements used to define the schema of the database. 

```command
D .schema
```
```command
CREATE TABLE fliers(animal VARCHAR);;
CREATE TABLE swimmers(animal VARCHAR);;
CREATE TABLE walkers(animal VARCHAR);;
```

## Opening Database Files
In addition to connecting to a database when opening the CLI, a new database connection can be made by using the `.open` command. If no additional parameters are supplied, a new in-memory database connection is created. This database will not be persisted when the CLI connection is closed. 

```command
D .open
```

The `.open` command optionally accepts several options, but the final parameter can be used to indicate a path to a persistent database (or where one should be created). The special string `:memory:` can also be used to open a temporary in-memory database.

```command
D .open persistent.duckdb
```

One important parameter accepted by `.open` is the `--readonly` flag. This disallows any editing of the database. To open in read only mode, the database must already exist. This also means that a new in-memory database can't be opened in read only mode since in-memory databases are created upon connection.

```command
D .open --readonly preexisting.duckdb
```

## Writing Results to a File

By default, the DuckDB CLI sends results to standard output. However, this can be modified using either the `.output` or `.once` commands. The only parameter to these commands is the desired output file location. The `.once` command will only output the next set of results and then revert to standard out, but `.output` will redirect all subsequent output to that file location. Note that each result will overwrite the entire file at that destination. To revert back to standard output, enter `.output` with no file parameter.

In this example, the output format is changed to markdown, the destination is identified as a markdown file, and then DuckDB will write the output of the SQL statement to that file. Output is then reverted to standard output.
```sql
D .mode markdown
D .output my_results.md
D SELECT 'taking flight' AS output_column;
D .output
D SELECT 'back to the terminal' as displayed_column;
```
```command
|   displayed_column   |
|----------------------|
| back to the terminal |
```

TODO: Document -e and -x


Output can also be sent to a temporary .csv file and automatically displayed in the user's default spreadsheet program using the `.excel` command.  