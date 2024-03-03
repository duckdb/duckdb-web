---
layout: docu
title: ODBC API - macOS
---

A driver manager is required to manage communication between applications and the ODBC driver.
We tested and support `unixODBC` that is a complete ODBC driver manager for macOS (and Linux).
Users can install it from the command line:

## Brew

```bash
brew install unixodbc 
```

## Step 1: Download ODBC Driver

DuckDB releases the ODBC driver as asset. For macOS, download it from the <a href="https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-osx-universal.zip">ODBC macOS asset</a> that contains the following artifacts:

**libduckdb_odbc.dylib**: the DuckDB ODBC driver compiled to macOS (with Intel and Apple Silicon support).

## Step 2: Extracting ODBC Artifacts

Run unzip to extract the files to a permanent directory:

```bash
mkdir duckdb_odbc
unzip duckdb_odbc-osx-universal.zip -d duckdb_odbc
```

## Step 3: Configure the ODBC Driver

There are two ways to configure the ODBC driver, either by initializing the configuration files listed below,
or by connecting with [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16).
A combination of the two is also possible.

Furthermore, the ODBC driver supports all the [configuration options](../../configuration/overview) included in DuckDB.

> If a configuration is set in both the connection string passed to `SQLDriverConnect` and in the `odbc.ini` file,
> the one passed to `SQLDriverConnect` will take precedence.

### The `odbc.ini` or `.odbc.ini` File

The `.odbc.ini` contains the DSNs for the drivers, which can have specific knobs.

Example of `.odbc.ini` with DuckDB:

```ini
[DuckDB]
Driver = DuckDB Driver
Database=:memory:
access_mode=read_only
allow_unsigned_extensions=true
```

* `[DuckDB]`: between the brackets is a DSN for the DuckDB.
* `Driver`: Describes the driver's name, as well as where to find the configurations in the **.odbcinst.ini**.
* `Database`: Describes the database name used by DuckDB, can also be a file path to a `.db` in the system.
* `access_mode`: The mode in which to connect to the database
* `allow_unsigned_extensions`: Allow the use of unsigned extensions

### The `.odbcinst.ini` File

The `.odbcinst.ini` contains general configurations for the ODBC installed drivers in the system.
A driver section starts with the driver name between brackets, and then it follows specific configuration knobs belonging to that driver.

Example of `.odbcinst.ini` with the DuckDB:

```ini
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /User/⟨user⟩/duckdb_odbc/libduckdb_odbc.dylib
```

* `[ODBC]`: it is the DM configuration section.
* `Trace`: it enables the ODBC trace file using the option `yes`.
* `TraceFile`: the absolute system file path for the ODBC trace file.
* `[DuckDB Driver]`: the section of the DuckDB installed driver.
* `Driver`: the absolute system file path of the DuckDB driver.

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
