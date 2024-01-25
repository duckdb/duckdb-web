---
layout: docu
title: ODBC API - Overview
redirect_from:
  - /docs/api/odbc
  - /docs/api/odbc/
---

The ODBC (Open Database Connectivity) is a C-style API that provides access to different flavors of Database Management Systems (DBMSs).
The ODBC API consists of the Driver Manager (DM) and the ODBC drivers.

The DM is part of the system library, e.g., unixODBC, which manages the communications between the user applications and the ODBC drivers.
Typically, applications are linked against the DM, which uses Data Source Name (DSN) to look up the correct ODBC driver.
<!--- with dynamically linkage call the ODBC driver. -->

The ODBC driver is a DBMS implementation of the ODBC API, which handles all the internals of that DBMS.

The DM maps user application calls of ODBC functions to the correct ODBC driver that performs the specified function and returns the proper values.

## DuckDB ODBC Driver

DuckDB supports the ODBC version 3.0 according to the [Core Interface Conformance](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/core-interface-conformance?view=sql-server-ver15).

We release the ODBC driver as assets for Linux and Windows.
Users can download them from the [Latest Release of DuckDB](https://github.com/duckdb/duckdb/releases).

## Operating Systems

| Operating System   | Supported Versions             |
|--------------------|--------------------------------|
| Linux              | Ubuntu 20.04 or later          |
| Microsoft Windows  | Microsoft Windows 10 or later  |

## Pages in This Section
