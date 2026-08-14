---
github_repository: https://github.com/duckdb/duckdb-spatial
layout: docu
redirect_from:
- /docs/extensions/spatial
- /docs/stable/extensions/spatial
- /docs/stable/extensions/spatial/overview
- /docs/preview/core_extensions/spatial/overview
- /docs/stable/core_extensions/spatial/overview
title: Spatial Extension
---

The `spatial` extension provides support for geospatial data processing in DuckDB.
For an overview of the extension, see our [blog post]({% post_url 2023-04-28-spatial %}).

## Installing and Loading

To install the `spatial` extension, run:

```sql
INSTALL spatial;
```

Note that the `spatial` extension is not autoloadable.
Therefore, you need to load it before using it:

```sql
LOAD spatial;
```
