---
layout: docu
redirect_from:
- /docs/clients/rust/functions
- /docs/preview/clients/rust/functions
- /docs/stable/clients/rust/functions
title: Define Functions
---

## Overview

The Rust client can register user-defined functions written in Rust: scalar functions with the `vscalar` feature and table functions with the `vtab` feature. Both operate on DuckDB's columnar data chunks, so a single call processes a batch of rows. This page covers building and registering both, and points to the template for packaging them as a loadable extension.

## Scalar Functions

A scalar function is a type that implements the `VScalar` trait, registered on a connection with `register_scalar_function()`. DuckDB calls the function's `invoke()` once per data chunk, passing a batch of input rows and expecting the corresponding output values written back. `signatures()` declares the argument and return types.

The following defines `add_one(BIGINT) -> BIGINT`, adapted from the crate's [`vscalar` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/vscalar.rs). It reads the single `BIGINT` argument as a slice of `i64` and writes each result into the output vector:

```rust
use duckdb::{
    Connection, Result,
    core::{DataChunkHandle, LogicalTypeHandle, LogicalTypeId},
    vscalar::{ScalarFunctionSignature, VScalar},
    vtab::arrow::WritableVector,
};

struct AddOne;

impl VScalar for AddOne {
    // No per-function state is needed.
    type State = ();

    fn invoke(
        _: &Self::State,
        input: &mut DataChunkHandle,
        output: &mut dyn WritableVector,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let len = input.len();
        let src = input.flat_vector(0);
        let src = unsafe { src.as_slice_with_len::<i64>(len) };

        let mut out = output.flat_vector();
        let dst = unsafe { out.as_mut_slice_with_len::<i64>(len) };

        for (d, s) in dst.iter_mut().zip(src) {
            *d = s + 1;
        }
        Ok(())
    }

    fn signatures() -> Vec<ScalarFunctionSignature> {
        vec![ScalarFunctionSignature::exact(
            vec![LogicalTypeHandle::from(LogicalTypeId::Bigint)],
            LogicalTypeHandle::from(LogicalTypeId::Bigint),
        )]
    }
}

fn main() -> Result<()> {
    let conn = Connection::open_in_memory()?;
    conn.register_scalar_function::<AddOne>("add_one")?;

    let mut stmt = conn.prepare("SELECT add_one(i) FROM range(5) t(i)")?;
    let values: Vec<i64> = stmt.query_map([], |row| row.get(0))?.collect::<Result<_>>()?;
    assert_eq!(values, vec![1, 2, 3, 4, 5]);
    Ok(())
}
```

Once registered, the function is called from SQL by the name passed to `register_scalar_function()`:

```sql
SELECT add_one(41);
```

The `associated type State` holds any per-function state shared across calls; use `()` when none is needed. The example reads its input as a typed slice for brevity and assumes non-null input; a production function should also check each value's validity. This feature requires `features = ["vscalar"]`.

## Table Functions

A table function is a type that implements the `VTab` trait, registered with `register_table_function()` and queried like any other table. `VTab` splits the work across three callbacks:

* `bind` runs once when the statement is prepared. It declares the result columns with `add_result_column()` and reads the call's arguments with `get_parameter()`, returning read-only bind data.
* `init` runs once before execution and returns per-scan state, such as a cursor.
* `func` produces one chunk of rows per call. It fills the output vectors and sets the chunk length; a length of `0` ends the scan. DuckDB calls it repeatedly until the scan is done, so a large result is delivered over several calls.
* `parameters` declares the function's parameter types.

The crate's [`vtab` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/vtab.rs) defines a `numbers(BIGINT)` function that returns one row per integer in `0..count`, over columns of increasing complexity. Its skeleton, showing the bind data, init state, and per-chunk execution model:

