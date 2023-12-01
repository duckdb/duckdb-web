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
	"log"

	_ "github.com/marcboeker/go-duckdb"
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

For more examples, see the [examples in the `duckdb-go` repository](https://github.com/marcboeker/go-duckdb/tree/master/examples).

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/marcboeker/go-duckdb)
