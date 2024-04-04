---
layout: docu
title: ODBC Configuration
---

This page documents the files using the ODBC configuration.

## The `odbc.ini` or `.odbc.ini` File

The `.odbc.ini` contains the DSNs for the drivers, which can have specific knobs.

Example of `.odbc.ini` with DuckDB:

```ini
[DuckDB]
Driver = DuckDB Driver
Database = :memory:
access_mode = read_only
allow_unsigned_extensions = true
```

* `[DuckDB]`: between the brackets is a DSN for the DuckDB.
* `Driver`: Describes the driver's name, as well as where to find the configurations in the `.odbcinst.ini`.
* `Database`: Describes the database name used by DuckDB, can also be a file path to a `.db` in the system.
* `access_mode`: The mode in which to connect to the database.
* `allow_unsigned_extensions`: Allow the use of [unsigned extensions](../../extensions/overview#unsigned-extensions).

## The `.odbcinst.ini` File

The `.odbcinst.ini` contains general configurations for the ODBC installed drivers in the system.
A driver section starts with the driver name between brackets, and then it follows specific configuration knobs belonging to that driver.

Example of `.odbcinst.ini` with the DuckDB:

```ini
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /path/to/libduckdb_odbc.dylib
```

* `[ODBC]`: it is the DM configuration section.
* `Trace`: it enables the ODBC trace file using the option `yes`.
* `TraceFile`: the absolute system file path for the ODBC trace file.
* `[DuckDB Driver]`: the section of the DuckDB installed driver.
* `Driver`: the absolute system file path of the DuckDB driver. Change to match your configuration.
