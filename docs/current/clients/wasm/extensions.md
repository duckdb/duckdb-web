---
layout: docu
redirect_from:
- /docs/api/wasm/extensions
- /docs/clients/wasm/extensions
- /docs/preview/clients/wasm/extensions
- /docs/stable/clients/wasm/extensions
title: Load Extensions
---

## Overview

DuckDB-Wasm's (dynamic) extension loading is modeled after regular DuckDB's extension loading, with a few relevant differences due to the difference in platform. A growing subset of core, community, and external extensions is supported.

This page explains the extension format, how `INSTALL` and `LOAD` behave, autoloading, which extensions are available, signing, and how extensions are fetched and served.

## Format

Extensions in DuckDB are binaries to be dynamically loaded via `dlopen`. A cryptographical signature is appended to the binary.

An extension in DuckDB-Wasm is a regular Wasm file to be dynamically loaded via Emscripten's `dlopen`. A cryptographical signature is appended to the Wasm file as a WebAssembly custom section called `duckdb_signature`. This ensures the file remains a valid WebAssembly file.

> Currently, this custom section is required to be the last one, but this requirement may be relaxed in the future.

## `INSTALL` and `LOAD`

The `INSTALL` semantic in native embeddings of DuckDB is to fetch, decompress from `gzip` and store data in local disk.
The `LOAD` semantic in native embeddings of DuckDB is to (optionally) perform signature checks *and* dynamic load the binary with the main DuckDB binary.

In DuckDB-Wasm, `INSTALL` performs no durable installation, because there is no cross-session storage; it only records where an extension will be fetched from (for example, with `INSTALL ⟨name⟩ FROM community`), deferring the actual fetch to `LOAD`. The `LOAD` operation will fetch (and decompress on the fly), perform signature checks *and* dynamically load via the Emscripten implementation of `dlopen`.

## Autoloading

[Autoloading]({% link docs/current/extensions/overview.md %}), i.e., the possibility for DuckDB to add extension functionality on-the-fly, is enabled by default in DuckDB-Wasm.

## Available Extensions

A growing subset of extensions is supported for DuckDB-Wasm, spanning [core extensions]({% link docs/current/core_extensions/overview.md %}), [community extensions]({% link docs/current/extensions/community_extensions.md %}), and external extensions. Most are fetched on the fly when they are autoloaded or explicitly loaded, rather than being bundled into the DuckDB-Wasm binary. For example:

```sql
-- Explicitly load a core extension
LOAD icu;

-- Load spatial for geospatial support
INSTALL spatial;
LOAD spatial;

-- Install a community extension, then load it
INSTALL h3 FROM community;
LOAD h3;

-- Install an external extension from a repository
INSTALL sqlite_scanner FROM 'https://extensions.duckdb.org';
LOAD sqlite_scanner;
```

The core extensions commonly used with DuckDB-Wasm include:

| Extension name                                                          | Description                                                      | Aliases         |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------- |
| [autocomplete]({% link docs/current/core_extensions/autocomplete.md %}) | Adds support for autocomplete in the shell                       |                 |
| [excel]({% link docs/current/core_extensions/excel.md %})               | Adds support for Excel-like format strings                       |                 |
| [fts]({% link docs/current/core_extensions/full_text_search.md %})      | Adds support for Full-Text Search indexes                        |                 |
| [icu]({% link docs/current/core_extensions/icu.md %})                   | Adds support for time zones and collations using the ICU library |                 |
| [inet]({% link docs/current/core_extensions/inet.md %})                 | Adds support for IP-related data types and functions             |                 |
| [json]({% link docs/current/data/json/overview.md %})                   | Adds support for JSON operations                                 |                 |
| [parquet]({% link docs/current/data/parquet/overview.md %})             | Adds support for reading and writing Parquet files               |                 |
| [spatial]({% link docs/current/core_extensions/spatial/overview.md %})  | Adds support for geospatial data types and functions             |                 |
| [sqlite]({% link docs/current/core_extensions/sqlite.md %})             | Adds support for reading SQLite database files                   | sqlite, sqlite3 |
| [tpcds]({% link docs/current/core_extensions/tpcds.md %})               | Adds TPC-DS data generation and query support                    |                 |
| [tpch]({% link docs/current/core_extensions/tpch.md %})                 | Adds TPC-H data generation and query support                     |                 |

