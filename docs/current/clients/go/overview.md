---
github_repository: https://github.com/duckdb/duckdb-go
layout: docu
redirect_from:
- /docs/api/go
- /docs/clients/go
- /docs/clients/go/overview
- /docs/current/clients/go
- /docs/preview/clients/go
- /docs/preview/clients/go/overview
- /docs/stable/clients/go
- /docs/stable/clients/go/overview
title: Go Client
---

> Installation To use the DuckDB Go client, visit the [Go installation page]({% link install/index.html %}?environment=go).
>
> The latest stable version of the DuckDB Go client is {% if site.current_duckdb_go_version != "" %}{{ site.current_duckdb_go_version }}{% else %}{{ site.lts_duckdb_go_version }}{% endif %}.

The DuckDB Go client, [`duckdb-go`](https://github.com/duckdb/duckdb-go), is a SQL driver that conforms to Go's built-in [`database/sql`](https://pkg.go.dev/database/sql) interface, so DuckDB is used through the same API as any other Go SQL database. On top of `database/sql`, the client adds DuckDB-specific interfaces for the [Appender]({% link docs/current/clients/go/data_import.md %}#appender), [Apache Arrow]({% link docs/current/clients/go/result_handling.md %}), [user-defined functions]({% link docs/current/clients/go/functions.md %}), and [profiling]({% link docs/current/clients/go/profiling.md %}). This page focuses on installation. The other pages in this section cover connecting and each feature in detail.

For general instructions on the `database/sql` interface, see the [official documentation](https://pkg.go.dev/database/sql) and the [Go database access tutorial](https://go.dev/doc/tutorial/database-access).

## Installation

The client is a Go module. Add it to a project with `go get`, using the `/v2` major-version suffix:

```batch
go get github.com/duckdb/duckdb-go/v2
```

DuckDB is written in C++, so the client uses [cgo](https://pkg.go.dev/cmd/cgo) and requires a C compiler to build. By default it statically links a pre-built DuckDB library into the binary, so no separate DuckDB installation is needed. Pre-built libraries ship for macOS (amd64, arm64), Linux (amd64, arm64), and Windows (amd64). Other platforms, custom builds, and dynamic linking are covered in [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}#linking-duckdb).

## Importing

To register the driver, import the package for its side effects with the blank identifier alongside `database/sql`:

```go
import (
    "database/sql"

    _ "github.com/duckdb/duckdb-go/v2"
)
```

The import registers a driver named `duckdb` with `database/sql`. Code that calls the client's own types and functions directly, such as the Appender or user-defined functions, imports the package under its `duckdb` name instead of with the blank identifier:

```go
import "github.com/duckdb/duckdb-go/v2"
```

## Versioning

Starting with DuckDB v1.5.0, the `duckdb-go` version encodes the DuckDB version it bundles in its second semantic-versioning component. The format is `v2.⟨major_minor_patch⟩.x`: for example, DuckDB v1.5.0 maps to `duckdb-go` v2.10500.x, and DuckDB {{ site.current_duckdb_go_version }} maps to v2.10505.0. The [README](https://github.com/duckdb/duckdb-go#readme) has the full mapping table for earlier releases.

For the LTS release line that stays on DuckDB 1.4 Andium, use the `v1.4-andium` branch.

> This project moved from `github.com/marcboeker/go-duckdb` to `github.com/duckdb/duckdb-go` starting with v2.5.0. All versions prior to v2.5.0 use the old import paths. See [Migrating from `marcboeker/go-duckdb`](#migrating-from-marcboekergo-duckdb) below.

## Basic API Usage

Open a database with `sql.Open()`, passing the driver name `duckdb` and a [data source name (DSN)](#data-source-names). An empty DSN opens an in-memory database, and a file path opens (or creates) a persistent database. From there, `Exec`, `Query`, and `QueryRow` run statements exactly as they do for any `database/sql` driver:

```go
package main

import (
    "database/sql"
    "errors"
    "fmt"
    "log"

    _ "github.com/duckdb/duckdb-go/v2"
)

func main() {
    db, err := sql.Open("duckdb", "")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    _, err = db.Exec(`CREATE TABLE people (id INTEGER, name VARCHAR)`)
    if err != nil {
        log.Fatal(err)
    }
    _, err = db.Exec(`INSERT INTO people VALUES (42, 'John')`)
    if err != nil {
        log.Fatal(err)
    }

    var (
        id   int
        name string
    )
    row := db.QueryRow(`SELECT id, name FROM people`)
    err = row.Scan(&id, &name)
    if errors.Is(err, sql.ErrNoRows) {
        log.Println("no rows")
    } else if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("id: %d, name: %s\n", id, name)
}
```

This example follows the client's [`simple` example](https://github.com/duckdb/duckdb-go/tree/main/examples/simple). [Run Queries]({% link docs/current/clients/go/querying.md %}) covers sending queries, binding parameters, and reading results in full.

### Data Source Names

The DSN passed to `sql.Open()` is the database path followed by optional [DuckDB configuration options]({% link docs/current/configuration/overview.md %}) as URL-style query parameters:

```go
// In-memory database.
db, err := sql.Open("duckdb", "")

// Persistent database, created if it does not exist.
db, err := sql.Open("duckdb", "/path/to/foo.db")

// Persistent database with configuration options.
db, err := sql.Open("duckdb", "/path/to/foo.db?access_mode=read_only&threads=4")
```

To run initialization steps, such as `SET` statements, before the first query, open the database with `sql.OpenDB()` and a `Connector`. See [Connect]({% link docs/current/clients/go/connecting.md %}) for connectors, configuration, and the connection lifetime.

## Build Tags

Some client features are gated behind Go [build tags](https://pkg.go.dev/go/build#hdr-Build_Constraints), passed to `go build` with the `-tags` flag, for example `go build -tags=duckdb_arrow`. The available tags:

<div class="monospace_table"></div>

| Build tag | Enables |
|--|--|
| `duckdb_arrow` | The [Apache Arrow interface]({% link docs/current/clients/go/result_handling.md %}). It is a heavy dependency, so it is opt-in. |
| `duckdb_use_lib` | Dynamically link against a `libduckdb` library on the system instead of statically linking the bundled one. See [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}#linking-a-dynamic-library). |
| `duckdb_use_static_lib` | Statically link against a custom DuckDB static library instead of the bundled one. See [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}#linking-a-custom-static-library). |

## Bundled Extensions

Every pre-built library statically links DuckDB's default extensions: [ICU]({% link docs/current/core_extensions/icu.md %}), [JSON]({% link docs/current/data/json/overview.md %}), [Parquet]({% link docs/current/data/parquet/overview.md %}), and [Autocomplete]({% link docs/current/core_extensions/autocomplete.md %}). [Automatic extension loading]({% link docs/current/extensions/overview.md %}#autoloading-extensions) is also enabled, so other core extensions install and load on first use.

## Migrating from `marcboeker/go-duckdb`

The project moved from `github.com/marcboeker/go-duckdb` to `github.com/duckdb/duckdb-go` with v2.5.0. To migrate a project, update the dependency and rewrite the import paths with `gofmt`:

```bash
# Update the dependency.
go get github.com/duckdb/duckdb-go/v2@v2.5.0

# Rewrite the import paths.
gofmt -w -r '"github.com/marcboeker/go-duckdb/v2" -> "github.com/duckdb/duckdb-go/v2"' .

# If the mapping or arrowmapping submodules are used, also run:
gofmt -w -r '"github.com/marcboeker/go-duckdb/mapping" -> "github.com/duckdb/duckdb-go/v2/mapping"' .
gofmt -w -r '"github.com/marcboeker/go-duckdb/arrowmapping" -> "github.com/duckdb/duckdb-go/v2/arrowmapping"' .

# Clean up.
go mod tidy
```

Moving to v2 also introduced a few breaking changes, including opt-in Arrow support and stricter JSON scanning. See [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}#scanning-json-values) and the [README](https://github.com/duckdb/duckdb-go#breaking-changes) for the complete list.

## Further Reading

* [Connect]({% link docs/current/clients/go/connecting.md %}) — opening in-memory and file-backed databases, DSN configuration, connectors, and the connection lifetime.
* [Run Queries]({% link docs/current/clients/go/querying.md %}) — `Exec`, `Query`, prepared statements, parameter binding, transactions, and scanning results into Go values.
* [Import Data]({% link docs/current/clients/go/data_import.md %}) — bulk loading with the Appender and reading directly from Parquet, CSV, and JSON files.
* [Handle Results]({% link docs/current/clients/go/result_handling.md %}) — the Apache Arrow interface for columnar result exchange.
* [Write User Defined Functions]({% link docs/current/clients/go/functions.md %}) — scalar and table user-defined functions, and replacement scans.
* [Profile and Monitor]({% link docs/current/clients/go/profiling.md %}) — query profiling and log storage.
* [Troubleshoot]({% link docs/current/clients/go/troubleshoot.md %}) — linking, cgo, Windows setup, and other build and runtime issues.
* [Clients Overview]({% link docs/current/clients/overview.md %}) — the other client APIs DuckDB provides alongside Go.

## Acknowledgements

We would like to thank [Marc Boeker](https://github.com/marcboeker) for the initial implementation of the DuckDB Go client and for his continued work on it as part of this joint effort with the DuckDB team.
</content>
</invoke>
