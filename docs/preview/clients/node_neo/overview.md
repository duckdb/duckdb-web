---
layout: docu
title: Node.js Client (Neo)
---

> Tip To use the DuckDB Node.js client, visit the [Node.js installation page]({% link install/index.html %}?environment=nodejs).
>
> The latest stable version of the DuckDB Node.js (Neo) client is {{ site.current_duckdb_node_neo_version }}.

An API for using [DuckDB]({% link index.html %}) in [Node.js](https://nodejs.org/).

The primary package, [@duckdb/node-api](https://www.npmjs.com/package/@duckdb/node-api), is a high-level API meant for applications.
It depends on low-level bindings that adhere closely to [DuckDB's C API]({% link docs/preview/clients/c/overview.md %}),
available separately as [@duckdb/node-bindings](https://www.npmjs.com/package/@duckdb/node-bindings).

## Features

### Main Differences from [duckdb-node](https://www.npmjs.com/package/duckdb)

* Native support for Promises; no need for separate [duckdb-async](https://www.npmjs.com/package/duckdb-async) wrapper.
* DuckDB-specific API; not based on the [SQLite Node API](https://www.npmjs.com/package/sqlite3).
* Lossless & efficient support for values of all [DuckDB data types]({% link docs/preview/sql/data_types/overview.md %}).
* Wraps [released DuckDB binaries](https://github.com/duckdb/duckdb/releases) instead of rebuilding DuckDB.
* Built on [DuckDB's C API]({% link docs/preview/clients/c/overview.md %}); exposes more functionality.

### Roadmap

Some features are not yet complete:
* Binding and appending the MAP and UNION data types
* Appending default values row-by-row
* User-defined types & functions
* Profiling info
* Table description
* APIs for Arrow

See the [issues list on GitHub](https://github.com/duckdb/duckdb-node-neo/issues)
for the most up-to-date roadmap.

### Supported Platforms

* Linux arm64
* Linux x64
* Mac OS X (Darwin) arm64 (Apple Silicon)
* Mac OS X (Darwin) x64 (Intel)
* Windows (Win32) x64

## Examples

### Get Basic Information

```ts
import duckdb from '@duckdb/node-api';

console.log(duckdb.version());

console.log(duckdb.configurationOptionDescriptions());
```

### Connect

```ts
import { DuckDBConnection } from '@duckdb/node-api';

const connection = await DuckDBConnection.create();
```

This uses the default instance.
For advanced usage, you can create instances explicitly.

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

Set [configuration options]({% link docs/preview/configuration/overview.md %}):
```ts
const instance = await DuckDBInstance.create('my_duckdb.db', {
  threads: '4'
});
```

### Instance Cache

Multiple instances in the same process should not
attach the same database.

To prevent this, an instance cache can be used:
```ts
const instance = await DuckDBInstance.fromCache('my_duckdb.db');
```

This uses the default instance cache. For advanced usage, you can create
instance caches explicitly:
```ts
import { DuckDBInstanceCache } from '@duckdb/node-api';

const cache = new DuckDBInstanceCache();
const instance = await cache.getOrCreateInstance('my_duckdb.db');
```

### Connect to Instance

```ts
const connection = await instance.connect();
```

### Disconnect

Connections will be disconnected automatically soon after their reference
is dropped, but you can also disconnect explicitly if and when you want:

```ts
connection.disconnectSync();
```

or, equivalently:

```ts
connection.closeSync();
```

### Run SQL

```ts
const result = await connection.run('from test_all_types()');
```

### Parameterize SQL

```ts
const prepared = await connection.prepare('select $1, $2, $3');
prepared.bindVarchar(1, 'duck');
prepared.bindInteger(2, 42);
prepared.bindList(3, listValue([10, 11, 12]), LIST(INTEGER));
const result = await prepared.run();
```

or:

```ts
const prepared = await connection.prepare('select $a, $b, $c');
prepared.bind({
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
}, {
  'a': VARCHAR,
  'b': INTEGER,
  'c': LIST(INTEGER),
});
const result = await prepared.run();
```

or even:

```ts
const result = await connection.run('select $a, $b, $c', {
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
}, {
  'a': VARCHAR,
  'b': INTEGER,
  'c': LIST(INTEGER),
});
```

Unspecified types will be inferred:

```ts
const result = await connection.run('select $a, $b, $c', {
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
});
```

### Specifying Values

Values of many data types are represented using one of the JS primitives
`boolean`, `number`, `bigint`, or `string`.
Also, any type can have `null` values.

Values of some data types need to be constructed using special functions.
These are:

| Type | Function |
| ---- | -------- |
| `ARRAY` | `arrayValue` |
| `BIT` | `bitValue` |
| `BLOB` | `blobValue` |
| `DATE` | `dateValue` |
| `DECIMAL` | `decimalValue` |
| `INTERVAL` | `intervalValue` |
| `LIST` | `listValue` |
| `MAP` | `mapValue` |
| `STRUCT` | `structValue` |
| `TIME` | `timeValue` |
| `TIMETZ` | `timeTZValue` |
| `TIMESTAMP` | `timestampValue` |
| `TIMESTAMPTZ` | `timestampTZValue` |
| `TIMESTAMP_S` | `timestampSecondsValue` |
| `TIMESTAMP_MS` | `timestampMillisValue` |
| `TIMESTAMP_NS` | `timestampNanosValue` |
| `UNION` | `unionValue` |
| `UUID` | `uuidValue` |

### Stream Results

Streaming results evaluate lazily when rows are read.

```ts
const result = await connection.stream('from range(10_000)');
```

### Inspect Result Metadata

Get column names and types:
```ts
const columnNames = result.columnNames();
const columnTypes = result.columnTypes();
```

### Read Result Data

Run and read all data:
```ts
const reader = await connection.runAndReadAll('from test_all_types()');
const rows = reader.getRows();
// OR: const columns = reader.getColumns();
```

Stream and read up to (at least) some number of rows:
```ts
const reader = await connection.streamAndReadUntil(
  'from range(5000)',
  1000
);
const rows = reader.getRows();
// rows.length === 2048. (Rows are read in chunks of 2048.)
```

Read rows incrementally:
```ts
const reader = await connection.streamAndRead('from range(5000)');
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

### Get Result Data

Result data can be retrieved in a variety of forms:

```ts
const reader = await connection.runAndReadAll(
  'from range(3) select range::int as i, 10 + i as n'
);

const rows = reader.getRows();
// [ [0, 10], [1, 11], [2, 12] ]

const rowObjects = reader.getRowObjects();
// [ { i: 0, n: 10 }, { i: 1, n: 11 }, { i: 2, n: 12 } ]

const columns = reader.getColumns();
// [ [0, 1, 2], [10, 11, 12] ]

const columnsObject = reader.getColumnsObject();
// { i: [0, 1, 2], n: [10, 11, 12] }
```

### Convert Result Data

By default, data values that cannot be represented as JS built-ins
are returned as specialized JS objects; see `Inspect Data Values` below.

To retrieve data in a different form, such as JS built-ins or values that
can be losslessly serialized to JSON, use the `JS` or `Json` forms of the
above result data methods.

Custom converters can be supplied as well. See the implementations of
[JSDuckDBValueConverter](https://github.com/duckdb/duckdb-node-neo/blob/main/api/src/JSDuckDBValueConverter.ts)
and [JsonDuckDBValueConverters](https://github.com/duckdb/duckdb-node-neo/blob/main/api/src/JsonDuckDBValueConverter.ts)
for how to do this.

Examples (using the `Json` forms):

```ts
const reader = await connection.runAndReadAll(
  'from test_all_types() select bigint, date, interval limit 2'
);

const rows = reader.getRowsJson();
// [
//   [
//     "-9223372036854775808",
//     "5877642-06-25 (BC)",
//     { "months": 0, "days": 0, "micros": "0" }
//   ],
//   [
//     "9223372036854775807",
//     "5881580-07-10",
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// ]

const rowObjects = reader.getRowObjectsJson();
// [
//   {
//     "bigint": "-9223372036854775808",
//     "date": "5877642-06-25 (BC)",
//     "interval": { "months": 0, "days": 0, "micros": "0" }
//   },
//   {
//     "bigint": "9223372036854775807",
//     "date": "5881580-07-10",
//     "interval": { "months": 999, "days": 999, "micros": "999999999" }
//   }
// ]

const columns = reader.getColumnsJson();
// [
//   [ "-9223372036854775808", "9223372036854775807" ],
//   [ "5877642-06-25 (BC)", "5881580-07-10" ],
//   [
//     { "months": 0, "days": 0, "micros": "0" },
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// ]

const columnsObject = reader.getColumnsObjectJson();
// {
//   "bigint": [ "-9223372036854775808", "9223372036854775807" ],
//   "date": [ "5877642-06-25 (BC)", "5881580-07-10" ],
//   "interval": [
//     { "months": 0, "days": 0, "micros": "0" },
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// }
```

These methods handle nested types as well:

```ts
const reader = await connection.runAndReadAll(
  'from test_all_types() select int_array, struct, map, "union" limit 2'
);

const rows = reader.getRowsJson();
// [
//   [
//     [],
//     { "a": null, "b": null },
//     [],
//     { "tag": "name", "value": "Frank" }
//   ],
//   [
//     [ 42, 999, null, null, -42],
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" },
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ],
//     { "tag": "age", "value": 5 }
//   ]
// ]

const rowObjects = reader.getRowObjectsJson();
// [
//   {
//     "int_array": [],
//     "struct": { "a": null, "b": null },
//     "map": [],
//     "union": { "tag": "name", "value": "Frank" }
//   },
//   {
//     "int_array": [ 42, 999, null, null, -42 ],
//     "struct": { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" },
//     "map": [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ],
//     "union": { "tag": "age", "value": 5 }
//   }
// ]

const columns = reader.getColumnsJson();
// [
//   [
//     [],
//     [42, 999, null, null, -42]
//   ],
//   [
//     { "a": null, "b": null },
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" }
//   ],
//   [
//     [],
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose"}
//     ]
//   ],
//   [
//     { "tag": "name", "value": "Frank" },
//     { "tag": "age", "value": 5 }
//   ]
// ]

const columnsObject = reader.getColumnsObjectJson();
// {
//   "int_array": [
//     [],
//     [42, 999, null, null, -42]
//   ],
//   "struct": [
//     { "a": null, "b": null },
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" }
//   ],
//   "map": [
//     [],
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ]
//   ],
//   "union": [
//     { "tag": "name", "value": "Frank" },
//     { "tag": "age", "value": 5 }
//   ]
// }
```

Column names and types can also be serialized to JSON:
```ts
const columnNamesAndTypes = reader.columnNamesAndTypesJson();
// {
//   "columnNames": [
//     "int_array",
//     "struct",
//     "map",
//     "union"
//   ],
//   "columnTypes": [
//     {
//       "typeId": 24,
//       "valueType": {
//         "typeId": 4
//       }
//     },
//     {
//       "typeId": 25,
//       "entryNames": [
//         "a",
//         "b"
//       ],
//       "entryTypes": [
//         {
//           "typeId": 4
//         },
//         {
//           "typeId": 17
//         }
//       ]
//     },
//     {
//       "typeId": 26,
//       "keyType": {
//         "typeId": 17
//       },
//       "valueType": {
//         "typeId": 17
//       }
//     },
//     {
//       "typeId": 28,
//       "memberTags": [
//         "name",
//         "age"
//       ],
//       "memberTypes": [
//         {
//           "typeId": 17
//         },
//         {
//           "typeId": 3
//         }
//       ]
//     }
//   ]
// }

const columnNameAndTypeObjects = reader.columnNameAndTypeObjectsJson();
// [
//   {
//     "columnName": "int_array",
//     "columnType": {
//       "typeId": 24,
//       "valueType": {
//         "typeId": 4
//       }
//     }
//   },
//   {
//     "columnName": "struct",
//     "columnType": {
//       "typeId": 25,
//       "entryNames": [
//         "a",
//         "b"
//       ],
//       "entryTypes": [
//         {
//           "typeId": 4
//         },
//         {
//           "typeId": 17
//         }
//       ]
//     }
//   },
//   {
//     "columnName": "map",
//     "columnType": {
//       "typeId": 26,
//       "keyType": {
//         "typeId": 17
//       },
//       "valueType": {
//         "typeId": 17
//       }
//     }
//   },
//   {
//     "columnName": "union",
//     "columnType": {
//       "typeId": 28,
//       "memberTags": [
//         "name",
//         "age"
//       ],
//       "memberTypes": [
//         {
//           "typeId": 17
//         },
//         {
//           "typeId": 3
//         }
//       ]
//     }
//   }
// ]
```

### Fetch Chunks

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
  if (chunk.rowCount === 0) {
    break;
  }
  chunks.push(chunk);
}
```

For materialized (non-streaming) results, chunks can be read by index:
```ts
const rowCount = result.rowCount;
const chunkCount = result.chunkCount;
for (let i = 0; i < chunkCount; i++) {
  const chunk = result.getChunk(i);
  // ...
}
```

Get chunk data:
```ts
const rows = chunk.getRows();

const rowObjects = chunk.getRowObjects(result.deduplicatedColumnNames());

const columns = chunk.getColumns();

const columnsObject =
  chunk.getColumnsObject(result.deduplicatedColumnNames());
```

Get chunk data (one value at a time)
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
  const bits = columnValue.toBits(); // array of 0s and 1s
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

### Displaying Timezones

Converting a TIMESTAMP_TZ value to a string depends on a timezone offset.
By default, this is set to the offset for the local timezone when the Node
process is started.

To change it, set the `timezoneOffsetInMinutes`
property of `DuckDBTimestampTZValue`:

```ts
DuckDBTimestampTZValue.timezoneOffsetInMinutes = -8 * 60;
const pst = DuckDBTimestampTZValue.Epoch.toString();
// 1969-12-31 16:00:00-08

DuckDBTimestampTZValue.timezoneOffsetInMinutes = +1 * 60;
const cet = DuckDBTimestampTZValue.Epoch.toString();
// 1970-01-01 01:00:00+01
```

Note that the timezone offset used for this string
conversion is distinct from the `TimeZone` setting of DuckDB.

The following sets this offset to match the `TimeZone` setting of DuckDB:

```ts
const reader = await connection.runAndReadAll(
  `select (timezone(current_timestamp) / 60)::int`
);
DuckDBTimestampTZValue.timezoneOffsetInMinutes =
  reader.getColumns()[0][0];
```

### Append To Table

```ts
await connection.run(
  `create or replace table target_table(i integer, v varchar)`
);

const appender = await connection.createAppender('target_table');

appender.appendInteger(42);
appender.appendVarchar('duck');
appender.endRow();

appender.appendInteger(123);
appender.appendVarchar('mallard');
appender.endRow();

appender.flushSync();

appender.appendInteger(17);
appender.appendVarchar('goose');
appender.endRow();

appender.closeSync(); // also flushes
```

### Append Data Chunk

```ts
await connection.run(
  `create or replace table target_table(i integer, v varchar)`
);

const appender = await connection.createAppender('target_table');

const chunk = DuckDBDataChunk.create([INTEGER, VARCHAR]);
chunk.setColumns([
  [42, 123, 17],
  ['duck', 'mallard', 'goose'],
]);
// OR:
// chunk.setRows([
//   [42, 'duck'],
//   [123, 'mallard'],
//   [17, 'goose'],
// ]);

appender.appendDataChunk(chunk);
appender.flushSync();
```

See "Specifying Values" above for how to supply values to the appender.

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

### Ways to Run SQL

```ts
// Run to completion but don't yet retrieve any rows.
// Optionally take values to bind to SQL parameters,
// and (optionally) types of those parameters,
// either as an array (for positional parameters),
// or an object keyed by parameter name.
const result = await connection.run(sql);
const result = await connection.run(sql, values);
const result = await connection.run(sql, values, types);

// Run to completion but don't yet retrieve any rows.
// Wrap in a DuckDBDataReader for convenient data retrieval.
const reader = await connection.runAndRead(sql);
const reader = await connection.runAndRead(sql, values);
const reader = await connection.runAndRead(sql, values, types);

// Run to completion, wrap in a reader, and read all rows.
const reader = await connection.runAndReadAll(sql);
const reader = await connection.runAndReadAll(sql, values);
const reader = await connection.runAndReadAll(sql, values, types);

// Run to completion, wrap in a reader, and read at least
// the given number of rows. (Rows are read in chunks, so more than
// the target may be read.)
const reader = await connection.runAndReadUntil(sql, targetRowCount);
const reader =
  await connection.runAndReadAll(sql, targetRowCount, values);
const reader =
  await connection.runAndReadAll(sql, targetRowCount, values, types);

// Create a streaming result and don't yet retrieve any rows.
const result = await connection.stream(sql);
const result = await connection.stream(sql, values);
const result = await connection.stream(sql, values, types);

// Create a streaming result and don't yet retrieve any rows.
// Wrap in a DuckDBDataReader for convenient data retrieval.
const reader = await connection.streamAndRead(sql);
const reader = await connection.streamAndRead(sql, values);
const reader = await connection.streamAndRead(sql, values, types);

// Create a streaming result, wrap in a reader, and read all rows.
const reader = await connection.streamAndReadAll(sql);
const reader = await connection.streamAndReadAll(sql, values);
const reader = await connection.streamAndReadAll(sql, values, types);

// Create a streaming result, wrap in a reader, and read at least
// the given number of rows.
const reader = await connection.streamAndReadUntil(sql, targetRowCount);
const reader =
  await connection.streamAndReadUntil(sql, targetRowCount, values);
const reader =
  await connection.streamAndReadUntil(sql, targetRowCount, values, types);

// Prepared Statements

// Prepare a possibly-parametered SQL statement to run later.
const prepared = await connection.prepare(sql);

// Bind values to the parameters.
prepared.bind(values);
prepared.bind(values, types);

// Run the prepared statement. These mirror the methods on the connection.
const result = prepared.run();

const reader = prepared.runAndRead();
const reader = prepared.runAndReadAll();
const reader = prepared.runAndReadUntil(targetRowCount);

const result = prepared.stream();

const reader = prepared.streamAndRead();
const reader = prepared.streamAndReadAll();
const reader = prepared.streamAndReadUntil(targetRowCount);

// Pending Results

// Create a pending result.
const pending = await connection.start(sql);
const pending = await connection.start(sql, values);
const pending = await connection.start(sql, values, types);

// Create a pending, streaming result.
const pending = await connection.startStream(sql);
const pending = await connection.startStream(sql, values);
const pending = await connection.startStream(sql, values, types);

// Create a pending result from a prepared statement.
const pending = await prepared.start();
const pending = await prepared.startStream();

while (pending.runTask() !== DuckDBPendingResultState.RESULT_READY) {
  // optionally sleep or do other work between tasks
}

// Retrieve the result. If not yet READY, will run until it is.
const result = await pending.getResult();

const reader = await pending.read();
const reader = await pending.readAll();
const reader = await pending.readUntil(targetRowCount);
```

### Ways to Get Result Data

```ts
// From a result

// Asynchronously retrieve data for all rows:
const columns = await result.getColumns();
const columnsJson = await result.getColumnsJson();
const columnsObject = await result.getColumnsObject();
const columnsObjectJson = await result.getColumnsObjectJson();
const rows = await result.getRows();
const rowsJson = await result.getRowsJson();
const rowObjects = await result.getRowObjects();
const rowObjectsJson = await result.getRowObjectsJson();

// From a reader

// First, (asynchronously) read some rows:
await reader.readAll();
// or:
await reader.readUntil(targetRowCount);

// Then, (synchronously) get result data for the rows read:
const columns = reader.getColumns();
const columnsJson = reader.getColumnsJson();
const columnsObject = reader.getColumnsObject();
const columnsObjectJson = reader.getColumnsObjectJson();
const rows = reader.getRows();
const rowsJson = reader.getRowsJson();
const rowObjects = reader.getRowObjects();
const rowObjectsJson = reader.getRowObjectsJson();

// Individual values can also be read directly:
const value = reader.value(columnIndex, rowIndex);

// Using chunks

// If desired, one or more chunks can be fetched from a result:
const chunk = await result.fetchChunk();
const chunks = await result.fetchAllChunks();

// And then data can be retrieved from each chunk:
const columnValues = chunk.getColumnValues(columnIndex);
const columns = chunk.getColumns();
const rowValues = chunk.getRowValues(rowIndex);
const rows = chunk.getRows();

// Or, values can be visited:
chunk.visitColumnValues(columnIndex,
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitColumns((column, columnIndex, type) => { /* ... */ });
chunk.visitColumnMajor(
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitRowValues(rowIndex,
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitRows((row, rowIndex) => { /* ... */ });
chunk.visitRowMajor(
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);

// Or converted:
// The `converter` argument implements `DuckDBValueConverter`,
// which has the single method convertValue(value, type).
const columnValues = chunk.convertColumnValues(columnIndex, converter);
const columns = chunk.convertColumns(converter);
const rowValues = chunk.convertRowValues(rowIndex, converter);
const rows = chunk.convertRows(converter);

// The reader abstracts these low-level chunk manipulations
// and is recommended for most cases.
```
