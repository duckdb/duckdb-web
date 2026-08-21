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

DuckDB has been compiled to WebAssembly, so it can run inside any browser on any device. DuckDB-Wasm offers a layered API: it can be embedded as a [JavaScript + WebAssembly library](https://www.npmjs.com/package/@duckdb/duckdb-wasm), as a [Web shell](https://www.npmjs.com/package/@duckdb/duckdb-wasm-shell), or [built from source](https://github.com/duckdb/duckdb-wasm) according to your needs. This page introduces the client; the other pages in this section cover instantiating it, importing data, running queries, loading extensions, and deploying it.

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}

## Getting Started

A great starting point is to read the [DuckDB-Wasm launch blog post]({% post_url 2021-10-29-duckdb-wasm %}). The [GitHub repository](https://github.com/duckdb/duckdb-wasm) is another useful resource, and the full [DuckDB-Wasm API documentation](https://shell.duckdb.org/docs/modules/index.html) documents every class and method.

To use DuckDB-Wasm in an application, first [instantiate it]({% link docs/current/clients/wasm/instantiation.md %}), then [import data]({% link docs/current/clients/wasm/data_ingestion.md %}) and [run queries]({% link docs/current/clients/wasm/query.md %}) on it.

## How DuckDB-Wasm Works

DuckDB-Wasm uses [Apache Arrow](https://arrow.apache.org/) as its data protocol for both data import and query results. Arrow is a columnar, database-friendly format that the `apache-arrow` npm package implements in the browser, letting DuckDB-Wasm exchange data efficiently and interoperate with other JavaScript data tools without reimplementing SQL type logic in JavaScript.

DuckDB-Wasm is built on a virtual filesystem that treats local files, remote HTTP(S) servers and in-memory buffers uniformly. Because DuckDB understands file formats such as Parquet, it reads only the bytes a query needs rather than downloading an entire file: `SELECT count(*) FROM 'file.parquet'` can be answered from the file metadata alone, and selective filters or `LIMIT` … `OFFSET` clauses let entire row groups be skipped. This makes it practical to query large Parquet files hosted on a remote server directly from the browser.

## Limitations

* By default, the WebAssembly client only uses a single thread. Multithreading is available but still experimental.
* The WebAssembly client has a limited amount of memory available. [WebAssembly limits the amount of available memory to 4 GB](https://v8.dev/blog/4gb-wasm-memory) and browsers may impose even stricter limits.

## Further Reading

* [Instantiate DuckDB-Wasm]({% link docs/current/clients/wasm/instantiation.md %}) — the bundle-selection patterns for jsDelivr, webpack, Vite, and statically served files.
* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — registering files and inserting Apache Arrow, CSV, JSON, and Parquet data.
* [Run Queries]({% link docs/current/clients/wasm/query.md %}) — materialized and streaming queries, prepared statements, and exporting results.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — how extension loading differs from native DuckDB and which extensions are available.
* [Deploy DuckDB-Wasm]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — the components a deployment serves and the security considerations involved.
* [Clients Overview]({% link docs/current/clients/overview.md %}) — the other client APIs DuckDB provides alongside Wasm.
