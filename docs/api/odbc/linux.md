---
layout: docu
title: ODBC API - Linux
selected: Linux
---

# Driver Manager: unixODBC

A driver manager is required to manage communication between applications and the ODBC driver.
We tested and support the unixODBC that is a complete ODBC driver manager for Linux.
Users can install it from the command line:

## Debian SO flavors

```bash
sudo apt get install unixodbc
```

## Fedora SO flavors

```bash
sudo yum install unixodbc
# or
sudo dnf install unixodbc
```

# Step 1: Download ODBC Driver

DuckDB releases the ODBC driver as asset. For linux, download it from <a href="https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-linux-amd64.zip">ODBC Linux Asset</a> that contains the following artifacts:

**libduckdb_odbc.so**: the DuckDB driver compiled to Ubuntu 16.04.

**unixodbc_setup.sh**: a setup script to aid the configuration on Linux.

# Step 2: Extracting ODBC artifacts

Run unzip to extract the files:

```bash
mkdir duckdb_odbc
unzip duckdb_odbc-linux-amd64.zip -d duckdb_odbc
```

# Step 3: Configuring with unixODBC

The `unixodbc_setup.sh` script aids the configuration of the DuckDB ODBC Driver.
It is based on the unixODBC package that provides some commands to handle the ODBC setup and test like `odbcinst` and `isql`.

In a terminal window, change to the `duckdb_odbc` directory, and run the following commands with level options `-u` or `-s` either to configure DuckDB ODBC.

## User-level ODBC setup (**-u**)

The `-u` option based on the user home directory to setup the ODBC init files.

```bash
unixodbc_setup.sh -u
```

P.S.: The default configuration consists of a database `:memory:`.

## System-level ODBC setup (**-s**)

The **-s** changes the system level files that will be visible for all users, because of that it requires root privileges.

```bash
sudo unixodbc_setup.sh -s
```
P.S.: The default configuration consists of a database `:memory:`.


## Show usage (**--help**)

The option `--help` shows the usage of `unixodbc_setup.sh` that provides alternative options for a customer configuration, like `-db` and `-D`.

```bash
unixodbc_setup.sh --help

Usage: ./unixodbc_setup.sh <level> [options]

Example: ./unixodbc_setup.sh -u -db ~/database_path -D ~/driver_path/libduckdb_odbc.so

Level:
-s: System-level, using 'sudo' to configure DuckDB ODBC at the system-level, changing the files: /etc/odbc[inst].ini
-u: User-level, configuring the DuckDB ODBC at the user-level, changing the files: ~/.odbc[inst].ini.

Options:
-db database_path>: the DuckDB database file path, the default is ':memory:' if not provided.
-D driver_path: the driver file path (i.e., the path for libduckdb_odbc.so), the default is using the base script directory
```

## Step 4 (optional):  Configure the ODBC Driver

The ODBC setup on Linux is based on files, the well-known `.odbc.ini` and `.odbcinst.ini`.
These files can be placed at the system `/etc` directory or at the user home directory `/home/<user>` (shortcut as `~/`).
The DM prioritizes the user configuration files and then the system files.

### The `.odbc.ini` File

The `.odbc.ini` contains the DSNs for the drivers, which can have specific knobs.

An example of `.odbc.ini` with DuckDB would be:

```
[DuckDB]
Driver = DuckDB Driver
Database=:memory:
```

**[DuckDB]**: between the brackets is a DSN for the DuckDB.

**Driver**: it describes the driver's name, and other configurations will be placed at the **.odbcinst.ini**.

**Database**: it describes the database name used by DuckDB, and it can also be a file path to a `.db` in the system.

### The `.odbcinst.ini` File

The `.odbcinst.ini` contains general configurations for the ODBC installed drivers in the system.
A driver section starts with the driver name between brackets, and then it follows specific configuration knobs belonging to that driver.

An example of `.odbcinst.ini` with the DuckDB driver would be:

```
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /home/<user>/duckdb_odbc/libduckdb_odbc.so
```


**[ODBC]**: it is the DM configuration section.

**Trace**: it enables the ODBC trace file using the option `yes`.

**TraceFile**: the absolute system file path for the ODBC trace file.


**[DuckDB Driver]**: the section of the DuckDB installed driver.

**Driver**: the absolute system file path of the DuckDB driver.
