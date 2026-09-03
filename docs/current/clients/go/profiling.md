---
layout: docu
redirect_from:
- /docs/clients/go/profiling
- /docs/preview/clients/go/profiling
- /docs/stable/clients/go/profiling
title: Profile and Monitor
---

## Overview

The Go client can observe query execution: it can retrieve per-operator [profiling metrics](#profiling) after a query runs, and register a [log storage](#log-storage) that receives DuckDB's log messages. Both are described below.

## Profiling

Profiling information is connection-local, so it is read from a `*sql.Conn` checked out with `db.Conn()`. Enable profiling on that connection with the [`enable_profiling` and `profiling_mode` PRAGMAs]({% link docs/current/dev/profiling.md %}), run the query to profile, then read the result with `duckdb.GetProfilingInfo()`:

```go
db, err := sql.Open("duckdb", "")
check(err)
defer db.Close()

conn, err := db.Conn(context.Background())
check(err)
defer conn.Close()

// Do not print profiling output to stdout after each query.
_, err = conn.ExecContext(context.Background(), `PRAGMA enable_profiling = 'no_output'`)
check(err)
// Collect a comprehensive set of metrics per operator.
_, err = conn.ExecContext(context.Background(), `PRAGMA profiling_mode = 'detailed'`)
check(err)

// Run the query to profile.
res, err := conn.QueryContext(context.Background(), `SELECT 42`)
check(err)
res.Close()

// Retrieve the metrics collected for that query.
info, err := duckdb.GetProfilingInfo(conn)
check(err)

// Optionally, turn profiling off again.
_, err = conn.ExecContext(context.Background(), `PRAGMA disable_profiling`)
check(err)
```

`GetProfilingInfo()` returns a `duckdb.ProfilingInfo`, a tree that mirrors DuckDB's query plan. Each node has a `Metrics` map of metric name to value and a `Children` slice of child nodes. The root node (`QUERY_ROOT`) holds metrics measured over the whole query, and each descendant is a plan operator with its own metrics. Walk the tree to read them:

```go
log.Printf("query latency: %s", info.Metrics["LATENCY"])
for _, child := range info.Children {
    log.Printf("operator: %s", child.Metrics["OPERATOR_NAME"])
}
```

Which metrics are collected depends on the `profiling_mode` set on the connection; see the [Profiling page]({% link docs/current/dev/profiling.md %}) for the available modes and metric names.

## Log Storage

DuckDB can forward its [log messages]({% link docs/current/dev/profiling.md %}) to a custom storage registered from Go. Register one on a `Connector` with `duckdb.RegisterLogStorage()`, giving it a name and a `duckdb.LoggerCallbacks` whose `DefaultLoggerCallback` receives each entry's level, type, and message:

```go
connector, err := duckdb.NewConnector("", nil)
check(err)
defer connector.Close()

err = duckdb.RegisterLogStorage(connector, "my_log_storage", duckdb.LoggerCallbacks{
    DefaultLoggerCallback: func(level, logType, logMsg string) {
        log.Printf("[%s] %s: %s", level, logType, logMsg)
    },
})
check(err)

// Activate the registered storage, then DuckDB forwards log calls to the callback.
db := sql.OpenDB(connector)
_, err = db.Exec(`SET logging_storage = 'my_log_storage'`)
check(err)
```

After the storage is registered and selected with `SET logging_storage`, DuckDB forwards all log calls to the callback.

## Further Reading

* [Profiling]({% link docs/current/dev/profiling.md %}) — DuckDB's query profiling output, the `enable_profiling` and `profiling_mode` PRAGMAs, and its logging.
* [Run Queries]({% link docs/current/clients/go/querying.md %}) — running the queries whose metrics this page reads.
* [Connect]({% link docs/current/clients/go/connecting.md %}) — checking out the connection that profiling operates on, and the connector that log storage is registered on.
</content>
