---
layout: docu
title: Extensions
---

DuckDB-Wasm (dynamic) extextensions loading is modeled after regular DuckDB extension loading, with a few relevant differences due to the difference in platform.

### Format

Extensions in DuckDB are binaries to be dynamic loaded via dlopen. A cryptografical signature is appended to the binary.
Extensions in DuckDB-Wasm are a regular Wasm file to be dynamic loaded via Emscripten's dlopen. A cryptografical signature is appended to the Wasm file as a WebAssembly custom section called `duckdb_signature`.
This ensures the file remanins a valid WebAssembly file. Current assumption is that this custom section has to be the last one, but this can be potentially relaxed in the future.

### INSTALL and LOAD

INSTALL semantic in native embeddings of DuckDB is to fetch, decompress from gzip and store data in local disk.
LOAD semantic in native embeddings of DuckDB is to (optionally) perform signature checks AND dynamic load the binary with the main DuckDB binary.

In DuckDB-Wasm, INSTALL is a no-op given there is no durable cross-session storage. LOAD will fetch (and decompress on the fly), perform signature checks AND dynamic load via Emscripten implementation of dlopen.

### List of Officially Available Extensions

| Extension name | Description | Aliases |
|---|-----|--|
| autocomplete                                                                                                           | Adds support for autocomplete in the shell                                         |                 |
| [excel](excel)                                                                                                         | Adds support for Excel-like format strings                                         |                 |
| [fts](full_text_search)                                                                                                | Adds support for Full-Text Search Indexes                                          |                 |
| icu                                                                                                                    | Adds support for time zones and collations using the ICU library                   |                 |
| inet                                                                                                                   | Adds support for IP-related data types and functions                               |                 |
| [json](json)                                                                                                           | Adds support for JSON operations                                                   |                 |
| parquet                                                                                                                | Adds support for reading and writing parquet files                                 |                 |
| [sqlite_scanner](sqlite_scanner) [<span class="git">GitHub</span>](https://github.com/duckdblabs/sqlite_scanner)       | Adds support for reading SQLite database files                                     | sqlite, sqlite3 |
| sqlsmit      |  | |
| [substrait](substrait) [<span class="git">GitHub</span>](https://github.com/duckdblabs/substrait)                      | Adds support for the Substrait integration                                         |                 |
| tpcds                                                                                                                  | Adds TPC-DS data generation and query support                                      |                 |
| tpch                                                                                                                   | Adds TPC-H data generation and query support                                       |                 |

### HTTPFS

### Serving DuckDB-Wasm extensions

### Life cycle of DuckDB-Wasm extensions

### Tooling

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}
