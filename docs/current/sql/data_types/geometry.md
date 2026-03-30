---
layout: docu
redirect_from:
- /docs/preview/sql/data_types/geometry
- /docs/stable/sql/data_types/geometry
title: Geometry Data Type
---

| Name | Description |
|:--|:-----|
| `GEOMETRY` | Geospatial entity |

The `GEOMETRY` data type is used to store and manipulate geometric objects, such as points, lines, and polygons.

The `GEOMETRY` type was part of the [`spatial` extension]({% link docs/current/core_extensions/spatial/overview.md %}) but became a built-in data type in DuckDB v1.5. Most of the benefits of having `GEOMETRY` as a built-in type (e.g., storage optimizations, statistics, etc.) are therefore only available in databases using [storage version v1.5]({% link docs/current/internals/storage.md %}) and above. However, almost all of the associated functions for working with geometries (e.g., calculating distances, areas, intersections) are still part of `spatial`.

## Types of Geometries

Conceptually, the `GEOMETRY` type follows the core data model defined in the [Simple Features](https://en.wikipedia.org/wiki/Simple_Features) standard, which is widely used in geospatial databases and GIS software. A `GEOMETRY` value can therefore represent 7 types of shapes:

| Geometry Type | Description |
|:--|:--|
| **Point** | A single location in space, defined by its coordinates (e.g., longitude and latitude). |
| **LineString** | A sequence of points connected by straight lines, representing a path or route. |
| **Polygon** | A set of closed rings defined by a sequence of points, representing an area such as a country border or a building footprint. The first ring is the "shell", and "interior" rings represent holes in the polygon. |
| **MultiPoint** | A collection of points. |
| **MultiLineString** | A collection of LineStrings. |
| **MultiPolygon** | A collection of Polygons. |
| **GeometryCollection** | A collection of different geometry types, allowing for complex geometries that combine points, lines, and polygons or even other nested geometry collections. |

The textual representation of geometries uses ["Well-Known Text" (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format. Geometries can be cast to and from WKT strings, so you can use string literals to create geometries directly in SQL statements.

In the following example, we create a `GEOMETRY` column with the 7 different types of supported geometries:

```sql
CREATE TABLE geometries (
    id INTEGER,
    geom GEOMETRY
);

INSERT INTO geometries VALUES
  (1, 'POINT (30 10)'),
  (2, 'LINESTRING (30 10, 10 30, 40 40)'),
  (3, 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'),
  (4, 'MULTIPOINT ((10 40), (40 30), (20 20), (30 10))'),
  (5, 'MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20))'),
  (6, 'MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10,15 5)))'),
  (7, 'GEOMETRYCOLLECTION (POINT(40 10), LINESTRING(10 10,20 20,10 40), POLYGON((40 40,20 45,45 30,40 40)))');

SELECT * FROM geometries;
----
┌───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  id   │                                                     geom                                                     │
│ int32 │                                                   geometry                                                   │
├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│     1 │ POINT (30 10)                                                                                                │
│     2 │ LINESTRING (30 10, 10 30, 40 40)                                                                             │
│     3 │ POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))                                                                │
│     4 │ MULTIPOINT (10 40, 40 30, 20 20, 30 10)                                                                      │
│     5 │ MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20))                                               │
│     6 │ MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))                            │
│     7 │ GEOMETRYCOLLECTION (POINT (40 10), LINESTRING (10 10, 20 20, 10 40), POLYGON ((40 40, 20 45, 45 30, 40 40))) │
└───────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Multi-Dimensional Geometries

The `GEOMETRY` type is primarily used to model shapes in two dimensions (e.g. `X`/`Y` or `longitude`/`latitude`), but it also supports shapes with additional vertex dimensions such as `Z` for elevation or `M` for "measure", or both.

The vertex dimensions of a `GEOMETRY` value must be consistent across all vertices. For example, if one vertex has `X`, `Y`, and `Z` coordinates, then all other vertices in that geometry must also have `X`, `Y`, and `Z` coordinates. This means that you cannot have a mix of 2D and 3D vertices within the same geometry. This also applies for collections of geometries, such as `MULTIPOINT` or `GEOMETRYCOLLECTION`, where all geometries within the collection must have the same vertex dimensions.

Functions that operate on `GEOMETRY` values typically ignore any additional dimensions beyond the `X` and `Y` unless explicitly specified, but they can still be stored and can be retrieved if needed.

In the following example, we create a `GEOMETRY` table with 2D, 3D(Z), 3D(M) and 4D(ZM) points:

```sql
CREATE TABLE points (
    id INTEGER,
    geom GEOMETRY
);

INSERT INTO points VALUES
  (1, 'POINT (30 10)'),
  (2, 'POINT Z (30 10 5)'),
  (3, 'POINT M (30 10 1)'),
  (4, 'POINT ZM (30 10 5 1)');

SELECT * FROM points;
----
┌───────┬──────────────────────┐
│  id   │         geom         │
│ int32 │       geometry       │
├───────┼──────────────────────┤
│     1 │ POINT (30 10)        │
│     2 │ POINT Z (30 10 5)    │
│     3 │ POINT M (30 10 1)    │
│     4 │ POINT ZM (30 10 5 1) │
└───────┴──────────────────────┘

-- But we cannot mix different vertex dimensions within the same geometry!
INSERT INTO points VALUES
  (5, 'MULTIPOINT (POINT (30 10), POINT Z (30 10 5))');
----
Invalid Input Error:
Geometry has inconsistent Z/M dimension
```

## Empty Geometries

Geometries can also be "empty" (e.g., `POINT EMPTY`, `LINESTRING EMPTY`, `MULTIPOLYGON EMPTY`, etc.) which means they don't contain any vertices. Empty geometries are still valid geometries and can be used in spatial operations, but they are mostly useful for representing the result of topological operations that don't have a valid geometrical representation (e.g., the intersection of two non-overlapping geometries is an empty geometry).

## Geometry Storage

Internally `GEOMETRY` values are stored as a sequence of bytes, similarly to DuckDB's `BLOB` types. The exact binary format is not yet stabilized and may change in a future release, but as of DuckDB [storage version v1.5]({% link docs/current/internals/storage.md %}) it is based on little-endian [Well-Known Binary (WKB)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary), which is a standard binary encoding for geometries. In older storage versions, geometries were stored in a different custom binary format used by the `spatial` extension, but this conversion is performed automatically at the storage layer and is not visible to the execution engine or the user.

### Shredding and Compression

The `GEOMETRY` type supports a storage optimization called "shredding", which improves compression for geometry columns where all values share the same geometry type and vertex dimensions.

When a row group qualifies, DuckDB splits the geometry segment within the row group into primitive `STRUCT`, `LIST`, and `DOUBLE` segments that can be compressed independently using lightweight algorithms - far more efficiently than storing variable-size binary blobs.

The shredded layout depends on the geometry type:

- `POINT` - STRUCT(X DOUBLE, Y DOUBLE) (and/or Z, M)
- `LINESTRING` - STRUCT(X DOUBLE, Y DOUBLE)[]
- `POLYGON` - STRUCT(X DOUBLE, Y DOUBLE)[][]
- `MULTIPOINT`, `MULTILINESTRING`, `MULTIPOLYGON` - same as above, with one additional level of list nesting
 
Row groups are not shredded if they contain `GEOMETRYCOLLECTION`s, any `EMPTY` geometries, or multiple geometry sub-types.

Additionally, row groups are not shredded if they fall below the minimum size threshold (default: ~25% of the maximum row group size, i.e., 30,000 rows).

This threshold is configurable via the `geometry_minimum_shredding_size` setting. Set it to `0` to always shred, or `-1` to disable shredding entirely.

```sql
-- Disable shredding for geometry columns
SET geometry_minimum_shredding_size = -1;

-- Always shred geometry columns regardless of row group size
SET geometry_minimum_shredding_size = 0;
```

The primary benefit of shredding is significantly improved compression, but in the future we plan to add ways to expose the shredded representation directly to the execution engine without having to "reassemble" the geometry back into binary again.

The following example illustrates the effects of shredding on the storage footprint of a `GEOMETRY` column.

```sql
-- Attach a persistent database with storage version v1.5
ATTACH 'geometry_db.db' as geometry_db (STORAGE_VERSION 'v1.5.0');

USE geometry_db;

-- Disable shredding completely and create a table with 1 million 2D points
SET geometry_minimum_shredding_size = -1;

CREATE OR REPLACE TABLE points AS SELECT printf('POINT (%d %d)', x, y)::GEOMETRY AS geom 
FROM range(0, 1000) AS rx(x), range(0, 1000) AS ry(y);

-- Checkpoint the database to persist the data and storage layout to disk
CHECKPOINT;

-- Attach a second database
ATTACH 'shredded_db.db' as shredded_db (STORAGE_VERSION 'v1.5.0');

USE shredded_db;

-- This time, set the minimum shredding size to 0 to always shred geometry columns,
-- and create the same table with 1 million 2D points
SET geometry_minimum_shredding_size = 0;

CREATE OR REPLACE TABLE points AS SELECT printf('POINT (%d %d)', x, y)::GEOMETRY AS geom 
FROM range(0, 1000) AS rx(x), range(0, 1000) AS ry(y);

-- Checkpoint to persist the data and storage layout to disk, and apply shredding
CHECKPOINT;

-- Now check the storage layout and memory usage of the geometry column in both attached databases
SELECT database_name, database_size FROM pragma_database_size();
----
┌───────────────┬───────────────┐
│ database_name │ database_size │
│    varchar    │    varchar    │
├───────────────┼───────────────┤
│ shredded_db   │ 2.2 MiB       │ -- Almost 3x smaller storage thanks to shredding!
│ geometry_db   │ 6.5 MiB       │ 
│ memory        │ 0 bytes       │
└───────────────┴───────────────┘

-- We can inspect what type of segments are used to store the geometry column 
-- in each database using the `pragma_storage_info` function. 

-- The geometry column in `geometry_db` is stored as regular GEOMETRY segments
SELECT DISTINCT(segment_type) FROM pragma_storage_info('geometry_db.points');
----
┌──────────────┐
│ segment_type │
│   varchar    │
├──────────────┤
│ GEOMETRY     │
│ VALIDITY     │
└──────────────┘

-- While the geometry column in `shredded_db` is decomposed into primitive DOUBLE segments,
-- which can be compressed much more efficiently!
SELECT DISTINCT(segment_type) FROM pragma_storage_info('shredded_db.points');
----
┌──────────────┐
│ segment_type │
│   varchar    │
├──────────────┤
│ VALIDITY     │
│ DOUBLE       │
└──────────────┘
```

### Geometry Statistics 

`GEOMETRY` columns contain geometry-specific statistics that track the bounding box of the geometries in each row group, as well as the set of geometry types and vertex dimensions that are present within the row group.

You can inspect the statistics of a column using the `stats()` function:

```sql
CREATE TABLE geometries as select 'POINT Z (30 10 5)'::GEOMETRY as geom;

SELECT stats(geom) AS geom_stats FROM geometries;
----
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                             geom_stats                                                                                              │
│                                                                                               varchar                                                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [Extent: [X: [30.000000, 30.000000], Y: [10.000000, 10.000000], Z: [5.000000, 5.000000], M: [inf, -inf]], Types: [point_z], Flags: [Has Empty Geom: false, Has No Empty Geom: true, Has Empty Part: │
│  false, Has No Empty Part: true]][Has Null: false, Has No Null: true][Approx Unique: 1]                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

These statistics can be used by the query optimizer to skip row groups that don't match the geometry type or vertex dimensions required by a query, or to speed up spatial predicates by first checking if the bounding box of the geometries in the row group overlaps with the bounding box of the query geometry.

Currently, only the `&&` operator, which is used to check if the bounding box of a geometry intersects the bounding box of another geometry, can take advantage of geometry statistics when used in a `WHERE` clause. There is ongoing work to add support for more statistics-based optimizations to the functions in the `spatial` extension, such as `ST_Intersects`, `ST_Distance`, etc.

Persisting geometry statistics is only possible in storage versions v1.5 and above, and so if you are using an older storage version, the geometry statistics will turn into "unknown" statistics when checkpointing. In other words, the bounding box will be set to an infinitely large bounding box and all geometry types and vertex dimensions will be marked as maybe present, which means that the execution engine will not be able to do any optimizations based on the geometry statistics.

## Coordinate Reference Systems

As far as the execution engine is concerned, geometries are considered to exist in a Cartesian coordinate system. In practice, however, most geospatial data is associated with a specific **Coordinate Reference System** (CRS) that defines how the coordinates relate to real-world locations on the Earth's surface.

A helpful analogy is to think of CRSs as the equivalent of "time zones", but for geospatial data. Just like how time zones define how local time relates to a standard reference time (e.g., UTC), CRSs define how the coordinates of a geometry relate to a standard reference system (e.g., WGS 84). CRSs are usually either geographic (e.g., WGS 84, which uses latitude and longitude) or projected (e.g., UTM, which uses linear units like meters).

When working with geospatial data, it's important to be aware of the CRS associated with different datasets. Performing spatial operations on geometries in different CRSs without proper transformation will most likely lead to incorrect results.

### How are Coordinate Reference Systems stored in DuckDB?

To avoid these kinds of mistakes, DuckDB makes it possible to explicitly associate a CRS with a `GEOMETRY` column. 

This is done by passing a CRS "identifier" as a parameter of the `GEOMETRY` type. For example, a column of type `GEOMETRY('OGC:CRS84')` stores geometries that are associated with the "OGC CRS84" coordinate reference system. 

CRS identifiers in DuckDB are always strings. `OGC:CRS84` is the identifier for a common geographic coordinate system spanning the whole globe where the `X` coordinate represents longitude and the `Y` coordinate represents latitude. DuckDB only knows this because the identifier 'OGC:CRS84' is registered as a _known_ CRS in the system catalog.

By default, only a handful of common CRSs are registered as known, but extensions can also register additional known CRSs. In particular, the `spatial` extension registers over 7000 CRSs from the [EPSG Geodetic Parameter Dataset](https://epsg.org/home.html), which is arguably the most widely used database of coordinate reference systems. 

You can list all available CRSs known to DuckDB using the `duckdb_coordinate_systems()` function:

```sql
SELECT * FROM duckdb_coordinate_systems();
----
┌───────────────┬──────────────┬─────────────┬────────────┬─────────┬───────────┬───────────┬───────────┬───────────────────────────────────────┬───────────────────────────────────────┐
│ database_name │ database_oid │ schema_name │ schema_oid │ crs_oid │ crs_name  │ auth_name │ auth_code │               projjson                │               wkt2_2019               │
│    varchar    │    int64     │   varchar   │   int64    │  int64  │  varchar  │  varchar  │  varchar  │                varchar                │                varchar                │
├───────────────┼──────────────┼─────────────┼────────────┼─────────┼───────────┼───────────┼───────────┼───────────────────────────────────────┼───────────────────────────────────────┤
│ system        │            0 │ main        │          0 │    1354 │ OGC:CRS83 │ OGC       │ CRS83     │ {"$schema":"https://proj.org/schemas… │ GEOGCRS["NAD83 (CRS83)",DATUM["North… │
│ system        │            0 │ main        │          0 │    1353 │ OGC:CRS84 │ OGC       │ CRS84     │ {"$schema":"https://proj.org/schemas… │ GEOGCRS["WGS 84 (CRS84)",ENSEMBLE["W… │
└───────────────┴──────────────┴─────────────┴────────────┴─────────┴───────────┴───────────┴───────────┴───────────────────────────────────────┴───────────────────────────────────────┘
```

### Handling Unknown Coordinate Reference Systems

As mentioned above, only coordinate systems that are registered in the system catalog (and therefore "known" to DuckDB) can be used when creating `GEOMETRY` columns.
If you try to create a `GEOMETRY` column with an unknown CRS identifier, either manually or by importing an external geospatial dataset, the statement will fail with an error.

```sql
SELECT 'POINT(1 2)'::GEOMETRY('DUCK:1337') AS my_point;
----
Binder Error:
Encountered unrecognized coordinate system 'DUCK:1337' when trying to create GEOMETRY type
The coordinate system definition may be incomplete or invalid ...
```

This restriction exists because DuckDB needs the complete CRS definition, not just an identifier, to perform coordinate transformations and to export to formats that embed CRS metadata, such as GeoParquet. Without a system catalog entry, there is no way to resolve an identifier to its full definition.

You can set the `ignore_unknown_crs` configuration option to `true` to simply skip any unknown CRSs and create `GEOMETRY` columns without CRS instead.

```sql

-- Ignore any unknown CRS identifiers
SET ignore_unknown_crs = true;

select 'POINT(1 2)'::GEOMETRY('DUCK:1337') AS my_point;
----
┌─────────────┐
│  my_point   │
│  geometry   │ -- The geometry is created, but the CRS is dropped from the type!
├─────────────┤
│ POINT (1 2) │
└─────────────┘
```

Alternatively, if you are trying to define a `GEOMETRY` column yourself, you can provide a complete CRS definition in WKT or PROJJSON format instead of a shorthand identifier as the CRS parameter. However, as complete CRS definitions are usually very large, this gets unwieldy very quickly and is not recommended for interactive use.

It is currently not possible to define a custom CRS from within SQL, or to persist custom CRS definitions in a database such that DuckDB can use them to resolve CRS identifiers for geometry columns, but this is something we are considering for the future.

### Working with Geometries in Different Coordinate Reference Systems

One benefit of tracking CRSs as part of the type system is that it prevents a lot of common mistakes that can occur when working with geometries from different coordinate systems. Most spatial functions that operate on multiple `GEOMETRY` values verify that all input expressions have the same CRS before performing the operation. Similarly, `GEOMETRY` columns can only be implicitly cast to and from other `GEOMETRY` columns if the source or the target don't have a CRS specified.

To convert a geometry from one CRS to another, you can use the `ST_Transform(geom, crs)` function from the `spatial` extension. 

```sql

LOAD spatial;

SELECT ST_Transform('POINT(4.897070 52.377956)'::GEOMETRY('OGC:CRS84'), 'EPSG:3857') AS transformed;
----
┌────────────────────────────────────────────┐
│                transformed                 │
│           geometry('epsg:3857')            │
├────────────────────────────────────────────┤
│ POINT (545139.3387790163 6868755.38408516) │
└────────────────────────────────────────────┘
```

You can also use the `ST_SetCRS(geom, crs)` function to assign a CRS to a geometry that doesn't have one, or to reassign a CRS without transforming coordinates (e.g., when the data is already in the correct coordinate system but lacks the correct CRS).

```sql
SELECT ST_SetCRS('POINT(4.897070 52.377956)'::GEOMETRY, 'OGC:CRS84') AS with_crs;
----
┌───────────────────────────┐
│         with_crs          │
│   geometry('ogc:crs84')   │
├───────────────────────────┤
│ POINT (4.89707 52.377956) │
└───────────────────────────┘
```

Or if you want to remove the CRS from a geometry, you can either just cast to `GEOMETRY`, or set the CRS to `''`:

```sql
SELECT 'POINT(4.897070 52.377956)'::GEOMETRY('OGC:CRS84')::GEOMETRY AS no_crs;
----
┌───────────────────────────┐
│          no_crs           │
│         geometry          │
├───────────────────────────┤
│ POINT (4.89707 52.377956) │
└───────────────────────────┘

SELECT ST_SetCRS('POINT(4.897070 52.377956)'::GEOMETRY('OGC:CRS84'), '') AS no_crs;
----
┌───────────────────────────┐
│          no_crs           │
│         geometry          │
├───────────────────────────┤
│ POINT (4.89707 52.377956) │
└───────────────────────────┘
```

You can of course also use `ST_CRS(geom)` to retrieve the CRS of a geometry:

```sql
SELECT ST_CRS('POINT(4.897070 52.377956)'::GEOMETRY('OGC:CRS84')) AS crs;
----
┌───────────┐
│    crs    │
│  varchar  │
├───────────┤
│ OGC:CRS84 │
└───────────┘
```

## Functions

- See [geometry functions]({% link docs/current/sql/functions/geometry.md %}) for the list of built-in geometry functions.
- See the documentation of the [`spatial` extension]({% link docs/current/core_extensions/spatial/overview.md %}) for the large set of additional geometry functions provided by the extension, including functions for calculating areas, distances, intersections, unions, and much more.
