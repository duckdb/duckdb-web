-- Directly query Parquet file over HTTPS
SELECT
    station_name,
    count(*) AS num_services
FROM 'https://blobs.duckdb.org/train_services.parquet'
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 10;
