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
