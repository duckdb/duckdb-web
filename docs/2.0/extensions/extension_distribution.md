---
layout: docu
redirect_from:
- /docs/stable/extensions/extension_distribution
- /docs/current/extensions/extension_distribution
- /docs/lts/extensions/extension_distribution
- /docs/preview/extensions/extension_distribution
title: Extension Distribution
---

## Platforms

Extension binaries are distributed for several platforms (see below).
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually]({% link docs/2.0/extensions/advanced_installation_methods.md %}#installing-an-extension-from-an-explicit-path).

Most official extensions are distributed for the following platforms. Some extensions are only available on a subset of these platforms; see the individual extension pages for details.

| Platform name   | Operating system | Architecture    | CPU types                      |
| --------------- | ---------------- | --------------- | ------------------------------ |
| `linux_amd64`   | Linux            | x86_64  (AMD64) |                                |
| `linux_arm64`   | Linux            | AArch64 (ARM64) | AWS Graviton, Snapdragon, etc. |
| `osx_amd64`     | macOS            | x86_64  (AMD64) | Intel                          |
| `osx_arm64`     | macOS            | AArch64 (ARM64) | Apple Silicon M1, M2, etc.     |
| `windows_amd64` | Windows          | x86_64  (AMD64) | Intel, AMD, etc.               |
| `windows_arm64` | Windows          | AArch64 (ARM64) | Copilot+ PC with Qualcomm CPU  |

> Deprecated The `osx_amd64` platform (macOS on Intel) is being phased out. In DuckDB 2.0, DuckDB and its core extensions are still built for `osx_amd64`, but [community extensions]({% link docs/2.0/extensions/community_extensions.md %}) are no longer built for this platform. DuckDB 2.1 will stop supporting `osx_amd64`.

Some extensions are distributed for the following platforms:

* `linux_amd64_musl` and `linux_arm64_musl`
* `windows_amd64_mingw`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions]({% link docs/2.0/clients/wasm/extensions.md %}))

For platforms outside the ones listed above, we do not officially distribute extensions (e.g., `linux_arm64_android`, `openharmony_arm64`).

## Extensions Signing

### Signed Extensions

Extensions can be signed with a cryptographic key.
By default, DuckDB uses its built-in public keys to verify the integrity of extensions before loading them.
All core and community extensions are signed by the DuckDB team.
In addition, [custom extension repositories]({% link docs/2.0/extensions/extension_repositories.md %}) can serve extensions signed with their own keys: DuckDB pins the repository's public keys when the repository is created and verifies the extensions installed from it against these keys.

Signing the extension simplifies their distribution, this is why they can be distributed over HTTP without the need for HTTPS,
which itself is supported through an extension ([`httpfs`]({% link docs/2.0/core_extensions/httpfs/overview.md %})).

### Unsigned Extensions

> Warning Only load unsigned extensions from sources you trust.
> Avoid loading unsigned extensions over HTTP.
> Consult the [Securing DuckDB page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}) for guidelines on how to set up DuckDB in a secure manner.

If you wish to load your own extensions or extensions from third-parties you will need to enable the `allow_unsigned_extensions` flag.
To load unsigned extensions using the [CLI client]({% link docs/2.0/clients/cli/overview.md %}), pass the `-unsigned` flag to it on startup:

```batch
duckdb -unsigned
```

Now any extension can be loaded, signed or not:

```sql
LOAD './some/local/ext.duckdb_extension';
```

For client APIs, the `allow_unsigned_extensions` database configuration options needs to be set, see the respective [Client API docs]({% link docs/2.0/clients/overview.md %}).
For example, for the Python client, see the [Loading and Installing Extensions section in the Python API documentation]({% link docs/2.0/clients/python/overview.md %}#loading-and-installing-extensions).

## Binary Compatibility

To avoid binary compatibility issues, the binary extensions distributed by DuckDB are tied both to a specific DuckDB version and a [platform](#platforms).
This means that DuckDB can automatically detect binary compatibility between it and a loadable extension.
When trying to load an extension that was compiled for a different version or platform, DuckDB will throw an error and refuse to load the extension.

DuckDB stores this compatibility information in a metadata footer appended to the end of the extension binary.

> Warning Do not run [`strip`](https://sourceware.org/binutils/docs/binutils/strip.html) on an extension binary. Stripping removes or corrupts the appended metadata footer, after which DuckDB reports the metadata as invalid and refuses to load the extension. On some platforms, `strip` fails outright because the footer extends beyond the binary's segments.

### Skipping the Compatibility Check

For debugging purposes, extension developers can skip this check using the `allow_extensions_metadata_mismatch` setting.
This lets `INSTALL` and `UPDATE EXTENSIONS` accept extensions with mismatching or invalid metadata.
For `LOAD`, the setting only takes effect if `allow_unsigned_extensions` is also enabled:

```sql
SET allow_unsigned_extensions = true;
SET allow_extensions_metadata_mismatch = true;
LOAD './some/local/ext.duckdb_extension';
```

> Warning Loading an extension built for a different DuckDB version or platform may crash DuckDB or cause undefined behavior.

## Creating a Custom Repository

You can create a custom DuckDB extension repository.
To have DuckDB trust signed extensions from such a repository without enabling `allow_unsigned_extensions`, register it with its public keys using [`CREATE EXTENSION REPOSITORY`]({% link docs/2.0/extensions/extension_repositories.md %}).
A DuckDB repository is an HTTP, HTTPS, S3, or local file based directory that serves the extensions files in a specific structure.
This structure is described in the [“Downloading Extensions Directly from S3” section]({% link docs/2.0/extensions/advanced_installation_methods.md %}#downloading-extensions-directly-from-s3), and is the same
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
        └── tpch.duckdb_extension
```

See the [`extension-template` repository](https://github.com/duckdb/extension-template/) for all necessary code and scripts
to set up a repository.

When installing an extension from a custom repository, DuckDB will search for both a gzipped and non-gzipped version. For example:

```sql
INSTALL icu FROM '⟨custom_repository⟩';
```

The execution of this statement will first look for `icu.duckdb_extension.gz`, then `icu.duckdb_extension` in the repository's directory structure.

If the custom repository is served over HTTPS or S3, the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) is required. DuckDB will attempt to [autoload]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions)
the `httpfs` extension when an installation over HTTPS or S3 is attempted.
