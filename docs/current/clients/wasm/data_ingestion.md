---
layout: docu
redirect_from:
- /docs/api/wasm/data_ingestion
- /docs/clients/wasm/data_ingestion
- /docs/preview/clients/wasm/data_ingestion
- /docs/stable/clients/wasm/data_ingestion
title: Import Data
---

## Overview

DuckDB-Wasm has multiple ways to import data, depending on the format of the data. Importing happens in two steps.

1. The data file is registered in a virtual file system using one of the register functions ([registerFileBuffer](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileBuffer), [registerFileHandle](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileHandle), [registerFileText](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileText), [registerFileURL](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileURL)). These are called on the database object (`db`), because a registered file is visible to every connection.
2. The data is loaded into DuckDB using one of the insert functions ([insertArrowFromIPCStream](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowFromIPCStream), [insertArrowTable](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowTable), [insertCSVFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertCSVFromPath), [insertJSONFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertJSONFromPath)), which are called on a connection (`conn`). Alternatively, the Parquet, JSON, or [Wasm-flavored httpfs](#httpfs-wasm-flavored) extensions can read a registered — or remote — file directly from a `FROM` SQL query, and [`INSERT` statements]({% link docs/current/data/insert.md %}) can load values inline.

The examples below all use a connection named `conn`, opened from the `db` object created when you [instantiate DuckDB-Wasm]({% link docs/current/clients/wasm/instantiation.md %}).

## Opening and Closing a Connection

Every insert and query runs on a connection. Open one with `connect()`, and close it when you are done to release memory:

```ts
// Create a new connection
const conn = await db.connect();

// ... import data

// Close the connection to release memory
await conn.close();
```

## Apache Arrow

[Apache Arrow](https://arrow.apache.org/) is DuckDB-Wasm's native data protocol, so Arrow data can be inserted directly. Pass an existing `arrow.Table` to `insertArrowTable()`:

> Warning Use the same major version of the [`apache-arrow`](https://www.npmjs.com/package/apache-arrow) package that DuckDB-Wasm depends on (currently `^17`). A newer major version causes Arrow inserts such as `insertArrowTable()` and `insertArrowFromIPCStream()` to fail — often silently, leaving the target table uncreated. Check DuckDB-Wasm's `apache-arrow` dependency and pin your `apache-arrow` install to match.

```ts
import { tableFromArrays } from 'apache-arrow';

const arrowTable = tableFromArrays({
  id: [1, 2, 3],
  name: ['John', 'Jane', 'Jack'],
  age: [20, 21, 22],
});

await conn.insertArrowTable(arrowTable, { name: 'arrow_table' });
```

To insert data that arrives as a raw Arrow IPC stream — for example, from a `fetch()` response — read each chunk and pass it to `insertArrowFromIPCStream()`, then write the end-of-stream (EOS) marker to signal that the table is complete:

```ts
// EOS signal according to the Arrow IPC streaming format
// See https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format
const EOS = new Uint8Array([255, 255, 255, 255, 0, 0, 0, 0]);

const streamResponse = await fetch(`someapi`);
const streamReader = streamResponse.body.getReader();
const streamInserts = [];
while (true) {
    const { value, done } = await streamReader.read();
    if (done) break;
    streamInserts.push(conn.insertArrowFromIPCStream(value, { name: 'streamed' }));
}

// Write the EOS marker
streamInserts.push(conn.insertArrowFromIPCStream(EOS, { name: 'streamed' }));

await Promise.all(streamInserts);
```

## CSV

Register the CSV text as a file, then load it with `insertCSVFromPath()`. The insert options describe the target table and, when auto-detection is disabled, the CSV dialect and column types:

```ts
import { Int32, Utf8 } from 'apache-arrow';

const csvContent = '1|foo\n2|bar\n';
await db.registerFileText('data.csv', csvContent);

await conn.insertCSVFromPath('data.csv', {
    schema: 'main',
    name: 'foo',
    detect: false,
    header: false,
    delimiter: '|',
    columns: {
        col1: new Int32(),
        col2: new Utf8(),
    },
});
```

## JSON

`insertJSONFromPath()` accepts both row-major and column-major JSON. Register the document first, then insert it:

```ts
// Row-major format
const jsonRowContent = [
    { "col1": 1, "col2": "foo" },
    { "col1": 2, "col2": "bar" },
];
await db.registerFileText('rows.json', JSON.stringify(jsonRowContent));
await conn.insertJSONFromPath('rows.json', { name: 'rows' });

// Column-major format
const jsonColContent = {
    "col1": [1, 2],
    "col2": ["foo", "bar"]
};
await db.registerFileText('columns.json', JSON.stringify(jsonColContent));
await conn.insertJSONFromPath('columns.json', { name: 'columns' });
```

To import JSON fetched from an API, register the response bytes as a file buffer:

```ts
const streamResponse = await fetch(`someapi/content.json`);
await db.registerFileBuffer('file.json', new Uint8Array(await streamResponse.arrayBuffer()));
await conn.insertJSONFromPath('file.json', { name: 'JSONContent' });
```

## Parquet

A Parquet file is registered rather than loaded through a dedicated insert function, then read with SQL. Register a local file picked by the user with `registerFileHandle()`, a remote file with `registerFileURL()`, or bytes you have already fetched with `registerFileBuffer()`:

```ts
// Local file chosen by the user
const pickedFile: File = letUserPickFile();
await db.registerFileHandle('local.parquet', pickedFile, DuckDBDataProtocol.BROWSER_FILEREADER, true);

// Remote file, read lazily over HTTP
await db.registerFileURL('remote.parquet', 'https://origin/remote.parquet', DuckDBDataProtocol.HTTP, false);

// Bytes already fetched into memory
const res = await fetch('https://origin/remote.parquet');
await db.registerFileBuffer('buffer.parquet', new Uint8Array(await res.arrayBuffer()));
```

Once a file is registered, query it by its name:

```ts
await conn.query(`CREATE TABLE local AS SELECT * FROM 'local.parquet'`);
```

## httpfs (Wasm-Flavored)

With the [Wasm-flavored httpfs extension]({% link docs/current/clients/wasm/extensions.md %}#httpfs), you can skip registration and read a remote file directly by putting its URL in the SQL text:

```ts
await conn.query(`
    CREATE TABLE direct AS
        SELECT * FROM 'https://origin/remote.parquet'
`);
```

> Tip Reading a remote file makes the browser issue the request, so it is subject to the browser's CORS policy. If a query over an S3 or other remote file fails with a network error, see [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}#network-error-when-querying-remote-files).

## Insert Statement

Finally, [`INSERT` statements]({% link docs/current/data/insert.md %}) load values directly, without registering a file — useful for small amounts of data or for appending to an existing table:

```ts
await conn.query(`
    INSERT INTO existing_table
    VALUES (1, 'foo'), (2, 'bar')`);
```

## Further Reading

* [Run Queries]({% link docs/current/clients/wasm/query.md %}) — querying the data imported here and exporting results.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — the Parquet, JSON, and Wasm-flavored httpfs extensions used to read files directly in SQL.
* [`INSERT` Statement]({% link docs/current/data/insert.md %}) — DuckDB's SQL-level `INSERT`, an alternative to the insert functions above.
* [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) — creating the `db` and connection these imports run on.
* [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}) — CORS network errors when reading remote files.
