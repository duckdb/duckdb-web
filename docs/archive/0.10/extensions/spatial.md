---
github_repository: https://github.com/duckdb/duckdb_spatial
layout: docu
title: Spatial Extension
---

The `spatial` extension provides support for geospatial data processing in DuckDB.
For an overview of the extension, see our [blog post](/2023/04/28/spatial).

## Installing and Loading

To install and load the `spatial` extension, run:

```sql
INSTALL spatial;
LOAD spatial;
```

## `GEOMETRY` Type

The core of the spatial extension is the `GEOMETRY` type. If you're unfamiliar with geospatial data and GIS tooling, this type probably works very different from what you'd expect.

In short, while the `GEOMETRY` type is a binary representation of "geometry" data made up out of sets of vertices (pairs of X and Y `double` precision floats), it actually stores one of several geometry subtypes. These are `POINT`, `LINESTRING`, `POLYGON`, as well as their "collection" equivalents, `MULTIPOINT`, `MULTILINESTRING` and `MULTIPOLYGON`. Lastly there is `GEOMETRYCOLLECTION`, which can contain any of the other subtypes, as well as other `GEOMETRYCOLLECTION`s recursively.

This may seem strange at first, since DuckDB already have types like `LIST`, `STRUCT` and `UNION` which could be used in a similar way, but the design and behaviour of the `GEOMETRY` type is actually based on the [Simple Features](https://en.wikipedia.org/wiki/Simple_Features) geometry model, which is a standard used by many other databases and GIS software.

That said, the spatial extension also includes a couple of experimental non-standard explicit geometry types, such as `POINT_2D`, `LINESTRING_2D`, `POLYGON_2D` and `BOX_2D` that are based on DuckDBs native nested types, such as structs and lists. In theory it should be possible to optimize a lot of operations for these types much better than for the `GEOMETRY` type (which is just a binary blob), but only a couple functions are implemented so far.

All of these are implicitly castable to `GEOMETRY` but with a conversion cost, so the `GEOMETRY` type is still the recommended type to use for now if you are planning to work with a lot of different spatial functions.

`GEOMETRY` is not currently capable of storing additional geometry types, Z/M coordinates, or SRID information. These features may be added in the future.

## Spatial Scalar Functions

The spatial extension implements a large number of scalar functions and overloads. Most of these are implemented using the [GEOS](https://libgeos.org/) library, but we'd like to implement more of them natively in this extension to better utilize DuckDB's vectorized execution and memory management. The following symbols are used to indicate which implementation is used:

🧭 – GEOS – functions that are implemented using the [GEOS](https://libgeos.org/) library

🦆 – DuckDB – functions that are implemented natively in this extension that are capable of operating directly on the DuckDB types

🔄 – `CAST(GEOMETRY)` – functions that are supported by implicitly casting to `GEOMETRY` and then using the `GEOMETRY` implementation

The currently implemented spatial functions can roughly be categorized into the following groups:

### Geometry Conversion

Convert between geometries and other formats.

| Scalar functions | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D |
|-----|---|--|--|--|---|
| `VARCHAR ST_AsText(GEOMETRY)`       | 🧭       | 🦆       | 🦆           | 🦆         | 🔄 (as `POLYGON`) |
| `WKB_BLOB ST_AsWKB(GEOMETRY)`       | 🦆       | 🦆       | 🦆           | 🦆         | 🦆              |
| `VARCHAR ST_AsHEXWKB(GEOMETRY)`     | 🦆       | 🦆       | 🦆           | 🦆         | 🦆              |
| `VARCHAR ST_AsGeoJSON(GEOMETRY)`    | 🔄       | 🔄       | 🔄           | 🔄         | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_GeomFromText(VARCHAR)` | 🧭       | 🔄       | 🔄           | 🔄         | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_GeomFromWKB(BLOB)`     | 🦆       | 🦆       | 🦆           | 🦆         | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_GeomFromHEXWKB(VARCHAR)` | 🦆     |          |              |             |                 |
| `GEOMETRY ST_GeomFromGeoJSON(VARCHAR)` | 🦆    |          |              |             |                 |

### Geometry Construction

Construct new geometries from other geometries or other data.

| Scalar functions | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D |
|-----|---|--|--|--|---|
| `GEOMETRY ST_Point(DOUBLE, DOUBLE)`                      | 🦆        | 🦆        |               |            |                |
| `GEOMETRY ST_ConvexHull(GEOMETRY)`                       | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Boundary(GEOMETRY)`                         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Buffer(GEOMETRY)`                           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Centroid(GEOMETRY)`                         | 🧭        | 🦆        | 🦆             | 🦆          | 🦆              |
| `GEOMETRY ST_Collect(GEOMETRY[]) `                       | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| `GEOMETRY ST_Normalize(GEOMETRY)`                        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_SimplifyPreserveTopology(GEOMETRY, DOUBLE)` | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Simplify(GEOMETRY, DOUBLE)`                 | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Union(GEOMETRY, GEOMETRY)`                  | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_Intersection(GEOMETRY, GEOMETRY)`           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_MakeLine(GEOMETRY[]) `                      | 🦆        |           | 🦆             |            |                |
| `GEOMETRY ST_Envelope(GEOMETRY)`                         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_FlipCoordinates(GEOMETRY)`                  | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| `GEOMETRY ST_Transform(GEOMETRY, VARCHAR, VARCHAR)`      | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| `BOX_2D ST_Extent(GEOMETRY)`                             | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| `GEOMETRY ST_PointN(GEOMETRY, INTEGER)`                  | 🦆        |           | 🦆             |             |                 |
| `GEOMETRY ST_StartPoint(GEOMETRY)`                       | 🦆        |           | 🦆             |             |                 |
| `GEOMETRY ST_EndPoint(GEOMETRY)`                         | 🦆        |           | 🦆             |             |                 |
| `GEOMETRY ST_ExteriorRing(GEOMETRY)`                     | 🦆        |           |                | 🦆          |                 |
| `GEOMETRY ST_Reverse(GEOMETRY)`                          | 🧭        | 🔄        | 🔄             | 🔄         | 🔄              |
| `GEOMETRY ST_RemoveRepeatedPoints(GEOMETRY)`             | 🧭        | 🔄        | 🔄             | 🔄         | 🔄 (as `POLYGON` ) |
| `GEOMETRY ST_RemoveRepeatedPoints(GEOMETRY, DOUBLE)`     | 🧭        | 🔄        | 🔄             | 🔄         | 🔄 (as `POLYGON` ) |
| `GEOMETRY ST_ReducePrecision(GEOMETRY, DOUBLE)`          | 🧭        | 🔄        | 🔄             | 🔄         | 🔄 (as `POLYGON` ) |
| `GEOMETRY ST_PointOnSurface(GEOMETRY)`                   | 🧭        | 🔄        | 🔄             | 🔄         | 🔄 (as `POLYGON`) |
| `GEOMETRY ST_CollectionExtract(GEOMETRY)`                | 🦆        |           |                |            |                 |
| `GEOMETRY ST_CollectionExtract(GEOMETRY, INTEGER)`       | 🦆        |           |                |            |                 |

### Spatial Properties

Calculate and access spatial properties of geometries.

| Scalar functions | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D |
|-----|---|--|--|--|---|
| `DOUBLE ST_Area(GEOMETRY)`               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| `BOOLEAN ST_IsClosed(GEOMETRY)`          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_IsEmpty(GEOMETRY)`           | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_IsRing(GEOMETRY)`            | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_IsSimple(GEOMETRY)`          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_IsValid(GEOMETRY)`           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `DOUBLE ST_X(GEOMETRY)`                  | 🧭        | 🦆        |                |             |                    |
| `DOUBLE ST_Y(GEOMETRY)`                  | 🧭        | 🦆        |                |             |                    |
| `DOUBLE ST_XMax(GEOMETRY)`               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆                |
| `DOUBLE ST_YMax(GEOMETRY)`               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆                |
| `DOUBLE ST_XMin(GEOMETRY)`               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆                |
| `DOUBLE ST_YMin(GEOMETRY)`               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆                |
| `GeometryType ST_GeometryType(GEOMETRY)` | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as `POLYGON`) |
| `DOUBLE ST_Length(GEOMETRY)`             | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as `POLYGON`) |
| `INTEGER ST_NGeometries(GEOMETRY)`       | 🦆        |           |                |             |                    |
| `INTEGER ST_NPoints(GEOMETRY)`           | 🦆        | 🦆        | 🦆             | 🦆         |  🦆                 |
| `INTEGER ST_NInteriorRings(GEOMETRY)`    | 🦆        |           |                | 🦆         |                     |

### Spatial Relationships

Compute relationships and spatial predicates between geometries.

| Scalar functions | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D |
|-----|---|--|--|--|---|
| `BOOLEAN ST_Within(GEOMETRY, GEOMETRY)`          | 🧭        | 🦆 or 🔄  | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Touches(GEOMETRY, GEOMETRY)`         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Overlaps(GEOMETRY, GEOMETRY)`        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Contains(GEOMETRY, GEOMETRY)`        | 🧭        | 🔄        | 🔄             | 🦆 or 🔄    | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_CoveredBy(GEOMETRY, GEOMETRY)`       | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Covers(GEOMETRY, GEOMETRY)`          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Crosses(GEOMETRY, GEOMETRY)`         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Difference(GEOMETRY, GEOMETRY)`      | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Disjoint(GEOMETRY, GEOMETRY)`        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Intersects(GEOMETRY, GEOMETRY)`      | 🧭        | 🔄        | 🔄             | 🔄          | 🦆                |
| `BOOLEAN ST_Equals(GEOMETRY, GEOMETRY)`          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `DOUBLE ST_Distance(GEOMETRY, GEOMETRY)`         | 🧭        | 🦆 or 🔄  | 🦆 or 🔄        | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_DWithin(GEOMETRY, GEOMETRY, DOUBLE)` | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as `POLYGON`) |
| `BOOLEAN ST_Intersects_Extent(GEOMETRY, GEOMETRY)`| 🦆        | 🦆        | 🦆             | 🦆          | 🦆                |

