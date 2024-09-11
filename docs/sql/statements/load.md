---
layout: docu
title: LOAD Statement
railroad: statements/load.js
---

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
