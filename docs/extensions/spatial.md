---
layout: docu
title: Spatial
selected: Documentation/Spatial
---
The __spatial__ extension provides support for geospatial data processing in DuckDB.

## GEOMETRY type
The core of the spatial extension is the `GEOMETRY` type. If you're unfamiliar with geospatial data and GIS tooling, this type is probably works very different from what you'd expect. 

In short, while the `GEOMETRY` type is a binary representation of "geometry" data made up out of sets of vertices (pairs of X and Y `double` precision floats), it actually stores one of several geometry subtypes. These are `POINT`, `LINESTRING`, `POLYGON`, as well as their "collection" equivalents, `MULTIPOINT`, `MULTILINESTRING` and `MULTIPOLYGON`. Lastly there is `GEOMETRYCOLLECTION`, which can contain any of the other subtypes, as well as other `GEOMETRYCOLLECTION`s recursively. 

This may seem strange at first, since DuckDB already have types like `LIST`, `STRUCT` and `UNION` which could be used in a similar way, but the design and behaviour of the `GEOMETRY` type is actually based on the [Simple Features](https://en.wikipedia.org/wiki/Simple_Features) geometry model, which is a standard used by many other databases and GIS software.

That said, the spatial extension also includes a couple of experimental non-standard explicit geometry types, such as `POINT_2D`, `LINESTRING_2D`, `POLYGON_2D` and `BOX_2D` that are based on DuckDBs native nested types, such as structs and lists. In theory it should be possible to optimize a lot of operations for these types much better than for the `GEOMETRY` type (which is just a binary blob), but only a couple functions are implemented so far. 

All of these are implicitly castable to `GEOMETRY` but with a conversion cost, so the `GEOMETRY` type is still the recommended type to use for now if you are planning to work with a lot of different spatial functions.

`GEOMETRY` is not currently capable of storing additional geometry types, Z/M coordinates, or SRID information. These features may be added in the future. 

## Spatial scalar Functions
The spatial extension implements a large number of scalar functions and overloads. Most of these are implemented using the [GEOS](https://libgeos.org/) library, but we'd like to implement more of them natively in this extension to better utilize DuckDB's vectorized execution and memory management. The following symbols are used to indicate which implementation is used:

🧭 - GEOS - functions that are implemented using the [GEOS](https://libgeos.org/) library

🦆 - DuckDB - functions that are implemented natively in this extension that are capable of operating directly on the DuckDB types

🔄 - CAST(GEOMETRY) - functions that are supported by implicitly casting to `GEOMETRY` and then using the `GEOMETRY` implementation

The currently implemented spatial functions can roughly be categorized into the following groups:

### Geometry Conversion
Convert between geometries and other formats. 

| Scalar functions                  | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D         |
| --------------------------------- | -------- | -------- | ------------- | ---------- | -------------- |
| VARCHAR ST_AsHEXWKB(GEOMETRY)     | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| VARCHAR ST_AsText(GEOMETRY)       | 🧭        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |
| WKB_BLOB ST_AsWKB(GEOMETRY)       | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| GEOMETRY ST_GeomFromText(VARCHAR) | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_GeomFromWKB(BLOB)     | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |
| VARCHAR ST_AsGeoJSON(VARCHAR)     | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |

### Geometry Construction
Construct new geometries from other geometries or other data.

| Scalar functions                                       | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D         |
| ------------------------------------------------------ | -------- | -------- | ------------- | ---------- | -------------- |
| GEOMETRY ST_Point(DOUBLE, DOUBLE)                      | 🦆        | 🦆        |               |            |                |
| GEOMETRY ST_ConvexHull(GEOMETRY)                       | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Boundary(GEOMETRY)                         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Buffer(GEOMETRY)                           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Centroid(GEOMETRY)                         | 🧭        | 🦆        | 🦆             | 🦆          | 🦆              |
| GEOMETRY ST_Collect(GEOMETRY[])                    | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| GEOMETRY ST_Normalize(GEOMETRY)                        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_SimplifyPreserveTopology(GEOMETRY, DOUBLE) | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Simplify(GEOMETRY, DOUBLE)                 | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Union(GEOMETRY, GEOMETRY)                  | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_Intersection(GEOMETRY, GEOMETRY)           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_MakeLine(GEOMETRY[])                                   | 🦆        |          | 🦆             |            |                |
| GEOMETRY ST_Envelope(GEOMETRY)                         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GEOMETRY ST_FlipCoordinates(GEOMETRY)                  | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| GEOMETRY ST_Transform(GEOMETRY, VARCHAR, VARCHAR)                        | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |


### Spatial Properties
Calculate and access spatial properties of geometries.

| Scalar functions                       | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D         |
| -------------------------------------- | -------- | -------- | ------------- | ---------- | -------------- |
| DOUBLE ST_Area(GEOMETRY)               | 🦆        | 🦆        | 🦆             | 🦆          | 🦆              |
| BOOLEAN ST_IsClosed(GEOMETRY)          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_IsEmpty(GEOMETRY)           | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |
| BOOLEAN ST_IsRing(GEOMETRY)            | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_IsSimple(GEOMETRY)          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_IsValid(GEOMETRY)           | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| DOUBLE ST_X(GEOMETRY)                  | 🧭        | 🦆        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| DOUBLE ST_Y(GEOMETRY)                  | 🧭        | 🦆        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| GeometryType ST_GeometryType(GEOMETRY) | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |
| DOUBLE ST_Length(GEOMETRY)             | 🦆        | 🦆        | 🦆             | 🦆          | 🔄 (as POLYGON) |


### Spatial Relationships
Compute relationships and spatial predicates between geometries.

| Scalar functions                               | GEOMETRY | POINT_2D | LINESTRING_2D | POLYGON_2D | BOX_2D         |
| ---------------------------------------------- | -------- | -------- | ------------- | ---------- | -------------- |
| BOOLEAN ST_Within(GEOMETRY, GEOMETRY)          | 🧭        | 🦆 or 🔄   | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Touches(GEOMETRY, GEOMETRY)         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Overlaps(GEOMETRY, GEOMETRY)        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Contains(GEOMETRY, GEOMETRY)        | 🧭        | 🔄        | 🔄             | 🦆 or 🔄     | 🔄 (as POLYGON) |
| BOOLEAN ST_CoveredBy(GEOMETRY, GEOMETRY)       | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Covers(GEOMETRY, GEOMETRY)          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Crosses(GEOMETRY, GEOMETRY)         | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Difference(GEOMETRY, GEOMETRY)      | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Disjoint(GEOMETRY, GEOMETRY)        | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Intersects(GEOMETRY, GEOMETRY)      | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_Equals(GEOMETRY, GEOMETRY)          | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |
| DOUBLE ST_Distance(GEOMETRY, GEOMETRY)         | 🧭        | 🦆 or 🔄   | 🦆 or 🔄        | 🔄          | 🔄 (as POLYGON) |
| BOOLEAN ST_DWithin(GEOMETRY, GEOMETRY, DOUBLE) | 🧭        | 🔄        | 🔄             | 🔄          | 🔄 (as POLYGON) |


## Spatial Table Functions
The spatial extension provides a `ST_Read` table function based on the [GDAL](https://github.com/OSGeo/gdal) translator library to read spatial data from a variety of geospatial vector file formats as if they were DuckDB tables. For example to create a new table from a GeoJSON file, you can use the following query:
```sql
CREATE TABLE <table> AS SELECT * FROM ST_Read('some/file/path/filename.json');
```

`ST_Read` can take a number of optional arguments, the full signature is: 
```sql
ST_Read(VARCHAR, sequential_layer_scan : BOOLEAN, spatial_filter : WKB_BLOB, open_options : VARCHAR[], layer : VARCHAR, allowed_drivers : VARCHAR[], sibling_files : VARCHAR[], spatial_filter_box : BOX_2D)
```
- `sequential_layer_scan` (default: `false`): If set to `true`, the table function will scan through all layers sequentially and return the first layer that matches the given `layer` name. This is required for some drivers to work properly, e.g. the `OSM` driver.
- `spatial_filter` (default: `NULL`): If set to a WKB blob, the table function will only return rows that intersect with the given WKB geometry. Some drivers may support efficient spatial filtering natively, in which case it will be pushed down. Otherwise the filtering is done by GDAL which may be much slower.
- `open_options` (default: `[]`): A list of key-value pairs that are passed to the GDAL driver to control the opening of the file. E.g. the `GeoJSON` driver supports a `FLATTEN_NESTED_ATTRIBUTES=YES` option to flatten nested attributes.
- `layer` (default: `NULL`): The name of the layer to read from the file. If `NULL`, the first layer is returned. Can also be a layer index (starting at 0).
- `allowed_drivers` (default: `[]`): A list of GDAL driver names that are allowed to be used to open the file. If empty, all drivers are allowed.
- `sibling_files` (default: `[]`): A list of sibling files that are required to open the file. E.g. the `ESRI Shapefile` driver requires a `.shx` file to be present. Although most of the time these can be discovered automatically.
- `spatial_filter_box` (default: `NULL`): If set to a `BOX_2D`, the table function will only return rows that intersect with the given bounding box. Similar to `spatial_filter`.

Note that GDAL is single-threaded, so this table function will not be able to make full use of parllelism. We're planning to implement support for the most common vector formats natively in this extension with additional table functions in the future. 

We currently support over 50 different formats. You can generate the following table of supported GDAL drivers youself by executing `SELECT * FROM ST_Drivers()`.

| short_name     | long_name                                           | can_create | can_copy | can_open | help_url                                           |
| -------------- | --------------------------------------------------- | ---------- | -------- | -------- | -------------------------------------------------- |
| ESRI Shapefile | ESRI Shapefile                                      | true       | false    | true     | https://gdal.org/drivers/vector/shapefile.html     |
| MapInfo File   | MapInfo File                                        | true       | false    | true     | https://gdal.org/drivers/vector/mitab.html         |
| UK .NTF        | UK .NTF                                             | false      | false    | true     | https://gdal.org/drivers/vector/ntf.html           |
| LVBAG          | Kadaster LV BAG Extract 2.0                         | false      | false    | true     | https://gdal.org/drivers/vector/lvbag.html         |
| S57            | IHO S-57 (ENC)                                      | true       | false    | true     | https://gdal.org/drivers/vector/s57.html           |
| DGN            | Microstation DGN                                    | true       | false    | true     | https://gdal.org/drivers/vector/dgn.html           |
| OGR_VRT        | VRT - Virtual Datasource                            | false      | false    | true     | https://gdal.org/drivers/vector/vrt.html           |
| Memory         | Memory                                              | true       | false    | true     |                                                    |
| CSV            | Comma Separated Value (.csv)                        | true       | false    | true     | https://gdal.org/drivers/vector/csv.html           |
| GML            | Geography Markup Language (GML)                     | true       | false    | true     | https://gdal.org/drivers/vector/gml.html           |
| GPX            | GPX                                                 | true       | false    | true     | https://gdal.org/drivers/vector/gpx.html           |
| KML            | Keyhole Markup Language (KML)                       | true       | false    | true     | https://gdal.org/drivers/vector/kml.html           |
| GeoJSON        | GeoJSON                                             | true       | false    | true     | https://gdal.org/drivers/vector/geojson.html       |
| GeoJSONSeq     | GeoJSON Sequence                                    | true       | false    | true     | https://gdal.org/drivers/vector/geojsonseq.html    |
| ESRIJSON       | ESRIJSON                                            | false      | false    | true     | https://gdal.org/drivers/vector/esrijson.html      |
| TopoJSON       | TopoJSON                                            | false      | false    | true     | https://gdal.org/drivers/vector/topojson.html      |
| OGR_GMT        | GMT ASCII Vectors (.gmt)                            | true       | false    | true     | https://gdal.org/drivers/vector/gmt.html           |
| GPKG           | GeoPackage                                          | true       | true     | true     | https://gdal.org/drivers/vector/gpkg.html          |
| SQLite         | SQLite / Spatialite                                 | true       | false    | true     | https://gdal.org/drivers/vector/sqlite.html        |
| WAsP           | WAsP .map format                                    | true       | false    | true     | https://gdal.org/drivers/vector/wasp.html          |
| OpenFileGDB    | ESRI FileGDB                                        | true       | false    | true     | https://gdal.org/drivers/vector/openfilegdb.html   |
| DXF            | AutoCAD DXF                                         | true       | false    | true     | https://gdal.org/drivers/vector/dxf.html           |
| CAD            | AutoCAD Driver                                      | false      | false    | true     | https://gdal.org/drivers/vector/cad.html           |
| FlatGeobuf     | FlatGeobuf                                          | true       | false    | true     | https://gdal.org/drivers/vector/flatgeobuf.html    |
| Geoconcept     | Geoconcept                                          | true       | false    | true     |                                                    |
| GeoRSS         | GeoRSS                                              | true       | false    | true     | https://gdal.org/drivers/vector/georss.html        |
| VFK            | Czech Cadastral Exchange Data Format                | false      | false    | true     | https://gdal.org/drivers/vector/vfk.html           |
| PGDUMP         | PostgreSQL SQL dump                                 | true       | false    | false    | https://gdal.org/drivers/vector/pgdump.html        |
| OSM            | OpenStreetMap XML and PBF                           | false      | false    | true     | https://gdal.org/drivers/vector/osm.html           |
| GPSBabel       | GPSBabel                                            | true       | false    | true     | https://gdal.org/drivers/vector/gpsbabel.html      |
| WFS            | OGC WFS (Web Feature Service)                       | false      | false    | true     | https://gdal.org/drivers/vector/wfs.html           |
| OAPIF          | OGC API - Features                                  | false      | false    | true     | https://gdal.org/drivers/vector/oapif.html         |
| EDIGEO         | French EDIGEO exchange format                       | false      | false    | true     | https://gdal.org/drivers/vector/edigeo.html        |
| SVG            | Scalable Vector Graphics                            | false      | false    | true     | https://gdal.org/drivers/vector/svg.html           |
| ODS            | Open Document/ LibreOffice / OpenOffice Spreadsheet | true       | false    | true     | https://gdal.org/drivers/vector/ods.html           |
| XLSX           | MS Office Open XML spreadsheet                      | true       | false    | true     | https://gdal.org/drivers/vector/xlsx.html          |
| Elasticsearch  | Elastic Search                                      | true       | false    | true     | https://gdal.org/drivers/vector/elasticsearch.html |
| Carto          | Carto                                               | true       | false    | true     | https://gdal.org/drivers/vector/carto.html         |
| AmigoCloud     | AmigoCloud                                          | true       | false    | true     | https://gdal.org/drivers/vector/amigocloud.html    |
| SXF            | Storage and eXchange Format                         | false      | false    | true     | https://gdal.org/drivers/vector/sxf.html           |
| Selafin        | Selafin                                             | true       | false    | true     | https://gdal.org/drivers/vector/selafin.html       |
| JML            | OpenJUMP JML                                        | true       | false    | true     | https://gdal.org/drivers/vector/jml.html           |
| PLSCENES       | Planet Labs Scenes API                              | false      | false    | true     | https://gdal.org/drivers/vector/plscenes.html      |
| CSW            | OGC CSW (Catalog  Service for the Web)              | false      | false    | true     | https://gdal.org/drivers/vector/csw.html           |
| VDV            | VDV-451/VDV-452/INTREST Data Format                 | true       | false    | true     | https://gdal.org/drivers/vector/vdv.html           |
| MVT            | Mapbox Vector Tiles                                 | true       | false    | true     | https://gdal.org/drivers/vector/mvt.html           |
| NGW            | NextGIS Web                                         | true       | true     | true     | https://gdal.org/drivers/vector/ngw.html           |
| MapML          | MapML                                               | true       | false    | true     | https://gdal.org/drivers/vector/mapml.html         |
| TIGER          | U.S. Census TIGER/Line                              | false      | false    | true     | https://gdal.org/drivers/vector/tiger.html         |
| AVCBin         | Arc/Info Binary Coverage                            | false      | false    | true     | https://gdal.org/drivers/vector/avcbin.html        |
| AVCE00         | Arc/Info E00 (ASCII) Coverage                       | false      | false    | true     | https://gdal.org/drivers/vector/avce00.html        |

Note that far from all of these drivers have been tested properly, and some may require additional options to be passed to work as expected. 
If you run into any issues please first [consult the GDAL docs](https://gdal.org/drivers/vector/index.html).

## Spatial Copy Functions

Much like the `ST_Read` table function the spatial extension provides a GDAL based `COPY` function to export duckdb tables to different geospatial vector formats.
For example to export a table to a GeoJSON file, with generated bounding boxes, you can use the following query:
```sql
COPY <table> TO 'some/file/path/filename.geojson'
WITH (FORMAT GDAL, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
```
- `FORMAT`: is the only required option and must be set to `GDAL` to use the GDAL based copy function.
- `DRIVER`: is the GDAL driver to use for the export. See the table above for a list of available drivers.
- `LAYER_CREATION_OPTIONS`: list of options to pass to the GDAL driver. See the GDAL docs for the driver you are using for a list of available options.

## Extra Information
See [the repo](https://github.com/duckdblabs/duckdb_spatial) for the source code of the extension, or the [blog post](/2023/04/28/spatial).
