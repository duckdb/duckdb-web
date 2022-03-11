---
layout: docu
title: ODBC API
selected: Client APIs
---
## ODBC driver
The ODBC (Open Database Connectivity) is a C-style API that provides access to different flavors of database management systems (DBMSs).
Someone can see the ODBC API composed of the Driver Manager (DM) and the ODBC drivers.

The DM is part of the system library, e.g., unixODBC, which manages the communications between the user applications and the ODBC drivers.
Typically, applications are linked against the DM, which uses Data Source Name (DSN) to look up the correct ODBC driver.
<!--- with dynamically linkage call the ODBC driver. -->

The ODBC driver is a DBMS implementation of the ODBC API, which handles all the internals of that DBMS.

The DM maps user application calls of ODBC functions to the correct ODBC driver that performs the specified function and returns the proper values.

## DuckDB ODBC Assets

DuckDB supports the ODBC version 3.0 according to the [Core Interface Conformance](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/core-interface-conformance?view=sql-server-ver15). 

We release the ODBC driver as assets for Linux and Windows.
Users can download them from the [Latest Release of DuckBD](https://github.com/duckdb/duckdb/releases).

There, there are two assets: **duckdb\_odbc-linux-amd64.zip** and **duckdb\_odbc-windows-amd64.zip**).
These assets have specific driver artifacts to the corresponding operating system.

## Linux Setup
The ODBC setup on Linux is based on files, the well-known **.odbc.ini** and **.odbcinst.ini**.
These files can be placed at the system `/etc` directory or at the user home directory `/home/<user>` (shortcut as `~/`).
The DM prioritizes the user configuration files and then the system files.

### The ".odbc.ini" File

The **.odbc.ini** contains the DSNs for the drivers, which can have specific knobs.

An example of **.odbc.ini** with DuckDB would be:

```
[DuckDB]
Driver = DuckDB Driver
Database=:memory:
```

**[DuckDB]**: between the brackets is a DSN for the DuckDB.

**Driver**: it describes the driver's name, and other configurations will be placed in the **.odbcinst.ini**.

**Database**: it describes the database name used by DuckDB, and it can also be a file path to a `.db` in the system.

### The ".odbcinst.ini" File

The **.odbcinst.ini** contains general configurations for the ODBC installed drivers in the system.
A driver section starts with the driver name between brackets, and then it follows specific configuration knobs belonging to that driver.

An example of **.odbcinst.ini** with the DuckDB driver would be:

```
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /home/<user>/duckdb/build/release/tools/odbc/libduckdb_odbc.so
```


**[ODBC]**: it is the DM configuration section.

**Trace**: it enables the ODBC trace file using the option `yes`.

**TraceFile**: the absolute system file path for the ODBC trace file.


**[DuckDB Driver]**: the section of the DuckDB installed driver.

**Driver**: the absolute system file path of the DuckDB driver. 



## Windows Setup
The ODBC setup on Windows is based on registry keys ([Registry Entries for ODBC Components
](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15)).
The ODBC entries can be placed at the current user registry key (`HKCU`) or the system registry key (`HKLM`).

We have tested and used the system entries based on `HKLM->SOFTWARE->ODBC`.
In that registry, there are two subkeys: `ODBC.INI` and `ODBCINST.INI`.

The `ODBC.INI` is where users usually insert DSN registry entries for the drivers.

For example, the DSN registry for DuckDB would look like this:

![`HKLM->SOFTWARE->ODBC->ODBC.INI->DuckDB`](/images/blog/odbc/odbc_ini-registry-entry.png)


The `ODBCINST.INI` contains one entry for each ODBC driver and other keys predefined for [Windows ODBC configuration](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15).

### ODBC Windows Installer

To simplify and facilitate the installation process, we provide the ODBC installer (`odbc_install.exe`) with the Windows asset.

Users can just run: `odbc_install.exe /Install`, and all required Windows registries will be configured using the default database `:memory:`.


### DSN Windows Setup

After the installation, it is possible to change the default DSN configuration or add a new one using the Windows ODBC config tool `odbcad32.exe`:

![Windows ODBC Config Tool](/images/blog/odbc/odbcad32_exe.png)


Selecting the default DSN (i.e., `DuckDB`) or add a new configuration, the following setup window will display:

![DuckDB Windows DSN Setup](/images/blog/odbc/duckdb_DSN_setup.png)

For now, it is possible to set the DSN and the database file path associated with that DSN.
