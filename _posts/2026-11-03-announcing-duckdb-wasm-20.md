---
layout: post
title: "Announcing DuckDB-Wasm 2.0"
authors:
  - Carlo Piovesan
  - Geertjan Wielenga
thumb: "/images/blog/thumbs/webassembly.svg"
image: "/images/blog/thumbs/webassembly.png"
excerpt: "DuckDB-Wasm 2.0 updates the browser engine to DuckDB 2.0 LTS. It simplifies the bundle model down to two variants, ships a slimmer binary built on nanoarrow, spills larger-than-memory queries to disk, forwards HTTP authentication headers, and loads extensions into the threaded build."
tag: release
---

[DuckDB-Wasm]({% link docs/2.0/clients/wasm/overview.md %}) compiles the full DuckDB engine to [WebAssembly](https://webassembly.org/) so that it runs entirely inside the browser, with no server to send queries to and no data leaving the user's machine. Now that DuckDB 2.0.0 LTS [“Cinnamon Teal”]({% post_url 2026-10-21-announcing-duckdb-200 %}) has shipped, DuckDB-Wasm 2.0 rebuilds the browser engine on top of it.

It is a big release, and one change is breaking: how bundles are named and selected. The sections below cover what is new, followed by what you need to change when you upgrade.

To install it, run:

```bash
npm install @duckdb/duckdb-wasm
```

## A Simpler Bundle Model: `base` and `threads`

DuckDB-Wasm ships WebAssembly modules compiled for different browser feature sets, and `selectBundle` picks the fastest one a given browser can run. Previous releases shipped three variants: `mvp` (the WebAssembly 1.0 baseline), `eh` (adding exception handling), and `coi` (adding threading and requiring cross-origin isolation).

Every modern browser now supports WebAssembly exception handling, which DuckDB relies on to propagate errors from its C++ core without emulating them through JavaScript. There is no longer a reason to ship the plain MVP baseline, so DuckDB-Wasm 2.0 drops it and settles on two bundles:

* `base`: single-threaded, requires exception handling, and runs everywhere. This is the new baseline.
* `threads`: adds SIMD and threading for parallel query execution, and requires the page to be [cross-origin isolated]({% link docs/2.0/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation).

`getJsDelivrBundles()` now returns the `base` bundle, and the loading code you already use is unchanged:

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

const bundle = await duckdb.selectBundle(duckdb.getJsDelivrBundles());

const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker}");`], { type: 'text/javascript' })
);
const worker = new Worker(worker_url);
const db = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(), worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
URL.revokeObjectURL(worker_url);
```

If you declare bundles manually (for webpack, Vite, or self-hosted files), the artifacts are now named after the two flavors, for example `duckdb-base.wasm` and `duckdb-browser-base.worker.js`. See [Instantiate]({% link docs/2.0/clients/wasm/instantiation.md %}#bundle-selection) for the full set of patterns.

## A Slimmer Binary with nanoarrow

DuckDB-Wasm uses [Apache Arrow](https://arrow.apache.org/) for both data import and query results. Internally, it previously linked the full Arrow C++ library to read and write the Arrow IPC format. In 2.0, that dependency is replaced by [nanoarrow](https://arrow.apache.org/nanoarrow/), a minimal Arrow implementation. Query results are serialized with nanoarrow, Arrow IPC inserts are read with it, and CSV and JSON are now parsed through DuckDB's own readers rather than a separate code path.

The result is a smaller download and a simpler build, with no change to the data protocol on the JavaScript side. Your code keeps exchanging `apache-arrow` tables exactly as before. As in earlier releases, pin your `apache-arrow` install to the major version DuckDB-Wasm depends on (currently `^17`), because a newer major version can cause Arrow inserts to fail. See [Import Data]({% link docs/2.0/clients/wasm/data_ingestion.md %}#apache-arrow).

## Larger-Than-Memory Queries

WebAssembly [limits a module to 4 GB of memory](https://v8.dev/blog/4gb-wasm-memory), and browsers may impose stricter limits, so queries that native DuckDB handles comfortably could run out of memory in the browser. DuckDB-Wasm 2.0 spills intermediate data that does not fit in memory to a temporary directory, so many larger-than-memory queries that previously failed now complete.

Spilling is on by default and writes to `js_buffer://tmp`, buffers the runtime holds outside the Wasm heap. You can turn it off with `spill: false`, or redirect it into the browser's [Origin Private File System](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) by pointing `temporaryDirectory` at an `opfs://` path:

```ts
await db.open({
    path: 'opfs://analytics.duckdb',
    temporaryDirectory: 'opfs://tmp',
});
```

