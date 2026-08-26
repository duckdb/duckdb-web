---
layout: docu
redirect_from:
- /docs/clients/rust/data_import
- /docs/preview/clients/rust/data_import
- /docs/stable/clients/rust/data_import
title: Import Data
---

## Overview

The Rust client offers two ways to get data into DuckDB in bulk: the high-performance [Appender](#appender) for inserting rows from Rust, and reading directly from [data files](#reading-data-files) such as Parquet, CSV, and JSON. This page describes both.

## Appender

The [Appender]({% link docs/current/data/appender.md %}) is the fastest way to insert rows generated in Rust. Create one from a `Connection` with `appender()`, passing the target table name, then push rows with `append_row()`. Each row is a parameter list built with the `params!` macro:

```rust
use duckdb::{params, Connection, Result};

fn insert_rows(conn: &Connection) -> Result<()> {
    conn.execute_batch("CREATE TABLE foo (a INTEGER, b INTEGER)")?;

    let mut app = conn.appender("foo")?;
    app.append_row(params![1, 2])?;
    app.append_row(params![3, 4])?;
    app.flush()?;
    Ok(())
}
```

To append many rows from an iterator of parameter lists in one call, use `append_rows()`:

```rust
app.append_rows([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])?;
```

Additional constructors target tables outside the default schema: `appender_to_db()` takes a schema name, and `appender_to_catalog_and_db()` takes a catalog and a schema. To append only a subset of columns, use `appender_with_columns()` (and its schema and catalog variants).

> Warning DuckDB buffers appended rows and checks constraints such as `NOT NULL` and foreign keys only when the buffer is flushed, so `append_row()` may return `Ok` for a row that later fails a constraint check. Always call `flush()` explicitly and check its result before the appender is dropped. Dropping an appender flushes any remaining rows, but errors raised during that implicit flush are discarded, because Rust's `Drop` cannot report them.

The `Appender` is `Sync` but not `Send`, because it borrows the `Connection`. To append from another thread, move the `Connection` to that thread and create the appender there.

### Appending Inside a Transaction

For a large load, wrapping the appends in a transaction lets DuckDB commit them as a single unit. Begin a transaction with `Connection::transaction()`, set it to commit on drop, and create the appender from the transaction. The following bulk-inserts ten million rows, adapted from the crate's [`appender` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/appender.rs):

```rust
use duckdb::{params, Connection, DropBehavior, Result};

fn main() -> Result<()> {
    let mut db = Connection::open_in_memory()?;
    db.execute_batch(
        "CREATE TABLE test (id INTEGER NOT NULL, area CHAR(6), age TINYINT NOT NULL, active TINYINT NOT NULL)",
    )?;

    let row_count = 10_000_000;
    {
        let mut tx = db.transaction()?;
        tx.set_drop_behavior(DropBehavior::Commit);
        let mut app = tx.appender("test")?;
        for i in 0..row_count {
            app.append_row(params![i, "123456", 15, 1])?;
        }
    } // the appender flushes and the transaction commits here, on drop

    let count = db.query_row("SELECT count(*) FROM test", [], |row| row.get::<_, i64>(0))?;
    assert_eq!(count, row_count);
    Ok(())
}
```

A `Transaction` rolls back by default when dropped. Call `set_drop_behavior(DropBehavior::Commit)` to commit on drop instead, or call `tx.commit()` explicitly. The other `DropBehavior` variants are `Rollback` (the default), `Ignore` (leave the transaction open), and `Panic`.

### Appending Arrow Data

With the `appender-arrow` feature enabled, an Appender can append an [Apache Arrow](https://arrow.apache.org/) `RecordBatch` directly, which avoids building a parameter list per row. See [Handle Results]({% link docs/current/clients/rust/result_handling.md %}#apache-arrow) for the Arrow integration.

## Reading Data Files

DuckDB can read many file formats directly in SQL, which is often the simplest way to load external data. The Rust client just sends the query. For [Parquet]({% link docs/current/data/parquet/overview.md %}), enable the `parquet` feature and query `read_parquet()`, adapted from the crate's [`parquet` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/parquet.rs):

```rust
use duckdb::{Connection, Result};
use duckdb::arrow::record_batch::RecordBatch;

let conn = Connection::open_in_memory()?;
conn.execute_batch("INSTALL parquet; LOAD parquet;")?;

let batches: Vec<RecordBatch> = conn
    .prepare("SELECT * FROM read_parquet(?)")?
    .query_arrow(["data.parquet"])?
    .collect();
```

The same pattern reads [CSV]({% link docs/current/data/csv/overview.md %}) with `read_csv()` and [JSON]({% link docs/current/data/json/overview.md %}) with `read_json()` (the latter needs the `json` feature). To load a file into a table rather than query it in place, wrap the reader in a [`CREATE TABLE ... AS SELECT`]({% link docs/current/sql/statements/create_table.md %}#create-table--as-select-ctas) or [`COPY`]({% link docs/current/sql/statements/copy.md %}) statement sent with `execute()`.

## Further Reading

* [Appender]({% link docs/current/data/appender.md %}) — the engine-level Appender interface that the Rust `Appender` wraps.
* [Data Import]({% link docs/current/data/overview.md %}) — DuckDB's full set of bulk-loading options.
* [Handle Results]({% link docs/current/clients/rust/result_handling.md %}) — the Apache Arrow integration used to append and read record batches.
* [Run Queries]({% link docs/current/clients/rust/querying.md %}) — sending the `CREATE TABLE` and `COPY` statements the file readers build on.
