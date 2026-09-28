---
layout: docu
title: Writing JSON
---

The contents of tables or the result of queries can be written directly to a JSON file using the `COPY` statement.
For example:

```sql
CREATE TABLE cities AS
    FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
COPY cities TO 'cities.json';
```

This will result in `cities.json` with the following content:

```json
{"name":"Amsterdam","id":1}
{"name":"London","id":2}
```

See the [`COPY` statement]({% link docs/preview/sql/statements/copy.md %}#copy-to) for more information.

## GeoJSON

> New This feature will be introduced in DuckDB 2.0.

`COPY ... (FORMAT GEOJSON)` writes a GeoJSON `FeatureCollection`. `FORMAT GEOJSONL` (or `ARRAY true` with `FORMAT GEOJSON`) writes newline-delimited `Feature` objects. You do not need `json_geometry_format` for these copy formats.

```sql
COPY (SELECT 'POINT(0 1)'::GEOMETRY AS geom, 10 AS my_field)
    TO 'test.json' (FORMAT GEOJSON);
COPY (SELECT 'POINT(0 1)'::GEOMETRY AS geom, 10 AS my_field)
    TO 'test.jsonl' (FORMAT GEOJSONL);
```

Optional `ID_COLUMN` and `GEOMETRY_COLUMN` pick which columns become the Feature `id` and geometry. `st_asgeojson` / `st_geomfromgeojson` convert a single value. Reading GeoJSON is documented on the [Loading JSON]({% link docs/preview/data/json/loading_json.md %}) page.
