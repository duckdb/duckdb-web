---
github_repository: https://github.com/duckdb/duckdb-wasm
layout: docu
redirect_from:
- /docs/api/wasm
- /docs/api/wasm/overview
- /docs/clients/wasm/overview
- /docs/preview/clients/wasm/overview
- /docs/stable/clients/wasm/overview
title: DuckDB Wasm Client
---

> Installation To use the DuckDB Wasm client, visit the [`duckdb-wasm` GitHub repository](https://github.com/duckdb/duckdb-wasm#readme).
>
> The latest stable version of the DuckDB WebAssembly client is {% if site.current_duckdb_wasm_version != "" %}{{ site.current_duckdb_wasm_version }}{% else %}{{ site.lts_duckdb_wasm_version }}{% endif %}.

DuckDB-Wasm is a version of DuckDB that has been compiled to [WebAssembly](https://webassembly.org/), the portable binary format that browsers can run at near-native speed. This lets a full DuckDB engine run entirely inside any browser on any device, with no server to send queries to and no data leaving the user's machine.

It offers a layered API to fit different needs:

* embedded as a [JavaScript + WebAssembly library](https://www.npmjs.com/package/@duckdb/duckdb-wasm)
* used as a [Web shell](https://www.npmjs.com/package/@duckdb/duckdb-wasm-shell)
* [built from source](https://github.com/duckdb/duckdb-wasm)

This page covers installation and basic usage; the other pages in this section cover instantiating the client, importing data, running queries, loading extensions, and deploying it.

## Try It Yourself

The shell below is a full DuckDB engine running in your browser — type a SQL query and run it right here:

<div style="margin-top: 1.5rem;" markdown="0">
<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}
</div>

> Note The shell above is itself built with DuckDB-Wasm. It is the [`@duckdb/duckdb-wasm-shell`](https://www.npmjs.com/package/@duckdb/duckdb-wasm-shell) package, one of the layered APIs listed above, running on top of the same DuckDB-Wasm library this page describes. Every query you type executes client-side in WebAssembly, with no server round-trip, so it is a live demonstration of what your own application gets when it embeds DuckDB-Wasm.

## Installation

DuckDB-Wasm is published to npm as [`@duckdb/duckdb-wasm`](https://www.npmjs.com/package/@duckdb/duckdb-wasm). Install it with your package manager:

```bash
npm install @duckdb/duckdb-wasm
```

This installs the current stable release (the `latest` tag). To try the newest, unreleased build instead, install the `next` tag with `npm install @duckdb/duckdb-wasm@next`; it tracks the `main` branch and is intended for testing rather than production.

Alternatively, load a prebuilt bundle directly from a CDN such as jsDelivr without installing anything; see [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) for the bundle-selection options. To try it interactively with no setup, use the [DuckDB-Wasm Web shell](https://shell.duckdb.org/).

## Basic API Usage

The example below instantiates DuckDB-Wasm from a CDN bundle, opens a connection, runs a query, and reads the result. [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) covers the other ways to load the bundle, such as with webpack, Vite, or self-hosted files.

Refer to the externally hosted [DuckDB-Wasm API Reference](https://shell.duckdb.org/docs/modules/index.html) for details on every class and method. The [DuckDB-Wasm launch blog post]({% post_url 2021-10-29-duckdb-wasm %}) is another good introduction.

```ts
import * as duckdb from '@duckdb/duckdb-wasm';

// Instantiate DuckDB-Wasm from a jsDelivr bundle
const bundle = await duckdb.selectBundle(duckdb.getJsDelivrBundles());
const worker = new Worker(bundle.mainWorker!);
const db = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(), worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

// Open a connection and run a query
const conn = await db.connect();
const result = await conn.query('SELECT 42 AS answer');
console.log(result.toArray()[0].answer); // prints 42

// Release resources
await conn.close();
await db.terminate();
await worker.terminate();
```

## How DuckDB-Wasm Works

DuckDB-Wasm uses [Apache Arrow](https://arrow.apache.org/) as its data protocol for both data import and query results. Arrow is a columnar, database-friendly format that the `apache-arrow` npm package implements in the browser, letting DuckDB-Wasm exchange data efficiently and interoperate with other JavaScript data tools without reimplementing SQL type logic in JavaScript.

DuckDB-Wasm is built on a virtual filesystem that treats local files, remote HTTP(S) servers and in-memory buffers uniformly.

Because DuckDB understands file formats such as Parquet, it reads only the bytes a query needs rather than downloading an entire file: `SELECT count(*) FROM 'file.parquet'` can be answered from the file metadata alone, and selective filters or `LIMIT` … `OFFSET` clauses let entire row groups be skipped. This makes it practical to query large Parquet files hosted on a remote server directly from the browser.

> Note This partial-read behavior depends on which httpfs path serves the request. The JavaScript httpfs implementation fetches only the required byte ranges, but reading through the built-in httpfs extension may currently download the whole file instead (see [duckdb-wasm issue #2153](https://github.com/duckdb/duckdb-wasm/issues/2153)).

## Limitations

* By default, the WebAssembly client only uses a single thread. Multithreading is available but still experimental.
* The WebAssembly client has a limited amount of memory available. [WebAssembly limits the amount of available memory to 4 GB](https://v8.dev/blog/4gb-wasm-memory) and browsers may impose even stricter limits.

See [Troubleshoot]({% link docs/current/clients/wasm/troubleshoot.md %}) for workarounds when you run into these limits.

## Further Reading

* [Instantiate]({% link docs/current/clients/wasm/instantiation.md %}) — the bundle-selection patterns for jsDelivr, webpack, Vite, and statically served files.
* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — registering files and inserting Apache Arrow, CSV, JSON, and Parquet data.
* [Run Queries]({% link docs/current/clients/wasm/query.md %}) — materialized and streaming queries, prepared statements, and exporting results.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — how extension loading differs from native DuckDB and which extensions are available.
* [Deploy]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — the components a deployment serves and the security considerations involved.
* [Troubleshoot]({% link docs/current/clients/wasm/troubleshoot.md %}) — common issues and their workarounds, including CORS errors, memory limits, and threading.
* [Clients Overview]({% link docs/current/clients/overview.md %}) — the other client APIs DuckDB provides alongside Wasm.
