---
github_repository: https://github.com/duckdb/odbc-scanner
layout: docu
title: ODBC Extension
---

The ODBC extension allows connecting to other databases (using their [ODBC drivers](https://en.wikipedia.org/wiki/Open_Database_Connectivity)) and run queries with [odbc_query](functions#odbc_query) or copy data from DuckDB with [odbc_copy](functions#odbc_copy) functions.

## Installing and loading

> On Linux and macOS the extension requires [unixODBC](https://en.wikipedia.org/wiki/UnixODBC) driver manager to be installed.
> See [below](#installing-unixodbc-driver-manager-on-linux-or-macos) for installation instructions.

The extension can be installed automatically, but needs to be loaded manually with:

```sql
LOAD odbc;
```

## Usage example

```sql
-- load extension
LOAD odbc;

-- open ODBC connection to a remote DB
SET VARIABLE conn = odbc_connect('Driver={Oracle driver};DBQ=//127.0.0.1:1521/XE', 'scott', 'tiger');

-- simple query
FROM odbc_query(getvariable('conn'), 'SELECT SYSTIMESTAMP FROM DUAL');

-- query with parameters
FROM odbc_query(getvariable('conn') 
  'SELECT CAST(? AS NVARCHAR2(2)) || CAST(? AS VARCHAR2(5)) FROM DUAL',
  params=row('🦆', 'quack'));

-- copy data into remote DB
FROM odbc_copy(getvariable('conn'),
  source_file='https://blobs.duckdb.org/nl_stations.csv',
  dest_table='NL_TRAIN_STATIONS',
  create_table=TRUE);

-- close connection
SELECT odbc_close(getvariable('conn'));
```

## Installing nightly version

ODBC extension is built using the version-independent DuckDB C API. The same binary (for the specific platform, for example:  `windows_amd64`) can be installed and loaded on DuckDB version `1.2.0` or any newer version.

Binaries with the most recent changes, that are published to the DuckDB nightly repository, can be installed the following way:

```sql
INSTALL 'http://nightly-extensions.duckdb.org/v1.2.0/<platform>/odbc_scanner.duckdb_extension.gz';
```

> The URL with the version `1.2.0` in it should be used even if you are running later version of DuckDB


Where the `<platform>` is one of:

 - `linux_amd64`
 - `linux_arm64`
 - `linux_amd64_musl`
 - `linux_arm64_musl`
 - `osx_amd64`
 - `osx_arm64`
 - `windows_amd64`
 - `windows_arm64`

To update installed extension to the latest nightly version run:

```sql
FORCE INSTALL 'http://nightly-extensions.duckdb.org/v1.2.0/<platform>/odbc_scanner.duckdb_extension.gz';
```

Installed version (commit ID) can be checked using the following query:

```sql
FROM duckdb_extensions() WHERE extension_name = 'odbc_scanner';
```

To install a version built from a specific commit run:

```sql
FORCE INSTALL 'http://nightly-extensions.duckdb.org/odbc_scanner/<7_chars_commit_id>/v1.2.0/<platform>/odbc_scanner.duckdb_extension.gz';
```

## DBMS-specific types support status

Tier 1:

 - Oracle: [types coverage status](https://github.com/duckdb/odbc-scanner/tree/main/test/sql/oracle/README.md)
 - SQL Server: [types coverage status](https://github.com/duckdb/odbc-scanner/blob/main/test/sql/mssql/README.md)
 - DB2: [types coverage status](https://github.com/duckdb/odbc-scanner/blob/main/test/sql/db2/README.md)

 Tier 2:

 - PostgreSQL: basic types covered
 - MySQL/MariaDB: basic types covered
 - Firebird: [types coverage status](https://github.com/duckdb/odbc-scanner/blob/main/test/sql/firebird/README.md)

 Tier 3:

 - Snowflake: [types coverage status](https://github.com/duckdb/odbc-scanner/blob/main/test/sql/snowflake/README.md)
 - ClickHouse: basic types covered
 - Spark: basic types covered
 - Arrow Flight SQL: basic types covered

## Installing unixODBC driver manager on Linux or macOS

On Linux `unixODBC` can be installed using the system package manager. Depending on the Linux distribution one of the following installation commands can be used:

Debian, Ubuntu:

```bash
sudo apt-get install unixodbc
```

RHEL, Alma, Rocky, Amazon, Fedora:

```bash
sudo dnf install unixODBC
```

Alpine:

```sh
sudo apk add unixodbc
```

On macOS unixODBC can be installed using the [Homebrew package manager](https://en.wikipedia.org/wiki/Homebrew_(package_manager)):

```bash
brew install unixodbc
```

To use legacy `x86_64` ODBC drivers under the [Rosetta](https://en.wikipedia.org/wiki/Rosetta_(software)) translator, the unixODBC must
be installed using the `x86_64` version of Homebrew:

```bash
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
/usr/local/bin/brew install unixodbc
```

## Connection string examples

ODBC connection can be established using a data source name in a form `DSN=data_source1_name` or without a configured data source in a form `Driver={Driver name};parameter1=values1;...`.

[odbc_list_drivers](functions#odbc_list_drivers) and [odbc_list_data_sources](functions#odbc_list_data_sources) functions can be used to find out available drivers and data sources.

Example of connection strings without a configured data source:

Oracle: 
 
```
Driver={Oracle in instantclient_23_0};DBQ=//127.0.0.1:1521/XE;UID=scott;PWD=tiger;
```

SQL Server: 
 
```
Driver={ODBC Driver 18 for SQL Server};Server=tcp:127.0.0.1,1433;UID=sa;PWD=pwd;TrustServerCertificate=Yes;Database=test_db;
```

DB2: 

```
Driver={IBM DB2 ODBC DRIVER};HostName=127.0.0.1;Port=50000;Database=testdb;UID=db2inst1;PWD=pwd;
```

PostgreSQL: 

```
Driver={PostgreSQL Unicode};Server=127.0.0.1;Port=5432;Username=postgres;Password=postgres;Database=test_db;
```

MySQL/MariaDB: 

```
Driver={MariaDB ODBC 3.1 Driver};SERVER=127.0.0.1;PORT=3306;USER=root;PASSWORD=root;DATABASE=test_db;
```

Firebird: 

```
Driver={Firebird ODBC Driver};Database=127.0.0.1/3050:C:/path/to/test.fdb;UID=SYSDBA;PWD=pwd;CHARSET=UTF8;
```

Snowflake: 

```
Driver={SnowflakeDSIIDriver};Server=foobar-ab12345.snowflakecomputing.com;Database=SNOWFLAKE_SAMPLE_DATA;UID=username;PWD=pwd;
```

ClickHouse: 

```
Driver={ClickHouse ODBC Driver (Unicode)};Server=127.0.0.1;Port=8123;
```

Spark: 

```
Driver={Simba Spark ODBC Driver};Host=127.0.0.1;Port=10000;
```

Arrow Flight SQL (Dremio ODBC + GizmoSQL): 

```
Driver={Dremio Flight SQL ODBC Driver};Host=127.0.0.1;Port=31337;UID=gizmosql_username;PWD=gizmosql_password;useEncryption=true;
```

## Query parameters

When a DuckDB query is run using prepared statement, it is possible to pass input parameters from the client code. The extension allows to forward such input parameters over ODBC API to the queries to remote databases.

2 methods of passing query parameters are supported, using either `params` or `params_handle` named argument to [odbc_query](functions#odbc_query) function.

`params` argument takes a `STRUCT` value as an input. Struct field names are ignored, so the `row()` function can be used to create a `STRUCT` value inline:

```sql
FROM odbc_query(
  getvariable('conn'),
  '
    SELECT CAST(? AS VARCHAR2(3)) || CAST(? AS VARCHAR2(3)) FROM DUAL
  ', 
  params=row(?, ?))
```

If we prepare this query with `duckdb_prepare()`, bind `foo` and `bar` `VARCHAR` values to it with `duckdb_bind_value()` and
execute it with `duckdb_execute_prepared()` - the input parameters `foo` and `bar` will be forwarded to the ODBC query in the remote DB.

The problem with this approach, is that DuckDB is unable to resolve parameter types (specified in the outer query) before `duckdb_execute_prepared()` is called - such types may be different in subsequent invocations of `duckdb_execute_prepared()` and there is no way to specify these types explicitly.

This will result in re-preparing the inner query in remote DB every time `duckdb_execute_prepared()` is called.

To avoid this problem is it possible to use 2-step parameter binding with `params_handle` named argument to [odbc_query](functions#odbc_query):

```sql
-- create parameters handle
SET VARIABLE params = odbc_create_params();

-- when 'duckdb_prepare()' is called, the inner query will be prepared in the remote DB
FROM odbc_query(
  getvariable('conn'),
  '
    SELECT CAST(? AS VARCHAR2(3)) || CAST(? AS VARCHAR2(3)) FROM DUAL
  ', 
  params_handle=getvariable('params'));

-- now we can repeatedly bind new parameters to the handle using 'odbc_bind_params()'
-- and call 'duckdb_execute_prepared()' to run the prepared query with
-- these new parameters in remote DB
SELECT odbc_bind_params(getvariable('conn'), getvariable('params'), row(?, ?));
```

Parameter handle is tied to the prepared statement and will be freed when the statement is destroyed.

## Connections and concurrency

DuckDB uses a multi-threaded execution engine to run parts of the query in parallel. ODBC drivers may or may not support
using the same connection from different threads concurrently. To prevent possible concurrency problems the extension does not
allow to use the same connection from multiple threads. For example, the following query:

```sql
FROM odbc_query(getvariable('conn'), 'SELECT ''foo'' col1 FROM DUAL')
UNION ALL
FROM odbc_query(getvariable('conn'), 'SELECT ''bar'' col1 FROM DUAL')
```

will fail with:

```
Invalid Input Error:
'odbc_query' error: ODBC connection not found on global init, id: 139760181976192
```

This can be avoided by using multiple ODBC connections:

```sql
FROM odbc_query(getvariable('conn1'), 'SELECT ''foo'' col1 FROM DUAL')
UNION ALL
FROM odbc_query(getvariable('conn2'), 'SELECT ''bar'' col1 FROM DUAL')
```

Or by disabling multi-threaded execution setting `threads` DuckDB option to `1`.

## Transactions management

According to ODBC specification, connections to remote DB are expected to have auto-commit mode enabled by default.

As a general rule, transaction commands `BEGIN TRANSACTION`/`COMMIT`/`ROLLBACK` are not supposed to be sent over ODBC as SQL commands. Doing so may or may not be supported by the particular driver. Instead ODBC provides the API to manage transactions.

This API is exposed in the following functions:

 - [odbc_begin_transaction](functions#odbc_begin_transaction)
 - [odbc_commit](functions#odbc_commit)
 - [odbc_rollback](functions#odbc_rollback)

When [odbc_begin_transaction](functions#odbc_begin_transaction) is called on the connection, the auto-commit mode on this connection is disabled and an implicit transaction is started. There is currently no support for enabling auto-commit back on such connection.

After the transaction is started, call [odbc_commit](functions#odbc_commit) or [odbc_rollback](functions#odbc_rollback) to complete this transaction. After the completion is performed, new implicit transaction is started on this connection automatically.

## Performance

ODBC is not a high-performance API, [odbc_query](functions#odbc_query) uses multiple API calls per-row and performs `UCS-2` to `UTF-8` conversion for every `VARCHAR` value. Besides that, query processing is strictly single-threaded.

When [submitting issues](https://github.com/duckdb/odbc-scanner/issues) related only to performance please check the performance in comparable scenarios, for example with [pyodbc](https://pypi.org/project/pyodbc/).