## Spatial Aggregate Functions

<div class="narrow_table"></div>

| Aggregate functions                       | Implemented with |
|-------------------------------------------|------------------|
| `GEOMETRY ST_Envelope_Agg(GEOMETRY)`      | 🦆               |
| `GEOMETRY ST_Union_Agg(GEOMETRY)`         | 🧭               |
| `GEOMETRY ST_Intersection_Agg(GEOMETRY)`  | 🧭               |

## Spatial Table Functions

### `ST_Read()` – Read Spatial Data from Files

The spatial extension provides a `ST_Read` table function based on the [GDAL](https://github.com/OSGeo/gdal) translator library to read spatial data from a variety of geospatial vector file formats as if they were DuckDB tables. For example to create a new table from a GeoJSON file, you can use the following query:

```sql
CREATE TABLE ⟨table⟩ AS SELECT * FROM ST_Read('some/file/path/filename.json');
```

`ST_Read` can take a number of optional arguments, the full signature is:

```sql
ST_Read(
    VARCHAR,
    sequential_layer_scan : BOOLEAN,
    spatial_filter : WKB_BLOB,
    open_options : VARCHAR[],
    layer : VARCHAR,
    allowed_drivers : VARCHAR[],
    sibling_files : VARCHAR[],
    spatial_filter_box : BOX_2D,
    keep_wkb : BOOLEAN
)
```

* `sequential_layer_scan` (default: `false`): If set to `true`, the table function will scan through all layers sequentially and return the first layer that matches the given `layer` name. This is required for some drivers to work properly, e.g., the `OSM` driver.
* `spatial_filter` (default: `NULL`): If set to a WKB blob, the table function will only return rows that intersect with the given WKB geometry. Some drivers may support efficient spatial filtering natively, in which case it will be pushed down. Otherwise the filtering is done by GDAL which may be much slower.
* `open_options` (default: `[]`): A list of key-value pairs that are passed to the GDAL driver to control the opening of the file. E.g., the `GeoJSON` driver supports a `FLATTEN_NESTED_ATTRIBUTES=YES` option to flatten nested attributes.
* `layer` (default: `NULL`): The name of the layer to read from the file. If `NULL`, the first layer is returned. Can also be a layer index (starting at 0).
* `allowed_drivers` (default: `[]`): A list of GDAL driver names that are allowed to be used to open the file. If empty, all drivers are allowed.
* `sibling_files` (default: `[]`): A list of sibling files that are required to open the file. E.g., the `ESRI Shapefile` driver requires a `.shx` file to be present. Although most of the time these can be discovered automatically.
* `spatial_filter_box` (default: `NULL`): If set to a `BOX_2D`, the table function will only return rows that intersect with the given bounding box. Similar to `spatial_filter`.
* `keep_wkb` (default: `false`): If set, the table function will return geometries in a `wkb_geometry` column with the type `WKB_BLOB` (which can be cast to `BLOB`) instead of `GEOMETRY`. This is useful if you want to use DuckDB with more exotic geometry subtypes that DuckDB spatial doesnt support representing in the `GEOMETRY` type yet.

Note that GDAL is single-threaded, so this table function will not be able to make full use of parallelism. We're planning to implement support for the most common vector formats natively in this extension with additional table functions in the future.

We currently support over 50 different formats. You can generate the following table of supported GDAL drivers yourself by executing `SELECT * FROM ST_Drivers()`.

| short_name | long_name | can_create | can_copy | can_open | help_url |
|--|---|-|-|-|---|
| ESRI Shapefile | ESRI Shapefile                                      | true       | false    | true     | <https://gdal.org/drivers/vector/shapefile.html>     |
| MapInfo File   | MapInfo File                                        | true       | false    | true     | <https://gdal.org/drivers/vector/mitab.html>         |
| UK .NTF        | UK .NTF                                             | false      | false    | true     | <https://gdal.org/drivers/vector/ntf.html>           |
| LVBAG          | Kadaster LV BAG Extract 2.0                         | false      | false    | true     | <https://gdal.org/drivers/vector/lvbag.html>         |
| S57            | IHO S-57 (ENC)                                      | true       | false    | true     | <https://gdal.org/drivers/vector/s57.html>           |
| DGN            | Microstation DGN                                    | true       | false    | true     | <https://gdal.org/drivers/vector/dgn.html>           |
| OGR_VRT        | VRT – Virtual Datasource                            | false      | false    | true     | <https://gdal.org/drivers/vector/vrt.html>           |
| Memory         | Memory                                              | true       | false    | true     |                                                      |
| CSV            | Comma Separated Value (.csv)                        | true       | false    | true     | <https://gdal.org/drivers/vector/csv.html>           |
| GML            | Geography Markup Language (GML)                     | true       | false    | true     | <https://gdal.org/drivers/vector/gml.html>           |
| GPX            | GPX                                                 | true       | false    | true     | <https://gdal.org/drivers/vector/gpx.html>           |
| KML            | Keyhole Markup Language (KML)                       | true       | false    | true     | <https://gdal.org/drivers/vector/kml.html>           |
| GeoJSON        | GeoJSON                                             | true       | false    | true     | <https://gdal.org/drivers/vector/geojson.html>       |
| GeoJSONSeq     | GeoJSON Sequence                                    | true       | false    | true     | <https://gdal.org/drivers/vector/geojsonseq.html>    |
| ESRIJSON       | ESRIJSON                                            | false      | false    | true     | <https://gdal.org/drivers/vector/esrijson.html>      |
| TopoJSON       | TopoJSON                                            | false      | false    | true     | <https://gdal.org/drivers/vector/topojson.html>      |
| OGR_GMT        | GMT ASCII Vectors (.gmt)                            | true       | false    | true     | <https://gdal.org/drivers/vector/gmt.html>           |
| GPKG           | GeoPackage                                          | true       | true     | true     | <https://gdal.org/drivers/vector/gpkg.html>          |
| SQLite         | SQLite / Spatialite                                 | true       | false    | true     | <https://gdal.org/drivers/vector/sqlite.html>        |
| WAsP           | WAsP .map format                                    | true       | false    | true     | <https://gdal.org/drivers/vector/wasp.html>          |
| OpenFileGDB    | ESRI FileGDB                                        | true       | false    | true     | <https://gdal.org/drivers/vector/openfilegdb.html>   |
| DXF            | AutoCAD DXF                                         | true       | false    | true     | <https://gdal.org/drivers/vector/dxf.html>           |
| CAD            | AutoCAD Driver                                      | false      | false    | true     | <https://gdal.org/drivers/vector/cad.html>           |
| FlatGeobuf     | FlatGeobuf                                          | true       | false    | true     | <https://gdal.org/drivers/vector/flatgeobuf.html>    |
| Geoconcept     | Geoconcept                                          | true       | false    | true     |                                                      |
| GeoRSS         | GeoRSS                                              | true       | false    | true     | <https://gdal.org/drivers/vector/georss.html>        |
| VFK            | Czech Cadastral Exchange Data Format                | false      | false    | true     | <https://gdal.org/drivers/vector/vfk.html>           |
| PGDUMP         | PostgreSQL SQL dump                                 | true       | false    | false    | <https://gdal.org/drivers/vector/pgdump.html>        |
| OSM            | OpenStreetMap XML and PBF                           | false      | false    | true     | <https://gdal.org/drivers/vector/osm.html>           |
| GPSBabel       | GPSBabel                                            | true       | false    | true     | <https://gdal.org/drivers/vector/gpsbabel.html>      |
| WFS            | OGC WFS (Web Feature Service)                       | false      | false    | true     | <https://gdal.org/drivers/vector/wfs.html>           |
| OAPIF          | OGC API – Features                                  | false      | false    | true     | <https://gdal.org/drivers/vector/oapif.html>         |
| EDIGEO         | French EDIGEO exchange format                       | false      | false    | true     | <https://gdal.org/drivers/vector/edigeo.html>        |
| SVG            | Scalable Vector Graphics                            | false      | false    | true     | <https://gdal.org/drivers/vector/svg.html>           |
| ODS            | Open Document/ LibreOffice / OpenOffice Spreadsheet | true       | false    | true     | <https://gdal.org/drivers/vector/ods.html>           |
| XLSX           | MS Office Open XML spreadsheet                      | true       | false    | true     | <https://gdal.org/drivers/vector/xlsx.html>          |
| Elasticsearch  | Elastic Search                                      | true       | false    | true     | <https://gdal.org/drivers/vector/elasticsearch.html> |
| Carto          | Carto                                               | true       | false    | true     | <https://gdal.org/drivers/vector/carto.html>         |
| AmigoCloud     | AmigoCloud                                          | true       | false    | true     | <https://gdal.org/drivers/vector/amigocloud.html>    |
| SXF            | Storage and eXchange Format                         | false      | false    | true     | <https://gdal.org/drivers/vector/sxf.html>           |
| Selafin        | Selafin                                             | true       | false    | true     | <https://gdal.org/drivers/vector/selafin.html>       |
| JML            | OpenJUMP JML                                        | true       | false    | true     | <https://gdal.org/drivers/vector/jml.html>           |
| PLSCENES       | Planet Labs Scenes API                              | false      | false    | true     | <https://gdal.org/drivers/vector/plscenes.html>      |
| CSW            | OGC CSW (Catalog  Service for the Web)              | false      | false    | true     | <https://gdal.org/drivers/vector/csw.html>           |
| VDV            | VDV-451/VDV-452/INTREST Data Format                 | true       | false    | true     | <https://gdal.org/drivers/vector/vdv.html>           |
| MVT            | Mapbox Vector Tiles                                 | true       | false    | true     | <https://gdal.org/drivers/vector/mvt.html>           |
| NGW            | NextGIS Web                                         | true       | true     | true     | <https://gdal.org/drivers/vector/ngw.html>           |
| MapML          | MapML                                               | true       | false    | true     | <https://gdal.org/drivers/vector/mapml.html>         |
| TIGER          | U.S. Census TIGER/Line                              | false      | false    | true     | <https://gdal.org/drivers/vector/tiger.html>         |
| AVCBin         | Arc/Info Binary Coverage                            | false      | false    | true     | <https://gdal.org/drivers/vector/avcbin.html>        |
| AVCE00         | Arc/Info E00 (ASCII) Coverage                       | false      | false    | true     | <https://gdal.org/drivers/vector/avce00.html>        |

Note that far from all of these drivers have been tested properly, and some may require additional options to be passed to work as expected.
If you run into any issues please first [consult the GDAL docs](https://gdal.org/drivers/vector/index.html).

### `ST_ReadOsm()` – Read Compressed OSM Data

The spatial extension also provides an experimental `ST_ReadOsm()` table function to read compressed OSM data directly from a `.osm.pbf` file.

This will use multithreading and zero-copy protobuf parsing which makes it a lot faster than using the `st_read()` `OSM` driver, but it only outputs the raw OSM data (Nodes, Ways, Relations), without constructing any geometries.
For node entities you can trivially construct `POINT` geometries, but it is also possible to construct `LINESTRING` AND `POLYGON` by manually joining refs and nodes together in SQL.

Example usage:

```sql
SELECT *
FROM st_readosm('tmp/data/germany.osm.pbf')
WHERE tags['highway'] != []
LIMIT 5;
```

| kind |   id   |                                                                      tags                                                                                   | refs |        lat         |    lon     | ref_roles | ref_types |
|------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|------|--------------------|------------|-----------|-----------|
| node | 122351 | {bicycle=yes, button_operated=yes, crossing=traffic_signals, highway=crossing, tactile_paving=no, traffic_signals:sound=yes, traffic_signals:vibration=yes} | NULL | 53.5492951         | 9.977553   | NULL      | NULL      |
| node | 122397 | {crossing=no, highway=traffic_signals, traffic_signals=signal, traffic_signals:direction=forward}                                                           | NULL | 53.520990100000006 | 10.0156924 | NULL      | NULL      |
| node | 122493 | {TMC:cid_58:tabcd_1:Class=Point, TMC:cid_58:tabcd_1:Direction=negative, TMC:cid_58:tabcd_1:LCLversion=9.00, TMC:cid_58:tabcd_1:LocationCode=10744, ...}     | NULL | 53.129614600000004 | 8.1970173  | NULL      | NULL      |
| node | 123566 | {highway=traffic_signals}                                                                                                                                   | NULL | 54.617268200000005 | 8.9718171  | NULL      | NULL      |
| node | 125801 | {TMC:cid_58:tabcd_1:Class=Point, TMC:cid_58:tabcd_1:Direction=negative, TMC:cid_58:tabcd_1:LCLversion=10.1, TMC:cid_58:tabcd_1:LocationCode=25041, ...}     | NULL | 53.070685000000005 | 8.7819939  | NULL      | NULL      |

## Spatial Replacement Scans

The spatial extension also provides "replacement scans" for common geospatial file formats, allowing you to query files of these formats as if they were tables.

```sql
SELECT * FROM './path/to/some/shapefile/dataset.shp';
```

In practice this is just syntax-sugar for calling `ST_Read`, so there is no difference in performance. If you want to pass additional options, you should use the `ST_Read` table function directly.

The following formats are currently recognized by their file extension:

* ESRI ShapeFile, `.shp`
* GeoPackage, `.gpkg`
* FlatGeoBuf, `.fgb`

Similarly there is a `.osm.pbf` replacement scan for `ST_ReadOsm`.

## Spatial Copy Functions

Much like the `ST_Read` table function the spatial extension provides a GDAL based `COPY` function to export DuckDB tables to different geospatial vector formats.
For example to export a table to a GeoJSON file, with generated bounding boxes, you can use the following query:

```sql
COPY ⟨table⟩ TO 'some/file/path/filename.geojson'
WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
```

Available options:

* `FORMAT`: is the only required option and must be set to `GDAL` to use the GDAL based copy function.
* `DRIVER`: is the GDAL driver to use for the export. See the table above for a list of available drivers.
* `LAYER_CREATION_OPTIONS`: list of options to pass to the GDAL driver. See the GDAL docs for the driver you are using for a list of available options.
* `SRS`: Set a spatial reference system as metadata to use for the export. This can be a WKT string, an EPSG code or a proj-string, basically anything you would normally be able to pass to GDAL/OGR. This will not perform any reprojection of the input geometry though, it just sets the metadata if the target driver supports it.

## Limitations

Raster types are not supported and there is currently no plan to add them to the extension.