See [Out of Memory]({% link docs/2.0/clients/wasm/troubleshoot.md %}#out-of-memory) for details.

## Multithreading with Loadable Extensions

Multithreading in the browser remains experimental and off by default, but the threaded build can now load extensions, which it could not before. The `threads` bundle uses the `wasm_threads` extension platform, and the `base` bundle uses `wasm_base`, so each loads the extension build that matches it.

To opt into threading, add the `threads` bundle explicitly (because `getJsDelivrBundles()` returns only `base`), serve the page as cross-origin isolated, and set `maximumThreads`:

```ts
const DIST = 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/dist/';
const bundles: duckdb.DuckDBBundles = {
    ...duckdb.getJsDelivrBundles(),
    threads: {
        mainModule: `${DIST}duckdb-threads.wasm`,
        mainWorker: `${DIST}duckdb-browser-threads.worker.js`,
        pthreadWorker: `${DIST}duckdb-browser-threads.pthread.worker.js`,
    },
};
const bundle = await duckdb.selectBundle(bundles);
// ... instantiate as usual, then:
await db.open({ maximumThreads: 4 });
```

On a page that is not cross-origin isolated, `selectBundle` falls back to `base` and the same code runs single-threaded. See [Threading]({% link docs/2.0/clients/wasm/instantiation.md %}#threading).

## Better HTTP: Authentication Headers and Real Errors

When DuckDB-Wasm reads a remote file through the httpfs extension, it issues the request from the browser, so it has to follow the browser's rules. DuckDB-Wasm 2.0 reworks that Wasm HTTP client in two ways:

* It forwards the request headers that DuckDB's httpfs sets, including the `Authorization` header configured through an [httpfs secret]({% link docs/2.0/core_extensions/httpfs/overview.md %}), so endpoints that require authentication can be read directly.
* On a failed request it surfaces the real HTTP status code and response body instead of a generic network error, which makes authenticated APIs such as the Iceberg REST catalog far easier to debug.

CORS rules still apply, since the browser issues the request. See [Troubleshoot]({% link docs/2.0/clients/wasm/troubleshoot.md %}#network-error-when-querying-remote-files).

## Persistence and Secrets in OPFS

DuckDB-Wasm can open a database at an `opfs://` path so it survives reloads and browser restarts, as we covered in [“Persistent Databases in the Browser with DuckDB-Wasm and OPFS”]({% post_url 2026-09-18-opfs-wasm %}). The 2.0 OPFS layer adds directory support, synchronous file creation, and automatic registration of `opfs://` files referenced in SQL. Setting `homeDirectory` to `opfs://home` lets DuckDB keep the data it stores next to the user, such as persistent secrets, across sessions.

## New Configuration Options

The configuration object passed to `open()` has several new fields in 2.0:

* `spill` and `temporaryDirectory`, for larger-than-memory queries.
* `homeDirectory`, for persistent secrets and other per-user data.
* `extensionRepository`, equivalent to `custom_extension_repository`, to load extensions from a mirror.
* `filesystem`, to tune HTTP range requests and the full-download fallback.
* `arrowLosslessConversion`, to preserve the full range and precision of DuckDB values in Arrow.
* `customUserAgent`, to append a string to the user agent on outgoing requests.

See [Configuration]({% link docs/2.0/clients/wasm/instantiation.md %}#configuration) for the complete list.

## Upgrading

Most applications only need to touch their bundle definitions. The breaking changes are:

* The `mvp`, `eh`, and `coi` bundles are gone. Use `base` in their place, and `threads` where you used `coi`. If you call `getJsDelivrBundles()` and `selectBundle()` without naming bundles yourself, no change is required.
* The distribution filenames follow the new names: `duckdb-base.wasm`, `duckdb-browser-base.worker.js`, `duckdb-threads.wasm`, `duckdb-browser-threads.worker.js`, and `duckdb-browser-threads.pthread.worker.js`. Update any hardcoded paths.
* Extension platforms are now `wasm_base` and `wasm_threads`. The `wasm_mvp` and `wasm_eh` platforms no longer exist.
* Exception handling is required. A browser too old to support it can no longer run DuckDB-Wasm, and `selectBundle` throws rather than falling back to an MVP build.

## Conclusion

DuckDB-Wasm 2.0 updates the browser engine to DuckDB 2.0 LTS and simplifies how you set it up: two bundles instead of three, a smaller binary thanks to nanoarrow, and spilling to disk on by default so larger datasets no longer need special handling. Authenticated HTTP, extensions in the threaded build, and persistent secrets in OPFS are new as well.

Try it in your own application, and share what you build on [GitHub](https://github.com/duckdb/duckdb-wasm) or [Discord](https://discord.duckdb.org). You can also try the engine without installing anything at [shell.duckdb.org](https://shell.duckdb.org).

## Further Reading

* [DuckDB-Wasm documentation]({% link docs/2.0/clients/wasm/overview.md %})
* [Persistent Databases in the Browser with DuckDB-Wasm and OPFS]({% post_url 2026-09-18-opfs-wasm %}), on opening a database that survives reloads
* [DuckDB-Wasm: Efficient Analytical SQL in the Browser]({% post_url 2021-10-29-duckdb-wasm %}), the original launch post
* [Announcing DuckDB 2.0.0 LTS “Cinnamon Teal”]({% post_url 2026-10-21-announcing-duckdb-200 %}), the engine release this one tracks
* The [`duckdb-wasm` repository](https://github.com/duckdb/duckdb-wasm), with source, examples, and the issue tracker

