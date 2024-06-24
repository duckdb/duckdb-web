---
layout: docu
title: ODBC API on Linux
---

## Driver Manager

A driver manager is required to manage communication between applications and the ODBC driver.
We tested and support `unixODBC` that is a complete ODBC driver manager for Linux.
Users can install it from the command line:

On Debian-based distributions (Ubuntu, Mint, etc.), run:

```bash
sudo apt-get install unixodbc odbcinst
```

On Fedora-based distributions (Amazon Linux, RHEL, CentOS, etc.), run:

```bash
sudo yum install unixODBC
```

## Setting Up the Driver

1. Download the ODBC Linux Asset corresponding to your architecture:

   <!-- markdownlint-disable MD034 -->

   * [x86_64 (AMD64)](https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-linux-amd64.zip)
   * [arm64](https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-linux-aarch64.zip)

   <!-- markdownlint-enable MD034 -->

2. The package contains the following files:

   * `libduckdb_odbc.so`: the DuckDB driver.
   * `unixodbc_setup.sh`: a setup script to aid the configuration on Linux.

   To extract them, run:

   ```bash
   mkdir duckdb_odbc && unzip duckdb_odbc-linux-amd64.zip -d duckdb_odbc
   ```

3. The `unixodbc_setup.sh` script performs the configuration of the DuckDB ODBC Driver. It is based on the unixODBC package that provides some commands to handle the ODBC setup and test like `odbcinst` and `isql`.

   Run the following commands with either option `-u` or `-s` to configure DuckDB ODBC.

   The `-u` option based on the user home directory to setup the ODBC init files.

   ```bash
   ./unixodbc_setup.sh -u
   ```

   The `-s` option changes the system level files that will be visible for all users, because of that it requires root privileges.

   ```bash
   sudo ./unixodbc_setup.sh -s
   ```

   The option `--help` shows the usage of `unixodbc_setup.sh` prints the help.

   ```bash
   ./unixodbc_setup.sh --help
   ```

   ```text
   Usage: ./unixodbc_setup.sh <level> [options]

   Example: ./unixodbc_setup.sh -u -db ~/database_path -D ~/driver_path/libduckdb_odbc.so

   Level:
   -s: System-level, using 'sudo' to configure DuckDB ODBC at the system-level, changing the files: /etc/odbc[inst].ini
   -u: User-level, configuring the DuckDB ODBC at the user-level, changing the files: ~/.odbc[inst].ini.

   Options:
   -db database_path>: the DuckDB database file path, the default is ':memory:' if not provided.
   -D driver_path: the driver file path (i.e., the path for libduckdb_odbc.so), the default is using the base script directory
   ```

4. The ODBC setup on Linux is based on the `.odbc.ini` and `.odbcinst.ini` files.

   These files can be placed to the user home directory `/home/⟨username⟩` or in the system `/etc` directory.
   The Driver Manager prioritizes the user configuration files over the system files.

   For the details of the configuration parameters, see the [ODBC configuration page](configuration).