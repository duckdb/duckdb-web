---
layout: docu
title: ODBC API on macOS
---

A driver manager is required to manage communication between applications and the ODBC driver.
We tested and support `unixODBC` that is a complete ODBC driver manager for macOS (and Linux).
Users can install it from the command line:

## Brew

```bash
brew install unixodbc
```

## Step 1: Download ODBC Driver

DuckDB releases the ODBC driver as asset. For macOS, download it from the <a href="https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-osx-universal.zip">ODBC macOS asset</a> that contains the `libduckdb_odbc.dylib` artifact, the DuckDB ODBC driver compiled to macOS (with Intel and Apple Silicon support).

```bash
wget https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-osx-universal.zip
```

## Step 2: Extracting ODBC Artifacts

Run unzip to extract the files to a permanent directory:

```bash
mkdir duckdb_odbc
unzip duckdb_odbc-osx-universal.zip -d duckdb_odbc
```

## Step 3: Configure the ODBC Driver

There are two ways to configure the ODBC driver, either by initializing via the configuration files,
or by connecting with [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16).
A combination of the two is also possible.

Furthermore, the ODBC driver supports all the [configuration options](../../configuration/overview) included in DuckDB.

> If a configuration is set in both the connection string passed to `SQLDriverConnect` and in the `odbc.ini` file,
> the one passed to `SQLDriverConnect` will take precedence.

See the [ODBC configuration page](configuration) for details.

## Step 4 (Optional): Test the ODBC Driver

After the configuration, for validate the installation, it is possible to use an odbc client. unixODBC use a command line tool called `isql`.

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
