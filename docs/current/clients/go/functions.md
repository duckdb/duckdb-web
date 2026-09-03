---
layout: docu
redirect_from:
- /docs/clients/go/functions
- /docs/preview/clients/go/functions
- /docs/stable/clients/go/functions
title: Write User Defined Functions
---

## Overview

The Go client can register user-defined functions written in Go: [scalar functions](#scalar-functions) that map input rows to a single output value, and [table functions](#table-functions) that produce a set of rows. It can also register a [replacement scan](#replacement-scans) that rewrites an unresolved table name into a query. All three are registered on a connection checked out with `db.Conn()`, and the function is then callable from SQL like any built-in. The sections below build and register each.

## Scalar Functions

A scalar function is a Go type that implements the `duckdb.ScalarFunc` interface, which has two methods:

* `Config()` returns a `duckdb.ScalarFuncConfig` declaring the input parameter types, the result type, and, for a variadic function, the variadic parameter type. Types are built with `duckdb.NewTypeInfo()` and the composite constructors such as `duckdb.NewListInfo()`.
* `Executor()` returns a `duckdb.ScalarFuncExecutor` holding the callback. The simplest form is `RowExecutor`, a `func(values []driver.Value) (any, error)` called once per row.

Register an instance on a connection with `duckdb.RegisterScalarUDF()`. The following defines `my_length(VARCHAR) -> INTEGER`, adapted from the client's [`scalar_udf` example](https://github.com/duckdb/duckdb-go/tree/main/examples/scalar_udf):

```go
type varcharLen struct{}

func (*varcharLen) Config() duckdb.ScalarFuncConfig {
    inputType, err := duckdb.NewTypeInfo(duckdb.TYPE_VARCHAR)
    check(err)
    resultType, err := duckdb.NewTypeInfo(duckdb.TYPE_INTEGER)
    check(err)

    return duckdb.ScalarFuncConfig{
        InputTypeInfos: []duckdb.TypeInfo{inputType},
        ResultTypeInfo: resultType,
    }
}

func (*varcharLen) Executor() duckdb.ScalarFuncExecutor {
    return duckdb.ScalarFuncExecutor{
        RowExecutor: func(values []driver.Value) (any, error) {
            return int32(len(values[0].(string))), nil
        },
    }
}

func main() {
    db, err := sql.Open("duckdb", "")
    check(err)
    defer db.Close()

    conn, err := db.Conn(context.Background())
    check(err)
    defer conn.Close()

    var udf *varcharLen
    check(duckdb.RegisterScalarUDF(conn, "my_length", udf))

    var length int32
    row := db.QueryRow(`SELECT my_length('hello world')`)
    check(row.Scan(&length)) // 11
}
```

Once registered, the function is called from SQL by the name passed to `RegisterScalarUDF()`:

```sql
SELECT my_length('hello world');
```

Set `VariadicTypeInfo` in the config to accept a variable number of trailing arguments; use `duckdb.TYPE_ANY` for it to accept any type. To register several overloads under one name, for example one taking a `VARCHAR` and another taking a `LIST`, implement each as its own `ScalarFunc` and register them together with `duckdb.RegisterScalarUDFSet()`:

```go
check(duckdb.RegisterScalarUDFSet(conn, "my_length", varcharUDF, listUDF))
```

For a callback that processes a whole data chunk at once rather than a row at a time, set `ChunkContextExecutor` in the executor instead of `RowExecutor`; the [`scalar_udf` example](https://github.com/duckdb/duckdb-go/tree/main/examples/scalar_udf) demonstrates both.

## Table Functions

A table function produces rows and is queried in the `FROM` clause. It is described by a `duckdb.RowTableFunction`, whose `Config` declares the argument types and whose `BindArguments` callback is invoked once per call to bind the arguments and return a *table source*. The table source drives execution through its methods:

* `ColumnInfos()` declares the result columns, each a `duckdb.ColumnInfo` with a name and a `TypeInfo`.
* `Init()` runs once before the scan.
* `FillRow()` is called repeatedly, filling one `duckdb.Row` per call with `duckdb.SetRowValue()` and returning `true` while there are more rows, `false` to end the scan.
* `Cardinality()` returns an optional row-count estimate.

Register the function with `duckdb.RegisterTableUDF()`. The following defines `increment(BIGINT)`, which returns one row per integer up to the argument, adapted from the client's [`table_udf` example](https://github.com/duckdb/duckdb-go/tree/main/examples/table_udf):

```go
type incrementTableUDF struct {
    tableSize  int64
    currentRow int64
}

func bindTableUDF(namedArgs map[string]any, args ...any) (duckdb.RowTableSource, error) {
    return &incrementTableUDF{
        currentRow: 0,
        tableSize:  args[0].(int64),
    }, nil
}

func (udf *incrementTableUDF) ColumnInfos() []duckdb.ColumnInfo {
    t, err := duckdb.NewTypeInfo(duckdb.TYPE_BIGINT)
    check(err)
    return []duckdb.ColumnInfo{{Name: "result", T: t}}
}

func (udf *incrementTableUDF) Init() {}

func (udf *incrementTableUDF) FillRow(row duckdb.Row) (bool, error) {
    if udf.currentRow+1 > udf.tableSize {
        return false, nil // no more rows: end the scan
    }
    udf.currentRow++
    err := duckdb.SetRowValue(row, 0, udf.currentRow)
    return true, err
}

func (udf *incrementTableUDF) Cardinality() *duckdb.CardinalityInfo {
    return &duckdb.CardinalityInfo{Cardinality: uint(udf.tableSize), Exact: true}
}

func main() {
    db, err := sql.Open("duckdb", "")
    check(err)
    defer db.Close()

    conn, err := db.Conn(context.Background())
    check(err)
    defer conn.Close()

    t, err := duckdb.NewTypeInfo(duckdb.TYPE_BIGINT)
    check(err)
    udf := duckdb.RowTableFunction{
        Config:        duckdb.TableFunctionConfig{Arguments: []duckdb.TypeInfo{t}},
        BindArguments: bindTableUDF,
    }
    check(duckdb.RegisterTableUDF(conn, "increment", udf))

    rows, err := db.QueryContext(context.Background(), `SELECT * FROM increment(100)`)
    check(err)
    defer rows.Close()
}
```

```sql
SELECT * FROM increment(100);
```

For a function whose scan can run on several threads, implement `duckdb.ParallelRowTableSource` and register a `duckdb.ParallelRowTableFunction` instead. Its `Init()` returns a `duckdb.ParallelTableSourceInfo` that sets `MaxThreads`, a `NewLocalState()` method provides per-thread state, and `FillRow()` receives that state so each thread can claim and emit its own range of rows. The client's [`table_udf_parallel` example](https://github.com/duckdb/duckdb-go/tree/main/examples/table_udf_parallel) shows the full pattern.

## Replacement Scans

A replacement scan intercepts a query that references a table name DuckDB cannot resolve and rewrites it into a table function call. Register one on a `Connector` with `duckdb.RegisterReplacementScan()`, passing a callback of type `duckdb.ReplacementScanCallback`. The callback receives the unresolved table name and returns the replacement function name and its arguments:

```go
connector, err := duckdb.NewConnector("", nil)
check(err)
defer connector.Close()

duckdb.RegisterReplacementScan(connector, func(tableName string) (string, []any, error) {
    // Treat any bare table name as a Parquet file of that name.
    return "read_parquet", []any{tableName + ".parquet"}, nil
})

db := sql.OpenDB(connector)
// SELECT * FROM foo now reads from read_parquet('foo.parquet').
```

Returning an error from the callback surfaces it as a query error. This is the mechanism DuckDB clients use to make external data sources appear as ordinary tables.

## Further Reading

* [Run Queries]({% link docs/current/clients/go/querying.md %}) — calling registered functions from SQL.
* [Handle Results]({% link docs/current/clients/go/result_handling.md %}) — registering an Arrow stream as a queryable view, a related way to expose external data.
* [Connect]({% link docs/current/clients/go/connecting.md %}) — checking out the connection that functions are registered on, and the connector for replacement scans.
</content>
