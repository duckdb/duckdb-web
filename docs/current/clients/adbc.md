---
layout: docu
title: ADBC Client
---

> Tip To use the DuckDB ADBC client, download the [`libduckdb` archive]({% link install/index.html %}?environment=c) for your platform and follow the [instructions below](#installing-the-library).
>
> The latest stable version of the DuckDB ADBC client is {{ site.current_duckdb_version }}.

[Arrow Database Connectivity (ADBC)](https://arrow.apache.org/adbc/), similarly to ODBC and JDBC, is a C-style API that enables code portability between different database systems. This allows developers to effortlessly build applications that communicate with database systems without using code specific to that system. The main difference between ADBC and ODBC/JDBC is that ADBC uses [Arrow](https://arrow.apache.org/) to transfer data between the database system and the application. DuckDB has an ADBC driver, which takes advantage of the [zero-copy integration between DuckDB and Arrow]({% post_url 2021-12-03-duck-arrow %}) to efficiently transfer data.

Please refer to the [ADBC documentation page](https://arrow.apache.org/adbc/current/) for a more extensive discussion on ADBC and a detailed API explanation.

## Implemented Functionality

The DuckDB-ADBC driver implements the full ADBC specification, with the exception of the `ConnectionReadPartition` and `StatementExecutePartitions` functions. Both of these functions exist to support systems that internally partition the query results, which does not apply to DuckDB.
In this section, we will describe the main functions that exist in ADBC, along with the arguments they take and provide examples for each function.

### Database

Set of functions that operate on a database.

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `DatabaseNew` | Allocate a new (but uninitialized) database. | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |
| `DatabaseSetOption` | Set a char* option. | `(AdbcDatabase *database, const char *key, const char *value, AdbcError *error)` | `AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error)` |
| `DatabaseInit` | Finish setting options and initialize the database. | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `DatabaseRelease` | Destroy the database. | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseRelease(&adbc_database, &adbc_error)` |

### Connection

A set of functions that create and destroy a connection to interact with a database.

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `ConnectionNew` | Allocate a new (but uninitialized) connection. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionNew(&adbc_connection, &adbc_error)` |
| `ConnectionSetOption` | Options may be set before ConnectionInit. | `(AdbcConnection*, const char*, const char*, AdbcError*)` | `AdbcConnectionSetOption(&adbc_connection, ADBC_CONNECTION_OPTION_AUTOCOMMIT, ADBC_OPTION_VALUE_DISABLED, &adbc_error)` |
| `ConnectionInit` | Finish setting options and initialize the connection. | `(AdbcConnection*, AdbcDatabase*, AdbcError*)` | `AdbcConnectionInit(&adbc_connection, &adbc_database, &adbc_error)` |
| `ConnectionRelease` | Destroy this connection. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRelease(&adbc_connection, &adbc_error)` |

A set of functions that retrieve metadata about the database. In general, these functions will return Arrow objects, specifically an ArrowArrayStream.

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `ConnectionGetObjects` | Get a hierarchical view of all catalogs, database schemas, tables and columns. | `(AdbcConnection*, int, const char*, const char*, const char*, const char**, const char*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `ConnectionGetTableSchema` | Get the Arrow schema of a table. | `(AdbcConnection*, const char*, const char*, const char*, ArrowSchema*, AdbcError*)` | `AdbcDatabaseRelease(&adbc_database, &adbc_error)` |
| `ConnectionGetTableTypes` | Get a list of table types in the database. | `(AdbcConnection*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |

A set of functions with transaction semantics for the connection. By default, all connections start with auto-commit mode on, but this can be turned off via the ConnectionSetOption function.

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `ConnectionCommit` | Commit any pending transactions. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionCommit(&adbc_connection, &adbc_error)` |
| `ConnectionRollback` | Rollback any pending transactions. | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRollback(&adbc_connection, &adbc_error)` |

### Statement

Statements hold state related to query execution. They represent both one-off queries and prepared statements. They can be reused; however, doing so will invalidate prior result sets from that statement.

The functions used to create, destroy and set options for a statement:

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `StatementNew` | Create a new statement for a given connection. | `(AdbcConnection*, AdbcStatement*, AdbcError*)` | `AdbcStatementNew(&adbc_connection, &adbc_statement, &adbc_error)` |
| `StatementRelease` | Destroy a statement. | `(AdbcStatement*, AdbcError*)` | `AdbcStatementRelease(&adbc_statement, &adbc_error)` |
| `StatementSetOption` | Set a string option on a statement. | `(AdbcStatement*, const char*, const char*, AdbcError*)` | `StatementSetOption(&adbc_statement, ADBC_INGEST_OPTION_TARGET_TABLE, "TABLE_NAME", &adbc_error)` |

Functions related to query execution:

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `StatementSetSqlQuery` | Set the SQL query to execute. The query can then be executed with StatementExecuteQuery. | `(AdbcStatement*, const char*, AdbcError*)` | `AdbcStatementSetSqlQuery(&adbc_statement, "SELECT * FROM TABLE", &adbc_error)` |
| `StatementSetSubstraitPlan` | Set a substrait plan to execute. The query can then be executed with StatementExecuteQuery. | `(AdbcStatement*, const uint8_t*, size_t, AdbcError*)` | `AdbcStatementSetSubstraitPlan(&adbc_statement, substrait_plan, length, &adbc_error)` |
| `StatementExecuteQuery` | Execute a statement and get the results. | `(AdbcStatement*, ArrowArrayStream*, int64_t*, AdbcError*)` | `AdbcStatementExecuteQuery(&adbc_statement, &arrow_stream, &rows_affected, &adbc_error)` |
| `StatementPrepare` | Turn this statement into a prepared statement to be  executed multiple times. | `(AdbcStatement*, AdbcError*)` | `AdbcStatementPrepare(&adbc_statement, &adbc_error)` |

Functions related to binding, used for bulk insertion or in prepared statements.

| Function name | Description | Arguments | Example |
|:---|:-|:---|:----|
| `StatementBindStream` |  Bind Arrow Stream. This can be used for bulk inserts or prepared statements. | `(AdbcStatement*, ArrowArrayStream*, AdbcError*)` | `StatementBindStream(&adbc_statement, &input_data, &adbc_error)` |

## Setting Up the DuckDB ADBC Driver

Before using DuckDB as an ADBC driver, you must install the `libduckdb` shared library on your system and make it available to your application. This library contains the core DuckDB engine that the ADBC driver interfaces with.

### Downloading libduckdb

Download the appropriate `libduckdb` library for your platform from the [DuckDB releases page](https://github.com/duckdb/duckdb/releases):

- **Linux**: `libduckdb-linux-amd64.zip` (contains `libduckdb.so`)
- **macOS**: `libduckdb-osx-universal.zip` (contains `libduckdb.dylib`)
- **Windows**: `libduckdb-windows-amd64.zip` (contains `duckdb.dll`)

Extract the archive to obtain the shared library file.

### Installing the Library

#### Linux

1. Extract the `libduckdb.so` file from the downloaded archive
2. Make sure your code can use the library. You can:

    - Either copy it to a system library directory (requires root access):

      ```bash
      sudo cp libduckdb.so /usr/local/lib/
      sudo ldconfig
      ```

    - Or place it in a custom directory and add that directory to your `LD_LIBRARY_PATH`:

      ```bash
      mkdir -p ~/lib
      cp libduckdb.so ~/lib/
      export LD_LIBRARY_PATH=~/lib:$LD_LIBRARY_PATH
      ```

#### macOS

1. Extract the `libduckdb.dylib` file from the downloaded archive
2. Make sure your code can use the library. You can:

    - Either copy it to a system library directory:

      ```bash
      sudo cp libduckdb.dylib /usr/local/lib/
      ```

    - Or place it in a custom directory and add that directory to your `DYLD_LIBRARY_PATH`:

      ```bash
      mkdir -p ~/lib
      cp libduckdb.dylib ~/lib/
      export DYLD_LIBRARY_PATH=~/lib:$DYLD_LIBRARY_PATH
      ```

#### Windows

1. Extract the `duckdb.dll` file from the downloaded archive
2. Place it in one of the following locations:
   - The same directory as your application executable
   - A directory listed in your `PATH` environment variable
   - The Windows system directory (e.g., `C:\Windows\System32`)


### Understanding Library Paths

The `LD_LIBRARY_PATH` (Linux) and `DYLD_LIBRARY_PATH` (macOS) are environment variables that tell the system where to look for shared libraries at runtime. When your application tries to load `libduckdb`, the system searches these paths to locate the library file.

### Verifying Installation

You can verify that the library is properly installed and accessible:

**Linux/macOS:**
```bash
ldd path/to/your/application  # Linux
otool -L path/to/your/application  # macOS
```

## Examples

Regardless of the programming language being used, there are two database options which will be required to utilize ADBC with DuckDB. The first one is the `driver`, which takes a path to the DuckDB library (see [Setting Up the DuckDB ADBC Driver](#setting-up-the-duckdb-adbc-driver) above for installation instructions). The second option is the `entrypoint`, which is an exported function from the DuckDB-ADBC driver that initializes all the ADBC functions. Once we have configured these two options, we can optionally set the `path` option, providing a path on disk to store our DuckDB database. If not set, an in-memory database is created. After configuring all the necessary options, we can proceed to initialize our database. Below is how you can do so with various different language environments.

### C++

We begin our C++ example by declaring the essential variables for querying data through ADBC. These variables include Error, Database, Connection, Statement handling and an Arrow Stream to transfer data between DuckDB and the application.

```cpp
AdbcError adbc_error;
AdbcDatabase adbc_database;
AdbcConnection adbc_connection;
AdbcStatement adbc_statement;
ArrowArrayStream arrow_stream;
```

We can then initialize our database variable. Before initializing the database, we need to set the `driver` and `entrypoint` options as mentioned above. Then we set the `path` option and initialize the database. The `driver` option should point to your installed `libduckdb` library – see [Setting Up the DuckDB ADBC Driver](#setting-up-the-duckdb-adbc-driver) for installation instructions.

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

### Python

The first thing to do is to use `pip` and install the ADBC Driver manager. You will also need to install the `pyarrow` to directly access Apache Arrow formatted result sets (such as using `fetch_arrow_table`).

```bash
pip install adbc_driver_manager pyarrow
```

> For details on the `adbc_driver_manager` package, see the [`adbc_driver_manager` package documentation](https://arrow.apache.org/adbc/current/python/api/adbc_driver_manager.html).

As with C++, we need to provide initialization options consisting of the location of the libduckdb shared object and entrypoint function. Notice that the `path` argument for DuckDB is passed in through the `db_kwargs` dictionary.

```python
import adbc_driver_duckdb.dbapi

with adbc_driver_duckdb.dbapi.connect("test.db") as conn, conn.cursor() as cur:
    cur.execute("SELECT 42")
    # fetch a pyarrow table
    tbl = cur.fetch_arrow_table()
    print(tbl)
```

Alongside `fetch_arrow_table`, other methods from DBApi are also implemented on the cursor, such as `fetchone` and `fetchall`. Data can also be ingested via `arrow_streams`. We just need to set options on the statement to bind the stream of data and execute the query.

```python
import adbc_driver_duckdb.dbapi
import pyarrow

data = pyarrow.record_batch(
    [[1, 2, 3, 4], ["a", "b", "c", "d"]],
    names = ["ints", "strs"],
)

with adbc_driver_duckdb.dbapi.connect("test.db") as conn, conn.cursor() as cur:
    cur.adbc_ingest("AnswerToEverything", data)
```

### Go

Make sure to install the `libduckdb` library first – see [Setting Up the DuckDB ADBC Driver](#setting-up-the-duckdb-adbc-driver) for detailed installation instructions.

The following example uses an in-memory DuckDB database to modify in-memory Arrow RecordBatches via SQL queries:

{% raw %}
```go
package main

import (
    "bytes"
    "context"
    "fmt"
    "io"

    "github.com/apache/arrow-adbc/go/adbc"
    "github.com/apache/arrow-adbc/go/adbc/drivermgr"
    "github.com/apache/arrow-go/v18/arrow"
    "github.com/apache/arrow-go/v18/arrow/array"
    "github.com/apache/arrow-go/v18/arrow/ipc"
    "github.com/apache/arrow-go/v18/arrow/memory"
)

func _makeSampleArrowRecord() arrow.Record {
    b := array.NewFloat64Builder(memory.DefaultAllocator)
    b.AppendValues([]float64{1, 2, 3}, nil)
    col := b.NewArray()

    defer col.Release()
    defer b.Release()

    schema := arrow.NewSchema([]arrow.Field{{Name: "column1", Type: arrow.PrimitiveTypes.Float64}}, nil)
    return array.NewRecord(schema, []arrow.Array{col}, int64(col.Len()))
}

type DuckDBSQLRunner struct {
    ctx  context.Context
    conn adbc.Connection
    db   adbc.Database
}

func NewDuckDBSQLRunner(ctx context.Context) (*DuckDBSQLRunner, error) {
    var drv drivermgr.Driver
    db, err := drv.NewDatabase(map[string]string{
        "driver":     "duckdb",
        "entrypoint": "duckdb_adbc_init",
        "path":       ":memory:",
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create new in-memory DuckDB database: %w", err)
    }
    conn, err := db.Open(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to open connection to new in-memory DuckDB database: %w", err)
    }
    return &DuckDBSQLRunner{ctx: ctx, conn: conn, db: db}, nil
}

func serializeRecord(record arrow.Record) (io.Reader, error) {
    buf := new(bytes.Buffer)
    wr := ipc.NewWriter(buf, ipc.WithSchema(record.Schema()))
    if err := wr.Write(record); err != nil {
        return nil, fmt.Errorf("failed to write record: %w", err)
    }
    if err := wr.Close(); err != nil {
        return nil, fmt.Errorf("failed to close writer: %w", err)
    }
    return buf, nil
}

func (r *DuckDBSQLRunner) importRecord(sr io.Reader) error {
    rdr, err := ipc.NewReader(sr)
    if err != nil {
        return fmt.Errorf("failed to create IPC reader: %w", err)
    }
    defer rdr.Release()

    _, err = adbc.IngestStream(r.ctx, r.conn, rdr, "temp_table", adbc.OptionValueIngestModeCreate, adbc.IngestStreamOptions{})

    return err
}

func (r *DuckDBSQLRunner) runSQL(sql string) ([]arrow.Record, error) {
    stmt, err := r.conn.NewStatement()
    if err != nil {
        return nil, fmt.Errorf("failed to create new statement: %w", err)
    }
    defer stmt.Close()

    if err := stmt.SetSqlQuery(sql); err != nil {
        return nil, fmt.Errorf("failed to set SQL query: %w", err)
    }
    out, n, err := stmt.ExecuteQuery(r.ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to execute query: %w", err)
    }
    defer out.Release()

    result := make([]arrow.Record, 0, n)
    for out.Next() {
        rec := out.Record()
        rec.Retain() // .Next() will release the record, so we need to retain it
        result = append(result, rec)
    }
    if out.Err() != nil {
        return nil, out.Err()
    }
    return result, nil
}

func (r *DuckDBSQLRunner) RunSQLOnRecord(record arrow.Record, sql string) ([]arrow.Record, error) {
    serializedRecord, err := serializeRecord(record)
    if err != nil {
        return nil, fmt.Errorf("failed to serialize record: %w", err)
    }
    if err := r.importRecord(serializedRecord); err != nil {
        return nil, fmt.Errorf("failed to import record: %w", err)
    }
    result, err := r.runSQL(sql)
    if err != nil {
        return nil, fmt.Errorf("failed to run SQL: %w", err)
    }

    if _, err := r.runSQL("DROP TABLE temp_table"); err != nil {
        return nil, fmt.Errorf("failed to drop temp table after running query: %w", err)
    }
    return result, nil
}

func (r *DuckDBSQLRunner) Close() {
    r.conn.Close()
    r.db.Close()
}

func main() {
    rec := _makeSampleArrowRecord()
    fmt.Println(rec)

    runner, err := NewDuckDBSQLRunner(context.Background())
    if err != nil {
        panic(err)
    }
    defer runner.Close()

    resultRecords, err := runner.RunSQLOnRecord(rec, "SELECT column1+1 FROM temp_table")
    if err != nil {
        panic(err)
    }

    for _, resultRecord := range resultRecords {
        fmt.Println(resultRecord)
        resultRecord.Release()
    }
}
```
{% endraw %}

Running it produces the following output:

```go
record:
  schema:
  fields: 1
    - column1: type=float64
  rows: 3
  col[0][column1]: [1 2 3]

record:
  schema:
  fields: 1
    - (column1 + 1): type=float64, nullable
  rows: 3
  col[0][(column1 + 1)]: [2 3 4]
```
