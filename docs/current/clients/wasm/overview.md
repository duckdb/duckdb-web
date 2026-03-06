---
github_repository: https://github.com/duckdb/duckdb-wasm
layout: docu
title: DuckDB Wasm
---

> Tip To use the DuckDB Wasm client, visit the [`duckdb-wasm` GitHub repository](https://github.com/duckdb/duckdb-wasm#readme).
>
> The latest stable version of the DuckDB WebAssembly client is {{ site.current_duckdb_wasm_version }}.

DuckDB has been compiled to WebAssembly, so it can run inside any browser on any device.

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}

DuckDB-Wasm offers a layered API, it can be embedded as a [JavaScript + WebAssembly library](https://www.npmjs.com/package/@duckdb/duckdb-wasm), as a [Web shell](https://www.npmjs.com/package/@duckdb/duckdb-wasm-shell), or [built from source](https://github.com/duckdb/duckdb-wasm) according to your needs.

## Getting Started with DuckDB-Wasm

A great starting point is to read the [DuckDB-Wasm launch blog post]({% post_url 2021-10-29-duckdb-wasm %})!

Another great resource is the [GitHub repository](https://github.com/duckdb/duckdb-wasm).

For details, see the full [DuckDB-Wasm API Documentation](https://shell.duckdb.org/docs/modules/index.html).

## Limitations

* By default, the WebAssembly client only uses a single thread.
* The WebAssembly client has a limited amount of memory available. [WebAssembly limits the amount of available memory to 4 GB](https://v8.dev/blog/4gb-wasm-memory) and browsers may impose even stricter limits.
