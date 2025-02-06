---
layout: docu
redirect_from:
- /docs/archive/1.1/extensions
- /docs/archive/1.1/extensions/
title: Extensions
---

## Overview

DuckDB has a flexible extension mechanism that allows for dynamically loading extensions.
These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality.

> Extensions are loadable on all clients (e.g., Python and R).
> Extensions distributed via the Core and Community repositories are built and tested on macOS, Windows and Linux. All operating systems are supported for both the AMD64 and the ARM64 architectures.

## Listing Extensions

To get a list of extensions, use `duckdb_extensions`:

```sql
SELECT extension_name, installed, description
FROM duckdb_extensions();
```

| extension_name    | installed | description                                                  |
|-------------------|-----------|--------------------------------------------------------------|
| arrow             | false     | A zero-copy data integration between Apache Arrow and DuckDB |
| autocomplete      | false     | Adds support for autocomplete in the shell                   |
| ...               | ...       | ...                                                          |

This list will show which extensions are available, which extensions are installed, at which version, where it is installed, and more.
The list includes most, but not all, available core extensions. For the full list, we maintain a [list of core extensions]({% link docs/archive/1.1/extensions/core_extensions.md %}).

## Built-In Extensions

DuckDB's binary distribution comes standard with a few built-in extensions. They are statically linked into the binary and can be used as is.
For example, to use the built-in [`json` extension]({% link docs/archive/1.1/data/json/overview.md %}) to read a JSON file:

```sql
SELECT *
FROM 'test.json';
```

