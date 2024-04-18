---
layout: docu
title: ODBC API on macOS
---

1. A driver manager is required to manage communication between applications and the ODBC driver. DuckDB supports `unixODBC`, which is is a complete ODBC driver manager for macOS and Linux. Users can install it from the command line via [Homebrew](https://brew.sh/):

   ```bash
   brew install unixodbc
   ```

<!-- markdownlint-disable MD034 -->

2. DuckDB releases a universal [ODBC driver for macOS](https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-osx-universal.zip) (supporting both Intel and Apple Silicon CPUs). To download it, run:

   ```bash
   wget https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-osx-universal.zip
   ```

<!-- markdownlint-enable MD034 -->

3. The archive contains the `libduckdb_odbc.dylib` artifact. To extract it to a directory, run:

   ```bash
   mkdir duckdb_odbc
   unzip duckdb_odbc-osx-universal.zip -d duckdb_odbc
   ```

4. There are two ways to configure the ODBC driver, either by initializing via the configuration files, or by connecting with [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16).
   A combination of the two is also possible.

   Furthermore, the ODBC driver supports all the [configuration options](../../configuration/overview) included in DuckDB.

   > If a configuration is set in both the connection string passed to `SQLDriverConnect` and in the `odbc.ini` file,
   > the one passed to `SQLDriverConnect` will take precedence.

   For the details of the configuration parameters, see the [ODBC configuration page](configuration).

5. After the configuration, to validate the installation, it is possible to use an ODBC client. unixODBC uses a command line tool called `isql`.

   Use the DSN defined in `odbc.ini` as a parameter of `isql`.

   ```bash
   isql DuckDB
   ```

   ```text
   +---------------------------------------+
   | Connected!                            |
   |                                       |
   | sql-statement                         |
   | help [tablename]                      |
   | echo [string]                         |
   | quit                                  |
   |                                       |
   +---------------------------------------+
   ```

   ```sql
   SQL> SELECT 42;
   ```

   ```text
   +------------+
   | 42         |
   +------------+
   | 42         |
   +------------+

   SQLRowCount returns -1
   1 rows fetched
   ```
