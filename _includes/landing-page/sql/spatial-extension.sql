-- Spatial extension for geospatial support
INSTALL spatial;
LOAD spatial;

SELECT 
    ST_Point(pickup_latitude, pickup_longitude) AS pickup_point,
    ST_Point(dropoff_latitude, dropoff_longitude) AS dropoff_point,
    dropoff_datetime::TIMESTAMP - pickup_datetime::TIMESTAMP AS time,
    trip_distance,
    ST_Distance(
        ST_Transform(pickup_point, 'EPSG:4326', 'ESRI:102718'), 
        ST_Transform(dropoff_point, 'EPSG:4326', 'ESRI:102718')) / 5280 
    AS aerial_distance, 
    trip_distance - aerial_distance AS diff
FROM rides 
WHERE diff > 0
ORDER BY diff DESC;