To make the DuckDB distribution lightweight, only a few essential extensions are built-in, varying slightly per distribution. Which extension is built-in on which platform is documented in the [list of core extensions]({% link docs/archive/1.1/extensions/core_extensions.md %}#default-extensions).

## Installing More Extensions

To make an extension that is not built-in available in DuckDB, two steps need to happen:

1. **Extension installation** is the process of downloading the extension binary and verifying its metadata. During installation, DuckDB stores the downloaded extension and some metadata in a local directory. From this directory DuckDB can then load the Extension whenever it needs to. This means that installation needs to happen only once.

2. **Extension loading** is the process of dynamically loading the binary into a DuckDB instance. DuckDB will search the local extension
directory for the installed extension, then load it to make its features available. This means that every time DuckDB is restarted, all
extensions that are used need to be (re)loaded

> Extension installation and loading are subject to a few [limitations]({% link docs/archive/1.1/extensions/working_with_extensions.md %}#limitations).

There are two main methods of making DuckDB perform the **installation** and **loading** steps for an installable extension: **explicitly** and through **autoloading**.

### Explicit `INSTALL` and `LOAD`

In DuckDB extensions can also be explicitly installed and loaded. Both non-autoloadable and autoloadable extensions can be installed this way.
To explicitly install and load an extension, DuckDB has the dedicated SQL statements `LOAD` and `INSTALL`. For example,
to install and load the [`spatial` extension]({% link docs/archive/1.1/extensions/spatial/overview.md %}), run:

```sql
INSTALL spatial;
LOAD spatial;
```

With these statements, DuckDB will ensure the spatial extension is installed (ignoring the `INSTALL` statement if it is already installed), then proceed
to `LOAD` the spatial extension (again ignoring the statement if it is already loaded).

#### Extension Repository

Optionally a repository can be provided where the extension should be installed from, by appending `FROM ⟨repository⟩` to the `INSTALL` / `FORCE INSTALL` command.
This repository can either be an alias, such as [`community`]({% link community_extensions/index.md %}), or it can be a direct URL, provided as a single-quoted string.

After installing/loading an extension, the [`duckdb_extensions` function](#listing-extensions) can be used to get more information.

### Autoloading Extensions

For many of DuckDB's core extensions, explicitly loading and installing extensions is not necessary. DuckDB contains an autoloading mechanism
which can install and load the core extensions as soon as they are used in a query. For example, when running:

```sql
SELECT *
FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv';
```

DuckDB will automatically install and load the [`httpfs`]({% link docs/archive/1.1/extensions/httpfs/overview.md %}) extension. No explicit `INSTALL` or `LOAD` statements are required.

Not all extensions can be autoloaded. This can have various reasons: some extensions make several changes to the running DuckDB instance, making autoloading technically not (yet) possible. For others, it is preferred to have users opt-in to the extension explicitly before use due to the way they modify behavior in DuckDB.

To see which extensions can be autoloaded, check the [core extensions list]({% link docs/archive/1.1/extensions/core_extensions.md %}).

### Community Extensions

DuckDB supports installing third-party [Community Extensions]({% link community_extensions/index.md %}).
These are contributed by community members but they are built, signed, and distributed in a centralized repository.

### Installing Extensions through Client APIs

For many clients, using SQL to load and install extensions is the preferred method. However, some clients have a dedicated
API to install and load extensions. For example the [Python API client]({% link docs/archive/1.1/api/python/overview.md %}#loading-and-installing-extensions),
which has dedicated `install_extension(name: str)` and `load_extension(name: str)` methods. For more details on a specific Client API, refer
to the [Client API docs]({% link docs/archive/1.1/api/overview.md %})

## Updating Extensions

While built-in extensions are tied to a DuckDB release due to their nature of being built into the DuckDB binary, installable extensions
can and do receive updates. To ensure all currently installed extensions are on the most recent version, call:

```sql
UPDATE EXTENSIONS;
```

For more details on extension version refer to [Extension Versioning]({% link docs/archive/1.1/extensions/versioning_of_extensions.md %}).

## Installation Location

By default, extensions are installed under the user's home directory:

```text
~/.duckdb/extensions/⟨duckdb_version⟩/⟨platform_name⟩/
```

For stable DuckDB releases, the `⟨duckdb_version⟩` will be equal to the version tag of that release. For nightly DuckDB builds, it will be equal
to the short git hash of the build. So for example, the extensions for DuckDB version v0.10.3 on macOS ARM64 (Apple Silicon) are installed to `~/.duckdb/extensions/v0.10.3/osx_arm64/`.
An example installation path for a nightly DuckDB build could be `~/.duckdb/extensions/fc2e4b26a6/linux_amd64_gcc4`.

To change the default location where DuckDB stores its extensions, use the `extension_directory` configuration option:

```sql
SET extension_directory = '/path/to/your/extension/directory';
```

Note that setting the value of the `home_directory` configuration option has no effect on the location of the extensions.

## Binary Compatibility

To avoid binary compatibility issues, the binary extensions distributed by DuckDB are tied both to a specific DuckDB version and a platform. This means that DuckDB can automatically detect binary compatibility between it and a loadable extension. When trying to load an extension that was compiled for a different version or platform, DuckDB will throw an error and refuse to load the extension.

See the [Working with Extensions page]({% link docs/archive/1.1/extensions/working_with_extensions.md %}#platforms) for details on available platforms.

## Developing Extensions

The same API that the core extensions use is available for developing extensions. This allows users to extend the functionality of DuckDB such that it suits their domain the best.
A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/). This template also holds some documentation on how to get started building your own extension.

## Extension Signing

Extensions are signed with a cryptographic key, which also simplifies distribution (this is why they are served over HTTP and not HTTPS).
By default, DuckDB uses its built-in public keys to verify the integrity of extension before loading them.
All extensions provided by the DuckDB core team are signed.

### Unsigned Extensions

> Warning Only load unsigned extensions from sources you trust. Also, avoid loading them over HTTP.

If you wish to load your own extensions or extensions from third-parties you will need to enable the `allow_unsigned_extensions` flag.
To load unsigned extensions using the [CLI client]({% link docs/archive/1.1/api/cli/overview.md %}), pass the `-unsigned` flag to it on startup:

```bash
duckdb -unsigned
```

Now any extension can be loaded, signed or not:

```sql
LOAD './some/local/ext.duckdb_extension';
```

For Client APIs, the `allow_unsigned_extensions` database configuration options needs to be set, see the respective [Client API docs]({% link docs/archive/1.1/api/overview.md %}).
For example, for the Python client, see the [Loading and Installing Extensions section in the Python API documentation]({% link docs/archive/1.1/api/python/overview.md %}#loading-and-installing-extensions).

## Working with Extensions

For advanced installation instructions and more details on extensions, see the [Working with Extensions page]({% link docs/archive/1.1/extensions/working_with_extensions.md %}).