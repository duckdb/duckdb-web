-- Spatial extension for geospatial support
INSTALL spatial;
LOAD spatial;

CREATE TABLE stations AS
    FROM 's3://duckdb-blobs/stations.parquet';

-- What are the top-3 closest Intercity stations
-- using aerial distance?
SELECT
    s1.name_long AS station1,
    s2.name_long AS station2,
    ST_Distance(
        ST_Point(s1.geo_lng, s1.geo_lat),
        ST_Point(s2.geo_lng, s2.geo_lat)
    ) * 111_139 AS distance
FROM stations s1, stations s2
WHERE s1.type LIKE '%Intercity%'
  AND s2.type LIKE '%Intercity%'
  AND s1.id < s2.id
ORDER BY distance ASC
LIMIT 3;
