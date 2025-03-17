---
layout: docu
title: Installing Extensions
redirect_from:
- /docs/extensions/troubleshooting
- /docs/extensions/troubleshooting/
- /docs/extensions/working_with_extensions
- /docs/stable/extensions/working_with_extensions
---

To install core DuckDB extensions, use the `INSTALL` command.
For example:

```sql
INSTALL httpfs;
```

This installs the extension from the default repository (`core`).

## Extension Repositories

By default, DuckDB extensions are installed from a single repository containing extensions built and signed by the core DuckDB team.
This ensures the stability and security of the core set of extensions.
These extensions live in the default `core` repository, which points to `http://extensions.duckdb.org`.

Besides the core repository, DuckDB also supports installing extensions from other repositories. For example, the `core_nightly` repository contains nightly builds for core extensions
that are built for the latest stable release of DuckDB. This allows users to try out new features in extensions before they are officially published.

### Installing Extensions from Different Repositories

To install extensions from the default repository (`core`), run:

```sql
INSTALL httpfs;
```

To explicitly install an extension from the core repository, run:

```sql
INSTALL httpfs FROM core;
-- or
INSTALL httpfs FROM 'http://extensions.duckdb.org';
```

To install an extension from the core nightly repository:

```sql
INSTALL spatial FROM core_nightly;
-- or
INSTALL spatial FROM 'http://nightly-extensions.duckdb.org';
```

To install an extension from a custom repository:

```sql
INSTALL ⟨custom_extension⟩ FROM 'https://my-custom-extension-repository';
```

Alternatively, the `custom_extension_repository` setting can be used to change the default repository used by DuckDB:

```sql
SET custom_extension_repository = 'http://nightly-extensions.duckdb.org';
```

DuckDB contains the following predefined repositories:

<div class="narrow_tabl"></div>

| Alias                 | URL                                      | Description                                                                            |
|:----------------------|:-----------------------------------------|:---------------------------------------------------------------------------------------|
| `core`                | `http://extensions.duckdb.org`           | DuckDB core extensions                                                                 |
| `core_nightly`        | `http://nightly-extensions.duckdb.org`   | Nightly builds for `core`                                                              |
| `community`           | `http://community-extensions.duckdb.org` | DuckDB community extensions                                                            |
| `local_build_debug`   | `./build/debug/repository`               | Repository created when building DuckDB from source in debug mode (for development)    |
| `local_build_release` | `./build/release/repository`             | Repository created when building DuckDB from source in release mode (for development)  |

## Working with Multiple Repositories

When working with extensions from different repositories, especially mixing `core` and `core_nightly`, it is important to know the origins and version of the different extensions.
For this reason, DuckDB keeps track of this in the extension installation metadata.
For example:

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

## Force Installing to Upgrade Extensions

When DuckDB installs an extension, it is copied to a local directory to be cached and avoid future network traffic.
Any subsequent calls to `INSTALL ⟨extension_name⟩`{:.language-sql .highlight} will use the local version instead of downloading the extension again.
To force re-downloading the extension, run:

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

### Switching between Repositories

To switch repositories for an extension, use the `FORCE INSTALL` command.
For example, if you have installed `httpfs` from the `core_nightly` repository but would like to switch back to using `core`, run:

```sql
FORCE INSTALL httpfs FROM core;
```

## Installing Extensions through Client APIs

For many clients, using SQL to load and install extensions is the preferred method. However, some clients have a dedicated
API to install and load extensions. For example, the [Python client]({% link docs/stable/clients/python/overview.md %}#loading-and-installing-extensions), has dedicated `install_extension(name: str)` and `load_extension(name: str)` methods. For more details on a specific client API, refer
to the [Client API documentation]({% link docs/stable/clients/overview.md %})

## Installation Location

By default, extensions are installed under the user's home directory:

```{:.language-sql .highlight}
~/.duckdb/extensions/⟨duckdb_version⟩/⟨platform_name⟩/
```

For stable DuckDB releases, the `⟨duckdb_version⟩`{:.language-sql .highlight} will be equal to the version tag of that release. For nightly DuckDB builds, it will be equal
to the short git hash of the build. So for example, the extensions for DuckDB version v0.10.3 on macOS ARM64 (Apple Silicon) are installed to `~/.duckdb/extensions/v0.10.3/osx_arm64/`.
An example installation path for a nightly DuckDB build could be `~/.duckdb/extensions/fc2e4b26a6/linux_amd64_gcc4`.

To change the default location where DuckDB stores its extensions, use the `extension_directory` configuration option:

```sql
SET extension_directory = '/path/to/your/extension/directory';
```

Note that setting the value of the `home_directory` configuration option has no effect on the location of the extensions.

## Uninstalling Extensions

Currently, DuckDB does not provide a command to uninstall extensions.
To uninstall an extension, navigate to the extension's [Installation Location](#installation-location) and remove its `.duckdb_extension` binary file:
For example:

```bash
rm ~/.duckdb/extensions/v1.2.1/osx_arm64/excel.duckdb_extension
```

## Sharing Extensions between Clients

The shared installation location allows extensions to be shared between the client APIs _of the same DuckDB version_, as long as they share the same `platform` or ABI. For example, if an extension is installed with version 1.2.1 of the CLI client on macOS, it is available from the Python, R, etc. client libraries provided that they have access to the user's home directory and use DuckDB version 1.2.1.

## Limitations

DuckDB's extension mechanism has the following limitations:

* Extensions cannot be unloaded.
* Extensions cannot be reloaded. If you [update extensions]({% link docs/stable/sql/statements/update_extensions.md %}), restart the DuckDB process to use newer extensions.
