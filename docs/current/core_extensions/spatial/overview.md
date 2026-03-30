---
github_repository: https://github.com/duckdb/duckdb-spatial
layout: docu
redirect_from:
- /docs/extensions/spatial
- /docs/lts/extensions/spatial
- /docs/lts/extensions/spatial/overview
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

## The `GEOMETRY` Type

The core of the spatial extension is the [`GEOMETRY` type]({% link docs/current/sql/data_types/geometry.md %}), which is a flexible and extensible data type for representing geometric objects. The `GEOMETRY` type used to be provided by the `spatial` extension, but it became a built-in data type in DuckDB v1.5. However, almost all of the associated functions for working with geometries (e.g., calculating distances, areas, intersections) are still part of `spatial`.

Besides operating on `GEOMETRY`, the spatial extension also includes a couple of experimental non-standard explicit geometry types, such as `POINT_2D`, `LINESTRING_2D`, `POLYGON_2D` and `BOX_2D` that are based on DuckDBs native nested types, such as `STRUCT` and `LIST`. Since these have a fixed and predictable internal memory layout, it is theoretically possible to optimize a lot of geospatial algorithms to be much faster when operating on these types than on the `GEOMETRY` type. However, only a couple of functions in the spatial extension have been explicitly specialized for these types so far. All of these new types are implicitly castable to `GEOMETRY`, but with a small conversion cost, so the `GEOMETRY` type is still the recommended type to use if you are planning to work with a lot of different spatial functions.
