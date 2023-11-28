---
layout: docu
title: Go
---

The DuckDB Go driver, `go-duckdb`, allows using DuckDB via the `database/sql` interface.
For examples on how to use this interface, see the [official documentation](https://pkg.go.dev/database/sql) and [tutorial](https://go.dev/doc/tutorial/database-access).

> The Go client is provided as a third-party library.

## Installation

To install the `go-duckdb` client, run:

```bash
go get github.com/marcboeker/go-duckdb
```

## Importing

To import the DuckDB Go package, add the following entries to your imports:

```go
import (
	"database/sql"
	_ "github.com/marcboeker/go-duckdb"
)
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
	_ "github.com/marcboeker/go-duckdb"
	"log"
)

func check(msg string, args ...interface{}) {
	err := args[len(args)-1]
	if err != nil {
		log.Println(fmt.Sprintf("fatal error: %s", msg))
		log.Fatal(err)
	}
}

func main() {
	db, err := sql.Open("duckdb", "")
	check("failed to open db", err)
	defer func(db *sql.DB) {
		err = db.Close()
		check("failed to close db", err)
	}(db)

	_, err = db.Exec(`CREATE TABLE person (id INTEGER, name VARCHAR)`)
	check("failed to create table", err)
	_, err = db.Exec(`INSERT INTO person VALUES (42, 'John')`)
	check("failed to insert values into table", err)

	var (
		id   int
		name string
	)
	row := db.QueryRow(`SELECT id, name FROM person`)
	err = row.Scan(&id, &name)
	if errors.Is(err, sql.ErrNoRows) {
		log.Println("no rows")
	} else {
		check("failed to query rows", err)
	}

	fmt.Println("id:", id, "name:", name)
}
```

### More Examples

For more examples, see the [examples in the `duckdb-go` repository](https://github.com/marcboeker/go-duckdb/tree/master/examples).

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/marcboeker/go-duckdb)
