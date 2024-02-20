---
layout: docu
title: Extensions
redirect_from:
  - /docs/extensions
  - /docs/extensions/
---

## Overview

DuckDB has a flexible extension mechanism that allows for dynamically loading extensions.
These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality.

> Extensions are loadable on all clients (e.g., Python and R).
> Extensions distributed via the official repository are built and tested on macOS (AMD64 and ARM64), Windows (AMD64) and Linux (AMD64 and ARM64).

We maintain a [list of official extensions](official_extensions).

## Using Extensions

### Listing Extensions

To get a list of extensions, run:

```sql
FROM duckdb_extensions();
```

|  extension_name  | loaded | installed | install_path |                                    description                                     |      aliases      |
|------------------|--------|-----------|--------------|------------------------------------------------------------------------------------|-------------------|
| arrow            | false  | false     |              | A zero-copy data integration between Apache Arrow and DuckDB                       | []                |
| autocomplete     | false  | false     |              | Adds support for autocomplete in the shell                                         | []                |
| ... | ... | ... | ... | ... | ... |

## Extension Types

DuckDB has three types of extensions.

### Built-In Extensions

Built-in extensions are loaded at startup and are immediately available for use.

```sql
SELECT *
FROM 'test.json';
```

This will use the [`json` extension](json) to read the JSON file.

> To make the DuckDB distribution lightweight, it only contains a few fundamental built-in extensions (e.g., [`autocomplete`](autocomplete), [`json`](json), [`parquet`](parquet)), which are loaded automatically.

### Autoloadable Extensions

Autoloadable extensions are loaded on first use.

```sql
SELECT *
FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv';
```

To access files via the HTTPS protocol, DuckDB will automatically load the [`httpfs` extension](../extensions/httpfs).
Similarly, other autoloadable extensions ([`aws`](aws), [`fts`](full_text_search)) will be loaded on-demand.
If an extension is not already available locally, it will be installed from the official extension repository (`extensions.duckdb.org`).

### Explicitly Loadable Extensions

Some extensions make several changes to the running DuckDB instance, hence, autoloading them may not be possible.
These extensions have to be installed and loaded using the following SQL statements:

```sql
INSTALL spatial;
LOAD spatial;
```

### Extension Handling through the Python API

If you are using the [Python API client](../api/python/overview), you can install and load them with the `install_extension(name: str)` and `load_extension(name: str)` methods.

> Autoloadable extensions can also be installed explicitly.

## Ensuring the Integrity of Extensions

Extensions are signed with a cryptographic key, which also simplifies distribution (this is why they are served over HTTP and not HTTPS).
By default, DuckDB uses its built-in public keys to verify the integrity of extension before loading them.
All extensions provided by the DuckDB core team are signed.

If you wish to load your own extensions or extensions from third-parties you will need to enable the `allow_unsigned_extensions` flag.
To load unsigned extensions using the [CLI client](../api/cli), pass the `-unsigned` flag to it on startup.
For the Python client, see the [Loading and Installing Extensions section in the Python API documentation](../api/python/overview#loading-and-installing-extensions).

### Sharing Extensions between Clients

The shared installation location allows extensions to be shared between the client APIs _of the same DuckDB version_, as long as they share the same `platfrom` or ABI. For example, if an extension is installed with version 0.10.0 of the CLI client on macOS, it is available from the Python, R, etc. client libraries provided that they have access to the user's home directory and use DuckDB version 0.10.0.

See the [Working with Extensions page](working_with_extensions#platforms) for details on available platforms.

## Installation Location

Extensions are by default installed under the user's home directory:

```text
~/.duckdb/extensions/v{duckdb_version}/{platform_name}/
```

For example, the extensions for DuckDB version 0.10.0 on macOS ARM64 (Apple Silicon) are installed to `~/.duckdb/extensions/v0.10.0/osx_arm64/`.

> For development builds, the directory of the extensions corresponds to the Git hash of the build, e.g., `~/.duckdb/extensions/fc2e4b26a6/linux_amd64_gcc4`.

### Changing the Extension Directory

To specify a different extension directory, use the `extension_directory` configuration option:

```sql
SET extension_directory = '/path/to/your/extension/directory';
```

## Developing Extensions

The same API that the official extensions use is available for developing extensions. This allows users to extend the functionality of DuckDB such that it suits their domain the best.
A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/).

## Working with Extensions

For advanced installation instructions and more details on extensions, see the [Working with Extensions page](working_with_extensions).

## Pages in This Section
