---
layout: post
title: "DuckDB Node Neo Client"
author: "Jeff Raymakers"
thumb: "/images/blog/thumbs/nodejs.svg"
image: "/images/blog/thumbs/nodejs.png"
excerpt: "The new DuckDB Node client, “Neo”, provides a powerful and friendly way to use your favorite database"
tags: ["using DuckDB"]
---

Meet the newest DuckDB client API: [DuckDB Node “Neo”]({% link docs/stable/clients/node_neo/overview.md %})!

You may be familiar with DuckDB’s [old Node client](https://www.npmjs.com/package/duckdb). While it has served the community well over the years, “Neo” aims to learn from and improve upon its predecessor. It presents a friendlier API, supports more features, and uses a more robust and maintainable architecture. It provides both high-level conveniences and low-level access. Let’s take a tour!

## What Does It Offer?

### Friendly, Modern API

The old Node client’s API is based on [SQLite’s](https://www.npmjs.com/package/sqlite3). While familiar to many, it uses an awkward, dated callback-based style. Neo uses [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) natively.

```ts
const result = await connection.run(`SELECT 'Hello, Neo!'`);
```

Additionally, Neo is built from the ground up in [TypeScript](https://www.typescriptlang.org/). Carefully chosen names and types minimize the need to check documentation.

```ts
const columnNames = result.columnNames();
const columnTypes = result.columnTypes();
```

Neo also provides convenient helpers to read only as many rows as needed and return them in either column-major or row-major format.

```ts
const reader = await connection.runAndReadUtil('FROM range(5000)',
    1000);
const rows = reader.getRows();
// OR: const columns = reader.getColumns();
```

### Full Data Type Support

DuckDB supports a [rich variety of data types]({% link docs/stable/sql/data_types/overview.md %}). Neo supports every built-in type as well as custom types such as [`JSON`]({% link docs/stable/data/json/json_type.md %}). For example, `ARRAY`:

```ts
if (columnType.typeId === DuckDBTypeId.ARRAY) {
  const arrayValueType = columnType.valueType;
  const arrayLength = columnType.length;
}
```

`DECIMAL`:

```ts
if (columnType.typeId === DuckDBTypeId.DECIMAL) {
  const decimalWidth = columnType.width;
  const decimalScale = columnType.scale;
}
```

And `JSON`:

```ts
if (columnType.alias === 'JSON') {
  const json = JSON.parse(columnValue);
}
```

Type-specific utilities ease common conversions such as producing human-readable strings from [`TIMESTAMP`]({% link docs/stable/sql/data_types/timestamp.md %})s or [`DECIMAL`]({% link docs/stable/sql/data_types/numeric.md %}#fixed-point-decimals)s, while preserving access to the raw values for lossless processing.

```ts
if (columnType.typeId === DuckDBTypeId.TIMESTAMP) {
  const timestampMicros = columnValue.micros; // bigint
  const timestampString = columnValue.toString();
  const {
    date: { year, month, day },
    time: { hour, min, sec, micros },
  } = columnValue.toParts();
}
```

### Advanced Features

Need to bind specific types of values to [prepared statements]({% link docs/stable/sql/query_syntax/prepared_statements.md %}), or precisely [control SQL execution]({% link docs/stable/clients/c/api.md %}#pending-result-interface)? Perhaps you want to leverage DuckDB’s parser to [extract statements]({% link docs/stable/clients/c/api.md %}#extract-statements), or efficiently [append data to a table]({% link docs/stable/clients/c/appender.md %}). Neo has you covered, providing full access to these powerful features of DuckDB.

#### Binding Values to Prepared Statements

When binding values to parameters of [prepared statements]({% link docs/stable/sql/query_syntax/prepared_statements.md %}), you can select the SQL data type. This is useful for types that don’t have a natural equivalent in JavaScript.

```ts
const prepared = await connection.prepare('SELECT $1, $2');
prepared.bindTimestamp(1, new DuckDBTimestampValue(micros));
prepared.bindDecimal(2, new DuckDBDecimalValue(value, width, scale));
const result = await prepared.run();
```

#### Controlling Task Execution

Using [pending results]({% link docs/stable/clients/c/api.md %}#pending-result-interface) allows pausing or stopping SQL execution at any point, even before the result is ready.

```ts
import { DuckDBPendingResultState } from '@duckdb/node-api';

// Placeholder to demonstrate doing other work between tasks.
async function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const prepared = await connection.prepare('FROM range(10_000_000)');
const pending = prepared.start();
// Run tasks until the result is ready.
// This allows execution to be paused and resumed as needed.
// Other work can be done between tasks.
while (pending.runTask() !== DuckDBPendingResultState.RESULT_READY) {
  console.log('not ready');
  await sleep(1);
}
console.log('ready');
const result = await pending.getResult();
// ...
```

#### Extracting Statements and Running Them with Parameters

You can run multi-statement SQL containing parameters using the [extract statements API]({% link docs/stable/clients/c/api.md %}#extract-statements).

```ts
// Parse this multi-statement input into separate statements.
const extractedStatements = await connection.extractStatements(`
  CREATE OR REPLACE TABLE numbers AS FROM range(?);
  FROM numbers WHERE range < ?;
  DROP TABLE numbers;
`);
const parameterValues = [10, 7];
const stmtCount = extractedStatements.count;
// Run each statement, binding values as needed.
for (let stmtIndex = 0; stmtIndex < stmtCount; stmtIndex++) {
  const prepared = await extractedStatements.prepare(stmtIndex);
  const paramCount = prepared.parameterCount;
  for (let paramIndex = 1; paramIndex <= paramCount; paramIndex++) {
    prepared.bindInteger(paramIndex, parameterValues.shift());
  }
  const result = await prepared.run();
  // ...
}
```

#### Appending Data to a Table

The [appender API]({% link docs/stable/clients/c/appender.md %}) is the most efficient way to bulk insert data into a table.

```ts
await connection.run(
  `CREATE OR REPLACE TABLE target_table(i INTEGER, v VARCHAR)`
);

const appender = await connection.createAppender('main', 'target_table');

appender.appendInteger(100);
appender.appendVarchar('walk');
appender.endRow();

appender.appendInteger(200);
appender.appendVarchar('swim');
appender.endRow();

appender.appendInteger(300);
appender.appendVarchar('fly');
appender.endRow();

appender.close();
```

## How Is It Built?

### Dependencies

Neo uses a different implementation approach from most other DuckDB client APIs, including the old Node client. It binds to DuckDB’s [C API]({% link docs/stable/clients/c/overview.md %}) instead of the C++ API.

Why should you care? Using DuckDB’s C++ API means building all of DuckDB from scratch. Each client API using this approach ships with a slightly different build of DuckDB. This can create headaches for both library maintainers and consumers.

Maintainers need to pull in the entire DuckDB source code. This increases the cost and complexity of the build, and thus the cost of code changes and especially DuckDB version updates. These costs often lead to significant delays in fixing bugs or supporting new versions.

Consumers are impacted by these delays. There’s also the possibility of subtle behavioral differences between the builds in each client, perhaps introduced by different compile-time configuration.

> Some client APIs reside in the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/tools). This addresses some of the problems above, but increases the cost and complexity of maintaining DuckDB itself.

To use DuckDB’s C API, on the other hand, one only needs to depend on [released binaries](https://github.com/duckdb/duckdb/releases). This significantly simplifies the maintenance required, speeds up builds, and minimizes the cost of updates. It removes the uncertainty and risk of rebuilding DuckDB.

### Packages

DuckDB requires different binaries for each platform. Distributing platform-specific binaries in Node packages is notoriously challenging. It can often lead to inscrutable errors when installing, when the package manager attempts to rebuild some component from source, using whatever build and configuration tools happen to be around.

Neo uses a package design aimed to avoid these problems. Inspired by [ESBuild](https://github.com/evanw/esbuild/pull/1621), Neo packages pre-built binaries for each supported platform in a separate package. Each of these packages declares the particular platform (e.g., `os` and `cpu`) it supports. Then, the main package depends on all these platform-specific packages using `optionalDependencies`.

When the main package is installed, the package manager will only install optionalDependencies for supported platforms. So you only get exactly the binaries you need, no more. If installed on an unsupported platform, no binaries will be installed. At no point will an attempt to build from source occur during install.

### Layers

The DuckDB Node Neo client has multiple layers. Most people will want to use Neo’s main “api” package, [@duckdb/node-api](https://www.npmjs.com/package/@duckdb/node-api). This contains the friendly API with convenient helpers. But, for advanced use cases, Neo also exposes the lower-level “bindings” package, [@duckdb/node-bindings](https://www.npmjs.com/package/@duckdb/node-bindings), which implements a more direct translation of DuckDB’s C API into Node.

This API has TypeScript definitions, but, as it follows the conventions of C, it can be awkward to use from Node. However, it provides a relatively unopinionated way to access DuckDB, which supports building special-purpose applications or alternate higher-level APIs.

## Where Is It Headed?

Neo is currently marked “alpha”. This is an indication of completeness and maturity, not robustness. Most of the functionality of DuckDB’s C API is exposed, and what is exposed has extensive tests. But it’s relatively new, so it may contain undiscovered bugs.

Additionally, some areas of functionality are not yet complete:

* Appending and binding advanced data types. These require additional functions in DuckDB’s C API. The goal is to add these for the next release of DuckDB 1.2, [currently planned for January 2025]({% link release_calendar.md %}).

* Writing to data chunk [vectors]({% link docs/stable/internals/vector.md %}). Modifying binary buffers in a way that can be seen by a native layer presents special challenges in the Node environment. This is a high priority to work on in the near future.

* User-defined types & functions. The necessary functions and types were added to the DuckDB C API relatively recently, in v1.1.0. This is on the near-term roadmap.

* Profiling info. This was added in v1.1.0. It’s on the roadmap.

* Table descriptions. This was also added in v1.1.0. It’s on the roadmap.

New versions of DuckDB will include additions to the C API. Since Neo aims to cover all the functionality of the C API, these additions will be added to the roadmap as they are released.

If you have a feature request, or other feedback, [let us know](https://github.com/duckdb/duckdb-node-neo/issues)! [Pull requests](https://github.com/duckdb/duckdb-node-neo/pulls) are also welcome.

## What Now?

DuckDB Node Neo provides a friendly and powerful way to use DuckDB with Node. By leveraging DuckDB’s C API, it exemplifies a new, more maintainable way to build on DuckDB, providing benefits to maintainers and consumers alike. It’s still young, but growing up fast. [Try it yourself](https://www.npmjs.com/package/@duckdb/node-api)!
