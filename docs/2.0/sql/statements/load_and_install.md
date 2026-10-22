---
layout: docu
railroad: statements/load_and_install.js
redirect_from:
- /docs/sql/statements/load_and_install
- /docs/stable/sql/statements/load_and_install
- /docs/current/sql/statements/load_and_install
- /docs/lts/sql/statements/load_and_install
- /docs/preview/sql/statements/load_and_install
title: LOAD / INSTALL Statements
---

## `INSTALL`

The `INSTALL` statement downloads an extension so it can be loaded into a DuckDB session.

### Examples

Install the [`httpfs`]({% link docs/2.0/core_extensions/httpfs/overview.md %}) extension:

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

`LOAD` does not install extensions: if the extension is not installed yet, `LOAD` fails with an error asking you to run `INSTALL` first. Use [`INSTALL AND LOAD`](#install-and-load) to do both in one step. (When a query uses a function or feature of a known core extension, [autoloading]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) installs and loads it automatically.) Loading an extension also installs and loads any extensions it depends on. For example, loading [`iceberg`]({% link docs/2.0/core_extensions/iceberg/overview.md %}) also installs the [`avro`]({% link docs/2.0/core_extensions/avro.md %}) extension that it depends on.

### Examples

Load the [`httpfs`]({% link docs/2.0/core_extensions/httpfs/overview.md %}) extension:

```sql
LOAD httpfs;
```

Load the [`spatial`]({% link docs/2.0/core_extensions/spatial/overview.md %}) extension:

```sql
LOAD spatial;
```

### Syntax

<div id="rrdiagram1"></div>

## `INSTALL AND LOAD`

> New The `INSTALL AND LOAD` statement was introduced in DuckDB 2.0.

The `INSTALL AND LOAD` statement installs an extension and loads it into the current session in a single step. It is equivalent to running `INSTALL` followed by `LOAD`. If the extension is already installed, the installation step is skipped; if it is already loaded, the loading step is skipped.

`INSTALL AND LOAD` supports the same clauses as `INSTALL`: it can be prefixed with `FORCE` and can be followed by a `FROM` clause to select the [repository]({% link docs/2.0/extensions/installing_extensions.md %}#extension-repositories) and a `VERSION` clause to [select the version]({% link docs/2.0/extensions/versioning_of_extensions.md %}#installing-a-specific-extension-version).

### Examples

Install and load the [`spatial`]({% link docs/2.0/core_extensions/spatial/overview.md %}) extension:

```sql
INSTALL AND LOAD spatial;
```

Install and load the [`h3` community extension]({% link community_extensions/extensions/h3.md %}):

```sql
INSTALL AND LOAD h3 FROM community;
```

Reinstall the [`httpfs`]({% link docs/2.0/core_extensions/httpfs/overview.md %}) extension from the `core_nightly` repository and load it:

```sql
FORCE INSTALL AND LOAD httpfs FROM core_nightly;
```
