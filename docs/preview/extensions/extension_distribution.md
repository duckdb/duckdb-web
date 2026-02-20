---
layout: docu
title: Extension Distribution
---

## Platforms

Extension binaries are distributed for several platforms (see below).
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually]({% link docs/preview/extensions/advanced_installation_methods.md %}#installing-an-extension-from-an-explicit-path).

All official extensions are distributed for the following platforms.

| Platform name      | Operating system | Architecture    | CPU types                      |
|--------------------|------------------|-----------------|--------------------------------|
| `linux_amd64`      | Linux            | x86_64  (AMD64) |                                |
| `linux_arm64`      | Linux            | AArch64 (ARM64) | AWS Graviton, Snapdragon, etc. |
| `osx_amd64`        | macOS            | x86_64  (AMD64) | Intel                          |
| `osx_arm64`        | macOS            | AArch64 (ARM64) | Apple Silicon M1, M2, etc.     |
| `windows_amd64`    | Windows          | x86_64  (AMD64) | Intel, AMD, etc.               |
| `windows_arm64`    | Windows          | AArch64 (ARM64) | Copilot+ PC with Qualcomm CPU |

Some extensions are distributed for the following platforms:

* `windows_amd64_mingw`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions]({% link docs/preview/clients/wasm/extensions.md %}))

For platforms outside the ones listed above, we do not officially distribute extensions (e.g., `linux_arm64_android`).

## Extensions Signing

### Signed Extensions

Extensions can be signed with a cryptographic key.
By default, DuckDB uses its built-in public keys to verify the integrity of extensions before loading them.
All core and community extensions are signed by the DuckDB team.

Signing the extension simplifies their distribution, this is why they can be distributed over HTTP without the need for HTTPS,
which itself is supported through an extension ([`httpfs`]({% link docs/preview/core_extensions/httpfs/overview.md %})).

### Unsigned Extensions

> Warning Only load unsigned extensions from sources you trust.
> Avoid loading unsigned extensions over HTTP.
> Consult the [Securing DuckDB page]({% link docs/preview/operations_manual/securing_duckdb/securing_extensions.md %}) for guidelines on how to set up DuckDB in a secure manner.

If you wish to load your own extensions or extensions from third-parties you will need to enable the `allow_unsigned_extensions` flag.
To load unsigned extensions using the [CLI client]({% link docs/preview/clients/cli/overview.md %}), pass the `-unsigned` flag to it on startup:

```batch
duckdb -unsigned
```

Now any extension can be loaded, signed or not:

```sql
LOAD './some/local/ext.duckdb_extension';
```

For client APIs, the `allow_unsigned_extensions` database configuration options needs to be set, see the respective [Client API docs]({% link docs/preview/clients/overview.md %}).
For example, for the Python client, see the [Loading and Installing Extensions section in the Python API documentation]({% link docs/preview/clients/python/overview.md %}#loading-and-installing-extensions).

## Binary Compatibility

To avoid binary compatibility issues, the binary extensions distributed by DuckDB are tied both to a specific DuckDB version and a [platform](#platforms).
This means that DuckDB can automatically detect binary compatibility between it and a loadable extension.
When trying to load an extension that was compiled for a different version or platform, DuckDB will throw an error and refuse to load the extension.

## Creating a Custom Repository

You can create a custom DuckDB extension repository.
A DuckDB repository is an HTTP, HTTPS, S3, or local file based directory that serves the extensions files in a specific structure.
This structure is described in the [“Downloading Extensions Directly from S3” section]({% link docs/preview/extensions/advanced_installation_methods.md %}#downloading-extensions-directly-from-s3), and is the same
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
INSTALL icu FROM '⟨custom_repository⟩';
```

The execution of this statement will first look for `icu.duckdb_extension.gz`, then `icu.duckdb_extension` in the repository's directory structure.

If the custom repository is served over HTTPS or S3, the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) is required. DuckDB will attempt to [autoload]({% link docs/preview/extensions/overview.md %}#autoloading-extensions)
the `httpfs` extension when an installation over HTTPS or S3 is attempted.
