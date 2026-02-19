---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
title: ODBC API on Windows
---

## Setup

Using the DuckDB ODBC API on Windows requires the following steps:

1. Microsoft Windows requires an ODBC Driver Manager to manage communication between applications and the ODBC drivers.
   The Driver Manager on Windows is provided in a DLL file `odbccp32.dll`, and other files and tools.
   For detailed information check out the [Common ODBC Component Files](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/odbc/dn170563(v=vs.85)).

2. <!-- markdownlint-disable MD034 --> DuckDB releases the ODBC driver as an asset. For Windows, download it from the [Windows ODBC asset (x86_64/AMD64)](https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-windows-amd64.zip). <!-- markdownlint-enable MD034 -->

3. The archive contains the following artifacts:

   * `duckdb_odbc.dll`: the DuckDB driver compiled for Windows.
   * `duckdb_odbc_setup.dll`: a setup DLL used by the Windows ODBC Data Source Administrator tool.
   * `odbc_install.exe`: an installation script to aid the configuration on Windows.

   Decompress the archive to a directory (e.g., `duckdb_odbc`).

4. The `odbc_install.exe` binary performs the configuration of the DuckDB ODBC Driver on Windows. It depends on the `Odbccp32.dll` that provides functions to configure the ODBC registry entries.

   Inside the permanent directory (e.g., `duckdb_odbc`), double-click on the `odbc_install.exe`.

   Windows administrator privileges are required. In case of a non-administrator, a User Account Control prompt will occur.

5. `odbc_install.exe` adds a default DSN configuration into the ODBC registries with a default database `:memory:`.

### DSN Windows Setup

After the installation, it is possible to change the default DSN configuration or add a new one using the Windows ODBC Data Source Administrator tool `odbcad32.exe`.

It also can be launched through the Windows start:

<img src="/images/blog/odbc/launch_odbcad.png" style="width: 60%; height: 60%"/>

### Default DuckDB DSN

The newly installed DSN is visible on the ***System DSN*** in the Windows ODBC Data Source Administrator tool:

![Windows ODBC Config Tool](/images/blog/odbc/odbcad32_exe.png)

### Changing DuckDB DSN

When selecting the default DSN (i.e., `DuckDB`) or adding a new configuration, the following setup window will display:

![DuckDB Windows DSN Setup](/images/blog/odbc/duckdb_DSN_setup.png)

This window allows you to set the DSN and the database file path associated with that DSN.

## More Detailed Windows Setup

There are two ways to configure the ODBC driver, either by altering the registry keys as detailed below,
or by connecting with [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16).
A combination of the two is also possible.

Furthermore, the ODBC driver supports all the [configuration options]({% link docs/preview/configuration/overview.md %})
included in DuckDB.

> If a configuration is set in both the connection string passed to `SQLDriverConnect` and in the `odbc.ini` file,
> the one passed to `SQLDriverConnect` will take precedence.

For the details of the configuration parameters, see the [ODBC configuration page]({% link docs/preview/clients/odbc/configuration.md %}).

### Registry Keys

The ODBC setup on Windows is based on registry keys (see [Registry Entries for ODBC Components](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15)).
The ODBC entries can be placed at the current user registry key (`HKCU`) or the system registry key (`HKLM`).

We have tested and used the system entries based on `HKLM->SOFTWARE->ODBC`.
The `odbc_install.exe` changes this entry that has two subkeys: `ODBC.INI` and `ODBCINST.INI`.

The `ODBC.INI` is where users usually insert DSN registry entries for the drivers.

For example, the DSN registry for DuckDB would look like this:

![`HKLM->SOFTWARE->ODBC->ODBC.INI->DuckDB`](/images/blog/odbc/odbc_ini-registry-entry.png)

The `ODBCINST.INI` contains one entry for each ODBC driver and other keys predefined for [Windows ODBC configuration](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15).

### Updating the ODBC Driver

When a new version of the ODBC driver is released, installing the new version will overwrite the existing one.
However, the installer doesn't always update the version number in the registry.
To ensure the correct version is used,
check that `HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\DuckDB Driver` has the most recent version,
and `HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBC.INI\DuckDB\Driver` has the correct path to the new driver.
