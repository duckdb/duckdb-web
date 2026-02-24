---
layout: docu
redirect_from:
- /docs/extensions
- /docs/extensions/overview
title: Extensions
---

DuckDB has a flexible extension mechanism that allows for dynamically loading extensions.
Extensions can enhance DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality.

> Extensions are loadable on all clients (e.g., Python and R).
> Extensions distributed via the Core and Community repositories are built and tested on macOS, Windows and Linux. All operating systems are supported for both the AMD64 and the ARM64 architectures.

## Listing Extensions

To get a list of extensions, use the `duckdb_extensions` function:

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
The list includes most, but not all, available core extensions. For the full list, we maintain a [list of core extensions]({% link docs/stable/core_extensions/overview.md %}).

> Tip We provide an endpoint that serves weekly extension download statistics as JSON files: [core extensions](https://extensions.duckdb.org/downloads-last-week.json) and [community extensions](https://community-extensions.duckdb.org/downloads-last-week.json).

## Built-In Extensions

DuckDB's binary distribution comes standard with a few built-in extensions. They are statically linked into the binary and can be used as is.
For example, to use the built-in [`json` extension]({% link docs/stable/data/json/overview.md %}) to read a JSON file:

```sql
SELECT *
FROM 'test.json';
```

To make the DuckDB distribution lightweight, only a few essential extensions are built-in, varying slightly per distribution. Which extension is built-in on which platform is documented in the [list of core extensions]({% link docs/stable/core_extensions/overview.md %}#default-extensions).

## Installing More Extensions

To make an extension that is not built-in available in DuckDB, two steps need to happen:

1. **Extension installation** is the process of downloading the extension binary and verifying its metadata. During installation, DuckDB stores the downloaded extension and some metadata in a local directory. From this directory DuckDB can then load the Extension whenever it needs to. This means that installation needs to happen only once.

2. **Extension loading** is the process of dynamically loading the binary into a DuckDB instance. DuckDB will search the local extension
directory for the installed extension, then load it to make its features available. This means that every time DuckDB is restarted, all
extensions that are used need to be (re)loaded

> Extension installation and loading are subject to a few [limitations]({% link docs/stable/extensions/installing_extensions.md %}#limitations).

There are two main methods of making DuckDB perform the **installation** and **loading** steps for an installable extension: **explicitly** and through **autoloading**.

### Explicit `INSTALL` and `LOAD`

In DuckDB extensions can also be explicitly installed and loaded. Both non-autoloadable and autoloadable extensions can be installed this way.
To explicitly install and load an extension, DuckDB has the dedicated SQL statements `LOAD` and `INSTALL`. For example,
to install and load the [`spatial` extension]({% link docs/stable/core_extensions/spatial/overview.md %}), run:

```sql
INSTALL spatial;
LOAD spatial;
```

With these statements, DuckDB will ensure the spatial extension is installed (ignoring the `INSTALL` statement if it is already installed), then proceed
to `LOAD` the spatial extension (again ignoring the statement if it is already loaded).

#### Extension Repository

Optionally a repository can be provided where the extension should be installed from, by appending `FROM ⟨repository⟩`{:.language-sql .highlight} to the `INSTALL` / `FORCE INSTALL` command.
This repository can either be an alias, such as [`community`]({% link community_extensions/index.md %}), or it can be a direct URL, provided as a single-quoted string.

After installing/loading an extension, the [`duckdb_extensions` function](#listing-extensions) can be used to get more information.

### Autoloading Extensions

For many of DuckDB's core extensions, explicitly loading and installing extensions is not necessary. DuckDB contains an autoloading mechanism
which can install and load the core extensions as soon as they are used in a query. For example, when running:

```sql
SELECT *
FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv';
```

DuckDB will automatically install and load the [`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %}) extension. No explicit `INSTALL` or `LOAD` statements are required.

Not all extensions can be autoloaded. This can have various reasons: some extensions make several changes to the running DuckDB instance, making autoloading technically not (yet) possible. For others, it is preferred to have users opt-in to the extension explicitly before use due to the way they modify behavior in DuckDB.

To see which extensions can be autoloaded, check the [core extensions list]({% link docs/stable/core_extensions/overview.md %}).

### Community Extensions

DuckDB supports installing third-party [community extensions]({% link community_extensions/index.md %}). For example, you can install the [`avro` community extension]({% link community_extensions/extensions/avro.md %}) via:

```sql
INSTALL avro FROM community;
```

Community extensions are contributed by community members but they are built, [signed]({% link docs/stable/extensions/extension_distribution.md %}#signed-extensions), and distributed in a centralized repository.

## Updating Extensions

While built-in extensions are tied to a DuckDB release due to their nature of being built into the DuckDB binary, installable extensions
can and do receive updates. To ensure all currently installed extensions are on the most recent version, call:

```sql
UPDATE EXTENSIONS;
```

For more details on extension versions, refer to the [Extension Versioning page]({% link docs/stable/extensions/versioning_of_extensions.md %}).

## Developing Extensions

The same API that the core extensions use is available for developing extensions. This allows users to extend the functionality of DuckDB such that it suits their domain the best.
A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/). This template also holds some documentation on how to get started building your own extension.

## Working with Extensions

See the [installation instructions]({% link docs/stable/extensions/installing_extensions.md %}) and the [advanced installation methods page]({% link docs/stable/extensions/advanced_installation_methods.md %}).
