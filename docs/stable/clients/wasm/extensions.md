---
layout: docu
redirect_from:
- /docs/api/wasm/extensions
- /docs/clients/wasm/extensions
title: Extensions
---

DuckDB-Wasm's (dynamic) extension loading is modeled after the regular DuckDB's extension loading, with a few relevant differences due to the difference in platform.

## Format

Extensions in DuckDB are binaries to be dynamically loaded via `dlopen`. A cryptographical signature is appended to the binary.
An extension in DuckDB-Wasm is a regular Wasm file to be dynamically loaded via Emscripten's `dlopen`. A cryptographical signature is appended to the Wasm file as a WebAssembly custom section called `duckdb_signature`.
This ensures the file remains a valid WebAssembly file.

> Currently, we require this custom section to be the last one, but this can be potentially relaxed in the future.

## `INSTALL` and `LOAD`

The `INSTALL` semantic in native embeddings of DuckDB is to fetch, decompress from `gzip` and store data in local disk.
The `LOAD` semantic in native embeddings of DuckDB is to (optionally) perform signature checks *and* dynamic load the binary with the main DuckDB binary.

In DuckDB-Wasm, `INSTALL` is a no-op given there is no durable cross-session storage. The `LOAD` operation will fetch (and decompress on the fly), perform signature checks *and* dynamically load via the Emscripten implementation of `dlopen`.

## Autoloading

[Autoloading]({% link docs/stable/extensions/overview.md %}), i.e., the possibility for DuckDB to add extension functionality on-the-fly, is enabled by default in DuckDB-Wasm.

## List of Officially Available Extensions

| Extension name                                                          | Description                                                      | Aliases         |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------- |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) | Adds support for autocomplete in the shell                       |                 |
| [excel]({% link docs/stable/core_extensions/excel.md %})               | Adds support for Excel-like format strings                       |                 |
| [fts]({% link docs/stable/core_extensions/full_text_search.md %})      | Adds support for Full-Text Search Indexes                        |                 |
| [icu]({% link docs/stable/core_extensions/icu.md %})                   | Adds support for time zones and collations using the ICU library |                 |
| [inet]({% link docs/stable/core_extensions/inet.md %})                 | Adds support for IP-related data types and functions             |                 |
| [json]({% link docs/stable/data/json/overview.md %})                   | Adds support for JSON operations                                 |                 |
| [parquet]({% link docs/stable/data/parquet/overview.md %})             | Adds support for reading and writing Parquet files               |                 |
| [sqlite]({% link docs/stable/core_extensions/sqlite.md %})             | Adds support for reading SQLite database files                   | sqlite, sqlite3 |
| [sqlsmith]({% link docs/stable/core_extensions/sqlsmith.md %})         |                                                                  |                 |
| [tpcds]({% link docs/stable/core_extensions/tpcds.md %})               | Adds TPC-DS data generation and query support                    |                 |
| [tpch]({% link docs/stable/core_extensions/tpch.md %})                 | Adds TPC-H data generation and query support                     |                 |

WebAssembly is basically an additional platform, and there might be platform-specific limitations that make some extensions not able to match their native capabilities or to perform them in a different way. We will document here relevant differences for DuckDB-hosted extensions.

### HTTPFS

The HTTPFS extension is, at the moment, not available in DuckDB-Wasm. Https protocol capabilities need to go through an additional layer, the browser, which adds both differences and some restrictions to what is doable from native.

Instead, DuckDB-Wasm has a separate implementation that for most purposes is interchangeable, but does not support all use cases (as it must follow security rules imposed by the browser, such as CORS).
Due to this CORS restriction, any requests for data made using the HTTPFS extension must be to websites that allow (using CORS headers) the website hosting the DuckDB-Wasm instance to access that data.
The [MDN website](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a great resource for more information regarding CORS.

## Extension Signing

As with regular DuckDB extensions, DuckDB-Wasm extension are by default checked on `LOAD` to verify the signature confirm the extension has not been tampered with.
Extension signature verification can be disabled via a configuration option.
Signing is a property of the binary itself, so copying a DuckDB extension (say to serve it from a different location) will still keep a valid signature (e.g., for local development).

## Fetching DuckDB-Wasm Extensions

Official DuckDB extensions are served at `extensions.duckdb.org`, and this is also the default value for the `default_extension_repository` option.
When installing extensions, a relevant URL will be built that will look like `extensions.duckdb.org/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.gz`.

DuckDB-Wasm extension are fetched only on load, and the URL will look like: `extensions.duckdb.org/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm`.

Note that an additional `duckdb-wasm` is added to the folder structure, and the file is served as a `.wasm` file.

DuckDB-Wasm extensions are served pre-compressed using Brotli compression. While fetched from a browser, extensions will be transparently uncompressed. If you want to fetch the `duckdb-wasm` extension manually, you can use `curl --compress extensions.duckdb.org/<...>/icu.duckdb_extension.wasm`.

## Serving Extensions from a Third-Party Repository

As with regular DuckDB, if you use `SET custom_extension_repository = 'https://some.url.com'`, subsequent loads will be attempted at `https://some.url.com/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm`.

Note that GET requests on the extensions needs to be [CORS enabled](https://www.w3.org/wiki/CORS_Enabled) for a browser to allow the connection.

## Tooling

Both DuckDB-Wasm and its extensions have been compiled using latest packaged Emscripten toolchain.

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}
