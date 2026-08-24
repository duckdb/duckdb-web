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

DuckDB-Wasm can be instantiated in several ways, depending on how your application bundles and serves its assets. Each approach resolves the `mainModule` (the WebAssembly file) and the `mainWorker` (the worker script) for the browser's capabilities, then hands them to `AsyncDuckDB`. This page shows the patterns for a jsDelivr CDN, webpack, Vite and statically served files. Once instantiated, the `db` object is used to [import data]({% link docs/current/clients/wasm/data_ingestion.md %}) and [run queries]({% link docs/current/clients/wasm/query.md %}).

## Bundle Selection

DuckDB-Wasm ships several WebAssembly modules compiled for different browser feature sets, because post-MVP WebAssembly features reach browsers at different speeds and each one can bring a flat performance improvement. The `selectBundle` function runs dynamic browser checks and picks the fastest bundle the current browser supports:

* `mvp` — the WebAssembly 1.0 (MVP) baseline, supported everywhere
* `eh` — adds Wasm-level exception handling, which improves performance; DuckDB and DuckDB-Wasm are written in C++ and use exceptions to propagate errors, so native exception handling avoids emulating them through JavaScript
* `coi` — adds threading for parallel query execution; it requires the page to be [cross-origin isolated]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation)

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
        mainModule: 'change/m/../duckdb-eh.wasm',
        mainWorker: 'change/m/../duckdb-browser-eh.worker.js',
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

## Further Reading

* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — registering files and inserting data into the instantiated database.
* [Run Queries]({% link docs/current/clients/wasm/query.md %}) — executing queries against the `db` object created here.
* [Deploy]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — serving the library, worker, and WebAssembly components that these bundles reference.
* [DuckDB Wasm Client]({% link docs/current/clients/wasm/overview.md %}) — the layered API and the examples the snippets above are drawn from.
