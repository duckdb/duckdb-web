---
layout: docu
redirect_from:
- /docs/clients/go/querying
- /docs/preview/clients/go/querying
- /docs/stable/clients/go/querying
title: Run Queries
---

## Overview

Because the Go client implements [`database/sql`](https://pkg.go.dev/database/sql), queries run through the standard methods:

* `Exec` and `ExecContext` send statements that do not return rows, such as `INSERT` or DDL, and report the number of affected rows.
* `Query`, `QueryContext`, `QueryRow`, and `QueryRowContext` run statements that return rows and hand back a `*sql.Rows` (or a single `*sql.Row`) to scan into Go values.

The `Context` variants take a [`context.Context`](https://pkg.go.dev/context) as their first argument, which is the recommended form because it lets a query be cancelled or time out. The sections below cover sending statements, binding parameters, prepared statements, transactions, and scanning results. For opening the database these run on, see [Connect]({% link docs/current/clients/go/connecting.md %}).

## Sending Statements

Use `Exec` (or `ExecContext`) for a statement that does not return rows, such as [`INSERT`]({% link docs/current/sql/statements/insert.md %}) or [`UPDATE`]({% link docs/current/sql/statements/update.md %}). It returns a `sql.Result`, from which `RowsAffected()` reports how many rows changed:

```go
_, err := db.ExecContext(ctx, `CREATE TABLE users (name VARCHAR, age INTEGER)`)
if err != nil {
    log.Fatal(err)
}

res, err := db.ExecContext(ctx, `INSERT INTO users VALUES ('marc', 99)`)
if err != nil {
    log.Fatal(err)
}
n, _ := res.RowsAffected()
log.Printf("inserted %d rows", n)
```

## Binding Parameters

Values are bound to a statement's placeholders rather than formatted into the SQL string, which avoids SQL injection and lets DuckDB reuse a plan. DuckDB accepts positional (`?`) and numbered (`$1`, `$2`) placeholders; pass the values as trailing arguments in order:

```go
rows, err := db.QueryContext(ctx, `
    SELECT name, age
    FROM users
    WHERE (name = ? OR name = ?) AND age > ?`,
    "macgyver", "marc", 30,
)
```

For named placeholders such as `$name`, wrap each argument with [`sql.Named`](https://pkg.go.dev/database/sql#Named):

```go
row := db.QueryRowContext(ctx,
    "SELECT $age >= 18 AND $name = 'Alice'",
    sql.Named("age", minAge),
    sql.Named("name", name),
)
```

> Warning Do *not* use prepared statements to insert large amounts of data into DuckDB. See [Import Data]({% link docs/current/clients/go/data_import.md %}) for the Appender, which is far faster for bulk inserts.

### Forcing a Parameter Type

The client infers the DuckDB type of a bound value from its Go type. When that inference is not what you want, wrap the value with `duckdb.Typed()` to pin the DuckDB [logical type]({% link docs/current/sql/data_types/overview.md %}). This matters most for timestamps: a bare `time.Time` binds as `TIMESTAMP_TZ`, so binding against a `TIMESTAMP_NS` column needs the hint:

```go
start := time.Date(2024, time.April, 5, 0, 0, 0, 0, time.UTC)
end := time.Date(2024, time.April, 6, 0, 0, 0, 0, time.UTC)

row := db.QueryRow(`
    SELECT count(*)
    FROM (VALUES (TIMESTAMP_NS '2024-04-05 12:00:00.000000001')) events(ts)
    WHERE ts >= ? AND ts < ?`,
    duckdb.Typed(start, duckdb.TYPE_TIMESTAMP_NS),
    duckdb.Typed(end, duckdb.TYPE_TIMESTAMP_NS),
)
```

`duckdb.Typed()` is a scalar binding hint; DuckDB validates the value against the requested type when the parameter is bound. See [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}#timestamp-versus-timestamp_tz) for the details of how the client maps `time.Time` to DuckDB's timestamp types.

## Prepared Statements

`db.PrepareContext()` compiles a statement once so it can be executed many times, which pays off in a loop. The returned `*sql.Stmt` has its own `Exec` and `Query` methods, and must be closed when no longer needed:

```go
stmt, err := db.PrepareContext(ctx, `INSERT INTO users VALUES (?, ?)`)
if err != nil {
    log.Fatal(err)
}
defer stmt.Close()

for _, u := range users {
    if _, err := stmt.ExecContext(ctx, u.name, u.age); err != nil {
        log.Fatal(err)
    }
}
```

## Transactions

`db.BeginTx()` starts a transaction and returns a `*sql.Tx` whose `Exec` and `Query` methods run inside it. Commit the transaction with `tx.Commit()`, or roll it back with `tx.Rollback()`:

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    log.Fatal(err)
}

if _, err := tx.ExecContext(ctx, `INSERT INTO users VALUES ('gru', 25)`); err != nil {
    tx.Rollback()
    log.Fatal(err)
}

if err := tx.Commit(); err != nil {
    log.Fatal(err)
}
```

## Scanning Results

`QueryContext` returns a `*sql.Rows` cursor. Advance it with `Next()`, read the current row's columns into pointers with `Scan()`, and always check `Err()` after the loop and close the cursor. `Scan` matches columns to the destination Go types by position:

```go
rows, err := db.QueryContext(ctx, `SELECT name, age FROM users WHERE age > ?`, 30)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var (
        name string
        age  int
    )
    if err := rows.Scan(&name, &age); err != nil {
        log.Fatal(err)
    }
    log.Printf("%s is %d years old", name, age)
}
if err := rows.Err(); err != nil {
    log.Fatal(err)
}
```

When the column set is not known ahead of time, `rows.Columns()` returns the column names, and scanning into a slice of `any` reads each column into a `driver.Value`. Remember that a scanned value can be `nil` for a SQL `NULL`.

## Reading Nested and Composite Types

DuckDB's [nested types]({% link docs/current/sql/data_types/overview.md %}#nested--composite-types), such as `LIST`, `STRUCT`, and `MAP`, and its [`JSON`]({% link docs/current/data/json/overview.md %}) type, are scanned through the generic `duckdb.Composite[T]` wrapper. Choose the Go type parameter to match the SQL shape, then read the decoded value with `Get()`:

```go
// A JSON (or LIST) value read into a slice.
var arr duckdb.Composite[[]any]
row := db.QueryRow(`SELECT json_array('foo', 'bar')`)
if err := row.Scan(&arr); err != nil {
    log.Fatal(err)
}
log.Printf("first element: %s", arr.Get()[0])

// A JSON object (or STRUCT) value read into a map.
var obj duckdb.Composite[map[string]any]
row = db.QueryRow(`SELECT '{"family": "anatidae", "coolness": 42.42}'::JSON`)
if err := row.Scan(&obj); err != nil {
    log.Fatal(err)
}
log.Printf("family: %s", obj.Get()["family"])
```

This follows the client's [`json` example](https://github.com/duckdb/duckdb-go/tree/main/examples/json). To read whole result sets as columnar batches instead of row by row, see [Handle Results]({% link docs/current/clients/go/result_handling.md %}).

## Further Reading

* [Handle Results]({% link docs/current/clients/go/result_handling.md %}) — reading results as Apache Arrow record batches instead of row by row.
* [Import Data]({% link docs/current/clients/go/data_import.md %}) — the Appender, the recommended alternative to prepared statements for bulk inserts.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries used here.
* [Connect]({% link docs/current/clients/go/connecting.md %}) — opening the database that these statements run on.
</content>
