---
github_repository: https://github.com/duckdb/duckdb-rs
layout: docu
redirect_from:
- /docs/api/rust
- /docs/clients/rust
title: Rust Client
---

> The latest stable version of the DuckDB Rust client is {{ site.current_duckdb_rust_version }}.

## Installation

The DuckDB Rust client can be installed from [crates.io](https://crates.io/crates/duckdb). Please see the [docs.rs](http://docs.rs/duckdb) for details.

## Basic API Usage

duckdb-rs is an ergonomic wrapper based on the [DuckDB C API](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb.h), please refer to the [README](https://github.com/duckdb/duckdb-rs) for details.

### Startup & Shutdown

To use duckdb, you must first initialize a `Connection` handle using `Connection::open()`. `Connection::open()` takes as parameter the database file to read and write from. If the database file does not exist, it will be created (the file extension may be `.db`, `.duckdb`, or anything else). You can also use `Connection::open_in_memory()` to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the process).

```rust
use duckdb::{params, Connection, Result};
let conn = Connection::open_in_memory()?;
```

The `Connection` will automatically close the underlying db connection for you when it goes out of scope (via `Drop`). You can also explicitly close the `Connection` with `conn.close()`. There is not much difference between these in the typical case, but in case there is an error, you'll have the chance to handle it with the explicit close.

### Querying

SQL queries can be sent to DuckDB using the `execute()` method of connections, or we can also prepare the statement and then query on that.

```rust
#[derive(Debug)]
struct Person {
    id: i32,
    name: String,
    data: Option<Vec<u8>>,
}

conn.execute(
    "INSERT INTO person (name, data) VALUES (?, ?)",
    params![me.name, me.data],
)?;

let mut stmt = conn.prepare("SELECT id, name, data FROM person")?;
let person_iter = stmt.query_map([], |row| {
    Ok(Person {
        id: row.get(0)?,
        name: row.get(1)?,
        data: row.get(2)?,
    })
})?;

for person in person_iter {
    println!("Found person {:?}", person.unwrap());
}
```

## Appender

The Rust client supports the [DuckDB Appender API]({% link docs/stable/data/appender.md %}) for bulk inserts. For example:

```rust
fn insert_rows(conn: &Connection) -> Result<()> {
    let mut app = conn.appender("foo")?;
    app.append_rows([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])?;
    Ok(())
}
```
