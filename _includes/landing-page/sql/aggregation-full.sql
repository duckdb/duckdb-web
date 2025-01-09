-- Create table from Parquet file
CREATE TABLE train_services AS
    FROM 's3://duckdb-blobs/train_services.parquet';

-- Get the top-3 busiest train stations
SELECT
    station_name,
    count(*) AS num_services
FROM train_services
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 3;
