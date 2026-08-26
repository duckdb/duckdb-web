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

DuckDB-Wasm provides functions for querying data. Queries are run sequentially:

1. First, create a connection by calling [connect](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#connect).
2. Then, run queries by calling [query](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#query) to materialize the whole result, or [send](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#send) to fetch result chunks lazily.

This page covers running queries, prepared statements, converting results to JSON, and exporting to Parquet.

## Query Execution

Use `query()` when you want the entire result at once, or `send()` to iterate over [Apache Arrow](https://arrow.apache.org/) record batches as they are produced — useful for large results that you would rather stream than hold in memory all at once:

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

Prepared statements let you parse a query once and run it repeatedly with different parameter values, binding each value in place of a `?` placeholder. Both `query()` (materialized) and `send()` (streamed) are available on a prepared statement:

```ts
// Create a new connection
const conn = await db.connect();
// Prepare the query
const stmt = await conn.prepare(`SELECT v + ? FROM generate_series(0, 10_000) t(v);`);
// ... and run it with materialized results
await stmt.query(234);
// ... or as result chunks
for await (const batch of await stmt.send(234)) {
    // ...
}
// Close the statement to release memory
await stmt.close();
// Closing the connection releases its statements as well
await conn.close();
```

## Arrow Table to JSON

Query results are returned as Arrow tables. To convert a result into plain JavaScript objects, map over the table's rows and call `toJSON()` on each:

```ts
// Create a new connection
const conn = await db.connect();

// Query the data
const arrowResult = await conn.query<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);

// Convert the Arrow table to an array of JSON objects
const result = arrowResult.toArray().map((row) => row.toJSON());

// Close the connection to release memory
await conn.close();
```

## Export Parquet

To export a query result, write it to a Parquet file in the virtual file system with `COPY`, then copy that file's bytes into a buffer you can download or process:

```ts
// Create a new connection
const conn = await db.connect();

// Export the query result to a Parquet file in the virtual file system
await conn.query(`COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT parquet);`);

// Copy the file contents into a buffer
const parquetBuffer = await db.copyFileToBuffer('result-snappy.parquet');

// Generate a download link
const link = URL.createObjectURL(new Blob([parquetBuffer]));

// Close the connection to release memory
await conn.close();
```

## Further Reading

* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — loading the data that these queries read.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — the Parquet extension used by the export example and other query-time extensions.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries shown here.
* [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) — creating the `db` that connections are opened on.
* [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}) — streaming results with `send()` to stay within the memory limit.
