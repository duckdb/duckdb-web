---
layout: docu
redirect_from:
- /docs/clients/go/result_handling
- /docs/preview/clients/go/result_handling
- /docs/stable/clients/go/result_handling
title: Handle Results
---

## Overview

DuckDB is columnar, and beyond reading a result set [row by row]({% link docs/current/clients/go/querying.md %}#scanning-results) through `database/sql`, the Go client can exchange whole results with [Apache Arrow](https://arrow.apache.org/) as a stream of record batches, and register an Arrow stream as a queryable view. Both are described below.

## Enabling the Arrow Interface

The DuckDB Arrow interface is a heavy dependency, so starting with v2 it is opt-in. Enable it with the `duckdb_arrow` [build tag]({% link docs/current/clients/go/overview.md %}#build-tags):

```bash
go build -tags=duckdb_arrow
```

Without the tag, the Arrow types and functions described here are not compiled in. The interface builds on [`apache/arrow-go`](https://github.com/apache/arrow-go), so its `array` and `arrow` packages provide the record and schema types.

## Reading a Result as Arrow

Wrap a raw DuckDB connection with `duckdb.NewArrowFromConn()`, then call `QueryContext()` to run a query and get back an `array.RecordReader`. Iterate it with `Next()`, reading one `arrow.RecordBatch` at a time, and release it when done:

```go
connector, err := duckdb.NewConnector("", nil)
if err != nil {
    log.Fatal(err)
}
defer connector.Close()

conn, err := connector.Connect(context.Background())
if err != nil {
    log.Fatal(err)
}
defer conn.Close()

arrow, err := duckdb.NewArrowFromConn(conn)
if err != nil {
    log.Fatal(err)
}

reader, err := arrow.QueryContext(context.Background(), "SELECT * FROM generate_series(1, 10)")
if err != nil {
    log.Fatal(err)
}
defer reader.Release()

for reader.Next() {
    record := reader.RecordBatch()
    // Process one record batch at a time.
    log.Printf("%d rows", record.NumRows())
}
if err := reader.Err(); err != nil {
    log.Fatal(err)
}
```

`QueryContext()` accepts bound parameters as trailing arguments, the same as [`database/sql` queries]({% link docs/current/clients/go/querying.md %}#binding-parameters).

## Registering an Arrow Stream as a View

An Arrow stream produced elsewhere in a program, an `array.RecordReader`, can be registered as a DuckDB view and queried in SQL. `RegisterView()` takes the reader and a view name, and returns a `release` function that unregisters the view; call it when the view is no longer needed:

```go
release, err := arrow.RegisterView(reader, "my_arrow_view")
if err != nil {
    log.Fatal(err)
}
defer release()

result, err := arrow.QueryContext(context.Background(),
    "SELECT count(*) FROM my_arrow_view")
```

DuckDB scans the registered view like any other table, so it can be filtered, joined, and aggregated in SQL.

> Warning Arrow connections are not safe for concurrent use, and they do not benefit from `database/sql` connection pooling. Use one Arrow handle per connection, and do not share it across goroutines.

## Further Reading

* [Run Queries]({% link docs/current/clients/go/querying.md %}) — sending the queries whose results this page reads, and reading them row by row.
* [Build Tags]({% link docs/current/clients/go/overview.md %}#build-tags) — the `duckdb_arrow` tag that enables the Arrow interface, and the other build tags.
* [Write User Defined Functions]({% link docs/current/clients/go/functions.md %}) — replacement scans, another way to expose external data to SQL.
</content>
