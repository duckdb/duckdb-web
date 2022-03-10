---
layout: docu
title: ODBC API
selected: Client APIs
---
## ODBC driver
The ODBC (Open Database Connectivity) API is a C-style library that provides access to different flavours of database management systems (DBMSs). Someone can see the ODBC API composed of two components: the Driver Manager (DM) and the ODBC drivers.

The DM is part of the operational system library, .e.g, unixODBC, which manages the communications between the user applications and the ODBC drivers. Typically, applications are linked against the DM that based on Data Source Name (DSN) to look up for the correct ODBC driver.
<!--- with dynamically linkage call the ODBC driver. -->

The ODBC driver is a DBMS implementation of the ODBC API, which handles all the internals of the DBMS.

The DM maps user application calls for ODBC functions to the correct ODBC driver that performs the specified function and returns the proper values.

## DuckDB ODBC Assets

DuckDB releases the ODBC driver as assets for Linux and Windows.

They can be downloaded from the [Latest Release of DuckBD](https://github.com/duckdb/duckdb/releases).
There, there are two assets: **duckdb\_odbc-linux-amd64.zip** and **duckdb\_odbc-windows-amd64.zip**).

## Linux Setup
The ODBC setup on Linux is based on files, the well-known **.odbc.ini** and **.odbcinst.ini**.
These files can be placed at the system `/etc` directory or at the user home directory `/home/<user>` (shortcuted as `~/`). The DM gives the priority to the user configuration files and then to the system files.

### The ".odbc.ini" file

The **.odbc.ini** contains the DSNs for the drivers, in which can exist specific knobs.

An example of **.odbcinst.ini** with DuckDB would be:

```
[DuckDB]
Driver = DuckDB Driver
Database=:memory:
```

**[DuckDB]**: between the brackets is a DSN for the DuckDB.

**Driver**: describes the name of the driver, which will contains more configuration details in the **.odbcinst.ini**.

**Database**: describes the database name used by the DuckDB, it can also contain a file path to a `.db` in the system.

### The ".odbcinst.ini" file

The **.odbcinst.ini** contains general configurtaions for the ODBC installed drivers in the system. A driver section start with the driver name between brackets, then it follows specific configuration knobs belonging to that driver.

An example of **.odbcinst.ini** with the DuckDB driver would be:

```
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /home/<user>/duckdb/build/release/tools/odbc/libduckdb_odbc.so
```


**[ODBC]**: this is the DM configuration section.

**Trace**: enabling the ODBC trace file with the option `yes`.

**TraceFile**: absolute system file path of the ODBC trace file.


**[DuckDB Driver]**: the section of the DuckDB installed driver.

**Driver**: absolute system file path of the DuckDB driver. 



## Windows Setup
## Windows Setup
The ODBC setup on Windows is based on registry keys. The ODBC entries can be placed at the current user registry key (HKCU) or at the system registry key (HKLM).

We have tested and used the system entries based on `HKLM->SOFTWARE->ODBC`.
In that registry there are two subkeys: `ODBC.INI` and `ODBCINST.INI`.

In general, in the `ODBC.INI` users insert DSN entries for the drivers.
For example, the DSN registry for DuckDB would look like:

![`HKLM->SOFTWARE->ODBC->ODBC.INI->DuckDB`](/images/blog/odbc/odbc_ini-registry-entry.png)

<img src="/images/blog/odbc/odbc_ini-registry-entry.png" alt="DuckDB DSN Windows Registry Entry" title="Figure 1: DuckDB DSN Windows Registry Entry" style="max-width:90%;width:90%;height:auto"/>








