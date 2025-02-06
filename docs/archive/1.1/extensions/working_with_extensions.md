---
layout: docu
redirect_from:
- /docs/archive/1.1/extensions/troubleshooting
- /docs/archive/1.1/extensions/troubleshooting/
title: Working with Extensions
---

## Platforms

Extension binaries must be built for each platform. Pre-built binaries are distributed for several platforms (see below).
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually](#installing-an-extension-from-an-explicit-path).

All official extensions are distributed for the following platforms.

| Platform name      | Operating system | Architecture    | CPU types                      | Used by                    |
|--------------------|------------------|-----------------|--------------------------------|----------------------------|
| `linux_amd64`      | Linux            | x86_64  (AMD64) |                                | Node.js packages, etc.     |
| `linux_amd64_gcc4` | Linux            | x86_64  (AMD64) |                                | Python packages, CLI, etc. |
| `linux_arm64`      | Linux            | AArch64 (ARM64) | AWS Graviton, Snapdragon, etc. | All packages               |
| `osx_amd64`        | macOS            | x86_64  (AMD64) | Intel                          | All packages               |
| `osx_arm64`        | macOS            | AArch64 (ARM64) | Apple Silicon M1, M2, etc.     | All packages               |
| `windows_amd64`    | Windows          | x86_64  (AMD64) | Intel, AMD, etc.               | All packages               |

> For some Linux ARM distributions (e.g., Python), two different binaries are distributed. These target either the `linux_arm64` or `linux_arm64_gcc4` platforms. Note that extension binaries are distributed for the first, but not the second. Effectively that means that on these platforms your glibc version needs to be 2.28 or higher to use the distributed extension binaries.

Some extensions are distributed for the following platforms:

* `windows_amd64_mingw`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions]({% link docs/archive/1.1/api/wasm/extensions.md %}))

For platforms outside the ones listed above, we do not officially distribute extensions (e.g., `linux_arm64_android`, `linux_arm64_gcc4`).

### Sharing Extensions between Clients

The shared installation location allows extensions to be shared between the client APIs _of the same DuckDB version_, as long as they share the same `platform` or ABI. For example, if an extension is installed with version 0.10.0 of the CLI client on macOS, it is available from the Python, R, etc. client libraries provided that they have access to the user's home directory and use DuckDB version 0.10.0.

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
INSTALL ⟨custom_extension⟩ FROM 'https://my-custom-extension-repository';
```

Alternatively, the `custom_extension_repository` setting can be used to change the default repository used by DuckDB:

```sql
SET custom_extension_repository = 'http://nightly-extensions.duckdb.org';
```

While any URL or local path can be used as a repository, DuckDB currently contains the following predefined repositories:

<div class="narrow_tabl"></div>

| Alias                 | URL                                      | Description                                                                            |
|:----------------------|:-----------------------------------------|:---------------------------------------------------------------------------------------|
| `core`                | `http://extensions.duckdb.org`           | DuckDB core extensions                                                                 |
| `core_nightly`        | `http://nightly-extensions.duckdb.org`   | Nightly builds for `core`                                                              |
| `community`           | `http://community-extensions.duckdb.org` | DuckDB community extensions                                                            |
| `local_build_debug`   | `./build/debug/repository`               | Repository created when building DuckDB from source in debug mode (for development)    |
| `local_build_release` | `./build/release/repository`             | Repository created when building DuckDB from source in release mode (for development)  |

### Working with Multiple Repositories

When working with extensions from different repositories, especially mixing `core` and `core_nightly`, it is important to keep track of the origins
and version of the different extensions. For this reason, DuckDB keeps track of this in the extension installation metadata. For example:

```sql
INSTALL httpfs FROM core;
INSTALL aws FROM core_nightly;
SELECT extension_name, extension_version, installed_from, install_mode
FROM duckdb_extensions();
```

This outputs:

<div class="monospace_table"></div>

| extensions_name | extensions_version | installed_from | install_mode |
|:----------------|:-------------------|:---------------|:-------------|
| httpfs          | 62d61a417f         | core           | REPOSITORY   |
| aws             | 42c78d3            | core_nightly   | REPOSITORY   |
| ...             | ...                | ...            | ...          |

### Creating a Custom Repository

A DuckDB repository is an HTTP, HTTPS, S3, or local file based directory that serves the extensions files in a specific structure.
This structure is described in the [“Downloading Extensions Directly from S3” section](#downloading-extensions-directly-from-s3), and is the same
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

If the custom repository is served over HTTPS or S3, the [`httpfs` extension]({% link docs/archive/1.1/extensions/httpfs/overview.md %}) is required. DuckDB will attempt to [autoload]({% link docs/archive/1.1/extensions/overview.md %}#autoloading-extensions)
the `httpfs` extension when an installation over HTTPS or S3 is attempted.

## Force Installing to Upgrade Extensions

When DuckDB installs an extension, it is copied to a local directory to be cached and avoid future network traffic.
Any subsequent calls to `INSTALL ⟨extension_name⟩` will use the local version instead of downloading the extension again. To force re-downloading the extension, run:

```sql
FORCE INSTALL extension_name;
```

Force installing can also be used to overwrite an extension with an extension of the same name from another repository,

For example, first, `spatial` is installed from the core repository:

```sql
INSTALL spatial;
```

Then, to overwrite this installation with the `spatial` extension from the `core_nightly` repository:

```sql
FORCE INSTALL spatial FROM core_nightly;
```

## Alternative Approaches to Loading and Installing Extensions

### Downloading Extensions Directly from S3

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

### Installing an Extension from an Explicit Path

`INSTALL` can be used with the path to a `.duckdb_extension` file:

```sql
INSTALL 'path/to/httpfs.duckdb_extension';
```

Note that compressed `.duckdb_extension.gz` files need to be decompressed beforehand. It is also possible to specify remote paths.

### Loading an Extension from an Explicit Path

`LOAD` can be used with the path to a `.duckdb_extension`.
For example, if the file was available at the (relative) path `path/to/httpfs.duckdb_extension`, you can load it as follows:

```sql
LOAD 'path/to/httpfs.duckdb_extension';
```

This will skip any currently installed extensions and load the specified extension directly.

Note that using remote paths for compressed files is currently not possible.

### Building and Installing Extensions from Source

For building and installing extensions from source, see the [building guide]({% link docs/archive/1.1/dev/building/overview.md %}).

### Statically Linking Extensions

To statically link extensions, follow the [developer documentation's “Using extension config files” section](https://github.com/duckdb/duckdb/blob/main/extension/README.md#using-extension-config-files).

## In-Tree vs. Out-of-Tree

Originally, DuckDB extensions lived exclusively in the DuckDB main repository, `github.com/duckdb/duckdb`. These extensions are called in-tree. Later, the concept
of out-of-tree extensions was added, where extensions were separated into their own repository, which we call out-of-tree.

While from a user's perspective, there are generally no noticeable differences, there are some minor differences related to versioning:

* in-tree extensions use the version of DuckDB instead of having their own version
* in-tree extensions do not have dedicated release notes, their changes are reflected in the regular [DuckDB release notes](https://github.com/duckdb/duckdb/releases)
* core out-of tree extensions tend to live in a repository in `github.com/duckdb/duckdb_⟨ext_name⟩` but the name may vary. See the [full list]({% link docs/archive/1.1/extensions/core_extensions.md %}) of core extensions for details.

## Limitations

DuckDB's extension mechanism has the following limitations:

* Once loaded, an extension cannot be reinstalled.
* Extensions cannot be unloaded.