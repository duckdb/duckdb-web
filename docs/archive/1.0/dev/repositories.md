---
layout: docu
redirect_from:
- /internals/repositories
title: DuckDB Repositories
---

Several components of DuckDB are maintained in separate repositories.

## Main repositories

* [`duckdb`](https://github.com/duckdb/duckdb): core DuckDB project
* [`duckdb-wasm`](https://github.com/duckdb/duckdb-wasm): WebAssembly version of DuckDB
* [`duckdb-web`](https://github.com/duckdb/duckdb-web): documentation and blog

## Clients

* [`duckdb-java`](https://github.com/duckdb/duckdb-java): Java (JDBC) client
* [`duckdb-node`](https://github.com/duckdb/duckdb-node): Node.js client
* [`duckdb-node-neo`](https://github.com/duckdb/duckdb-node): Node.js client, second iteration (currently experimental)
* [`duckdb-odbc`](https://github.com/duckdb/duckdb-odbc): ODBC client
* [`duckdb-r`](https://github.com/duckdb/duckdb-r): R client
* [`duckdb-rs`](https://github.com/duckdb/duckdb-rs): Rust client
* [`duckdb-swift`](https://github.com/duckdb/duckdb-swift): Swift client
* [`duckplyr`](https://github.com/tidyverse/duckplyr): a drop-in replacement for dplyr in R
* [`go-duckdb`](https://github.com/marcboeker/go-duckdb): Go client

## Connectors

* [`dbt-duckdb`](https://github.com/duckdb/dbt-duckdb): dbt
* [`duckdb_mysql`](https://github.com/duckdb/duckdb_mysql): MySQL connector
* [`pg_duckdb`](https://github.com/duckdb/pg_duckdb): official PostgreSQL extension for DuckDB (run DuckDB in PostgreSQL)
* [`postgres_scanner`](https://github.com/duckdb/postgres_scanner): PostgreSQL connector (connect to PostgreSQL from DuckdB)
* [`sqlite_scanner`](https://github.com/duckdb/sqlite_scanner): SQLite connector

## Extensions

* Core extension repositories are linked in the [Official Extensions page]({% link docs/archive/1.0/extensions/core_extensions.md %})
* Community extensions are built in the [Community Extensions repository](https://github.com/duckdb/community-extensions)