WebAssembly is essentially an additional platform, and there may be platform-specific limitations that prevent some extensions from matching their native capabilities or that make them behave differently. Relevant differences for DuckDB-hosted extensions are documented below.

### HTTPFS

The native HTTPFS extension is not compiled into DuckDB-Wasm, because HTTPS capabilities have to go through an additional layer, the browser, which adds both differences and some restrictions relative to native. Instead, DuckDB-Wasm ships a separate JavaScript implementation of the same functionality. Running `LOAD httpfs;` opts into this re-implemented HTTP stack, which is interchangeable with the native extension for most purposes but does not support all use cases, as it must follow the security rules imposed by the browser.

In particular:

* Requests are always upgraded to HTTPS.
* Because of the browser's CORS policy, any request for data must target a site that allows (using CORS headers) the site hosting the DuckDB-Wasm instance to access that data.

The [MDN website](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a great resource for more information regarding CORS. If a query over a remote file fails with a network error, see [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}#network-error-when-querying-remote-files).

## Extension Signing

As with regular DuckDB extensions, DuckDB-Wasm extensions are by default checked on `LOAD` to verify the signature and confirm the extension has not been tampered with. Extension signature verification can be disabled via a configuration option.

Signing is a property of the binary itself, so copying a DuckDB extension (say to serve it from a different location) will still keep a valid signature (e.g., for local development).

## Fetching DuckDB-Wasm Extensions

Official DuckDB extensions are served at `extensions.duckdb.org`, and this is also the default value for the `default_extension_repository` option.
When installing extensions, a relevant URL will be built that will look like `extensions.duckdb.org/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.gz`.

DuckDB-Wasm extension are fetched only on load, and the URL will look like: `extensions.duckdb.org/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm`.

Note that an additional `duckdb-wasm` is added to the folder structure, and the file is served as a `.wasm` file.

DuckDB-Wasm extensions are served pre-compressed using Brotli compression. While fetched from a browser, extensions will be transparently uncompressed. If you want to fetch the `duckdb-wasm` extension manually, you can use `curl --compressed extensions.duckdb.org/<...>/icu.duckdb_extension.wasm`.

## Serving Extensions from a Third-Party Repository

As with regular DuckDB, if you use `SET custom_extension_repository = 'https://some.url.com'`, subsequent loads will be attempted at `https://some.url.com/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm`.

Note that `GET` requests for the extensions must be [CORS enabled](https://www.w3.org/wiki/CORS_Enabled) for a browser to allow the connection; see [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}#extension-fails-to-load-from-a-custom-repository) if a load fails.

## Tooling

Both DuckDB-Wasm and its extensions have been compiled using the latest packaged Emscripten toolchain.

## Further Reading

* [Deploy]({% link docs/current/clients/wasm/deploying_duckdb_wasm.md %}) — serving and mirroring extensions from a custom endpoint.
* [Core Extensions]({% link docs/current/core_extensions/overview.md %}) — the core extensions available across all DuckDB clients.
* [Community Extensions]({% link docs/current/extensions/community_extensions.md %}) — third-party extensions installable with `INSTALL … FROM community`.
* [Import Data]({% link docs/current/clients/wasm/data_ingestion.md %}) — using the Parquet, JSON, and Wasm-flavored httpfs extensions to read files.
* [Troubleshoot]({% link docs/current/clients/wasm/known_issues.md %}) — CORS errors when loading extensions from a custom repository.
