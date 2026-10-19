---
layout: docu
railroad: statements/load_and_install.js
title: LOAD / INSTALL Statements
---

## `INSTALL`

The `INSTALL` statement downloads an extension so it can be loaded into a DuckDB session.

### Examples

Install the [`httpfs`]({% link docs/preview/core_extensions/httpfs/overview.md %}) extension:

```sql
INSTALL httpfs;
```

Install the [`h3` community extension]({% link community_extensions/extensions/h3.md %}):

```sql
INSTALL h3 FROM community;
```

### Syntax

<div id="rrdiagram2"></div>

## `LOAD`

The `LOAD` statement loads an installed DuckDB extension into the current session.

When [`autoinstall_known_extensions`]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) is enabled (the default), `LOAD` first installs the extension if it is a known extension that is not yet installed, so an explicit `INSTALL` is not always required. Loading an extension also installs and loads any extensions it depends on. For example, loading [`iceberg`]({% link docs/preview/core_extensions/iceberg/overview.md %}) also installs the [`avro`]({% link docs/preview/core_extensions/avro.md %}) extension that it depends on.

### Examples

Load the [`httpfs`]({% link docs/preview/core_extensions/httpfs/overview.md %}) extension:

```sql
LOAD httpfs;
```

Load the [`spatial`]({% link docs/preview/core_extensions/spatial/overview.md %}) extension:

```sql
LOAD spatial;
```

### Syntax

<div id="rrdiagram1"></div>

## `INSTALL AND LOAD`

> New The `INSTALL AND LOAD` statement is available starting with DuckDB 2.0.

The `INSTALL AND LOAD` statement installs an extension and loads it into the current session in a single step. It is equivalent to running `INSTALL` followed by `LOAD`. If the extension is already installed, the installation step is skipped; if it is already loaded, the loading step is skipped.

`INSTALL AND LOAD` supports the same clauses as `INSTALL`: it can be prefixed with `FORCE` and can be followed by a `FROM` clause to select the [repository]({% link docs/preview/extensions/installing_extensions.md %}#extension-repositories) and a `VERSION` clause to [select the version]({% link docs/preview/extensions/versioning_of_extensions.md %}#installing-a-specific-extension-version).

### Examples

Install and load the [`spatial`]({% link docs/preview/core_extensions/spatial/overview.md %}) extension:

```sql
INSTALL AND LOAD spatial;
```

Install and load the [`h3` community extension]({% link community_extensions/extensions/h3.md %}):

```sql
INSTALL AND LOAD h3 FROM community;
```

Reinstall the [`httpfs`]({% link docs/preview/core_extensions/httpfs/overview.md %}) extension from the `core_nightly` repository and load it:

```sql
FORCE INSTALL AND LOAD httpfs FROM core_nightly;
```
