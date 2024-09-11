---
layout: docu
title: LOAD/INSTALL Statements
railroad: statements/load_and_install.js
---

# INSTALL

The `INSTALL` statement downloads an extension so it can be loaded into a duckdb session.

## Examples

Install the [`httpfs`]({% link docs/extensions/httpfs/overview.md %}) extension:

```sql
INSTALL httpfs;
```

Install the h3 [community extension]({% link docs/extensions/community_extensions.md %}):

```sql
INSTALL h3 from community;
```

## Syntax

<div id="rrdiagram2"></div>

# LOAD

The `LOAD` statement loads an installed duckdb extension into the current session.

## Examples

Load the [`httpfs`]({% link docs/extensions/httpfs/overview.md %}) extension:

```sql
LOAD httpfs;
```

Load the [`spatial`]({% link docs/extensions/spatial.md %}) extension:

```sql
LOAD spatial;
```

## Syntax

<div id="rrdiagram1"></div>
