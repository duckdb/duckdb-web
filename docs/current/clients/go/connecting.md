---
layout: docu
redirect_from:
- /docs/clients/go/connecting
- /docs/preview/clients/go/connecting
- /docs/stable/clients/go/connecting
title: Connect
---

## Overview

The Go client works through the standard [`database/sql`](https://pkg.go.dev/database/sql) types: a `*sql.DB` is a pool of connections to a DuckDB database. This page covers opening in-memory and file-backed databases, passing DuckDB configuration options, running initialization steps with a `Connector`, the client's thread-safety and connection-lifetime rules, and closing a database cleanly.

## Opening a Database

`sql.Open()` takes the driver name `duckdb` and a [data source name (DSN)](#data-source-names). An empty DSN opens an in-memory database; a file path opens a persistent database, creating the file if it does not exist:

```go
// In-memory database: nothing is persisted to disk.
db, err := sql.Open("duckdb", "")
if err != nil {
    log.Fatal(err)
}
defer db.Close()

// File-backed database: created if it does not exist.
db, err := sql.Open("duckdb", "/path/to/foo.db")
```

`sql.Open()` does not necessarily open a connection: it validates its arguments and returns a `*sql.DB` that opens connections lazily. Call `db.Ping()` to verify that the database is reachable.

## Data Source Names

DuckDB [configuration options]({% link docs/current/configuration/overview.md %}) are appended to the DSN as URL-style `name=value` query parameters, separated by `&`:

```go
db, err := sql.Open("duckdb", "/path/to/foo.db?access_mode=read_only&threads=4")
```

The `access_mode=read_only` option opens a database file so that several processes can read it at once. The full list of options is on the [Configuration page]({% link docs/current/configuration/overview.md %}). Options can also be changed after connecting with a [`SET` statement]({% link docs/current/sql/statements/set.md %}).

## Running Initialization Steps with a Connector

To run setup statements before any query, or to configure DuckDB in code rather than in the DSN, create a `Connector` with `duckdb.NewConnector()` and open the database with `sql.OpenDB()`. The connector's second argument is a callback that runs against each new connection, which is where boot queries belong:

```go
connector, err := duckdb.NewConnector("/path/to/foo.db?threads=4", func(execer driver.ExecerContext) error {
    bootQueries := []string{
        "SET schema = 'main'",
        "SET search_path = 'main'",
    }
    for _, query := range bootQueries {
        if _, err := execer.ExecContext(context.Background(), query, nil); err != nil {
            return err
        }
    }
    return nil
})
if err != nil {
    log.Fatal(err)
}
defer connector.Close()

db := sql.OpenDB(connector)
defer db.Close()
```

Pass `nil` as the callback when no initialization is needed. A `Connector` is also the entry point for the [Appender]({% link docs/current/clients/go/data_import.md %}#appender), [Arrow]({% link docs/current/clients/go/result_handling.md %}), and [replacement scans]({% link docs/current/clients/go/functions.md %}#replacement-scans), which operate on an individual connection obtained from it.

## Connection-Local Operations

Some features are scoped to a single connection rather than the pool: profiling, registering user-defined functions, and the Appender all act on one connection. Check a connection out of the pool with `db.Conn()`, which returns a `*sql.Conn` that is not shared with other goroutines until it is closed:

```go
conn, err := db.Conn(context.Background())
if err != nil {
    log.Fatal(err)
}
defer conn.Close()
```

The client also exposes two helpers that take a `*sql.Conn`: `duckdb.GetTableNames()` returns the table names referenced by a query, optionally fully qualified, and `duckdb.ConnId()` returns the underlying DuckDB connection id.

## Thread Safety and Concurrency

A `*sql.DB` is safe for concurrent use by multiple goroutines: it manages its own pool of connections and hands each in-flight query a connection of its own. A single `*sql.Conn` checked out with `db.Conn()`, and the DuckDB [Appender]({% link docs/current/clients/go/data_import.md %}#appender) and [Arrow]({% link docs/current/clients/go/result_handling.md %}) handles built on one, are not safe for concurrent use. DuckDB runs queries on its own pool of native threads, sized by the `threads` option and shared across the pool. See the [DuckDB concurrency documentation]({% link docs/current/connect/concurrency.md %}) for how connections and threads interact.

## Connection Lifetime

Temporary objects such as [temporary tables]({% link docs/current/sql/statements/create_table.md %}#temporary-tables) are scoped to a connection. When code closes a connection, `database/sql` may return it to the pool as an idle connection rather than actually closing it, so a temporary table can outlive the code that created it. To make closing a connection tear it down, disable idle connections:

```go
db.SetMaxIdleConns(0)
```

## Closing a Database

DuckDB runs in the same process as the Go application, so all of its memory is held by that process. Closing the `database/sql` objects is what frees DuckDB's memory and, for a persistent database, flushes the [write-ahead log]({% link docs/current/internals/storage.md %}) to disk. Always close every object that has a `Close()` method, which `defer` makes convenient:

```go
db, err := sql.Open("duckdb", "")
defer db.Close()

conn, err := db.Conn(context.Background())
defer conn.Close()

rows, err := conn.QueryContext(context.Background(), "SELECT 42")
defer rows.Close() // or drain the rows until Next() returns false

connector, err := duckdb.NewConnector("", nil)
defer connector.Close() // if the connector is passed to sql.OpenDB
```

Failing to close a persistent database can leave changes in the write-ahead log that are not synchronized to persistent storage. For long-running applications, closing results, connections, and databases promptly is essential to keep memory in check.

## Further Reading

* [Run Queries]({% link docs/current/clients/go/querying.md %}) — using the database and connections opened here to send queries and read results.
* [Configuration]({% link docs/current/configuration/overview.md %}) — the full list of DuckDB settings that can be passed in the DSN or the connector callback.
* [Concurrency]({% link docs/current/connect/concurrency.md %}) — how DuckDB handles multiple connections and threads.
* [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}) — cgo, linking, and other build problems encountered when opening a database.
</content>
