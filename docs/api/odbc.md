---
layout: docu
title: ODBC API
selected: Client APIs
---
## ODBC driver
The ODBC (Open Database Connectivity) API is a C-style library that provides access to different flavours of database management systems (DBMSs). Someone can see the ODBC API composed of two components: the Driver Manager (DM) and the ODBC driver.

The DM is part of the operational system library, .e.g, unixODBC, which manages the communications between the user applications and the ODBC drivers. Typically, applications are linked against the DM.

The ODBC driver is a DBMS implementation of the ODBC API, which handles all the internals of the DBMS.

The DM maps user application calls for ODBC functions to the correct ODBC driver that performs the specified function and returns the proper values.

The DM based on Data Source Name (DSN) to look up for the correct ODBC driver and with dynamically linkage call the ODBC driver.

## DuckDB ODBC Assets

DuckDB releases the ODBC driver as assets for Linux and Windows.

They can be downloaded from the [Latest Release of DuckBD](https://github.com/duckdb/duckdb/releases).
There, there are two assets: **duckdb\_odbc-linux-amd64.zip** and **duckdb\_odbc-windows-amd64.zip**).

## Linux Setup
The ODBC setup on Linux is based on files, the famous **.odbc.ini** and **.odbcinst.ini**.
These files can be placed at the system `/etc` directory or at the user home directory `/home/\<user\>` (shortcuted as `~/`). The DM gives the priority to the user configuration files and then to the system files.

One example for the **.odbc.ini** with DuckDB
```
[DuckDB]
Driver = DuckDB Driver
Database=:memory:
```

**[DuckDB]**: between the brackets is the DSN for the DuckDB

**Driver**: describes the name of the driver.

**Database**: describes the database name used by the DuckDB, it can also contain a file path path to a `.db` in the system.
