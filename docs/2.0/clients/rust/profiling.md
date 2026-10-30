---
layout: docu
redirect_from:
- /docs/clients/rust/profiling
- /docs/stable/clients/rust/profiling
- /docs/current/clients/rust/profiling
- /docs/lts/clients/rust/profiling
- /docs/preview/clients/rust/profiling
title: Profile and Monitor
---

## Overview

The Rust client can observe a running or completed query: it can retrieve per-operator [profiling metrics](#profiling) after a query runs, and [interrupt](#interrupting-queries) a long-running query from another thread. Both are shown below.

## Profiling

Profiling must be enabled on a connection before metrics are collected. Enable it with the [`enable_profiling` PRAGMA]({% link docs/2.0/dev/profiling.md %}), run a query, then read the result with `get_profiling_info()`:

```rust
use duckdb::Connection;

let conn = Connection::open_in_memory()?;

// Do not print profiling output to stdout after each query (the default when profiling is enabled).
conn.execute("PRAGMA enable_profiling = 'no_output'", [])?;

conn.execute("SELECT 42", [])?;

let info = conn.get_profiling_info().expect("profiling should be enabled");
println!("profiled children: {}", info.children.len());
```

`get_profiling_info()` returns an `Option<ProfilingInfo>`, which is `None` when profiling is not enabled. `ProfilingInfo` is a tree whose metrics are grouped and named in lowercase (see the [metrics list]({% link docs/2.0/dev/metrics.md %})): the root's children are the root plan operator, with metrics such as `type`, `timing`, and `intermediate_rows`, followed by one node per metric group, such as `query` with `total_time`. Read a node's metrics through its `metrics` map and its children through `children`.

## Interrupting Queries

A long-running query can be cancelled from another thread. Call `interrupt_handle()` on the connection to get an `Arc<InterruptHandle>`. `InterruptHandle` is both `Send` and `Sync`, so you can move it, or the connection, to another thread and call `interrupt()` from wherever is convenient. The interrupted query fails with an error:

```rust
use duckdb::{Connection, Result};

fn run_query(conn: Connection) -> Result<()> {
    let interrupt_handle = conn.interrupt_handle();

    let join_handle = std::thread::spawn(move || {
        conn.execute("⟨expensive query⟩", [])
    });

    // ... later, from this thread, cancel the query:
    interrupt_handle.interrupt();

    let query_result = join_handle.join().unwrap();
    assert!(query_result.is_err());
    Ok(())
}
```

`interrupt()` cancels whichever query is currently running on the connection the handle was obtained from. If the connection has already been dropped, calling `interrupt()` is a no-op.

## Further Reading

* [Profiling]({% link docs/2.0/dev/profiling.md %}) — DuckDB's query profiling output and the `enable_profiling` PRAGMA and the `tracked_metrics` setting.
* [Run Queries]({% link docs/2.0/clients/rust/querying.md %}) — running the queries whose metrics this page reads and whose execution it interrupts.
* [Connect]({% link docs/2.0/clients/rust/connecting.md %}) — the `Connection` that profiling and the interrupt handle operate on.
