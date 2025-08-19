---
layout: docu
title: GDAL Integration
redirect_from:
- /docs/stable/extensions/spatial/gdal
- /docs/stable/extensions/spatial/gdal/
---

The spatial extension integrates the [GDAL](https://gdal.org/en/latest/) translator library to read and write spatial data from a variety of geospatial vector file formats. See the documentation for the [`st_read` table function]({% link docs/stable/core_extensions/spatial/functions.md %}#st_read) for how to make use of this in practice.

In order to spare users from having to setup and install additional dependencies on their system, the spatial extension bundles its own copy of the GDAL library. This also means that spatial's version of GDAL may not be the latest version available or provide support for all of the file formats that a system-wide GDAL installation otherwise would. Refer to the section on the [`st_drivers` table function]({% link docs/stable/core_extensions/spatial/functions.md %}#st_drivers) to inspect which GDAL drivers are currently available.

## GDAL Based `COPY` Function

The spatial extension does not only enable _importing_ geospatial file formats (through the `ST_Read` function), it also enables _exporting_ DuckDB tables to different geospatial vector formats through a GDAL based `COPY` function.

For example, to export a table to a GeoJSON file, with generated bounding boxes, you can use the following query:

```sql
COPY ⟨table⟩ TO 'some/file/path/filename.geojson'
WITH (FORMAT gdal, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES', SRS 'EPSG:4326');
```

Available options:

* `FORMAT`: is the only required option and must be set to `GDAL` to use the GDAL based copy function.
* `DRIVER`: is the GDAL driver to use for the export. Use `ST_Drivers()` to list the names of all available drivers.
* `LAYER_CREATION_OPTIONS`: list of options to pass to the GDAL driver. See the GDAL docs for the driver you are using for a list of available options.
* `SRS`: Set a spatial reference system as metadata to use for the export. This can be a WKT string, an EPSG code or a proj-string, basically anything you would normally be able to pass to GDAL. Note that this will **not** perform any reprojection of the input geometry, it just sets the metadata if the target driver supports it.

## Limitations

Note that only vector based drivers are supported by the GDAL integration. Reading and writing raster formats are not supported.
