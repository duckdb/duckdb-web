CREATE TABLE stations AS
    FROM 's3://duckdb-blobs/stations.parquet';
CREATE TABLE tariffs AS
    FROM 's3://duckdb-blobs/tariffs.parquet';

-- Find the top-5 most expensive domestice train routes
SELECT s1.name_short, s2.name_short, tariffs.price
FROM tariffs
JOIN stations s1 ON tariffs.station1 = s1.code
JOIN stations s2 ON tariffs.station2 = s2.code
WHERE s1.country = s2.country
  AND s1.code < s2.code
ORDER BY price DESC
LIMIT 5;
