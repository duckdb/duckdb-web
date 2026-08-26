---
layout: docu
redirect_from:
- /docs/clients/rust/result_handling
- /docs/preview/clients/rust/result_handling
- /docs/stable/clients/rust/result_handling
title: Handle Results
---

## Overview

Beyond reading a result set [row by row]({% link docs/current/clients/rust/querying.md %}#mapping-rows-to-rust-values), the Rust client can hand a query result to [Apache Arrow](https://arrow.apache.org/) as a stream of record batches, register an Arrow batch as a queryable table, and return results as [Polars](https://pola.rs/) data frames. Each of these columnar result-handling options is described below.

## Apache Arrow

DuckDB is columnar, and its native way to return a result to Rust in bulk is [Apache Arrow](https://arrow.apache.org/). The crate re-exports the [`arrow`](https://docs.rs/arrow) crate, so no separate Arrow dependency or version alignment is required: reach the Arrow types through `duckdb::arrow`.

### Reading a Result as Arrow

Call `query_arrow()` on a prepared statement to get an iterator of `RecordBatch`. Collecting it materializes the whole result, while iterating it reads one batch at a time:

```rust
use duckdb::{Connection, Result};
use duckdb::arrow::record_batch::RecordBatch;
use duckdb::arrow::util::pretty::print_batches;

let conn = Connection::open_in_memory()?;
let mut stmt = conn.prepare("SELECT * FROM generate_series(1, 5)")?;
let batches: Vec<RecordBatch> = stmt.query_arrow([])?.collect();
print_batches(&batches).unwrap();
```

`get_schema()` on the returned handle reports the Arrow schema DuckDB inferred for the result.

### Streaming Arrow Results

`query_arrow()` runs the statement to completion and buffers the whole result on the client side, so a large result is held in memory even while the iterator is advanced one batch at a time. For a result that should be consumed lazily, fetching chunks only as the iterator advances, use `stream_arrow()`, which is otherwise identical:

```rust
let mut stmt = conn.prepare("SELECT * FROM big_table")?;
for batch in stmt.stream_arrow([])? {
    // process one RecordBatch at a time
    println!("{} rows", batch.num_rows());
}
```

DuckDB may still materialize the result internally for some statements. The streaming iterator panics if fetching or Arrow conversion fails after execution has started.

### Querying an Arrow Batch

An Arrow `RecordBatch` produced elsewhere in a Rust program can be registered as a DuckDB table function and queried in SQL. Enable the `vtab-arrow` feature, register the built-in `ArrowVTab` table function on the connection, and pass the batch as a query parameter with `arrow_recordbatch_to_query_params()`. The following is adapted from the crate's [`arrow_vtab` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/arrow_vtab.rs):

```rust
use duckdb::{Connection, arrow::record_batch::RecordBatch};
use duckdb::vtab::arrow::{arrow_recordbatch_to_query_params, ArrowVTab};

let conn = Connection::open_in_memory()?;
conn.register_table_function::<ArrowVTab>("arrow")?;

let params = arrow_recordbatch_to_query_params(cities_batch);
let batches: Vec<RecordBatch> = conn
    .prepare(
        "SELECT city, population
         FROM arrow(?, ?)
         WHERE coastal AND population >= 500000
         ORDER BY population DESC",
    )?
    .query_arrow(params)?
    .collect();
```

The batch is addressed by the name given to `register_table_function()` (`arrow` here), and DuckDB filters, orders, and aggregates it like any other table. `arrow_recordbatch_to_query_params()` expands a batch into the two parameters the `arrow(?, ?)` function expects.

## Polars Data Frames

With the `polars` feature enabled, a query result can be returned as [Polars](https://pola.rs/) `DataFrame`s. Call `query_polars()` on a prepared statement to get an iterator of data frames, one per result chunk:

```rust
use duckdb::{Connection, Result};
use polars::prelude::DataFrame;

let conn = Connection::open_in_memory()?;
let mut stmt = conn.prepare("SELECT * FROM test")?;
let dfs: Vec<DataFrame> = stmt.query_polars([])?.collect();
```

To combine the chunks into a single `DataFrame`, use [`accumulate_dataframes_vertical_unchecked`](https://docs.rs/polars-core/latest/polars_core/utils/fn.accumulate_dataframes_vertical_unchecked.html) from `polars_core`. The crate re-exports `polars`, so its types are also reachable through `duckdb::polars`.

## Further Reading

* [Run Queries]({% link docs/current/clients/rust/querying.md %}) — sending the queries whose results this page reads, and reading them row by row.
* [Write User Defined Functions]({% link docs/current/clients/rust/functions.md %}) — writing table functions, of which the built-in `ArrowVTab` is one.
* [Import Data]({% link docs/current/clients/rust/data_import.md %}) — appending Arrow record batches into a table with the `appender-arrow` feature.
