---
layout: docu
title: Node.js API (Neo)
---

An API for using [DuckDB](https://duckdb.org/) in [Node.js](https://nodejs.org/).

The primary package, [@duckdb/node-api](https://www.npmjs.com/package/@duckdb/node-api), is a high-level API meant for applications.
It depends on low-level bindings that adhere closely to [DuckDB's C API](https://duckdb.org/docs/api/c/overview),
available separately as [@duckdb/node-bindings](https://www.npmjs.com/package/@duckdb/node-bindings).

## Features

### Main Differences from [duckdb-node](https://www.npmjs.com/package/duckdb)

- Native support for Promises; no need for separate [duckdb-async](https://www.npmjs.com/package/duckdb-async) wrapper.
- DuckDB-specific API; not based on the [SQLite Node API](https://www.npmjs.com/package/sqlite3).
- Lossless & efficent support for values of all [DuckDB data types](https://duckdb.org/docs/sql/data_types/overview).
- Wraps [released DuckDB binaries](https://github.com/duckdb/duckdb/releases) instead of rebuilding DuckDB.
- Built on [DuckDB's C API](https://duckdb.org/docs/api/c/overview); exposes more functionality.

### Roadmap

Some features are not yet complete:

- Appending and binding advanced data types. (Additional DuckDB C API support needed.)
- Writing to data chunk vectors. (Needs special handling in Node.)
- User-defined types & functions. (Support for this was added to the DuckDB C API in v1.1.0.)
- Profiling info (Added in v1.1.0.)
- Table description (Added in v1.1.0.)
- APIs for Arrow. (This part of the DuckDB C API is [deprecated](https://github.com/duckdb/duckdb/blob/e791508e9bc2eb84bc87eb794074f4893093b743/src/include/duckdb.h#L3760).)

### Supported Platforms

- Linux arm64 (experimental)
- Linux x64
- Mac OS X (Darwin) arm64 (Apple Silicon)
- Mac OS X (Darwin) x64 (Intel)
- Windows (Win32) x64

## Examples

### Get Basic Information

```ts
import duckdb from '@duckdb/node-api';

console.log(duckdb.version());

console.log(duckdb.configurationOptionDescriptions());
```

### Create Instance

```ts
import { DuckDBInstance } from '@duckdb/node-api';
```

Create with an in-memory database:

```ts
const instance = await DuckDBInstance.create(':memory:');
```

Equivalent to the above:

```ts
const instance = await DuckDBInstance.create();
```

Read from and write to a database file, which is created if needed:

```ts
const instance = await DuckDBInstance.create('my_duckdb.db');
```

Set configuration options:

```ts
const instance = await DuckDBInstance.create('my_duckdb.db', {
  threads: '4'
});
```

### Connect

```ts
const connection = await instance.connect();
```

### Run SQL

```ts
const result = await connection.run('from test_all_types()');
```

### Parameterize SQL

```ts
const prepared = await connection.prepare('select $1, $2');
prepared.bindVarchar(1, 'duck');
prepared.bindInteger(2, 42);
const result = await prepared.run();
```

### Inspect Result

Get column names and types:

```ts
const columnNames = result.columnNames();
const columnTypes = result.columnTypes();
```

Fetch all chunks:

```ts
const chunks = await result.fetchAllChunks();
```

Fetch one chunk at a time:

```ts
const chunks = [];
while (true) {
  const chunk = await result.fetchChunk();
  // Last chunk will have zero rows.
  if (!chunk || chunk.rowCount === 0) {
    break;
  }
  chunks.push(chunk);
}
```

Read chunk data (column-major):

```ts
// array of columns, each as an array of values
const columns = chunk.getColumns(); 
```

Read chunk data (row-major):

```ts
// array of rows, each as an array of values
const rows = chunk.getRows(); 
```

Read chunk data (one value at a time):

```ts
const columns = [];
const columnCount = chunk.columnCount;
for (let columnIndex = 0; columnIndex < columnCount; columnIndex++) {
  const columnValues = [];
  const columnVector = chunk.getColumnVector(columnIndex);
  const itemCount = columnVector.itemCount;
  for (let itemIndex = 0; itemIndex < itemCount; itemIndex++) {
    const value = columnVector.getItem(itemIndex);
    columnValues.push(value);
  }
  columns.push(columnValues);
}
```

### Result Reader

Run and read all data:

```ts
const reader = await connection.runAndReadAll('from test_all_types()');
const rows = reader.getRows();
// OR: const columns = reader.getColumns();
```

Run and read up to (at least) some number of rows:

```ts
const reader = await connection.runAndReadUtil('from range(5000)', 1000);
const rows = reader.getRows();
// rows.length === 2048. (Rows are read in chunks of 2048.)
```

Read rows incrementally:

```ts
const reader = await connection.runAndRead('from range(5000)');
reader.readUntil(2000);
// reader.currentRowCount === 2048 (Rows are read in chunks of 2048.)
// reader.done === false
reader.readUntil(4000);
// reader.currentRowCount === 4096
// reader.done === false
reader.readUntil(6000);
// reader.currentRowCount === 5000
// reader.done === true
```

### Inspect Data Types

```ts
import { DuckDBTypeId } from '@duckdb/node-api';

if (columnType.typeId === DuckDBTypeId.ARRAY) {
  const arrayValueType = columnType.valueType;
  const arrayLength = columnType.length;
}

if (columnType.typeId === DuckDBTypeId.DECIMAL) {
  const decimalWidth = columnType.width;
  const decimalScale = columnType.scale;
}

if (columnType.typeId === DuckDBTypeId.ENUM) {
  const enumValues = columnType.values;
}

if (columnType.typeId === DuckDBTypeId.LIST) {
  const listValueType = columnType.valueType;
}

if (columnType.typeId === DuckDBTypeId.MAP) {
  const mapKeyType = columnType.keyType;
  const mapValueType = columnType.valueType;
}

if (columnType.typeId === DuckDBTypeId.STRUCT) {
  const structEntryNames = columnType.names;
  const structEntryTypes = columnType.valueTypes;
}

if (columnType.typeId === DuckDBTypeId.UNION) {
  const unionMemberTags = columnType.memberTags;
  const unionMemberTypes = columnType.memberTypes;
}

// For the JSON type (https://duckdb.org/docs/data/json/json_type)
if (columnType.alias === 'JSON') {
  const json = JSON.parse(columnValue);
}
```

Every type implements toString.
The result is both human-friendly and readable by DuckDB in an appropriate expression.

```ts
const typeString = columnType.toString();
```

### Inspect Data Values

```ts
import { DuckDBTypeId } from '@duckdb/node-api';

if (columnType.typeId === DuckDBTypeId.ARRAY) {
  const arrayItems = columnValue.items; // array of values
  const arrayString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.BIT) {
  const bools = columnValue.toBools(); // array of booleans
  const bits = columnValue.toBits(); // arrary of 0s and 1s
  const bitString = columnValue.toString(); // string of '0's and '1's
}

if (columnType.typeId === DuckDBTypeId.BLOB) {
  const blobBytes = columnValue.bytes; // Uint8Array
  const blobString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.DATE) {
  const dateDays = columnValue.days;
  const dateString = columnValue.toString();
  const { year, month, day } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.DECIMAL) {
  const decimalWidth = columnValue.width;
  const decimalScale = columnValue.scale;
  // Scaled-up value. Represented number is value/(10^scale).
  const decimalValue = columnValue.value; // bigint
  const decimalString = columnValue.toString();
  const decimalDouble = columnValue.toDouble();
}

if (columnType.typeId === DuckDBTypeId.INTERVAL) {
  const intervalMonths = columnValue.months;
  const intervalDays = columnValue.days;
  const intervalMicros = columnValue.micros; // bigint
  const intervalString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.LIST) {
  const listItems = columnValue.items; // array of values
  const listString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.MAP) {
  const mapEntries = columnValue.entries; // array of { key, value }
  const mapString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.STRUCT) {
  // { name1: value1, name2: value2, ... }
  const structEntries = columnValue.entries;
  const structString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_MS) {
  const timestampMillis = columnValue.milliseconds; // bigint
  const timestampMillisString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_NS) {
  const timestampNanos = columnValue.nanoseconds; // bigint
  const timestampNanosString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_S) {
  const timestampSecs = columnValue.seconds; // bigint
  const timestampSecsString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_TZ) {
  const timestampTZMicros = columnValue.micros; // bigint
  const timestampTZString = columnValue.toString();
  const {
    date: { year, month, day },
    time: { hour, min, sec, micros },
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP) {
  const timestampMicros = columnValue.micros; // bigint
  const timestampString = columnValue.toString();
  const {
    date: { year, month, day },
    time: { hour, min, sec, micros },
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIME_TZ) {
  const timeTZMicros = columnValue.micros; // bigint
  const timeTZOffset = columnValue.offset;
  const timeTZString = columnValue.toString();
  const {
    time: { hour, min, sec, micros },
    offset,
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIME) {
  const timeMicros = columnValue.micros; // bigint
  const timeString = columnValue.toString();
  const { hour, min, sec, micros } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.UNION) {
  const unionTag = columnValue.tag;
  const unionValue = columnValue.value;
  const unionValueString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.UUID) {
  const uuidHugeint = columnValue.hugeint; // bigint
  const uuidString = columnValue.toString();
}

// other possible values are: null, boolean, number, bigint, or string
```

### Append To Table

```ts
await connection.run(
  `create or replace table target_table(i integer, v varchar)`
);

const appender = await connection.createAppender('main', 'target_table');

appender.appendInteger(42);
appender.appendVarchar('duck');
appender.endRow();

appender.appendInteger(123);
appender.appendVarchar('mallard');
appender.endRow();

appender.flush();

appender.appendInteger(17);
appender.appendVarchar('goose');
appender.endRow();

appender.close(); // also flushes
```

### Extract Statements

```ts
const extractedStatements = await connection.extractStatements(`
  create or replace table numbers as from range(?);
  from numbers where range < ?;
  drop table numbers;
`);
const parameterValues = [10, 7];
const statementCount = extractedStatements.count;
for (let stmtIndex = 0; stmtIndex < statementCount; stmtIndex++) {
  const prepared = await extractedStatements.prepare(stmtIndex);
  let parameterCount = prepared.parameterCount;
  for (let paramIndex = 1; paramIndex <= parameterCount; paramIndex++) {
    prepared.bindInteger(paramIndex, parameterValues.shift());
  }
  const result = await prepared.run();
  // ...
}
```

### Control Evaluation of Tasks

```ts
import { DuckDBPendingResultState } from '@duckdb/node-api';

async function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const prepared = await connection.prepare('from range(10_000_000)');
const pending = prepared.start();
while (pending.runTask() !== DuckDBPendingResultState.RESULT_READY) {
  console.log('not ready');
  await sleep(1);
}
console.log('ready');
const result = await pending.getResult();
// ...
```