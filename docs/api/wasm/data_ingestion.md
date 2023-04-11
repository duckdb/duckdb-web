---
layout: docu
title: Data Ingestion
selected: Client APIs
---

DuckDB-Wasm has multiple ways to import data, depending on the format of the data.

There are two steps to import data into DuckDB.

First, the data file is imported into a local file system using register functions ([registerEmptyFileBuffer](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerEmptyFileBuffer), [registerFileBuffer](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileBuffer), [registerFileHandle](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileHandle), [registerFileText](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileText), [registerFileURL](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileURL)).

Then, the data file is imported into DuckDB using insert functions ([insertArrowFromIPCStream](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowFromIPCStream), [insertArrowTable](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowTable), [insertCSVFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertCSVFromPath), [insertJSONFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertJSONFromPath)) or directly using FROM SQL query (using extensions like parquet or [HTTPFS](../../extensions/httpfs)).

[Insert statements](../../data/insert) can also be used to import data.

## Data Import

Open & Close connection

```ts
// Create a new connection
const c = await db.connect();

// ... import data

// Close the connection to release memory
await c.close();

```

Apache Arrow

```ts
// Data can be inserted from an existing arrow.Table
// More Example https://arrow.apache.org/docs/js/
import { tableFromArrays } from 'apache-arrow';

const arrowTable = tableFromArrays({
  id: [1, 2, 3],
  name: ['John', 'Jane', 'Jack'],
  age: [20, 21, 22],
});
await c.insertArrowTable(arrowTable, { name: 'arrow_table' });

// ..., from a raw Arrow IPC stream
const streamResponse = await fetch(`someapi`);
const streamReader = streamResponse.body.getReader();
const streamInserts = [];
while (true) {
    const { value, done } = await streamReader.read();
    if (done) break;
    streamInserts.push(c.insertArrowFromIPCStream(value, { name: 'streamed' }));
}
await Promise.all(streamInserts);
```

CSV

```ts
// ..., from CSV files
// (interchangeable: registerFile{Text,Buffer,URL,Handle})
const csvContent = '1|foo\n2|bar\n';
await db.registerFileText(`data.csv`, csvContent);
// ... with typed insert options
await db.insertCSVFromPath('data.csv', {
    schema: 'main',
    name: 'foo',
    detect: false,
    header: false,
    delimiter: '|',
    columns: {
        col1: new arrow.Int32(),
        col2: new arrow.Utf8(),
    },
});
```

JSON

```ts
// ..., from JSON documents in row-major format
const jsonRowContent = [
    { "col1": 1, "col2": "foo" },
    { "col1": 2, "col2": "bar" },
];
await db.registerFileText(
    'rows.json',
    JSON.stringify(jsonRowContent),
);
await c.insertJSONFromPath('rows.json', { name: 'rows' });

// ... or column-major format
const jsonColContent = {
    "col1": [1, 2],
    "col2": ["foo", "bar"]
};
await db.registerFileText(
    'columns.json',
    JSON.stringify(jsonColContent),
);
await c.insertJSONFromPath('columns.json', { name: 'columns' });

// From API
const streamResponse = await fetch(`someapi/content.json`);
await db.registerFileBuffer('file.json', new Uint8Array(await streamResponse.arrayBuffer()))
await c.insertJSONFromPath('file.json', { name: 'JSONContent' });
```

Parquet

```ts
// from Parquet files
// ...Local
const pickedFile: File = letUserPickFile();
await db.registerFileHandle('local.parquet', pickedFile, DuckDBDataProtocol.BROWSER_FILEREADER, true);
// ...Remote
await db.registerFileURL('remote.parquet', 'https://origin/remote.parquet', DuckDBDataProtocol.HTTP, false);
// ... Using Fetch
const res = await fetch('https://origin/remote.parquet');
await db.registerFileBuffer('buffer.parquet', new Uint8Array(await res.arrayBuffer()));

// ..., by specifying URLs in the SQL text
await c.query(`
    CREATE TABLE direct AS
        SELECT * FROM "https://origin/remote.parquet"
`);
// ..., or by executing raw insert statements
await c.query(`INSERT INTO existing_table
    VALUES (1, "foo"), (2, "bar")`);
```

HTTPFS

```ts
// ..., by specifying URLs in the SQL text
await c.query(`
    CREATE TABLE direct AS
        SELECT * FROM "https://origin/remote.parquet"
`);
```

Insert statement

```ts
// ..., or by executing raw insert statements
await c.query(`INSERT INTO existing_table
    VALUES (1, "foo"), (2, "bar")`);
```
