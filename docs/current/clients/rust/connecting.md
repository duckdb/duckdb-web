---
layout: docu
redirect_from:
- /docs/clients/rust/connecting
- /docs/preview/clients/rust/connecting
- /docs/stable/clients/rust/connecting
title: Define Connections
---

## Overview

Every DuckDB feature reachable from Rust starts with a `Connection`. This page covers opening in-memory and file-backed databases, configuring a database instance with `Config`, opening read-only, pooling connections across threads, the crate's thread-safety guarantees, and closing a connection.

## Opening a Connection

A `Connection` is created with `Connection::open_in_memory()` for an in-memory database, or `Connection::open(path)` for a database file. Both return a `Result`, so the `?` operator propagates any error:

```rust
use duckdb::{Connection, Result};

// In-memory database: nothing is persisted to disk.
let conn = Connection::open_in_memory()?;

// File-backed database: created if it does not exist.
let conn = Connection::open("my_database.duckdb")?;
```

For an in-memory database no data is persisted to disk, so all data is lost when the process exits. A file-backed database is created if the file does not exist; the extension may be `.db`, `.duckdb`, or anything else.

## Configuring a Connection

To set DuckDB options when the database instance starts, build a `Config` and open the connection with `Connection::open_with_flags()` (or `Connection::open_in_memory_with_flags()`). `Config` uses a builder style: each method consumes the config and returns it, and each returns a `Result` because DuckDB validates the option:

```rust
use duckdb::{Config, Connection, Result};

let config = Config::default()
    .max_memory("4GB")?
    .threads(4)?;
let conn = Connection::open_with_flags("my_database.duckdb", config)?;
```

`Config` exposes typed methods for the most common options, including `access_mode()`, `max_memory()`, `threads()`, `default_order()`, `default_null_order()`, `enable_external_access()`, `enable_object_cache()`, `custom_user_agent()`, and `allow_unsigned_extensions()`. Any other DuckDB setting can be supplied by name with `with()`:

```rust
let config = Config::default()
    .with("temp_directory", "/path/to/temp/dir/")?
    .with("preserve_insertion_order", "false")?;
```

The full list of settings is on the [Configuration page]({% link docs/current/configuration/overview.md %}). Many of them can also be changed after connecting with a [`SET` statement]({% link docs/current/sql/statements/set.md %}) or the equivalent [`PRAGMA`]({% link docs/current/configuration/pragmas.md %}).

## Read-Only Connections

A database file can be opened in **read-only** mode, which is useful when several processes read the same file at once. Set the access mode on a `Config` with the `AccessMode` enum:

```rust
use duckdb::{AccessMode, Config, Connection, Result};

let config = Config::default().access_mode(AccessMode::ReadOnly)?;
let conn = Connection::open_with_flags("my_database.duckdb", config)?;
```

`AccessMode` has three variants: `Automatic` (the default), `ReadOnly`, and `ReadWrite`.

## Thread Safety

A `Connection` is `Send` but not `Sync`: it can be moved to another thread, but it cannot be shared between threads at the same time. The recommended pattern is one connection per thread. To open several connections to the same in-memory or file-backed database, use `Connection::try_clone()`, which opens a new connection to the already-opened database:

```rust
let conn = Connection::open("my_database.duckdb")?;
let conn2 = conn.try_clone()?; // a second connection to the same database
```

DuckDB runs queries on its own pool of native threads, sized by the `threads` option and shared by all connections to a database instance. See the [DuckDB concurrency documentation]({% link docs/current/connect/concurrency.md %}) for how connections and threads interact.

## Connection Pooling

For applications that hand a connection to each worker thread, the `r2d2` feature integrates DuckDB with the [`r2d2`](https://crates.io/crates/r2d2) connection pool. A `DuckdbConnectionManager` creates connections that the pool checks out and returns:

```rust
use duckdb::{params, DuckdbConnectionManager};

let manager = DuckdbConnectionManager::file("my_database.duckdb")?;
let pool = r2d2::Pool::new(manager)?;

// Each worker checks out its own connection from the pool.
let conn = pool.get()?;
conn.execute("INSERT INTO foo (bar) VALUES (?)", params![1])?;
```

`DuckdbConnectionManager::memory()` builds a manager for an in-memory database, and `DuckdbConnectionManager::file_with_flags()` and `memory_with_flags()` accept a `Config`. Enable the feature in `Cargo.toml` with `features = ["r2d2"]`.

## Closing a Connection

A `Connection` closes automatically when it is dropped (goes out of scope), which shuts down the underlying database. To close it explicitly and handle any error, call `close()`:

```rust
match conn.close() {
    Ok(()) => {}
    Err((_conn, err)) => eprintln!("failed to close connection: {err}"),
}
```

`close()` returns the connection back to the caller on failure, so closing can be retried. In the typical case there is little difference between an explicit `close()` and letting the connection drop, but `close()` gives a chance to observe and handle a shutdown error that `Drop` would otherwise discard.

## Further Reading

* [Run Queries]({% link docs/current/clients/rust/querying.md %}) — using the `Connection` to send queries and read results.
* [Configuration]({% link docs/current/configuration/overview.md %}) — the full list of DuckDB settings that can be passed to `Config`.
* [Concurrency]({% link docs/current/connect/concurrency.md %}) — how DuckDB handles multiple connections and threads.
* [Troubleshoot]({% link docs/current/clients/rust/known_issues.md %}) — linking and build problems encountered when opening a connection.
