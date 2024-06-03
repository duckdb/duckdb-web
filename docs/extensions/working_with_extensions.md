---
layout: docu
title: Working with Extensions
---

## Platforms

Extension binaries must be built for each platform. Pre-built binaries are distributed for several platforms (see below).
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually](#installing-extensions-from-an-explicit-path).

All official extensions are distributed for the following platforms.

<div class="narrow_table"></div>

| Platform name      | Description                              |
|--------------------|------------------------------------------|
| `linux_amd64`      | Linux AMD64 (Node.js packages, etc.)     |
| `linux_amd64_gcc4` | Linux AMD64 (Python packages, CLI, etc.) |
| `linux_arm64`      | Linux ARM64 (e.g., AWS Graviton)         |
| `osx_amd64`        | macOS (Intel CPUs)                       |
| `osx_arm64`        | macOS (Apple Silicon: M1, M2, M3 CPUs)   |
| `windows_amd64`    | Windows on Intel and AMD CPUs (x86_64)   |

> For some Linux ARM distributions (e.g., Python), two different binaries are distributed. These target either the `linux_arm64` or `linux_arm64_gcc4` platforms. Note that extension binaries are distributed for the first, but not the second. Effectively that means that on these platforms your glibc version needs to be 2.28 or higher to use the distributed extension binaries.

Some extensions are distributed for the following platforms:

* `windows_amd64_rtools`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions](../api/wasm/extensions))

For platforms outside the ones listed above, we do not officially distribute extensions (e.g., `linux_arm64_gcc4`, `windows_amd64_mingw`).

### Sharing Extensions between Clients

The shared installation location allows extensions to be shared between the client APIs _of the same DuckDB version_, as long as they share the same `platfrom` or ABI. For example, if an extension is installed with version 0.10.0 of the CLI client on macOS, it is available from the Python, R, etc. client libraries provided that they have access to the user's home directory and use DuckDB version 0.10.0.

## Extension Repositories

By default, DuckDB extensions are installed from a single repository containing extensions built and signed by the core
DuckDB team. This ensures the stability and security of the core set of extensions. These extensions live in the default `core` repository
which points to `http://extensions.duckdb.org`.

Besides the core repository, DuckDB also supports installing extensions from other repositories. For example, the `core_nightly` repository contains nightly builds for core extensions
that are built for the latest stable release of DuckDB. This allows users to try out new features in extensions before they are officially published.

### Installing Extensions from a Repository

To install extensions from the default repository (default repository: `core`):

```sql
INSTALL httpfs;
```

To explicitly install an extension from the core repository, run either of:

```sql 
INSTALL httpfs FROM core;
```

Or:

```sql
INSTALL httpfs FROM 'http://extensions.duckdb.org';
```

To install an extension from the core nightly repository:

```sql
INSTALL spatial FROM core_nightly;
```

Or:

```sql
INSTALL spatial FROM 'http://nightly-extensions.duckdb.org';
```

To install an extensions from a custom repository unknown to DuckDB:

```sql
INSTALL custom_extension FROM 'https://my-custom-extension-repository';
```

Alternatively, the `custom_extension_repository` setting can be used to change the default repository used by DuckDB:

```sql
SET custom_extension_repository = 'http://nightly-extensions.duckdb.org';
```

While any url or local path can be used as a repository, currently DuckDB contains the following predefined repositories:

<div class="narrow_table"></div>

| alias               | Url                                    | Description                                                                            |
|:--------------------|:---------------------------------------|:---------------------------------------------------------------------------------------|
| core                | `http://extensions.duckdb.org`         | DuckDB core extensions                                                                 |
| core_nightly        | `http://nightly-extensions.duckdb.org` | Nightly builds for `core`                                                              |
| local_build_debug   | `./build/debug/repository`             | Repository created when building DuckDB from source in debug mode (for development)    |
| local_build_release | `./build/release/repository`           | Repository created when building DuckDB from source in release mode (for development)  |

### Working with Multiple Repositories

When working with extensions from different repositories, especially mixing `core` and `core_nightly`, it is important to keep track of the origins
and version of the different extensions. For this reason, DuckDB keeps track of this in the extension installation metadata. For example:

