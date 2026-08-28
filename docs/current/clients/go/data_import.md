---
layout: docu
redirect_from:
- /docs/clients/go/data_import
- /docs/preview/clients/go/data_import
- /docs/stable/clients/go/data_import
title: Import Data
---

## Overview

The Go client offers two ways to load data into DuckDB in bulk: the high-performance [Appender](#appender) for inserting rows generated in Go, and reading directly from [data files](#reading-data-files) such as Parquet, CSV, and JSON. Both are described below. For inserting a handful of rows, an ordinary [`INSERT` statement]({% link docs/current/clients/go/querying.md %}#sending-statements) is fine; the options here are for volume.

## Appender

The [Appender]({% link docs/current/data/appender.md %}) is the fastest way to insert rows generated in Go, much faster than issuing `INSERT` statements. It operates on a raw DuckDB connection, so it is created from a `Connector` rather than a `*sql.DB`. Obtain a connection from the connector, then create the appender for a target table with `duckdb.NewAppenderFromConn()`, passing the schema (empty for the default) and table name:

```go
connector, err := duckdb.NewConnector("test.db", nil)
if err != nil {
    log.Fatal(err)
}
defer connector.Close()

conn, err := connector.Connect(context.Background())
if err != nil {
    log.Fatal(err)
}
defer conn.Close()

// The table must already exist.
appender, err := duckdb.NewAppenderFromConn(conn, "", "users")
if err != nil {
    log.Fatal(err)
}
defer appender.Close()

// Each argument is one column value, in table column order.
if err := appender.AppendRow("Fred", int32(34)); err != nil {
    log.Fatal(err)
}
```

Each argument to `AppendRow()` is a column value in table-column order, and its Go type must match the column's DuckDB type; the example passes `int32(34)` for an `INTEGER` column. Call `AppendRow()` once per row.

> Warning The appender buffers rows and flushes them to DuckDB in chunks, so a constraint violation such as a `NOT NULL` or foreign-key failure may surface only when the buffer is flushed rather than from the `AppendRow()` call that added the offending row. Call `Flush()` and check its error to force pending rows in before relying on them, and always check the error from `Close()`, which performs a final flush.

The following is the client's complete [`appender` example](https://github.com/duckdb/duckdb-go/tree/main/examples/appender), which creates the table through a `*sql.DB` opened on the same connector, appends a row, then reads it back:

```go
package main

import (
    "context"
    "database/sql"
    "log"

    "github.com/duckdb/duckdb-go/v2"
)

func main() {
    c, err := duckdb.NewConnector("", nil)
    if err != nil {
        log.Fatal(err)
    }

    con, err := c.Connect(context.Background())
    if err != nil {
        log.Fatal(err)
    }

    db := sql.OpenDB(c)
    if _, err := db.Exec(`CREATE TABLE users (name VARCHAR, age INTEGER)`); err != nil {
        log.Fatal(err)
    }

    a, err := duckdb.NewAppenderFromConn(con, "", "users")
    if err != nil {
        log.Fatal(err)
    }

    if err := a.AppendRow("Fred", int32(34)); err != nil {
        log.Fatal(err)
    }

    // Close flushes any buffered rows before closing the appender.
    if err := a.Close(); err != nil {
        log.Fatal(err)
    }

    var (
        name string
        age  int
    )
    row := db.QueryRowContext(context.Background(), `SELECT name, age FROM users`)
    if err := row.Scan(&name, &age); err != nil {
        log.Fatal(err)
    }
    log.Printf("User: name=%s, age=%d", name, age)
}
```

### Targeting Other Schemas and Column Subsets

Two more constructors target tables outside the default schema or append only some columns:

* `duckdb.NewAppender()` takes a catalog, a schema, and a table name, for appending to a table in a specific catalog and schema.
* `duckdb.NewAppenderWithColumns()` takes a catalog, a schema, a table, and a list of column names, so that only those columns are supplied and the rest take their defaults.

## Reading Data Files

DuckDB can read many file formats directly in SQL, which is often the simplest way to load external data: the Go client just sends the query. Because the [Parquet]({% link docs/current/data/parquet/overview.md %}), [CSV]({% link docs/current/data/csv/overview.md %}), and [JSON]({% link docs/current/data/json/overview.md %}) readers are among the [bundled extensions]({% link docs/current/clients/go/overview.md %}#bundled-extensions), no extra installation is needed. Query a file in place with the matching table function:

```go
rows, err := db.QueryContext(ctx, `SELECT * FROM read_parquet('data.parquet')`)
```

The same pattern reads CSV with `read_csv()` and JSON with `read_json()`. To load a file into a table rather than query it in place, wrap the reader in a [`CREATE TABLE ... AS SELECT`]({% link docs/current/sql/statements/create_table.md %}#create-table--as-select-ctas) or [`COPY`]({% link docs/current/sql/statements/copy.md %}) statement sent with `Exec`:

```go
_, err := db.ExecContext(ctx, `CREATE TABLE data AS SELECT * FROM read_parquet('data.parquet')`)
```

## Further Reading

* [Appender]({% link docs/current/data/appender.md %}) — the engine-level Appender interface that the Go `Appender` wraps.
* [Data Import]({% link docs/current/data/overview.md %}) — DuckDB's full set of bulk-loading options.
* [Run Queries]({% link docs/current/clients/go/querying.md %}) — sending the `CREATE TABLE` and `COPY` statements the file readers build on.
* [Connect]({% link docs/current/clients/go/connecting.md %}) — creating the `Connector` and connection the Appender operates on.
</content>
