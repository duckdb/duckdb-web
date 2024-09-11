---
layout: docu
title: INSTALL Statement
railroad: statements/install.js
---

The `INSTALL` statement downloads an extension so it can be [loaded]({% link docs/sql/statements/load.md %}) into a duckdb session.

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

<div id="rrdiagram1"></div>
