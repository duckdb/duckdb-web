---
layout: docu
title: ODBC Extension Functions
---


 - [odbc_begin_transaction](#odbc_begin_transaction)
 - [odbc_bind_params](#odbc_bind_params)
 - [odbc_close](#odbc_close)
 - [odbc_commit](#odbc_commit)
 - [odbc_connect](#odbc_connect)
 - [odbc_copy](#odbc_copy)
 - [odbc_create_params](#odbc_create_params)
 - [odbc_list_data_sources](#odbc_list_data_sources)
 - [odbc_list_drivers](#odbc_list_drivers)
 - [odbc_query](#odbc_query)
 - [odbc_rollback](#odbc_rollback)

### odbc_begin_transaction

```sql
odbc_begin_transaction(conn_handle BIGINT) -> VARCHAR
```

Sets the `SQL_ATTR_AUTOCOMMIT` attribute to `SQL_AUTOCOMMIT_OFF` on the specified connection thus effectively starting an implicit transaction. [odbc_commit](#odbc_commit) or [odbc_rollback](#odbc_rollback) must be called on such connection to complete the transaction. The completion starts another implicit transaction on this connection. See [Transactions management](overview#transactions-management) for details.

#### Parameters:

 - `conn_handle` (`BIGINT`): ODBC connection handle created with [odbc_connect](#odbc_connect)

#### Returns:

Always returns `NULL` (`VARCHAR`).

#### Example:

```sql
SELECT odbc_begin_transaction(getvariable('conn'))
```

### odbc_bind_params

```sql
odbc_bind_params(conn_handle BIGINT, params_handle BIGINT, params STRUCT) -> BIGINT
```

Binds specified parameter values to the specified parameters handle. Only necessary with 2-step parameters binding, see [Query parameters](#query-parameters) for details.

#### Parameters:

 - `conn_handle` (`BIGINT`): ODBC connection handle created with [odbc_connect](#odbc_connect)
 - `params_handle` (`BIGINT`): parameters handle created with [odbc_create_params](#odbc_create_params)
 - `params` (`STRUCT`): parameters values

#### Returns:

Parameters handle (`BIGINT`), the same one that was passed as a second argument.

#### Example:

```sql
SELECT odbc_bind_params(getvariable('conn'), getvariable('params1'), row(42, 'foo'))
```

### odbc_close

```sql
odbc_close(conn_handle BIGINT) -> VARCHAR
```

Closes specified ODBC connection to a remote DB. Does not throw errors if the connection is already closed.

#### Parameters:

 - `conn_handle` (`BIGINT`): ODBC connection handle created with [odbc_connect](#odbc_connect)

#### Returns:

Always returns `NULL` (`VARCHAR`).

#### Example:

```sql
SELECT odbc_close(getvariable('conn'))
```

### odbc_commit

```sql
odbc_commit(conn_handle BIGINT) -> VARCHAR
```

Calls `SQLEndTran` with `SQL_COMMIT` argument on the specified connection, completing the current transaction. [odbc_begin_transaction](#odbc_begin_transaction) must be called on this connection before this call for the completion to be effective. See [Transactions management](overview#transactions-management) for details.

#### Parameters:

 - `conn_handle` (`BIGINT`): ODBC connection handle created with [odbc_connect](#odbc_connect)

#### Returns:

Always returns `NULL` (`VARCHAR`).

#### Example:

```sql
SELECT odbc_commit(getvariable('conn'))
```

### odbc_connect

```sql
odbc_connect(conn_string VARCHAR) -> BIGINT
```
```sql
odbc_connect(conn_string VARCHAR, username VARCHAR, password VARCHAR) -> BIGINT
```

Opens an ODBC connection to a remote DB.

If `username` and `password` (positional) parameters are specified, they are appended to the connection string as `UID` and `PWD`.

#### Parameters:

 - `conn_string` (`VARCHAR`): ODBC connection string, passed to the Driver Manager.

#### Returns:

Connection handle that can be placed into a `VARIABLE`. Connection is not closed automatically, must be closed with [odbc_close](#odbc_close).

#### Example:

```sql
SET VARIABLE conn = odbc_connect('Driver={Oracle Driver};DBQ=//127.0.0.1:1521/XE;UID=scott;PWD=tiger')
```
```sql
SET VARIABLE conn = odbc_connect('Driver={Oracle Driver};DBQ=//127.0.0.1:1521/XE', 'scott', 'tiger')
```

### odbc_copy

```sql
odbc_copy(conn_handle BIGINT, [, <optional named parameters>]) -> TABLE
```
```sql
odbc_copy(conn_string VARCHAR, [, <optional named parameters>]) -> TABLE
```

Copies rows from a DuckDB accessible file or table into the remote DB.

#### Parameters:

 - `conn_handle_or_string` (`BIGINT` or `VARCHAR`), one of:
   - ODBC connection handle created with [odbc_connect](#odbc_connect)
   - ODBC connection string, intended for one-off queries, in this case new ODBC connection will be opened and will be closed automatically after the query is complete

Optional named parameters (source):

> Source query is executed using a separate DB instance from the instance on which `odbc_copy` is being called.
> Thus `source_query` cannot refer to pre-existing in-memory tables and cannot open currently opened DuckDB files.
> As a workaround, for complex source queries it is suggested to export the query result into a local Parquet file first and
> then run `odbc_copy` on that file.

 - `source_conn_string` (`VARCHAR`, default: `:memory:`): DuckDB connection string to the source DB, example: `ducklake:postgres:postgresql://username:pwd@127.0.0.1:5432/lake1`
 - `source_file` (`VARCHAR`): path to a Parquet, CSV or JSON file (remote or local) to be read with DuckDB, example: `https://blobs.duckdb.org/nl_stations.csv`, equivalent to `source_query='SELECT * FROM '<source_file>'`
 - `source_query` (`VARCHAR`): DuckDB SQL query to read the data, example: `FROM nl_train_stations`
 - `source_queries` (`LIST(VARCHAR)`): multiple DuckDB SQL queries executed one by one, last query must return the result set to copy, results of previous queries are discarded, results of all queries are materialized in memory, example:

```sql
source_queries=[
  'CREATE SECRET s (TYPE s3 [...])',
  'FROM nl_train_stations'
],
```

 - `source_limit` (`UBIGINT`, default: `0`): the number of records to read from source query/file at once, when this option is specified - the source query is run multiple times appending `LIMIT <limit> OFFSET <offset>` to it, must be more or equal to `2048`, `2048` must be dividable by it without a remainder

Optional named parameters (destination):

 - `dest_table` (`VARCHAR`): destination table name in remote DB, will be used in `INSERT` and `CREATE TABLE` queries, cannot be specified if `dest_query` is specified; different DBs have different rules regarding case sensitivity and the default case, thus the name of the destination table may need to be specified in upper-case: `TAB1` or in quoted form: `"tab1"` (or with a schema name: `"schema1"."tab1"`) 
 - `dest_query` (`VARCHAR`): query to be executed in remote DB for each source batch, must have the number of ODBC parameter placeholders `?` equal to the `source_columns_count * batch_size`, cannot be specified if `dest_table` is specified, example: `CALL import_city(?,?,?,?)`
 - `dest_query_single` (`VARCHAR`): only used when the `batch_size>0` and the number of rows read in the last source batch are less than the `batch_size`, in this case used instead of `dest_query`, must have the number of ODBC parameter placeholders `?` equal to the `source_columns_count`

Optional named parameters (create table):

 - `create_table` (`BOOLEAN`, default: `FALSE`): whether to create a table in the destination remote DB using the column names and column types from the source query, effectively implements CTAS (create table as select)
 - `column_types` (`MAP(VARCHAR, VARCHAR)`): when `create_table=TRUE` is specified, allows to provide/override the type mapping between source DuckDB types and destination RDBMS types, example:

```sql
create_table=TRUE,
column_types=MAP {
    'DUCKDB_TYPE_VARCHAR': 'VARCHAR2(10)',
    'DUCKDB_TYPE_DECIMAL': 'NUMBER({typmod1},{typmod2})'}
```

 - `column_quotes` (`VARCHAR`, default: `"`): quotation character (or string) to be used to quote column names in the generated `CREATE TABLE` and `INSERT` queries
 - `commit_after_create_table` (`BOOLEAN`, default: `FALSE`): whether to issue a `COMMIT` after executing `CREATE TABLE`, enabled automatically for Firebird

Optional named parameters (query parameters handling):

 - `decimal_params_as_chars` (`BOOLEAN`, default: `false`): pass `DECIMAL` parameters as `VARCHAR`s
 - `integral_params_as_decimals` (`BOOLEAN`, default: `false`): pass (unsigned) `TINYINT`, `SMALLINT`, `INTEGER` and `BIGINT` parameters as `SQL_C_NUMERIC`.

Optional named parameters (other):

 - `batch_size` (`UINTEGER`, default: `16`): number of records to be inserted (or executed in case of `dest_query`) in a single `SQLExecute` ODBC call to remote DB, allowed values: `1`, `2`, `4`, `8`, `16`, `32`, `64`, `128`, `256`, `512`, `1024`, `2048`
 - `use_insert_all` (`BOOLEAN`, default: `FALSE`): generate `INSERT ALL` batch insert query instead of batch insert with `INSERT ... VALUES (...), (...), ... (...)`, enabled automatically for Oracle
 - `use_insert_union` (`BOOLEAN`, default: `FALSE`): generate `INSERT ... SELECT FROM .. UNION ALL ...` batch insert query instead of batch insert with `INSERT ... VALUES (...), (...), ... (...)`, enabled automatically for Firebird
 - `dummy_table_name` (`VARCHAR`): name of the dummy table use for `INSERT ALL` and `INSERT UNION` queries, `dual` for Oracle
 - `copy_in_transaction` (`BOOLEAN`, default: `TRUE`): begin a transaction in remote DB for this copy call, commit transaction when all rows are processed, roll it back on error
 - `max_records_in_transaction` (`UBIGINT`, default: `0`): when specified causes the remote transaction to be committed every time after the specified number of rows is processed
 - `close_connection` (`BOOLEAN`, default: `false`): closes the passed connection after the function call is completed, intended to be used with one-shot invocations of the `odbc_copy`

#### Returns:

A table with the following columns:

 - `completed` (`BOOLEAN`): a flag whether this output row is the last row in result set
 - `rows_processed` (`UBIGINT`): a number of rows read from the source
 - `elapsed_seconds` (`FLOAT`): a number of seconds passed after the copy process has started
 - `rows_per_second` (`FLOAT`): a number of rows processed in one second
 - `table_ddl` (`VARCHAR`): generated `CREATE TABLE` query that was executed in remote DB before starting the copy process

 One resulting row is emitted for every `2048` rows read from source. Only the last row has the `completed=TRUE` and non null `table_ddl` (only when `create_table=TRUE` is specified) values.

#### Examples:

```sql
FROM odbc_copy(getvariable('conn'),
  source_file='https://blobs.duckdb.org/nl_stations.csv',
  dest_table='NL_TRAIN_STATIONS',
  create_table=TRUE)
```
```sql
FROM odbc_copy(getvariable('conn'),
  source_conn_string='ducklake:postgres:postgresql://username:pwd@127.0.0.1:5432/lake1',
  source_queries=[
    'CREATE SECRET s (TYPE s3 [...])',
    'FROM nl_train_stations'
  ],
  dest_table='NL_TRAIN_STATIONS',
  create_table=TRUE,
  batch_size=32,
  max_records_in_transaction=42);
```
### odbc_create_params

```sql
odbc_create_params() -> BIGINT
```

Creates a parameters handle. Only necessary with 2-step parameters binding, see [Query parameters](overview#query-parameters) for details.

#### Parameters:

None.

#### Returns:

Parameters handle (`BIGINT`). When the handle is passed to [odbc_query](#odbc_query) it gets tied to the underlying prepared statement and is closed automatically when the statement is closed.

#### Example:

```sql
SET VARIABLE params1 = odbc_create_params()
```

### odbc_list_data_sources

```sql
odbc_list_data_sources() -> TABLE(name VARCHAR, description VARCHAR, type VARCHAR)
```

Returns the list of ODBC data sources registered in the OS. Uses driver manager call `SQLDataSources`.

#### Parameters:

None.

#### Returns:

A table with the following columns:

 - `name` (`VARCHAR`): data source name
 - `description` (`VARCHAR`): data source description
 - `type` (`VARCHAR`): data source type, `USER` or `SYSTEM`

#### Example:

```sql
FROM odbc_list_data_sources()
```

### odbc_list_drivers

```sql
odbc_list_drivers() -> TABLE(description VARCHAR, attributes MAP(VARCHAR, VARCHAR))
```

Returns the list of ODBC drivers registered in the OS. Uses driver manager call `SQLDrivers`.

#### Parameters:

None.

#### Returns:

A table with the following columns:

 - `description` (`VARCHAR`): driver description
 - `attributes` (`MAP(VARCHAR, VARCHAR)`): driver attributes as a `name->value` map

#### Example:

```sql
FROM odbc_list_drivers()
```

### odbc_query

```sql
odbc_query(conn_handle BIGINT, query VARCHAR[, <optional named parameters>]) -> TABLE
```
```sql
odbc_query(conn_string VARCHAR, query VARCHAR[, <optional named parameters>]) -> TABLE
```

Runs specified query in a remote DB and returns the query results table.

#### Parameters:

 - `conn_handle_or_string` (`BIGINT` or `VARCHAR`), one of:
   - ODBC connection handle created with [odbc_connect](#odbc_connect)
   - ODBC connection string, intended for one-off queries, in this case new ODBC connection will be opened and will be closed automatically after the query is complete
 - `query` (`VARCHAR`): SQL query, passed to the remote DBMS

Optional named parameters that can be used to pass query parameters:

 - `params` (`STRUCT`): query parameters to pass to remote DBMS
 - `params_handle` (`BIGINT`): parameters handle created with [odbc_create_params](#odbc_create_params). Only used with 2-step parameters binding, see [Query parameters](#query-parameters) for details.

Optional named parameters that can change types mapping:

The extension supports a number of options that can be used to change how the query parameters are passed and how the resulting data is handled. For known DBs these options are set automatically. They also can be passed as named parameters to [odbc_query](#odbc_query) function to override the autoconfiguration:

 - `decimal_columns_as_chars` (`BOOLEAN`, default: `false`): read `DECIMAL` values as `VARCHAR`s that are parsed back into `DECIMAL`s before returning them to client
 - `decimal_columns_precision_through_ard` (`BOOLEAN`, default: `false`): when reading a `DECIMAL` specify its `precision` and `scale` through "Application Row Descriptor"
 - `decimal_columns_as_ard_type` (`BOOLEAN`, default: `false`): when reading a `DECIMAL` use `SQL_ARD_TYPE` instead of `SQL_C_NUMERIC`
 - `decimal_params_as_chars` (`BOOLEAN`, default: `false`): pass `DECIMAL` parameters as `VARCHAR`s
 - `integral_params_as_decimals` (`BOOLEAN`, default: `false`): pass (unsigned) `TINYINT`, `SMALLINT`, `INTEGER` and `BIGINT` parameters as `SQL_C_NUMERIC`.
 - `reset_stmt_before_execute` (`BOOLEAN`, default: `false`): reset the prepared statement (using `SQLFreeStmt(h, SQL_CLOSE)`) before executing it
 - `time_params_as_ss_time2` (`BOOLEAN`, default: `false`): pass `TIME` parameters as SQL Server's `TIME2` values
 - `timestamp_columns_as_timestamp_ns` (`BOOLEAN`, default: `false`): read `TIMESTAMP`-like (`TIMESTAMP WITH LOCAL TIME ZONE`, `DATETIME2`, `TIMESTAMP_NTZ` etc) columns with nanosecond precision (with nine fractional digits)
 - `timestamp_columns_with_typename_date_as_date` (`BOOLEAN`, default: `false`): read `TIMESTAMP` columns that have a type name `DATE` as DuckDB `DATE`s
 - `timestamp_max_fraction_precision` (`UTINYINT`, default: `9`): maximum number of fractional digits to use when reading a `TIMESTAMP` column with nanosecond precision
 - `timestamp_params_as_sf_timestamp_ntz` (`BOOLEAN`, default: `false`): pass `TIMESTAMP` parameters as Snowflake's `TIMESTAMP_NTZ`
 - `timestamptz_params_as_ss_timestampoffset` (`BOOLEAN`, default: `false`): pass `TIMESTAMP_TZ` parameters as SQL Server's `DATETIMEOFFSET`
 - `var_len_data_single_part` (`BOOLEAN`, default: `false`): read long `VARCHAR` or `VARBINARY` values as a single read (used when a driver does not support [Retrieving Variable-Length Data in Parts](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlgetdata-function?view=sql-server-ver17#retrieving-variable-length-data-in-parts))
 - `var_len_params_long_threshold_bytes` (`UINTEGER`, default: `4000`): a length threshold after that `SQL_WVARCHAR` parameters are passed as `SQL_WLONGVARCHAR`
 - `enable_columns_binding` (`BOOLEAN`, default: `false`): whether to allow using `SQLBindCol` instead of `SQLGetData` for fixed-size columns

Other optional named parameters:

 - `ignore_exec_failure` (`BOOLEAN`, default: `false`): when a query, that is run in remote DB, can be prepared successfully, but may or may not fail at execution time (for example, because of schema state like table existence), then this flag can be used to not throw an error when query execution fails. Empty result set is returned if query execution fails.
 - `close_connection` (`BOOLEAN`, default: `false`): closes the passed connection after the function call is completed, intended to be used with one-shot invocations of the `odbc_query`, example:

 ```sql
 FROM odbc_query(
    odbc_connect('Driver={Oracle Driver};DBQ=//127.0.0.1:1521/XE', 'scott', 'tiger'),
    'SELECT 42 FROM dual',
    close_connection=TRUE);
 ```

#### Returns:

A table with the query result.

#### Example:

```sql
FROM odbc_query(getvariable('conn'), 
  'SELECT CAST(? AS NVARCHAR2(2)) || CAST(? AS VARCHAR2(5)) FROM dual',
  params=row('🦆', 'quack')
)
```

### odbc_rollback

```sql
odbc_rollback(conn_handle BIGINT) -> VARCHAR
```

Calls `SQLEndTran` with `SQL_ROLLBACK` argument on the specified connection, completing the current transaction. [odbc_begin_transaction](#odbc_begin_transaction) must be called on this connection before this call for the completion to be effective. See [Transactions management](overview#transactions-management) for details.

#### Parameters:

 - `conn_handle` (`BIGINT`): ODBC connection handle created with [odbc_connect](#odbc_connect)

#### Returns:

Always returns `NULL` (`VARCHAR`).

#### Example:

```sql
SELECT odbc_rollback(getvariable('conn'))
```