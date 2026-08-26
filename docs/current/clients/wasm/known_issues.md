---
layout: docu
redirect_from:
- /docs/clients/wasm/known_issues
- /docs/preview/clients/wasm/known_issues
- /docs/stable/clients/wasm/known_issues
title: Troubleshoot
---

## Overview

This page collects common issues encountered when using DuckDB-Wasm, together with their workarounds. If you run into a problem that is not covered here, search the [`duckdb-wasm` issue tracker](https://github.com/duckdb/duckdb-wasm/issues) on GitHub.

## Network Error When Querying Remote Files

When DuckDB-Wasm reads a remote file — through the [Wasm-flavored httpfs extension]({% link docs/current/clients/wasm/extensions.md %}#httpfs) or `registerFileURL` — the browser issues the request, so it is subject to the browser's [CORS policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) and every request is upgraded to HTTPS.

The server hosting the data must allow (using CORS headers) the origin that hosts the DuckDB-Wasm instance to read it. If the server does not send the required headers, the query fails with a network error such as:

```console
Failed to execute 'send' on 'XMLHttpRequest'
```

For example, when querying files from Amazon S3, configure the bucket's CORS policy to allow `GET` and `HEAD` requests:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3000
    }
]
```

This array is a server-side bucket configuration (for Amazon S3, the bucket's CORS policy), not a value you pass to DuckDB-Wasm. There is no db or connection option and no `DuckDBGlobalFileInfo` field for it, because the browser, not DuckDB-Wasm, enforces CORS. Apply it where the data is hosted, then read the file as usual.

Beyond CORS, reading remote files has several other known limitations:

* Because every request is upgraded to HTTPS, an `http://` URL can be rewritten incorrectly (for example to `https://http//…`), which breaks reads against local or non-TLS endpoints (see [duckdb-wasm issue #2118](https://github.com/duckdb/duckdb-wasm/issues/2118)).
* DuckDB relies on HTTP range requests to read only part of a file. Range requests can fail on Firefox (see [issue #1932](https://github.com/duckdb/duckdb-wasm/issues/1932)) and are not detected correctly for some S3 pre-signed URLs (see [issue #2228](https://github.com/duckdb/duckdb-wasm/issues/2228)), which forces the whole file to be downloaded or makes the read fail.
* Cached reads of files in DuckDB's native format over HTTP can be corrupted (see [issue #1957](https://github.com/duckdb/duckdb-wasm/issues/1957)).
* HTTP authentication headers are not supported, so endpoints that require them cannot be read directly (see [issue #1967](https://github.com/duckdb/duckdb-wasm/issues/1967)).

## Extension Fails to Load from a Custom Repository

DuckDB-Wasm fetches each extension over the network when it is loaded. If you serve extensions from a [custom repository]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#duckdb-extensions) with `SET custom_extension_repository = '⟨https://some.url.com⟩'`, the `GET` requests for the extension files must be [CORS enabled](https://www.w3.org/wiki/CORS_Enabled) for the browser to allow the connection, exactly as for remote data files above.

Extensions remain signed regardless of where they are served, so copying an extension to a different location keeps its signature valid.

## Out of Memory

The WebAssembly client has a limited amount of memory available: [WebAssembly limits the available memory to 4 GB](https://v8.dev/blog/4gb-wasm-memory) and browsers may impose even stricter limits. Queries over large datasets can therefore run out of memory where native DuckDB would not. To stay within the limit:

* Stream large results with [`send()`]({% link docs/current/clients/wasm/query.md %}#query-execution) instead of materializing them all at once with `query()`.
* Read only the columns and rows you need. Because DuckDB reads Parquet files lazily, projections, filters, and `LIMIT` clauses let entire row groups be skipped rather than loaded into memory.

See [Limitations]({% link docs/current/clients/wasm/overview.md %}#limitations) for the other constraints of the WebAssembly client.

## Threading Is Not Available

By default, the WebAssembly client uses a single thread; multithreading is available through the `coi` bundle but is still experimental.

The threaded bundle relies on `SharedArrayBuffer`, which browsers only expose to pages that are [cross-origin isolated]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation). If the top-level document is not served with the `Cross-Origin-Embedder-Policy` and `Cross-Origin-Opener-Policy` headers, DuckDB-Wasm falls back to the single-threaded `mvp` or `eh` bundle.

See [Cross-Origin Isolation]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}#cross-origin-isolation) for the required headers, and [Threading]({% link docs/current/clients/wasm/instantiation.md %}#threading) for how to select and configure the `coi` bundle.

## Further Reading

* [DuckDB Wasm Client]({% link docs/current/clients/wasm/overview.md %}) — installation, basic usage, and the limitations behind several issues above.
* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — registering and reading remote files that are subject to the CORS rules above.
* [Load Extensions]({% link docs/current/clients/wasm/extensions.md %}) — how extensions are fetched, signed, and served, including the httpfs CORS behavior.
* [Deploy]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — serving components and configuring cross-origin isolation for threading.
