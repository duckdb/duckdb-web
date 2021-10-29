---

layout: post
title:  "DuckDB-Wasm: Efficient Analytical SQL in the Browser"
author: André Kohn and Dominik Moritz
excerpt_separator: <!--more-->

---

_TLDR: DuckDB-Wasm is an in-process analytical SQL database for the browser. 
It is powered by WebAssembly, speaks Arrow fluently, reads Parquet, CSV and JSON files backed by Filesystem APIs or HTTP requests and has been tested with Chrome, Firefox, Safari and Node.js.
You can try it in your browser at [shell.duckdb.org](https://shell.duckdb.org)._

<!--more-->

<img src="/images/blog/duckdb_wasm.svg"
     alt="DuckDB-Wasm logo"
     width=240
     />

*DuckDB-Wasm is fast! If you're here for performance numbers, head over to our benchmarks at [shell.duckdb.org/versus](https://shell.duckdb.org/versus).*

## Efficient Analytics in the Browser

The web browser has evolved to a universal computation platform that even runs in your car. Its rise has been accompanied by increasing requirements for the browser programming language JavaScript.
JavaScript was, first and foremost, designed to be very flexible which comes at the cost of a reduced processing efficiency compared to native languages like C++.
This becomes particularly apparent when considering the execution times of more complex data analysis tasks that often fall behind the native execution by orders of magnitude.
In the past, such analysis tasks have therefore been pushed to servers that tie any client-side processing to additional round-trips over the internet and introduce their own set of scalability problems.

The processing capabilities of browsers were boosted tremendously 4 years ago with the introduction of WebAssembly:

> WebAssembly (abbreviated Wasm) is a binary instruction format for a stack-based virtual machine. Wasm is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications.
>
> The Wasm stack machine is designed to be encoded in a size- and load-time efficient binary format. WebAssembly aims to execute at native speed by taking advantage of common hardware capabilities available on a wide range of platforms.
> 
> (ref: [https://webassembly.org/](https://webassembly.org/))

Four years later, the WebAssembly revolution is in full progress with first implementations being shipped in four major browsers. It has already brought us [game engines](https://blog.unity.com/technology/webassembly-is-here), [entire IDEs](https://blog.stackblitz.com/posts/introducing-webcontainers/) and even a browser version of [Photoshop](https://web.dev/ps-on-the-web/). Today, we join the ranks with a first release of the npm library [@duckdb/duckdb-wasm](https://www.npmjs.com/package/@duckdb/duckdb-wasm).

As an in-process analytical database, DuckDB has the rare opportunity to siginificantly speed up OLAP workloads in the browser. We believe that there is a need for a comprehensive and self-contained data analysis library. DuckDB-wasm automatically offloads your queries to dedicated worker threads and reads Parquet, CSV and JSON files from either your local filesystem and HTTP servers driven by plain SQL input.
In this blog post, we want to introduce the library and present challenges on our journey towards a browser-native OLAP database.

*DuckDB-Wasm is not yet stable. You will find rough edges and bugs in this release. Please share your thoughts with us [on GitHub](https://github.com/duckdb/duckdb-wasm/discussions).*

## How to get data in?

Let's dive into examples.
DuckDB-Wasm provides a variety of ways to load your data. First, raw SQL value clauses like `INSERT INTO sometable VALUES (1, 'foo'), (2, 'bar')` are easy to formulate and only depend on plain SQL text. Alternatively, SQL statements like `CREATE TABLE foo AS SELECT * FROM 'somefile.parquet'` consult our integrated web filesystem to resolve `somefile.parquet` locally, remotely or from a buffer. The methods `insertCSVFromPath` and `insertJSONFromPath` further provide convenient ways to import CSV and JSON files using additional typed settings like column types. And finally, the method `insertArrowFromIPCStream` (optionally through `insertArrowTable`, `insertArrowBatches` or `insertArrowVectors`) copies raw IPC stream bytes directly into a WebAssembly stream decoder.

The following example presents different options how data can be imported into DuckDB-Wasm:

```ts
// Data can be inserted from an existing arrow.Table
await c.insertArrowTable(existingTable, { name: "arrow_table" });
// ..., from Arrow vectors
await c.insertArrowVectors({
    col1: arrow.Int32Vector.from([1, 2]),
    col2: arrow.Utf8Vector.from(["foo", "bar"]),
}, {
    name: "arrow_vectors"
});
// ..., from a raw Arrow IPC stream
const c = await db.connect();
const streamResponse = await fetch(`someapi`);
const streamReader = streamResponse.body.getReader();
const streamInserts = [];
while (true) {
    const { value, done } = await streamReader.read();
    if (done) break;
    streamInserts.push(c.insertArrowFromIPCStream(value, { name: "streamed" }));
}
await Promise.all(streamInserts);

// ..., from CSV files
// (interchangeable: registerFile{Text,Buffer,URL,Handle})
await db.registerFileText(`data.csv`, "1|foo\n2|bar\n");
// ... with typed insert options
await db.importCSVFromPath('data.csv', {
    schema: 'main',
    name: 'foo',
    detect: false,
    header: false,
    delimiter: '|',
    columns: {
        col1: new arrow.Int32(),
        col2: new arrow.Utf8(),
    }
});

// ..., from JSON documents in row-major format
await db.registerFileText("rows.json", `[
    { “col1”: 1, “col2”: “foo” },
    { “col1”: 2, “col2”: “bar” },
]`);
// ... or column-major format
await db.registerFileText("columns.json", `{
    “col1”: [1, 2],
    “col2”: [“foo”, “bar”]
}`);
// ... with typed insert options
await db.importJSONFromPath('rows.json', { name: 'rows' });
await db.importJSONFromPath('columns.json', { name: 'columns' });

// ..., from Parquet files
const pickedFile: File = letUserPickFile();
await db.registerFileHandle("local.parquet", pickedFile);
await db.registerFileURL("remote.parquet", "https://origin/remote.parquet");

// ..., by specifying URLs in the SQL text
await c.query(`
    CREATE TABLE direct AS
        SELECT * FROM "https://origin/remote.parquet"
`);
// ..., or by executing raw insert statements
await c.query(`INSERT INTO existing_table
    VALUES (1, "foo"), (2, "bar")`);
```

## How to get data out?

Now that we have the data loaded, DuckDB-Wasm can run queries on two different ways that differ in the result materialization. First, the method `query` runs a query to completion and returns the results as single `arrow.Table`. Second, the method `send` fetches query results lazily through an `arrow.RecordBatchStreamReader`. Both methods are generic and allow for typed results in Typescript:

```ts
// Either materialize the query result
await conn.query<{ v: arrow.Int32 }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);
// ..., or fetch the result chunks lazily
for await (const batch of await conn.send<{ v: arrow.Int32 }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`)) {
    // ...
} 
```

Alternatively, you can prepare statements for parameterized queries using:

``` ts
// Prepare query
const stmt = await conn.prepare<{ v: arrow.Int32 }>(
    `SELECT (v + ?) as v FROM generate_series(0, 10000) as t(v);`
);
// ... and run the query with materialized results
await stmt.query(234);
// ... or result chunks
for await (const batch of await stmt.send(234)) {
    // ...
}
```

## Looks like Arrow to me

DuckDB-Wasm uses [Arrow](https://arrow.apache.org) as data protocol for the data import and all query results. Arrow is a database-friendly columnar format that is organized in chunks of column vectors, called record batches and that support zero-copy reads with only a small overhead. The npm library `apache-arrow` implements the Arrow format in the browser and is already used by other data processing frameworks, like [Arquero](https://github.com/uwdata/arquero). Arrow therefore not only spares us the implementation of the SQL type logic in JavaScript, it also makes us compatible to existing tools.

_Why not use plain Javascript objects?_

WebAssembly is isolated and memory-safe. This isolation is part of it's DNA and drives fundamental design decisions in DuckDB-Wasm. For example, WebAssembly introduces a barrier towards the traditional JavaScript heap. Crossing this barrier is difficult as JavaScript has to deal with native function calls, memory ownership and serialization performance. Languages like C++ make this worse as they rely on smart pointers that are not available through the FFI. They leave us with the choice to either pass memory ownership to static singletons within the WebAssembly instance or maintain the memory through C-style APIs in JavaScript, a language that is too dynamic for sound implementations of the [RAII idiom](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization). The memory-isolation forces us to serialize data before we can pass it to the WebAssembly instance. Browsers can serialize JavaScript objects natively to and from JSON using the functions `JSON.stringify` and `JSON.parse` but this is slower compared to, for example, copying raw native arrays.

## Web Filesystem

DuckDB-Wasm integrates a dedicated filesystem for WebAssembly. DuckDB itself is built on top of a virtual filesystem that decouples higher level tasks, such as reading a Parquet file, from low-level filesystem APIs that are specific to the operating system. We leverage this abstraction in DuckDB-Wasm to tailor filesystem implementations to the different WebAssembly environments.

The following figure shows our current web filesystem in action. The sequence diagram presents a user running a SQL query that scans a single Parquet file. The query is first offloaded to a dedicated web worker through a JavaScript API. There, it is passed to the WebAssembly module that processes the query until the execution hits the `parquet_scan` table function. This table function then reads the file using a buffered filesystem which, in turn, issues paged reads on the web filesystem. This web filesystem then uses an environment-specific runtime to read the file from several possible locations.

<p align="center">
    <img src="/images/blog/webfs.svg"
        alt="Example Web Filesystem shown visually"
        title="Web Filesystem"
        style="width:100%; max-width:800px"
        />
</p>

Depending on the context, the Parquet file may either reside on the local device, on a remote server or in a buffer that was registered by the user upfront. We deliberately treat all three cases equally to unify the retrieval and processing of external data. This does not only simplify the analysis, it also enables more advanced features like partially consuming structured file formats. Parquet files, for example, consist of multiple row groups that store data in a column-major fashion. As a result, we may not need to download the entire file for a query but only required bytes.

A query like `SELECT count(*) FROM parquet_scan(...)`, for example, can be evaluated on the file metadata alone and will finish in milliseconds even on remote files that are several terabytes large. Another more general example are paging scans with `LIMIT` and `OFFSET` qualifiers such as `SELECT * FROM parquet_scan(...) LIMIT 20 OFFSET 40`, or queries with selective filter predicates where entire row groups can be skipped based on metadata statistics. These partial file reads are no groundbreaking novelty and could be implemented in JavaScript today, but with DuckDB-Wasm, these optimizations are now driven by the semantics of SQL queries instead of fine-tuned application logic.

*Note: The common denominator among the available File APIs is unfortunately not large. This limits the features that we can provide in the browser. For example, local persistency of DuckDB databases would be a feature with significant impact but requires a way to either read and write synchronously into user-provided files or IndexedDB. We might be able to bypass these limitations in the future but this is subject of ongoing research.*

## Advanced Features

WebAssembly 1.0 has landed in all major browsers. The WebAssembly Community Group fixed the design of this first version back in November 2017, which is now referred to as WebAssembly MVP. Since then, the development has been ongoing with eight additional features that have been added to the standard and at least five proposals that are currently in progress.

The rapid pace of this development presents challenges and opportunities for library authors. On the one hand, the different features find their way into the browsers at different speeds which leads to a fractured space of post-MVP functionality. On the other hand, features can bring flat performance improvements and are therefore indispensable when aiming for a maximum performance.

The most promising feature for DuckDB-Wasm is [exception handling](https://github.com/WebAssembly/exception-handling/blob/main/proposals/exception-handling/Exceptions.md) which is already enabled by default in Chrome 95. DuckDB and DuckDB-Wasm are written in C++ and use exceptions for faulty situations. DuckDB does not use exceptions for general control flow but to automatically propagate errors upwards to the top-level plan driver. In native environments, these exceptions are implemented as “zero-cost exceptions” as they induce no overhead until they are thrown. With the WebAssembly MVP, however, that is no longer possible as the compiler toolchain Emscripten has to emulate exceptions through JavaScript. Without WebAssembly exceptions, DuckDB-Wasm calls throwing functions through a JavaScript hook that can catch exceptions emulated through JavaScript `aborts`. An example for these hook calls is shown in the following figure. Both stack traces originate from a single paged read of a Parquet file in DuckDB-Wasm. The left side shows a stack trace with the WebAssembly MVP and requires multiple calls through the functions `wasm-to-js-i*` . The right stack trace uses WebAssembly exceptions without any hook calls.

<p align="center">
    <img src="/images/blog/wasm-eh.png"
        alt="Exception handling shown visually"
        title="WebAssembly Exceptions"
        style="width:100%; max-width:600px;border-radius:4px;border:1px solid rgb(200,200,200);"
        />
</p>

This fractured feature space is a temporary challenge that will be resolved once high-impact features like exception handling, SIMD and bulk-memory operations are available everywhere. In the meantime, we will ship multiple WebAssembly modules that are compiled for different feature sets and adaptively pick the best bundle for you using dynamic browser checks.

The following example shows how the asynchronous version of DuckDB-Wasm can be instantiated using either manual or JsDelivr bundles:

```ts
// Import the ESM bundle (supports tree-shaking)
import * as duckdb from '@duckdb/duckdb-wasm/dist/duckdb-esm.js';

// Either bundle them manually, for example as Webpack assets
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb.wasm';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-next.wasm';
import duckdb_wasm_next_coi from '@duckdb/duckdb-wasm/dist/duckdb-next-coi.wasm';
const WEBPACK_BUNDLES: duckdb.DuckDBBundles = {
    asyncDefault: {
        mainModule: duckdb_wasm,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async.worker.js', import.meta.url).toString(),
    },
    asyncNext: {
        mainModule: duckdb_wasm_next,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async-next.worker.js', import.meta.url).toString(),
    },
    asyncNextCOI: {
        mainModule: duckdb_wasm_next_coi,
        mainWorker: new URL(
            '@duckdb/duckdb-wasm/dist/duckdb-browser-async-next-coi.worker.js',
            import.meta.url,
        ).toString(),
        pthreadWorker: new URL(
            '@duckdb/duckdb-wasm/dist/duckdb-browser-async-next-coi.pthread.worker.js',
            import.meta.url,
        ).toString(),
    },
};
// ..., or load the bundles from jsdelivr
const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);
// Instantiate the asynchronus version of DuckDB-Wasm
const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
```

*You can also test the features and selected bundle in your browser using the web shell command `.config` .*

## Multithreading

In 2018, the Spectre and Meltdown vulnerabilities sent crippling shockwaves through the internet. Today, we are facing the repercussions of these events, in particular in software that runs arbitrary user code - such as web browsers. Shortly after the publications, all major browser vendors restricted the use of `SharedArrayBuffers` to prevent dangerous timing attacks. `SharedArrayBuffers` are raw buffers that can be shared among web workers for global state and an alternative to the browser-specific message passing. These restrictions had detrimental effects on WebAssembly modules since  `SharedArrayBuffers` are neccessary for the implementation of POSIX threads in WebAssembly.

Without `SharedArrayBuffers`, WebAssembly modules can run in a dedicated web worker to unblock the main event loop but won't be able to spawn additional workers for parallel computations within the same instance. By default, we therefore cannot unleash the parallel query execution of DuckDB in the web. However, browser vendors have recently started to reenable `SharedArrayBuffers for Websites that are [cross-origin-isolated](https://web.dev/coop-coep/). A website is cross-origin-isolated if it ships the main document with the following HTTP headers:

```
Cross-Origin-Embedded-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
```

These headers will instruct browsers to A) isolate the top-level document from other top-level documents outside its own origin and B) prevent the document from making arbitrary cross-origin requests unless the requested resource explicitly opts in. Both restrictions have far reaching implications for a website since many third-party data sources won't yet provide the headers today and the top-level isolation currently hinders the communication with, for example, OAuth pop up's ([there are plans to lift that](https://github.com/whatwg/html/issues/6364)).

*We therefore assume that DuckDB-Wasm will find the majority of users on non-isolated websites. We are, however, experimenting with dedicated bundles for isolated sites using the suffix `-next-coi`) and will closely monitor the future need of our users. Share your thoughts with us [here]().*  

## Web Shell

We further host a web shell powered by DuckDB-Wasm alongside the library release at [shell.duckdb.org](https://shell.duckdb.org).
Use the following shell commands to query remote TPC-H files at scale factor 0.01.
When querying your own, make sure to properly set CORS headers since your browser will otherwise block these requests.
You can alternatively use the `.files` command to register files from the local filesystem.

```sql
.timer on

select count(*) from 'https://shell.duckdb.org/data/tpch/0_01/parquet/lineitem.parquet';
select count(*) from 'https://shell.duckdb.org/data/tpch/0_01/parquet/customer.parquet';
select avg(c_acctbal) from 'https://shell.duckdb.org/data/tpch/0_01/parquet/customer.parquet';

select * from 'https://shell.duckdb.org/data/tpch/0_01/parquet/orders.parquet' limit 10;

select n_name, avg(c_acctbal) from
  'https://shell.duckdb.org/data/tpch/0_01/parquet/customer.parquet',
  'https://shell.duckdb.org/data/tpch/0_01/parquet/nation.parquet'
where c_nationkey = n_nationkey group by n_name;

select * from
  'https://shell.duckdb.org/data/tpch/0_01/parquet/region.parquet',
  'https://shell.duckdb.org/data/tpch/0_01/parquet/nation.parquet'
where r_regionkey = n_regionkey;
```

## Evaluation

The following table teases the execution times of some TPC-H queries at scale factor 0.5 using the libraries [DuckDB-Wasm](https://www.npmjs.com/package/@duckdb/duckdb-wasm), [sql.js](https://github.com/sql-js/sql.js/), [Arquero](https://github.com/uwdata/arquero) and [Lovefield](https://github.com/google/lovefield). You can find a more in-depth discussion with all TPC-H queries, additional scale factors and Microbenchmarks [here](https://shell.duckdb.org/versus).

| Query | DuckDB-wasm | sql.js | Arquero | Lovefield |
|:--|--:|--:|--:|--:|
| 1 | **0.855 s** | 8.441 s | 24.031 s | 12.666 s |
| 3 | **0.179 s** | 1.758 s | 16.848 s | 3.587 s |
| 4 | **0.151 s** | 0.384 s | 6.519 s | 3.779 s |
| 5 | **0.197 s** | 1.965 s | 18.286 s | 13.117 s |
| 6 | **0.086 s** | 1.294 s | 1.379 s | 5.253 s |
| 7 | **0.319 s** | 2.677 s | 6.013 s | 74.926 s |
| 8 | **0.236 s** | 4.126 s | 2.589 s | 18.983 s |
| 10 | **0.351 s** | 1.238 s | 23.096 s | 18.229 s |
| 12 | **0.276 s** | 1.080 s | 11.932 s | 10.372 s |
| 13 | **0.194 s** | 5.887 s | 16.387 s | 9.795 s |
| 14 | **0.086 s** | 1.194 s | 6.332 s | 6.449 s |
| 16 | **0.137 s** | 0.453 s | 0.294 s | 5.590 s |
| 19 | **0.377 s** | 1.272 s | 65.403 s | 9.977 s |

## Future Research

We believe that WebAssembly unveils hitherto dormant potential for shared query processing between clients and servers. Pushing computation closer to the client can eliminate costly round-trips to the server and thus increase interactivity and scalability of in-browser analytics. We further believe that the release of DuckDB-Wasm could be the first step towards a more universal data plane spanning across multiple layers including traditional database servers, clients, CDN workers and computational storage. As an in-process analytical database, DuckDB might be the ideal driver for distributed query plans that increase the scalability and interactivity of SQL databases at low costs.

