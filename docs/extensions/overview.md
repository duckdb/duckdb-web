---
layout: docu
title: Extensions
---

## Overview

DuckDB has a flexible extension mechanism that allows for dynamically loading extension.
These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality.

> Extensions are loadable on all clients (e.g., Python and R).
> Extensions distributed via the official repository are built and tested on MacOS (amd64 and arm64), Windows (amd64) and Linux (amd64 and arm64).

## Using Extensions

### Listing Extensions

To get a list of extensions, run:

```sql
FROM duckdb_extensions();
```

```text
┌────────────────┬─────────┬───────────┬──────────────┬────────────────────────────────────────────┬───────────┐
│ extension_name │ loaded  │ installed │ install_path │                description                 │  aliases  │
│    varchar     │ boolean │  boolean  │   varchar    │                  varchar                   │ varchar[] │
├────────────────┼─────────┼───────────┼──────────────┼────────────────────────────────────────────┼───────────┤
│ autocomplete   │ true    │ true      │ (BUILT-IN)   │ Add supports for autocomplete in the shell │ []        │
| ...            | ...     | ...       | ...          | ...                                        |           |
└────────────────┴─────────┴───────────┴──────────────┴────────────────────────────────────────────┴───────────┘
```

### Extension Types 

DuckDB has three types of extensions.

#### Built-In Extensions

Built-in extensions are loaded at startup and are immediately available for use.

```sql
SELECT * FROM 'test.json';
```

This will use the `json` extension to read the JSON file.

> To make the DuckDB distribution lightweight, it only contains a few fundamental built-in extensions (e.g., `autocomplete`, `json`, `parquet`), which are loaded automatically upon startup.

#### Autoloadable Extensions

Autoloadable extensions are loaded on first use.

```sql
SELECT * FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv';
```

To access files via the HTTPS protocol, DuckDB will automatically load the `httpfs` extension.
Similarly, other autoloadable extensions (`aws`, `fts`) will be loaded on-demand.
If an extension is not already available locally, it will be installed from the official extension repository (`extensions.duckdb.org`).

#### Explicitly Loadable Extensions

Some extensions make several changes to the running DuckDB instance, hence, autoloading them may not be possible.
These extensions have to be installed and loaded using the following SQL statements:

```sql
INSTALL 'spatial';
LOAD 'spatial';
```

```sql
CREATE TABLE tbl(geom GEOMETRY);
```

If you are using the [Python API client](../api/python/overview), you can install and load them with the `load_extension(name: str)` and `install_extension(name: str)` methods.

> Autoloadable extensions can also be installed explicitly.

### Ensuring the Integrity of Extensions

Extensions are signed with a cryptographic key, which also simplifies distribution (this is why they are served over `http`, not `https`). By default, DuckDB uses its built-in public keys to verify the integrity of extension before loading them.
All extensions provided by the DuckDB core team are signed.

If you wish to load your own extensions or extensions from third-parties you will need to enable the `allow_unsigned_extensions` flag.
To load unsigned extensions using the [CLI](../api/cli), pass the `-unsigned` flag to it on startup.

### List of Official Extensions

| Extension name | Description | Aliases |
|---|-----|--|
| arrow [<span class="git">GitHub</span>](https://github.com/duckdblabs/arrow)                                           | A zero-copy data integration between Apache Arrow and DuckDB                       |                 |
| autocomplete                                                                                                           | Adds support for autocomplete in the shell                                         |                 |
| aws                                                                                                                    | Provides features that depend on the AWS SDK                                       |                 |
| azure                                                                                                                  | Adds a filesystem abstraction for Azure blob storage to DuckDB                     |                 |
| [excel](excel)                                                                                                         | Adds support for Excel-like format strings                                         |                 |
| [fts](full_text_search)                                                                                                | Adds support for Full-Text Search Indexes                                          |                 |
| [httpfs](httpfs)                                                                                                       | Adds support for reading and writing files over a HTTP(S) connection               | http, https, s3 |
| [iceberg](iceberg) [<span class="git">GitHub</span>](https://github.com/duckdblabs/duckdb_iceberg)                     | Adds support for Apache Iceberg                                                    |                 |
| icu                                                                                                                    | Adds support for time zones and collations using the ICU library                   |                 |
| inet                                                                                                                   | Adds support for IP-related data types and functions                               |                 |
| jemalloc                                                                                                               | Overwrites system allocator with JEMalloc                                          |                 |
| [json](json)                                                                                                           | Adds support for JSON operations                                                   |                 |
| parquet                                                                                                                | Adds support for reading and writing parquet files                                 |                 |
| [postgres_scanner](postgres_scanner) [<span class="git">GitHub</span>](https://github.com/duckdblabs/postgres_scanner) | Adds support for reading from a Postgres database                                  | postgres        |
| [spatial](spatial) [<span class="git">GitHub</span>](https://github.com/duckdblabs/duckdb_spatial)                     | Geospatial extension that adds support for working with spatial data and functions |                 |
| [sqlite_scanner](sqlite_scanner) [<span class="git">GitHub</span>](https://github.com/duckdblabs/sqlite_scanner)       | Adds support for reading SQLite database files                                     | sqlite, sqlite3 |
| [substrait](substrait) [<span class="git">GitHub</span>](https://github.com/duckdblabs/substrait)                      | Adds support for the Substrait integration                                         |                 |
| tpcds                                                                                                                  | Adds TPC-DS data generation and query support                                      |                 |
| tpch                                                                                                                   | Adds TPC-H data generation and query support                                       |                 |


### Developing Extensions

The same API that the official extensions use is available for developing extensions. This allows users to extend the functionaly of DuckDB such to suit their domain the best.
A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/).

### Working with Extensions

For more details, see the [Working with Extensions page](working_with_extensions).

### Pages in This Section

<!--
any extensions that have their own pages will automatically be added to a table of contents that is rendered directly below this list.
-->
