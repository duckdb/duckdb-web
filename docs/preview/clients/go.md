---
github_repository: https://github.com/duckdb/duckdb-go
layout: docu
title: Go Client
---

> Tip To use the DuckDB Go client, visit the [Go installation page]({% link install/index.html %}?environment=go).
>
> The latest stable version of the DuckDB Go client is {{ site.site.current_duckdb_go_version }}.

The DuckDB Go client, [`duckdb-go`](https://github.com/duckdb/duckdb-go), allows using DuckDB via the `database/sql` interface.
For examples on how to use this interface, see the [official documentation](https://pkg.go.dev/database/sql) and [tutorial](https://go.dev/doc/tutorial/database-access).

> The DuckDB Go client's project recently moved from `github.com/marcboeker/go-duckdb` to `github.com/duckdb/duckdb-go` starting with `v2.5.0`. Please follow the [migration guide](https://github.com/duckdb/duckdb-go#migration-from-marcboekergo-duckdb) to update to the new repository.

## Installation

To install the `duckdb-go` client, run:

```batch
go get github.com/duckdb/duckdb-go/v2
```

## Importing

To import the DuckDB Go package, add the following entries to your imports:

```go
import (
	"database/sql"
	_ "github.com/duckdb/duckdb-go/v2"
)
```

## Appender

The DuckDB Go client supports the [DuckDB Appender API]({% link docs/preview/data/appender.md %}) for bulk inserts. You can obtain a new Appender by supplying a DuckDB connection to `NewAppenderFromConn()`. For example:

```go
connector, err := duckdb.NewConnector("test.db", nil)
if err != nil {
  ...
}
conn, err := connector.Connect(context.Background())
if err != nil {
  ...
}
defer conn.Close()

// Retrieve appender from connection (note that you have to create the table 'test' beforehand).
appender, err := NewAppenderFromConn(conn, "", "test")
if err != nil {
  ...
}
defer appender.Close()

err = appender.AppendRow(...)
if err != nil {
  ...
}

// Optional, if you want to access the appended rows immediately.
err = appender.Flush()
if err != nil {
  ...
}
```

## Examples

### Simple Example

An example for using the Go API is as follows:

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

### More Examples

For more examples, see the [examples in the `duckdb-go` repository](https://github.com/duckdb/duckdb-go/tree/main/examples).

## Acknowledgements

We would like to thank [Marc Boeker](https://github.com/marcboeker) for the initial implementation of the DuckDB Go client.
