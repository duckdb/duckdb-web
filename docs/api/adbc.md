---
layout: docu
title: ADBC API
selected: Client APIs
---

# The Arrow Database Connectivity (ADBC)
The [ADBC](https://arrow.apache.org/adbc/0.5.1/index.html), (Arrow Database Connectivity), similar to ODBC and JDBC, is a C-style API that enables code portability between different database systems. This allows developers to effortlessly build applications that communicate with database systems without using code specific to that system. The main difference between ADBC and ODBC/JDBC is that ADBC uses [Arrow](https://arrow.apache.org/) to transfer data between the database system and the application. DuckDB has an ADBC driver, which takes advantage of the [zero-copy integration between DuckDB and Arrow](https://duckdb.org/2021/12/03/duck-arrow.html) to efficiently transfer data.

DuckDB's ADBC driver currently supports version 0.5.1 of ADBC.

Please refer to the [ADBC documentation page](https://arrow.apache.org/adbc/0.5.1/cpp/index.html) for a more extensive discussion on ADBC and a detailed API explanation.

## Implemented Functionality
The DuckDB-ADBC driver implements the full ADBC specification, with the exception of the `ConnectionReadPartition` and `StatementExecutePartitions` functions. Both of these functions exist to support systems that internally partition the query results, which does not apply to DuckDB.
In this section, we will describe the main functions that exist in ADBC, along with the arguments they take and provide examples for each function.

### Database
Set of functions that operate on a database.
| Function Name | Description | Arguments | Example |
|:---|:---|:---|:---|
| `DatabaseNew` | Allocate a new (but uninitialized) database. | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |
| `DatabaseSetOption` | Set a char* option. | `(AdbcDatabase *database, const char *key, const char *value,AdbcError *error)` | `AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error)` | 
| `DatabaseInit` | Finish setting options and initialize the database. | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `DatabaseRelease` | Destroy the database.| `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseRelease(&adbc_database, &adbc_error)` | 

### Connection
A set of functions that create and destroy a connection to interact with a database.
| Function Name | Description | Arguments | Example |
|:---|:---|:---|:---|
| `ConnectionNew` | Allocate a new (but uninitialized) connection.| `(AdbcConnection*, AdbcError*)` | `AdbcConnectionNew(&adbc_connection, &adbc_error)` |
| `ConnectionSetOption` | Options may be set before ConnectionInit.| `(AdbcConnection*, const char*, const char*, AdbcError*)` | `AdbcConnectionSetOption(&adbc_connection, ADBC_CONNECTION_OPTION_AUTOCOMMIT,ADBC_OPTION_VALUE_DISABLED, &adbc_error)` |
| `ConnectionInit` | Finish setting options and initialize the connection. | `(AdbcConnection*, AdbcDatabase*, AdbcError*)` | `AdbcConnectionInit(&adbc_connection, &adbc_database, &adbc_error)` | 
| `ConnectionRelease` | Destroy this connection. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRelease(&adbc_connection, &adbc_error)` |


FIXME: These are still pending on Thijs' PR
A set of functions that retrieve metadata about the database. In general, these functions will return Arrow objects, specifically an ArrowArrayStream.
| Function Name | Description | Arguments | Example |
| `ConnectionGetInfo` | Get metadata about the database/driver. | `(AdbcConnection*, uint32_t*, size_t, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error)` | 
| `ConnectionGetObjects` | Get a hierarchical view of all catalogs, database schemas, tables, and columns. | `(AdbcConnection*, int, const char*, const char*, const char*, const char**, const char*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `ConnectionGetTableSchema` | Get the Arrow schema of a table.| `(AdbcConnection*, const char*, const char*, const char*, ArrowSchema*, AdbcError*)` | `AdbcDatabaseRelease(&adbc_database, &adbc_error)` | 
| `ConnectionGetTableTypes` | Get a list of table types in the database. | `(AdbcConnection*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |


A set of functions with transaction semantics for the connection. By default, all connections start with auto-commit mode on, but this can be turned off via the ConnectionSetOption function.
| Function Name | Description | Arguments | Example |
| `ConnectionCommit` | Commit any pending transactions. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionCommit(&adbc_connection, &adbc_error)` |
| `ConnectionRollback` | Rollback any pending transactions. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRollback(&adbc_connection, &adbc_error)` | 

### Statement
Statements hold state related to query execution. They represent both one-off queries and prepared statements. They can be reused; however, doing so will invalidate prior result sets from that statement.

The functions used to create, destroy, and set options for a statement:
| Function Name | Description | Arguments | Example |
|:---|:---|:---|:---|
| `StatementNew` | Create a new statement for a given connection.| `(AdbcConnection*, AdbcStatement*, AdbcError*)` | `AdbcStatementNew(&adbc_connection, &adbc_statement, &adbc_error)` |
| `StatementRelease` | Destroy a statement. | `(AdbcStatement*, AdbcError*)` | `AdbcStatementRelease(&adbc_statement, &adbc_error)` |
| `StatementSetOption` | Set a string option on a statement. | `(AdbcStatement*, const char*, const char*, AdbcError*)` | `StatementSetOption(&adbc_statement, ADBC_INGEST_OPTION_TARGET_TABLE, "TABLE_NAME", &adbc_error)` |


Functions related to query execution:
| Function Name | Description | Arguments | Example |
|:---|:---|:---|:---|
| `StatementSetSqlQuery` | Set the SQL query to execute. The query can then be executed with StatementExecuteQuery.| `(AdbcStatement*, const char*, AdbcError*)` | `AdbcStatementSetSqlQuery(&adbc_statement, "SELECT * FROM TABLE", &adbc_error)` |
| `StatementSetSubstraitPlan` | Set a substrait plan to execute. The query can then be executed with StatementExecuteQuery.| `(AdbcStatement*, const uint8_t*, size_t, AdbcError*)` | `AdbcStatementSetSubstraitPlan(&adbc_statement, substrait_plan, length, &adbc_error)` |
| `StatementExecuteQuery` | Execute a statement and get the results.| `(AdbcStatement*, ArrowArrayStream*, int64_t*, AdbcError*)` | `AdbcStatementExecuteQuery(&adbc_statement, &arrow_stream, &rows_affected, &adbc_error)` |
| `StatementPrepare` | Turn this statement into a prepared statement to be  executed multiple times.| `(AdbcStatement*, AdbcError*)` | `AdbcStatementPrepare(&adbc_statement, &adbc_error)` |

Functions related to binding, used for bulk insertion or in prepared statements.
| Function Name | Description | Arguments | Example |
|:---|:---|:---|:---|
| `StatementBind` | Bind Arrow Array. This can be used for bulk inserts or prepared statements.| `(AdbcStatement*, ArrowArray*, ArrowSchema*, AdbcError*)` | `StatementBind(&adbc_statement,&input_data, &adbc_error)` |
| `StatementBindStream` |  Bind Arrow Stream. This can be used for bulk inserts or prepared statements.| `(AdbcStatement*, ArrowArrayStream*, AdbcError*)` | `StatementBindStream(&adbc_statement, &input_data, &adbc_error)` |
| `StatementGetParameterSchema` | Get the schema for bound parameters. Should be called after StatementPrepare.| `(AdbcStatement*, ArrowSchema*, AdbcError*)` | `StatementGetParameterSchema(&adbc_statement,&schema, &adbc_error)` |



## C++ Example
We begin our example by declaring the essential variables for querying data through ADBC. These variables include Error, Database, Connection, Statement handling, and an Arrow Stream to transfer data between DuckDB and the application.

```cpp
AdbcError adbc_error;
AdbcDatabase adbc_database;
AdbcConnection adbc_connection;
AdbcStatement adbc_statement;
ArrowArrayStream arrow_stream;
```

We can then initialize our database variable. Before initializing the database, we need to set two database options. The first one is the `driver`, which takes a path to the DuckDB library. The second option is the `entrypoint`, which is an exported function from the DuckDB-ADBC driver that initializes all the ADBC functions. Once we have configured these two options, we can optionally set the `path` option, providing a path on disk to store our DuckDB database. If not set, a memory database is created. After configuring all the necessary options, we can proceed to initialize our database.
```cpp
AdbcDatabaseNew(&adbc_database, &adbc_error);
AdbcDatabaseSetOption(&adbc_database, "driver", "path/to/libduckdb.dylib", &adbc_error);
AdbcDatabaseSetOption(&adbc_database, "entrypoint", "duckdb_adbc_init", &adbc_error);
// By default, we start an in-memory database, but you can optionally define a path to store it on disk.
AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error);
AdbcDatabaseInit(&adbc_database, &adbc_error);
```

After initializing the database, we must create and initialize a connection to it.
```cpp
AdbcConnectionNew(&adbc_connection, &adbc_error);
AdbcConnectionInit(&adbc_connection, &adbc_database, &adbc_error);
```

We can now initialize our statement and run queries through our connection. After the `AdbcStatementExecuteQuery` the `arrow_stream` is populated with the result.
```cpp
AdbcStatementNew(&adbc_connection, &adbc_statement, &adbc_error);
AdbcStatementSetSqlQuery(&adbc_statement, "SELECT 42", &adbc_error);
int64_t rows_affected;
AdbcStatementExecuteQuery(&adbc_statement, &arrow_stream, &rows_affected, &adbc_error);
arrow_stream.release(arrow_stream)
```

Besides running queries, we can also ingest data via `arrow_streams`. For this we need to set an option with the table name we want to insert to, bind the stream and then execute the query.
```cpp 
StatementSetOption(&adbc_statement, ADBC_INGEST_OPTION_TARGET_TABLE, "AnswerToEverything", &adbc_error);
StatementBindStream(&adbc_statement, &arrow_stream, &adbc_error);
StatementExecuteQuery(&adbc_statement, nullptr, nullptr, &adbc_error);
```