```sql
INSTALL httpfs FROM core;
INSTALL aws FROM core_nightly;
SELECT extensions_name, extensions_version, installed_from, install_mode FROM duckdb_extensions();
```
Would output:

| extensions_name | extensions_version | installed_from | install_mode |
|:----------------|:-------------------|:---------------|:-------------|
| httpfs          | 62d61a417f         | core           | REPOSITORY   |
| aws             | 42c78d3            | core_nightly   | REPOSITORY   |
| ...             | ...                | ...            | ...          |

### Creating a Custom Repository

A DuckDB repository is an HTTP, HTTPS, S3, or local file based directory that serves the extensions files in a specific structure.
This structure is describe [here](#downloading-extensions-directly-from-s3), and is the same
for local paths and remote servers, for example:

```text
base_repository_path_or_url
└── v1.0.0
    └── osx_arm64
        ├── autocomplete.duckdb_extension
        ├── httpfs.duckdb_extension
        ├── icu.duckdb_extension
        ├── inet.duckdb_extension
        ├── json.duckdb_extension
        ├── parquet.duckdb_extension
        ├── tpcds.duckdb_extension
        ├── tpcds.duckdb_extension
        └── tpch.duckdb_extension
```

See the [`extension-template` repository](https://github.com/duckdb/extension-template/) for all necessary code and scripts
to set up a repository.

When installing an extension from a custom repository, DuckDB will search for both a gzipped and non-gzipped version. For example:

```sql
INSTALL icu FROM '⟨custom repository⟩';
```

The execution of this statement will first look `icu.duckdb_extension.gz`, then `icu.duckdb_extension` in the repository's directory structure.

If the custom repository is served over HTTPS or S3, the [`httpfs` extension](httpfs/overview) is required. DuckDB will attempt to [autoload](overview#autoloading-extensions)
the `httpfs` extension when an installation over HTTPS or S3 is attempted.

## Downloading Extensions Directly from S3

Downloading an extension directly can be helpful when building a [Lambda service](https://aws.amazon.com/pm/lambda/) or container that uses DuckDB.
DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable.
As a result, a direct URL to the file must be used.
To download an extension file directly, use the following format:

```text
http://extensions.duckdb.org/v⟨duckdb_version⟩/⟨platform_name⟩/⟨extension_name⟩.duckdb_extension.gz
```

For example:

```text
http://extensions.duckdb.org/v{{ site.currentduckdbversion }}/windows_amd64/json.duckdb_extension.gz
```

## Loading and Installing an Extension from Explicit Paths

### Installing Extensions from an Explicit Path

`INSTALL` can be used with the path to either a `.duckdb_extension` file.
`.duckdb_extension.gz` files need to be decompressed before issuing `INSTALL name.duckdb_extension;`.

For example, if the file was available into the same directory as where DuckDB is being executed, you can install it as follows:

```sql
INSTALL 'path/to/httpfs.duckdb_extension';
```

It is also possible to specify remote paths.

## Force Installing Extensions

When DuckDB installs an extension, it is copied to a local directory to be cached, avoiding any network traffic.
Any subsequent calls to `INSTALL ⟨extension_name⟩` will use the local version instead of downloading the extension again. To force re-downloading the extension, run:

```sql
FORCE INSTALL extension_name;
```

Force installing can also be used to overwrite an extension with an extension with the same name from another repository,

For example, first, `spatial` is installed from the core repository:

```sql
INSTALL spatial;
```

Then, to overwrite this installation with the `spatial` extension from the `core_nightly` repository:

```sql
FORCE INSTALL spatial FROM core_nightly;
```

## Loading Extension from a Path

`LOAD` can be used with the path to a `.duckdb_extension`.
For example, if the file was available at the (relative) path `path/to/httpfs.duckdb_extension`, you can load it as follows:

```sql
LOAD 'path/to/httpfs.duckdb_extension';
```

This will skip any currently installed file in the specifed path.

Using remote paths for compressed files is currently not possible.

## Building and Installing Extensions

For building and installing extensions from source, see the [building guide](/dev/building#building-and-installing-extensions-from-source).

## Statically Linking Extensions

To statically link extensions, follow the [developer documentation's "Using extension config files" section](https://github.com/duckdb/duckdb/blob/main/extension/README.md#using-extension-config-files).
