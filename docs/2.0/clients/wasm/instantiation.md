---
layout: docu
redirect_from:
- /docs/api/wasm/instantiation
- /docs/clients/wasm/instantiation
- /docs/stable/clients/wasm/instantiation
- /docs/current/clients/wasm/instantiation
- /docs/lts/clients/wasm/instantiation
- /docs/preview/clients/wasm/instantiation
title: Instantiate
---

## Overview

DuckDB-Wasm can be instantiated in several ways, depending on how your application bundles and serves its assets. Each approach resolves the `mainModule` (the WebAssembly file) and the `mainWorker` (the worker script) for the browser's capabilities, then hands them to `AsyncDuckDB`.

This page shows the patterns for a jsDelivr CDN, webpack, Vite and statically served files. Once instantiated, the `db` object is used to [import data]({% link docs/2.0/clients/wasm/data_ingestion.md %}) and [run queries]({% link docs/2.0/clients/wasm/query.md %}).

## Bundle Selection

DuckDB-Wasm ships two WebAssembly modules compiled for different browser feature sets. The `selectBundle` function runs dynamic browser checks and picks the fastest bundle the current browser supports:

* `base` — single-threaded, and the baseline that runs everywhere. It requires Wasm-level exception handling; DuckDB and DuckDB-Wasm are written in C++ and use exceptions to propagate errors, so native exception handling avoids emulating them through JavaScript. Every modern browser supports it, and `selectBundle` throws if a browser does not.
* `threads` — adds threading for parallel query execution. It additionally requires Wasm SIMD and threads, and the page must be [cross-origin isolated]({% link docs/2.0/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation). It must be opted into explicitly (see [Threading](#threading)).

Earlier releases shipped three bundles: `mvp` (the WebAssembly 1.0 baseline with no exception handling), `eh` (adding exception handling), and `coi` (adding threading). DuckDB-Wasm now requires exception handling, so the `mvp` bundle has been removed. The `base` bundle replaces `eh` and is the new baseline, and the `threads` bundle replaces `coi`.

The examples below all call `selectBundle` so the browser receives the fastest bundle it can run. You can also inspect the selected bundle and feature set from the [web shell](https://shell.duckdb.org) with the `.features` command.

## `cdn(jsdelivr)`

The simplest way to load DuckDB-Wasm is straight from a CDN, with no build step or bundler configuration. `getJsDelivrBundles()` returns the set of bundles hosted on [jsDelivr](https://www.jsdelivr.com/package/npm/@duckdb/duckdb-wasm), and `selectBundle` picks the one that matches the browser. Because a Web Worker script must be same-origin, the CDN worker URL is wrapped in a `Blob` that `importScripts` it, and the temporary object URL is revoked once the worker has started.

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);

const worker_url = URL.createObjectURL(
  new Blob([`importScripts("${bundle.mainWorker}");`], {type: 'text/javascript'})
);

// Instantiate the asynchronous version of DuckDB-Wasm
const worker = new Worker(worker_url);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
URL.revokeObjectURL(worker_url);
```

## `webpack`

When your application is built with [webpack](https://webpack.js.org/), let the bundler resolve and emit DuckDB-Wasm's assets instead of fetching them from a CDN. Import the `.wasm` module directly, and reference the worker script with `new URL(..., import.meta.url)` so that webpack fingerprints it and rewrites the path to the emitted file. The bundle is declared manually because its final location is known only after the build. This declares the single-threaded `base` bundle; to add the threaded bundle, see [Threading](#threading).

```ts
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-base.wasm';
const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    base: {
        mainModule: duckdb_wasm,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-base.worker.js', import.meta.url).toString(),
    },
};
// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
// Instantiate the asynchronous version of DuckDB-Wasm
const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
```

## `vite`

[Vite](https://vitejs.dev/) resolves assets a little differently: appending the `?url` suffix to an import tells Vite to return the asset's final URL rather than its contents. Import the `.wasm` module and the worker script this way, assemble them into the manual bundle definition, and let `selectBundle` resolve the bundle for the browser at runtime. This declares the single-threaded `base` bundle; to add the threaded bundle, see [Threading](#threading).

```ts
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-base.wasm?url';
import base_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-base.worker.js?url';

const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    base: {
        mainModule: duckdb_wasm,
        mainWorker: base_worker,
    },
};
// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
// Instantiate the asynchronous version of DuckDB-Wasm
const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
```

## Statically Served

If you would rather not depend on a CDN or a bundler, you can host the DuckDB-Wasm files yourself. Manually download the distribution files from <https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/dist/>, serve them from your own origin, and point the bundle paths at those locations. This keeps every asset on your own server, which suits offline, air-gapped, or strict content-security-policy deployments. Update the placeholder paths below to match where you serve the files.

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    base: {
        mainModule: 'change/me/../duckdb-base.wasm',
        mainWorker: 'change/me/../duckdb-browser-base.worker.js',
    },
};
// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
// Instantiate the asynchronous version of DuckDB-Wasm
const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
```

## Configuration

`instantiate()` starts DuckDB-Wasm with default settings. To change how the database behaves, call `open()` on the `db` object before opening a connection, passing a configuration object:

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

await db.open({
    path: ':memory:',
    query: {
        castBigIntToDouble: true,
        castDecimalToDouble: true,
        castDurationToTime64: true,
        castTimestampToDate: true,
        queryPollingInterval: 1000,
    },
});

const conn = await db.connect();
```

Commonly used fields of the configuration object:

* `path`: the database file to open. Defaults to an in-memory database (`:memory:`). Use an `opfs://` path to persist data to the browser's Origin Private File System (see [Persistence with OPFS](#persistence-with-opfs)).
* `accessMode`: `duckdb.DuckDBAccessMode.READ_ONLY` or `duckdb.DuckDBAccessMode.READ_WRITE`.
* `allowUnsignedExtensions`: allow loading extensions that are not signed (see [Load Extensions]({% link docs/2.0/clients/wasm/extensions.md %})).
* `maximumThreads`: the number of threads to use. This takes effect only with the threaded bundle on a cross-origin-isolated page (see [Threading](#threading)).
* `query`: controls how query results are converted from Arrow into JavaScript values.
* `opfs`: controls how `opfs://` files other than the database file are registered. Set `fileHandling` to `'auto'` to register files referenced in SQL automatically; the default is manual registration (see [Persistence with OPFS](#persistence-with-opfs)).

DuckDB-Wasm also accepts fields that control spilling, storage locations, the extension repository, and data conversion:

* `spill`: spill data that does not fit in memory to the temporary directory, rather than failing with an out-of-memory error. This is enabled by default and can be turned off by setting it to `false`. See [Out of Memory]({% link docs/2.0/clients/wasm/troubleshoot.md %}#out-of-memory).
* `temporaryDirectory`: where spilled data is written. Defaults to `js_buffer://tmp`, which uses buffers held by the runtime outside the Wasm heap. Point it at an `opfs://` path to spill into the Origin Private File System instead.
* `homeDirectory`: DuckDB's home directory, where it stores data next to the user such as persistent secrets. Set it to `opfs://home` so that this data survives across sessions.
* `extensionRepository`: the repository extensions are loaded from, equivalent to `custom_extension_repository`. Defaults to `extensions.duckdb.org` (see [Load Extensions]({% link docs/2.0/clients/wasm/extensions.md %}#serving-extensions-from-a-third-party-repository)).
* `filesystem`: tunes HTTP reads. `reliableHeadRequests`, `allowFullHTTPReads`, and `forceFullHTTPReads` control whether range requests are used and whether a full download is allowed as a fallback (see [Troubleshoot]({% link docs/2.0/clients/wasm/troubleshoot.md %}#network-error-when-querying-remote-files)).
* `arrowLosslessConversion`: use an alternate Arrow conversion that preserves the full range and precision of DuckDB values.
* `customUserAgent`: append a custom string to the user agent that DuckDB-Wasm reports on outgoing requests.

The `query` object tunes the Arrow-to-JavaScript type mapping:

* `castBigIntToDouble`: return 64-bit integers as JavaScript numbers instead of `BigInt` values. This is convenient, but large integers can lose precision.
* `castDecimalToDouble`: return `DECIMAL` values as floating-point numbers instead of DuckDB's exact decimal representation.
* `castTimestampToDate`: return `TIMESTAMP` values as JavaScript `Date` objects.
* `castDurationToTime64`: return duration values as 64-bit (microsecond) time values.
* `queryPollingInterval`: the interval, in milliseconds, at which streaming queries poll for results.

## Threading

By default DuckDB-Wasm runs on a single thread. The threaded bundle runs queries across multiple threads, but it has two requirements: the page must be [cross-origin isolated]({% link docs/2.0/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation), and you must add the `threads` bundle to the set you pass to `selectBundle`, because `getJsDelivrBundles()` returns only the `base` bundle. The `threads` bundle also needs a third artifact, the pthread worker, alongside the usual module and worker:

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

const DIST = 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/dist/';

// getJsDelivrBundles() returns only base, so add threads explicitly
const bundles: duckdb.DuckDBBundles = {
    ...duckdb.getJsDelivrBundles(),
    threads: {
        mainModule: `${DIST}duckdb-threads.wasm`,
        mainWorker: `${DIST}duckdb-browser-threads.worker.js`,
        pthreadWorker: `${DIST}duckdb-browser-threads.pthread.worker.js`,
    },
};

// selectBundle picks threads only on a cross-origin-isolated page whose browser
// supports Wasm exceptions, SIMD, and threads; otherwise it falls back to base
const bundle = await duckdb.selectBundle(bundles);

// Worker scripts must be same-origin, so wrap the CDN worker in a Blob URL
const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], { type: 'text/javascript' })
);
const worker = new Worker(worker_url);
const db = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(), worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
URL.revokeObjectURL(worker_url);

// Configure the thread count (only effective on the threaded bundle)
await db.open({ maximumThreads: 4 });
const conn = await db.connect();
```

Because `selectBundle` falls back to the `base` bundle when the `threads` requirements are not met, the same code runs everywhere: on a page that is not cross-origin isolated it simply runs single-threaded, and `bundle.pthreadWorker` is `null`. Two things to keep in mind when deploying the threaded bundle:

* The page must be served with the `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` headers, which is what makes the browser expose `SharedArrayBuffer` and report the page as cross-origin isolated. See [Cross-Origin Isolation]({% link docs/2.0/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation).
* Extensions must be built for the threaded platform. The `threads` bundle uses the `wasm_threads` extension platform, while the `base` bundle uses `wasm_base`, so an extension has to be published for the platform of the bundle that loads it.

## Persistence with OPFS

By default a DuckDB-Wasm database lives in memory and is lost when the page closes. To persist data across page reloads and sessions, open the database from the browser's [Origin Private File System (OPFS)](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) by giving `open()` a `path` with the `opfs://` scheme:

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
await db.open({
    path: 'opfs://duckdb.db',
    accessMode: duckdb.DuckDBAccessMode.READ_WRITE,
});

const conn = await db.connect();
await conn.query(`CREATE TABLE t AS SELECT * FROM range(10) AS r(i)`);

// Flush changes to OPFS so they survive a reload
await conn.query(`CHECKPOINT`);
```

Reopening the same `opfs://` path in a later session restores the tables.

You can also read and write other `opfs://` files directly from SQL. By default, DuckDB-Wasm uses manual registration: every OPFS file other than the database file has to be registered with `db.registerOPFSFileName()` before a statement uses it, and dropped with `db.dropFile()` afterwards:

```ts
await db.open({
    path: 'opfs://duckdb.db',
    accessMode: duckdb.DuckDBAccessMode.READ_WRITE,
});

// Register the file, use it from SQL, then release its handle
await db.registerOPFSFileName('opfs://export.parquet');
await conn.query(`COPY (SELECT * FROM t) TO 'opfs://export.parquet'`);
await db.dropFile('opfs://export.parquet');
```

Alternatively, set `opfs.fileHandling` to `'auto'`. DuckDB-Wasm then scans each statement for single-quoted `'opfs://...'` literals, registers those files before execution (creating them and any missing directories if needed) and drops their handles afterwards. This option only takes effect when the database itself was opened from an `opfs://` path:

```ts
await db.open({
    path: 'opfs://duckdb.db',
    accessMode: duckdb.DuckDBAccessMode.READ_WRITE,
    opfs: { fileHandling: 'auto' },
});

// Read a Parquet file stored in OPFS, and write a CSV back to OPFS
await conn.query(`CREATE TABLE t AS SELECT * FROM 'opfs://data.parquet'`);
await conn.query(`COPY (SELECT * FROM t) TO 'opfs://export.csv'`);
```

Automatic registration is convenient for one-off reads. Manual registration requires more code but avoids re-acquiring an OPFS access handle on every statement, which adds up for applications that run many small queries.

> Note OPFS access relies on synchronous file access handles, which browsers expose only inside a Web Worker; DuckDB-Wasm's asynchronous API already runs in one. Keep these limitations in mind:
>
> * Call `CHECKPOINT` to flush writes to disk.
> * A file can be held by only one handle at a time. Drop registered files with `db.dropFile()` (or `db.dropFiles()`) before another connection or database instance opens them.
> * Moving files into or out of OPFS is not yet supported. Renaming files from SQL only works between two OPFS files that are both already registered.

## Further Reading

* [Import Data]({% link docs/2.0/clients/wasm/data_ingestion.md %}) — registering files and inserting data into the instantiated database.
* [Run Queries]({% link docs/2.0/clients/wasm/query.md %}) — executing queries against the `db` object created here.
* [Deploy]({% link docs/2.0/clients/wasm/deploying_duckdb_wasm.md %}) — serving the library, worker, and WebAssembly components that these bundles reference.
* [DuckDB Wasm Client]({% link docs/2.0/clients/wasm/overview.md %}) — the layered API and the examples the snippets above are drawn from.
