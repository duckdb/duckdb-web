---
github_repository: https://github.com/duckdb/duckdb-rs
layout: docu
redirect_from:
- /docs/api/rust
- /docs/clients/rust
- /docs/clients/rust/overview
- /docs/current/clients/rust
- /docs/preview/clients/rust
- /docs/preview/clients/rust/overview
- /docs/stable/clients/rust
- /docs/stable/clients/rust/overview
title: Rust Client
---

> Installation To use the DuckDB Rust client, visit the [Rust installation page]({% link install/index.html %}?environment=rust).
>
> The latest stable version of the DuckDB Rust client is {% if site.current_duckdb_rust_version != "" %}{{ site.current_duckdb_rust_version }}{% else %}{{ site.lts_duckdb_rust_version }}{% endif %}.

The DuckDB Rust client, [`duckdb-rs`](https://github.com/duckdb/duckdb-rs), is an ergonomic wrapper over the [DuckDB C API](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb.h) that exposes an interface modeled on [rusqlite](https://github.com/rusqlite/rusqlite). It supports type-safe queries, bulk loading with the Appender, [Apache Arrow](https://arrow.apache.org/) interchange, user-defined functions, and building DuckDB extensions in Rust. This page covers installation; the other pages in this section cover connecting and each feature in detail.

## Installation

The DuckDB Rust client is published on [crates.io](https://crates.io/crates/duckdb). The full API is documented on [docs.rs](https://docs.rs/duckdb). Add it to a project with `cargo`, enabling the `bundled` feature so that DuckDB is compiled from source and no system library is required:

```bash
cargo add duckdb --features bundled
```

The equivalent `Cargo.toml` entry pins the version. Starting with DuckDB v1.5.0 the crate version has the form `1.⟨major_minor_patch⟩.x`; a tilde requirement receives patch releases without changing the bundled DuckDB version:

```toml
[dependencies]
duckdb = { version = "~1.10505.0", features = ["bundled"] }
```

The `bundled` feature is the simplest way to get started. Without it, the [`libduckdb-sys`](https://crates.io/crates/libduckdb-sys) crate links against a system DuckDB library instead of compiling one, which is covered in [Troubleshoot]({% link docs/current/clients/rust/known_issues.md %}#linking-against-a-system-library).

To track the latest bindings before they are released on crates.io, depend on the `main` branch or a specific commit from git. The bundled DuckDB version is whatever that commit vendors:

```toml
[dependencies]
# Latest development version
duckdb = { git = "https://github.com/duckdb/duckdb-rs", branch = "main", features = ["bundled"] }

# A specific commit
duckdb = { git = "https://github.com/duckdb/duckdb-rs", rev = "abc123def", features = ["bundled"] }
```

For the LTS release line that stays on DuckDB 1.4 Andium, use the `v1.4-andium` branch.

> Tip The Rust client offers a large set of Cargo [feature flags](#feature-flags) that turn on file-format readers, the Arrow and Polars integrations, connection pooling, and the function and extension interfaces. Enable only the features a project uses to keep build times and binary size down.

## Basic API Usage

To use DuckDB, first initialize a `Connection` with `Connection::open_in_memory()` for an in-memory database, or `Connection::open(path)` for a database file. Queries are sent with `execute()` and `execute_batch()`, and results are read by preparing a statement and mapping each row to a Rust value with `query_map()`:

```rust
use duckdb::{params, Connection, Result};

#[derive(Debug)]
struct Person {
    id: i32,
    name: String,
    data: Option<Vec<u8>>,
}

fn main() -> Result<()> {
    let conn = Connection::open_in_memory()?;

    conn.execute_batch(
        r"CREATE SEQUENCE seq;
          CREATE TABLE person (
              id   INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq'),
              name TEXT NOT NULL,
              data BLOB
          );",
    )?;

    let me = Person {
        id: 0,
        name: "Steven".to_string(),
        data: None,
    };
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
    Ok(())
}
```

This example is adapted from the crate's [`basic` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/basic.rs). [Run Queries]({% link docs/current/clients/rust/querying.md %}) covers sending queries and reading results in full.

## Feature Flags

The crate is modular: most integrations are gated behind Cargo features that are off by default. Enable them in the dependency declaration, for example `features = ["bundled", "vtab", "appender-arrow"]`. The following is the complete set of the crate's Cargo features, grouped by purpose.

### Building DuckDB

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `bundled` | Compile DuckDB from the bundled source with the `cc` crate, so no system library is needed. |
| `bundled-cmake` | Experimental. Compile the bundled source with DuckDB's upstream CMake build instead of `cc`, which is required for the bundled extensions below. Only available from a `git` checkout, not from crates.io. Implies `bundled` and `parquet`. |
| `buildtime_bindgen` | Regenerate the C API bindings at build time with `bindgen` instead of using the shipped pregenerated bindings. |

### File Formats

Both imply `bundled`.

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `json` | Reading and writing [JSON]({% link docs/current/data/json/overview.md %}), statically linked. |
| `parquet` | Reading and writing [Parquet]({% link docs/current/data/parquet/overview.md %}), statically linked. |

### Bundled Extensions

Each statically links the matching bundled extension. All imply `bundled-cmake`, so they need a `git` checkout.

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `autocomplete` | The autocomplete extension. |
| `icu` | The [ICU extension]({% link docs/current/core_extensions/icu.md %}) for locale-aware and time-zone-aware operations, which the plain `bundled` build omits. |
| `tpch` | The TPC-H benchmark extension. |
| `tpcds` | The TPC-DS benchmark extension. |

### Table and Scalar Functions

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `vtab` | Base support for [table functions]({% link docs/current/clients/rust/functions.md %}#table-functions). |
| `vtab-arrow` | [Apache Arrow](https://arrow.apache.org/) integration for table functions, converting between an Arrow `RecordBatch` and DuckDB data chunks. Implies `vtab`. |
| `vscalar` | [Scalar functions]({% link docs/current/clients/rust/functions.md %}#scalar-functions). Implies `vtab-arrow`. |
| `vscalar-arrow` | Arrow-optimized scalar functions, intended for use alongside `vscalar`. |
| `appender-arrow` | Append Arrow `RecordBatch`es through the [Appender]({% link docs/current/clients/rust/data_import.md %}#appender). Implies `vtab-arrow`. |
| `loadable-extension` | Experimental. Build a loadable DuckDB extension rather than a client application. See [Building a Loadable Extension]({% link docs/current/clients/rust/functions.md %}#building-a-loadable-extension). |

### Ecosystem Integrations

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `polars` | Exchange query results as [Polars](https://pola.rs/) data frames. See [Handle Results]({% link docs/current/clients/rust/result_handling.md %}#polars-data-frames). |
| `r2d2` | A connection pool through the [`r2d2`](https://crates.io/crates/r2d2) crate. See [Define Connections]({% link docs/current/clients/rust/connecting.md %}#connection-pooling). |
| `chrono` | `ToSql` and `FromSql` conversions for `chrono` date and time types. |
| `rust_decimal` | `ToSql` and `FromSql` conversions for `rust_decimal::Decimal`. |
| `serde_json` | `ToSql` and `FromSql` conversions for `serde_json::Value`. |
| `url` | `ToSql` and `FromSql` conversions for `url::Url`. |
| `uuid` | `ToSql` and `FromSql` conversions for `uuid::Uuid`. |

### Umbrella Features

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `vtab-full` | `vtab-arrow` and `appender-arrow`, plus the deprecated `vtab-excel`. |
| `extensions-full` | `json`, `parquet` and `vtab-full`. |
| `modern-full` | `chrono`, `serde_json`, `url`, `r2d2`, `uuid`, `polars` and `rust_decimal`. |

### Deprecated Features

<div class="monospace_table"></div>

| Feature | Enables |
|--|--|
| `vtab-excel` | A no-op retained for feature compatibility. |
| `vtab-loadable` | Superseded by `loadable-extension`. |

## Further Reading

* [Define Connections]({% link docs/current/clients/rust/connecting.md %}) — opening in-memory and file-backed databases, `Config` options, connection pooling, and thread safety.
* [Run Queries]({% link docs/current/clients/rust/querying.md %}) — `execute()`, prepared statements, parameter binding, and mapping rows to Rust types.
* [Import Data]({% link docs/current/clients/rust/data_import.md %}) — bulk loading with the Appender and reading directly from Parquet, CSV, and JSON files.
* [Handle Results]({% link docs/current/clients/rust/result_handling.md %}) — Apache Arrow and Polars result interchange.
* [Define Functions]({% link docs/current/clients/rust/functions.md %}) — user-defined scalar and table functions, and loadable extensions.
* [Profile and Monitor]({% link docs/current/clients/rust/profiling.md %}) — query profiling and interrupting long-running queries.
* [Troubleshoot]({% link docs/current/clients/rust/known_issues.md %}) — linking, the ICU extension, and extension-versus-client build issues.
* [Clients Overview]({% link docs/current/clients/overview.md %}) — the other client APIs DuckDB provides alongside Rust.
