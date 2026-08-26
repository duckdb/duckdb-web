---
layout: docu
redirect_from:
- /docs/api/wasm/instantiation
- /docs/clients/wasm/instantiation
- /docs/preview/clients/wasm/instantiation
- /docs/stable/clients/wasm/instantiation
title: Instantiate
---

## Overview

DuckDB-Wasm can be instantiated in several ways, depending on how your application bundles and serves its assets. Each approach resolves the `mainModule` (the WebAssembly file) and the `mainWorker` (the worker script) for the browser's capabilities, then hands them to `AsyncDuckDB`.

This page shows the patterns for a jsDelivr CDN, webpack, Vite and statically served files. Once instantiated, the `db` object is used to [import data]({% link docs/current/clients/wasm/data_ingestion.md %}) and [run queries]({% link docs/current/clients/wasm/query.md %}).

## Bundle Selection

DuckDB-Wasm ships several WebAssembly modules compiled for different browser feature sets, because post-MVP WebAssembly features reach browsers at different speeds and each one can bring a flat performance improvement. The `selectBundle` function runs dynamic browser checks and picks the fastest bundle the current browser supports:

* `mvp` — the WebAssembly 1.0 (MVP) baseline, supported everywhere
* `eh` — adds Wasm-level exception handling, which improves performance; DuckDB and DuckDB-Wasm are written in C++ and use exceptions to propagate errors, so native exception handling avoids emulating them through JavaScript
* `coi` — adds threading for parallel query execution; it requires the page to be [cross-origin isolated]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation) and must be opted into explicitly (see [Threading](#threading))

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

When your application is built with [webpack](https://webpack.js.org/), let the bundler resolve and emit DuckDB-Wasm's assets instead of fetching them from a CDN. Import each `.wasm` module directly, and reference the worker scripts with `new URL(..., import.meta.url)` so that webpack fingerprints them and rewrites the paths to the emitted files. The bundles are declared manually because their final locations are known only after the build, and `selectBundle` then chooses between the `mvp` and `eh` variants at runtime.

```ts
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm';
const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    mvp: {
        mainModule: duckdb_wasm,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js', import.meta.url).toString(),
    },
    eh: {
        mainModule: duckdb_wasm_next,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js', import.meta.url).toString(),
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

[Vite](https://vitejs.dev/) resolves assets a little differently: appending the `?url` suffix to an import tells Vite to return the asset's final URL rather than its contents. Import both the `.wasm` modules and the worker scripts this way, assemble them into the manual bundle definition, and let `selectBundle` select the appropriate variant for the browser at runtime.

```ts
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    mvp: {
        mainModule: duckdb_wasm,
        mainWorker: mvp_worker,
    },
    eh: {
        mainModule: duckdb_wasm_eh,
        mainWorker: eh_worker,
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
    mvp: {
        mainModule: 'change/me/../duckdb-mvp.wasm',
        mainWorker: 'change/me/../duckdb-browser-mvp.worker.js',
    },
    eh: {
        mainModule: 'change/me/../duckdb-eh.wasm',
        mainWorker: 'change/me/../duckdb-browser-eh.worker.js',
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
    },
});

const conn = await db.connect();
```

Commonly used fields of the configuration object:

* `path`: the database file to open. Defaults to an in-memory database (`:memory:`). Use an `opfs://` path to persist data to the browser's Origin Private File System (see [Persistence with OPFS](#persistence-with-opfs)).
* `accessMode`: `duckdb.DuckDBAccessMode.READ_ONLY` or `duckdb.DuckDBAccessMode.READ_WRITE`.
* `allowUnsignedExtensions`: allow loading extensions that are not signed (see [Load Extensions]({% link docs/current/clients/wasm/extensions.md %})).
* `maximumThreads`: the number of threads to use. This takes effect only with the threaded `coi` bundle on a cross-origin-isolated page (see [Threading](#threading)).
* `query`: controls how query results are converted from Arrow into JavaScript values.

The `query` object tunes the Arrow-to-JavaScript type mapping:

* `castBigIntToDouble`: return 64-bit integers as JavaScript numbers instead of `BigInt` values. This is convenient, but large integers can lose precision.
* `castDecimalToDouble`: return `DECIMAL` values as floating-point numbers instead of DuckDB's exact decimal representation.
* `castTimestampToDate`: return `TIMESTAMP` values as JavaScript `Date` objects.
* `castDurationToTime64`: return duration values as 64-bit (microsecond) time values.
* `queryPollingInterval`: the interval, in milliseconds, at which streaming queries poll for results.

## Threading

By default DuckDB-Wasm runs on a single thread. The threaded `coi` bundle runs queries across multiple threads, but it has two requirements: the page must be [cross-origin isolated]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation), and you must add the `coi` bundle to the set you pass to `selectBundle`, because `getJsDelivrBundles()` returns only the `mvp` and `eh` bundles. The `coi` bundle also needs a third artifact, the pthread worker, alongside the usual module and worker:

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

const DIST = 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/dist/';

// getJsDelivrBundles() returns only mvp and eh, so add coi explicitly
const bundles: duckdb.DuckDBBundles = {
    ...duckdb.getJsDelivrBundles(),
    coi: {
        mainModule: `${DIST}duckdb-coi.wasm`,
        mainWorker: `${DIST}duckdb-browser-coi.worker.js`,
        pthreadWorker: `${DIST}duckdb-browser-coi.pthread.worker.js`,
    },
};

// selectBundle picks coi only on a cross-origin-isolated page whose browser
// supports Wasm exceptions, SIMD, and threads; otherwise it falls back to eh or mvp
const bundle = await duckdb.selectBundle(bundles);

const worker = new Worker(bundle.mainWorker!);
const db = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(), worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

// Configure the thread count (only effective on the coi bundle)
await db.open({ maximumThreads: 4 });
const conn = await db.connect();
```

Because `selectBundle` falls back to the `eh` or `mvp` bundle when the `coi` requirements are not met, the same code runs everywhere: on a page that is not cross-origin isolated it simply runs single-threaded, and `bundle.pthreadWorker` is `null`. Two things to keep in mind when deploying the threaded bundle:

* The page must be served with the `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` headers, which is what makes the browser expose `SharedArrayBuffer` and report the page as cross-origin isolated. See [Cross-Origin Isolation]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation).
* Extensions must be built for the threaded platform. The `coi` bundle uses the `wasm_threads` extension platform, so extensions published only for `wasm_mvp` or `wasm_eh` will not load into it.

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

Reopening the same `opfs://` path in a later session restores the tables. You can also read and write `opfs://` files directly from SQL. Set `opfs.fileHandling` to `'auto'` so that DuckDB-Wasm registers the `opfs://` paths referenced in a statement automatically:

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

> Note OPFS access relies on synchronous file access handles, which browsers expose only inside a Web Worker; DuckDB-Wasm's asynchronous API already runs in one. Keep these points in mind: call `CHECKPOINT` to flush writes to disk, drop registered files with `db.dropFile()` (or `db.dropFiles()`) before another connection or database instance opens them, because a file can be held by only one handle at a time, and note that moving files into or out of OPFS is not yet supported.

## Further Reading

* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — registering files and inserting data into the instantiated database.
* [Run Queries]({% link docs/current/clients/wasm/query.md %}) — executing queries against the `db` object created here.
* [Deploy]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — serving the library, worker, and WebAssembly components that these bundles reference.
* [DuckDB Wasm Client]({% link docs/current/clients/wasm/overview.md %}) — the layered API and the examples the snippets above are drawn from.
