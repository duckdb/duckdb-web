---
layout: docu
title: ODBC API - Windows
selected: Windows
---

# Windows ODBC Driver Manager: Odbccp32.dll

The Microsoft Windows requires an ODBC Driver Manager to manage communication between applications and the ODBC drivers.
The DM on Windows is provided in a DLL file ***Odbccp32.dll***, and other files and tools.
For detailed information checkout out the [Common ODBC Component Files](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/odbc/dn170563(v=vs.85)).


# Step 1: Download ODBC Driver

DuckDB releases the ODBC driver as asset. For Windows, download it from <a href="https://github.com/duckdb/duckdb/releases/download/v{{ site.currentduckdbversion }}/duckdb_odbc-windows-amd64.zip">Windows Asset</a> that contains the following artifacts:

**duckdb_odbc.dll**: the DuckDB driver compiled for Windows.

**duckdb_odbc_setup.dll**: a setup DLL used by the Windows ODBC Data Source Administrator tool.

**odbc_install.exe**: a installation script to aid the configuration on Windows.

# Step 2: Extracting ODBC artifacts

Unzip the file to a permanent directory (e.g., duckdb_odbc).

An example with `PowerShell` and `unzip` command would be:

```PowerShell
mkdir duckdb_odbc
unzip duckdb_odbc-linux-amd64.zip -d duckdb_odbc
```

# Step 3: ODBC Windows Installer

The `odbc_install.exe` aids the configuration of the DuckDB ODBC Driver on Windows.
It depends on the `Odbccp32.dll` that provides functions to configure the ODBC registry entries.

Inside the permanent directory (e.g., `duckdb_odbc`), double-click on the `odbc_install.exe`.

Windows administrator privileges is required, in case of a non-administrator a User Account Control shall display:

<img src="/images/blog/odbc/windows_privileges.png" style="width: 60%; height: 60%"/>


# Step 4: Configure the ODBC Driver

The `odbc_install.exe` adds a default DSN configuration into the ODBC registries with a default database `:memory:`.

## DSN Windows Setup

After the installation, it is possible to change the default DSN configuration or add a new one using the Windows ODBC Data Source Administrator tool `odbcad32.exe`.

It also can be launched thought the Windows start:

<img src="/images/blog/odbc/launch_odbcad.png" style="width: 60%; height: 60%"/>

## Default DuckDB DSN

In the Windows ODBC Data Source Administrator tool, at ***System DSN*** tab is placed the default installed DSN for ***DuckDB***:

![Windows ODBC Config Tool](/images/blog/odbc/odbcad32_exe.png)

## Changing DuckDB DSN

Selecting the default DSN (i.e., `DuckDB`) or add a new configuration, the following setup window will display:

![DuckDB Windows DSN Setup](/images/blog/odbc/duckdb_DSN_setup.png)

For now, it is possible to set the DSN and the database file path associated with that DSN.


# More Detailed Windows Setup
The ODBC setup on Windows is based on registry keys (see [Registry Entries for ODBC Components
](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15)).
The ODBC entries can be placed at the current user registry key (`HKCU`) or the system registry key (`HKLM`).

We have tested and used the system entries based on `HKLM->SOFTWARE->ODBC`.
The `odbc_install.exe` changes this entry that has two subkeys: `ODBC.INI` and `ODBCINST.INI`.

The `ODBC.INI` is where users usually insert DSN registry entries for the drivers.

For example, the DSN registry for DuckDB would look like this:

![`HKLM->SOFTWARE->ODBC->ODBC.INI->DuckDB`](/images/blog/odbc/odbc_ini-registry-entry.png)


The `ODBCINST.INI` contains one entry for each ODBC driver and other keys predefined for [Windows ODBC configuration](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15).
