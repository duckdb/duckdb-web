---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
title: ODBC API Overview
---

> Tip To use the DuckDB ODBC client, visit the [ODBC installation page]({% link install/index.html %}?environment=odbc).
>
> The latest stable version of the DuckDB ODBC client is {{ site.current_duckdb_odbc_short_version }}.

The ODBC (Open Database Connectivity) is a C-style API that provides access to different flavors of Database Management Systems (DBMSs).
The ODBC API consists of the Driver Manager (DM) and the ODBC drivers.

The Driver Manager is part of the system library, e.g., unixODBC, which manages the communications between the user applications and the ODBC drivers.
Typically, applications are linked against the DM, which uses Data Source Name (DSN) to look up the correct ODBC driver.

The ODBC driver is a DBMS implementation of the ODBC API, which handles all the internals of that DBMS.

The DM maps user application calls of ODBC functions to the correct ODBC driver that performs the specified function and returns the proper values.

## DuckDB ODBC Driver

DuckDB supports the ODBC version 3.0 according to the [Core Interface Conformance](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/core-interface-conformance?view=sql-server-ver15).

The ODBC driver is available for all operating systems. Visit the [installation page]({% link install/index.html %}) for direct links.