```rust
use duckdb::{
    Connection, Result,
    core::{DataChunkHandle, LogicalTypeHandle, LogicalTypeId},
    vtab::{BindInfo, InitInfo, TableFunctionInfo, VTab},
};
use std::sync::atomic::{AtomicUsize, Ordering};

struct Numbers;

// Computed once from the call's arguments; read-only during execution.
struct NumbersBind {
    count: usize,
}

// Tracks scan progress: func is called once per output chunk.
struct NumbersInit {
    cursor: AtomicUsize,
}

impl VTab for Numbers {
    type BindData = NumbersBind;
    type InitData = NumbersInit;

    fn bind(bind: &BindInfo) -> Result<Self::BindData, Box<dyn std::error::Error>> {
        bind.add_result_column("n", LogicalTypeId::Bigint.into());
        let count = bind.get_parameter(0).to_int64().max(0) as usize;
        Ok(NumbersBind { count })
    }

    fn init(_: &InitInfo) -> Result<Self::InitData, Box<dyn std::error::Error>> {
        Ok(NumbersInit { cursor: AtomicUsize::new(0) })
    }

    fn func(
        func: &TableFunctionInfo<Self>,
        output: &mut DataChunkHandle,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let count = func.get_bind_data().count;
        let cursor = &func.get_init_data().cursor;

        // A chunk holds at most a vector's worth of rows.
        let capacity = output.flat_vector(0).capacity();
        let start = cursor.fetch_add(capacity, Ordering::Relaxed);
        if start >= count {
            output.set_len(0); // no more rows: end the scan
            return Ok(());
        }
        let rows = capacity.min(count - start);

        let mut v = output.flat_vector(0);
        let slice = unsafe { v.as_mut_slice_with_len::<i64>(rows) };
        for (i, slot) in slice.iter_mut().enumerate() {
            *slot = (start + i) as i64;
        }
        output.set_len(rows);
        Ok(())
    }

    fn parameters() -> Option<Vec<LogicalTypeHandle>> {
        Some(vec![LogicalTypeId::Bigint.into()])
    }
}

fn main() -> Result<()> {
    let conn = Connection::open_in_memory()?;
    conn.register_table_function::<Numbers>("numbers")?;

    let total: i64 = conn.query_row("SELECT count(*) FROM numbers(5000)", [], |row| row.get(0))?;
    assert_eq!(total, 5000);
    Ok(())
}
```

```sql
SELECT * FROM numbers(6);
```

Because `func` claims its slice of the result with an atomic `fetch_add`, the scan stays correct even when DuckDB runs it on multiple threads. The full example also populates `DOUBLE`, `VARCHAR` (with `NULL` handling via `set_null`), `LIST<BIGINT>`, and `STRUCT` columns, showing how to write each vector kind. The Rust table function interface mirrors DuckDB's [C API table functions]({% link docs/current/clients/c/api.md %}) as closely as possible. This feature requires `features = ["vtab"]`; the `vtab-arrow` feature adds the built-in `ArrowVTab`, covered in [Handle Results]({% link docs/current/clients/rust/result_handling.md %}#querying-an-arrow-batch).

## Building a Loadable Extension

The functions above are registered on a `Connection` inside a client application. The same `VScalar` and `VTab` interfaces can instead be packaged as a [loadable DuckDB extension]({% link docs/current/core_extensions/overview.md %}) that any DuckDB client can `LOAD`. This uses the `loadable-extension` feature and the `duckdb_entrypoint_c_api` macro to declare the extension entry point; the crate's [`hello-ext` example](https://github.com/duckdb/duckdb-rs/tree/main/crates/duckdb/examples/hello-ext) registers a `hello(name)` table function this way.

> Warning Enable `loadable-extension` only when building an extension. In a client application, that feature makes calls such as `Connection::open_in_memory()` panic, because they run outside an extension context.

A plain `cargo build` does not produce a loadable file: DuckDB requires a file ending in `.duckdb_extension` with a valid metadata footer. Start from the official [extension-template-rs](https://github.com/duckdb/extension-template-rs) template, whose `make debug` produces a `.duckdb_extension` that loads with `duckdb -unsigned`.

## Further Reading

* [Handle Results]({% link docs/current/clients/rust/result_handling.md %}) — the built-in `ArrowVTab` table function and the Arrow vector API shared with user-defined functions.
* [C API]({% link docs/current/clients/c/api.md %}) — the table function interface that the Rust `VTab` API mirrors.
* [Extensions]({% link docs/current/core_extensions/overview.md %}) — DuckDB's extension system that a loadable Rust extension plugs into.
* [Run Queries]({% link docs/current/clients/rust/querying.md %}) — calling registered functions from SQL.
