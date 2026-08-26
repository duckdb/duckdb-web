---
layout: docu
redirect_from:
- /docs/clients/rust/querying
- /docs/preview/clients/rust/querying
- /docs/stable/clients/rust/querying
title: Run Queries
---

## Overview

Queries are sent on a `Connection` with `execute()`, `execute_batch()`, and prepared statements, and results are read by mapping each row to a Rust value. This page covers sending statements, binding parameters, and turning rows into typed Rust values. For opening the `Connection` these run on, see [Define Connections]({% link docs/current/clients/rust/connecting.md %}).

## Sending Statements

Use `execute()` for a single statement that does not return rows, such as [`INSERT`]({% link docs/current/sql/statements/insert.md %}) or [`UPDATE`]({% link docs/current/sql/statements/update.md %}). It takes the SQL and a list of parameters, and returns the number of affected rows. Pass an empty slice `[]` when there are no parameters:

```rust
conn.execute(
    "CREATE TABLE person (id INTEGER, name TEXT, data BLOB)",
    [],
)?;

let rows_changed = conn.execute(
    "INSERT INTO person (id, name) VALUES (1, 'Steven')",
    [],
)?;
```

To run several statements at once, for example a schema-setup script, use `execute_batch()`:

```rust
conn.execute_batch(
    r"CREATE SEQUENCE seq;
      CREATE TABLE person (
          id   INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq'),
          name TEXT NOT NULL,
          data BLOB
      );",
)?;
```

## Binding Parameters

Values are bound to a statement's placeholders rather than formatted into the SQL string. DuckDB uses positional (`?`) and numbered (`?1`, `?2`) placeholders. The `params!` macro packs a heterogeneous list of values into the parameter slice:

```rust
use duckdb::params;

conn.execute(
    "INSERT INTO person (id, name, data) VALUES (?, ?, ?)",
    params![1, "Steven", None::<Vec<u8>>],
)?;
```

For named placeholders such as `$name`, use the `named_params!` macro:

```rust
use duckdb::named_params;

conn.query_row(
    "SELECT $age >= 18 AND $name = 'Alice'",
    named_params! {
        "age": min_age,
        "name": name,
    },
    |row| row.get(0),
)?;
```

Any value bound as a parameter implements the `ToSql` trait, and any value read out of a row implements `FromSql`; the crate provides both for the standard Rust numeric, string, byte-slice, and boolean types. `Option<T>` maps to and from SQL `NULL`, so `None` binds as `NULL` and a `NULL` result reads back as `None`.

> Warning Do *not* use prepared statements to insert large amounts of data into DuckDB. See [Import Data]({% link docs/current/clients/rust/data_import.md %}) for the Appender and other faster options.

## Prepared Statements

`Connection::prepare()` compiles a statement once so it can be executed repeatedly. The returned `Statement` can be executed with `execute()`, or queried to read rows back.

```rust
let mut stmt = conn.prepare("INSERT INTO person (id, name) VALUES (?, ?)")?;
stmt.execute(params![1, "Steven"])?;
stmt.execute(params![2, "Jane"])?;
```

## Mapping Rows to Rust Values

To read a result set, prepare a `SELECT` and call `query_map()`, passing a closure that builds a value from each `Row`. Columns are read by 0-based index with `row.get()`, whose return type is inferred from the struct field it is assigned to. `query_map()` yields an iterator of `Result`, which can be collected into a `Vec`:

```rust
#[derive(Debug)]
struct Person {
    id: i32,
    name: String,
    data: Option<Vec<u8>>,
}

let mut stmt = conn.prepare("SELECT id, name, data FROM person")?;
let people = stmt
    .query_map([], |row| {
        Ok(Person {
            id: row.get(0)?,
            name: row.get(1)?,
            data: row.get(2)?,
        })
    })?
    .collect::<Result<Vec<_>>>()?;

for person in people {
    println!("Found person {person:?}");
}
```

Columns can also be read by name with `row.get("name")`. This example follows the crate's [`basic` example](https://github.com/duckdb/duckdb-rs/blob/main/crates/duckdb/examples/basic.rs).

## Reading a Single Row

When a query returns exactly one row, `Connection::query_row()` runs it and applies a closure to that row in one call, without preparing a statement by hand. The `<(T,)>::try_from(row)` helper converts a single-column row into a tuple:

```rust
let count = conn.query_row(
    "SELECT count(*) FROM person",
    [],
    |row| row.get::<_, i64>(0),
)?;

// A whole row can be converted to a tuple in one step.
let (n,) = conn.query_row("SELECT count(*) FROM person", [], |row| {
    <(i64,)>::try_from(row)
})?;
```

`query_row_and_then()` is the counterpart for a closure that returns a custom error type.

## Reading Nested and Composite Types

DuckDB's nested and composite types are read through the `Value` enum, which `row.get()` returns when the target type is `Value`. `Value` has variants such as `Value::List`, `Value::Struct`, `Value::Map`, `Value::Array`, `Value::Union`, `Value::Enum`, and `Value::Decimal`, so a query that selects nested columns can be matched on:

```rust
use duckdb::types::Value;

let mut stmt = conn.prepare("SELECT [1, 2, 3] AS l, {'a': 1, 'b': 2} AS s")?;
let mut rows = stmt.query([])?;
while let Some(row) = rows.next()? {
    let list: Value = row.get(0)?;
    let strukt: Value = row.get(1)?;
    println!("{list:?} {strukt:?}");
}
```

`Value`, `ValueRef`, and `Type` are marked non-exhaustive, so a `match` over them should include a wildcard arm to stay forward-compatible as DuckDB adds types. To read whole result sets as columnar batches instead of row by row, see [Handle Results]({% link docs/current/clients/rust/result_handling.md %}).

## Further Reading

* [Handle Results]({% link docs/current/clients/rust/result_handling.md %}) — reading results as Apache Arrow record batches or Polars data frames instead of row by row.
* [Import Data]({% link docs/current/clients/rust/data_import.md %}) — the Appender, the recommended alternative to prepared statements for bulk inserts.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries used here.
* [Define Connections]({% link docs/current/clients/rust/connecting.md %}) — opening the `Connection` that these statements run on.
