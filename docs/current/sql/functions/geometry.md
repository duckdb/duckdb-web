---
layout: docu
redirect_from:
- /docs/preview/sql/functions/geometry
- /docs/stable/sql/functions/geometry
title: Geometry Functions
---

This section describes the functions for for examining and manipulating [`GEOMETRY`]({% link docs/current/sql/data_types/geometry.md %}) values.

> Note: The `spatial` extension provides additional functions for working with `GEOMETRY` values, which are documented in the [Spatial Functions]({% link docs/current/core_extensions/spatial/functions.md %}) section.

## Geometry Operators

The table below lists the operators that can be used with `GEOMETRY` values.

| Operator | Description | Example | Result |
|:-|:--|:---|:--|
| `&&` | Returns true if the geometries bounding boxes intersect. Equivalent to `ST_IntersectsExtent`. | `'POINT(5 5)'::GEOMETRY && 'LINESTRING(0 0, 10 20)'::GEOMETRY` | `true` |

## Built-in Geometry Functions

| Name | Description |
|:-----|:------------|
| [`ST_GeomFromWKB`](#st_geomfromwkb-function) | Creates a geometry from Well-Known Binary (WKB) representation |
| [`ST_AsWKB`](#st_aswkb-function) | Returns the Well-Known Binary (WKB) representation of the geometry |
| [`ST_AsWKT`](#st_aswkt-function) | Returns the Well-Known Text (WKT) representation of the geometry |
| [`ST_Intersects_Extent`](#st_intersects_extent-function) | Returns true if the geometries bounding boxes intersect |
| [`ST_CRS`](#st_crs-function) | Returns the Coordinate Reference System (CRS) identifier of the geometry |
| [`ST_SetCRS`](#st_setcrs-function) | Sets the Coordinate Reference System (CRS) identifier of the geometry |

#### `ST_GeomFromWKB` function

<div class="nostroke_table"></div>

| **Description** | Creates a geometry from Well-Known Binary (WKB) representation |
| **Example** | `ST_GeomFromWKB('\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF0?\x00\x00\x00\x00\x00\x00\x00@')` |
| **Result** | `POINT(1 2)` |

#### `ST_AsWKB` function

<div class="nostroke_table"></div>

| **Description** | Returns the Well-Known Binary (WKB) representation of the geometry |
| **Example** | `ST_AsWKB('POINT(1 2)::GEOMETRY')` |
| **Result** | `\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF0?\x00\x00\x00\x00\x00\x00\x00@` |
| **Alias** | `ST_AsBinary` |

#### `ST_AsWKT` function

<div class="nostroke_table"></div>

| **Description** | Returns the Well-Known Text (WKT) representation of the geometry |
| **Example** | `ST_AsText('POINT(1 2)'::GEOMETRY)` |
| **Result** | `POINT (1 2)` |
| **Alias** | `ST_AsText` |

#### `ST_Intersects_Extent` function

<div class="nostroke_table"></div>

| **Description** | Returns true if the geometries bounding boxes intersect |
| **Example** | `'POINT(5 5)'::GEOMETRY && 'LINESTRING(0 0, 10 20)'::GEOMETRY` |
| **Result** | `true` |
| **Alias** | `&&` |

#### `ST_CRS` function

<div class="nostroke_table"></div>

| **Description** | Returns the Coordinate Reference System (CRS) identifier of the geometry |
| **Example** | `ST_CRS('POINT(1 2)'::GEOMETRY('OGC:CRS84'))` |
| **Result** | `OGC:CRS84` |

#### `ST_SetCRS` function

<div class="nostroke_table"></div>

| **Description** | Sets the Coordinate Reference System (CRS) identifier of the geometry |
| **Example** | `typeof(ST_SetCRS('POINT(1 2)'::GEOMETRY, 'OGC:CRS84'))` |
| **Result** | `GEOMETRY('OGC:CRS84')` |
