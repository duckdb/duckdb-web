---
layout: docu
title: Rust API
selected: Client APIs
---
## Installation
The DuckDB Rust API can be installed from [crate.io](https://crates.io/crates/duckdb). Please see the [docs.rs](http://docs.rs/duckdb) for details.

## Basic API Usage
duckdb-rs is an ergonomic wrapper based on the [DuckDB C API](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb.h), please refer to the [README](https://github.com/wangfenjin/duckdb-rs) for details.

### Startup & Shutdown

To use duckdb, you must first initialize a `Connection` handle using `Connection::open()`. `Connection::open()` takes as parameter the database file to read and write from. If the database file does not exist, it will be created. You can also use `Connection::open_in_memory()` to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process).

```rust
    use duckdb::{params, Connection, Result};
    let conn = Connection::open_in_memory()?;
```

You can `conn.close()` the `Connection` manually, or just leave it out of scope, we had implement the `Drop` trait which will automatically close the underlining db connection for you.

### Querying

SQL queries can be sent to DuckDB using the `execute()` method of connections, or we can also prepare the statement and then query on that.

```rust
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

