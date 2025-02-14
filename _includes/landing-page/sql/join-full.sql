CREATE TABLE stations AS
    FROM 's3://duckdb-blobs/stations.parquet';
CREATE TABLE distances AS
    FROM 's3://duckdb-blobs/distances.parquet';

-- Find the top-3 longest domestic train routes
SELECT s1.name_short, s2.name_short, d.distance
FROM distances d
JOIN stations s1 ON d.station1 = s1.code
JOIN stations s2 ON d.station2 = s2.code
WHERE s1.country = s2.country
  AND s1.code < s2.code
ORDER BY distance DESC
LIMIT 3;
