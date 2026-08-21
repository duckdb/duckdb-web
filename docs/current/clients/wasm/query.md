---
layout: docu
redirect_from:
- /docs/api/wasm/query
- /docs/clients/wasm/query
- /docs/preview/clients/wasm/query
- /docs/stable/clients/wasm/query
title: Run Queries
---

## Overview

DuckDB-Wasm provides functions for querying data. Queries are run sequentially. First, a connection needs to be created by calling [connect](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#connect). Then, queries can be run by calling [query](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#query) to materialize the whole result, or [send](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#send) to fetch result chunks lazily. This page covers running queries, prepared statements, converting results to JSON, and exporting to Parquet.

## Query Execution

```ts
// Create a new connection
const conn = await db.connect();

// Either materialize the query result
await conn.query<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);
// ..., or fetch the result chunks lazily
for await (const batch of await conn.send<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`)) {
    // ...
}

// Close the connection to release memory
await conn.close();
```

## Prepared Statements

```ts
// Create a new connection
const conn = await db.connect();
// Prepare query
const stmt = await conn.prepare(`SELECT v + ? FROM generate_series(0, 10_000) t(v);`);
// ... and run the query with materialized results
await stmt.query(234);
// ... or result chunks
for await (const batch of await stmt.send(234)) {
    // ...
}
// Close the statement to release memory
await stmt.close();
// Closing the connection will release statements as well
await conn.close();
```

## Arrow Table to JSON

```ts
// Create a new connection
const conn = await db.connect();

// Query
const arrowResult = await conn.query<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);

// Convert arrow table to json
const result = arrowResult.toArray().map((row) => row.toJSON());

// Close the connection to release memory
await conn.close();
```

## Export Parquet

```ts
// Create a new connection
const conn = await db.connect();

// Export Parquet
conn.send(`COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT parquet);`);
const parquet_buffer = await this._db.copyFileToBuffer('result-snappy.parquet');

// Generate a download link
const link = URL.createObjectURL(new Blob([parquet_buffer]));

// Close the connection to release memory
await conn.close();
```

## Further Reading

* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — loading the data that these queries read.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — the Parquet extension used by the export example and other query-time extensions.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries shown here.
* [Instantiate DuckDB-Wasm]({% link docs/current/clients/wasm/instantiation.md %}) — creating the `db` that connections are opened on.
