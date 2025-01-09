-- Directly query Parquet file in S3
SELECT
    station_name,
    count(*) AS num_services
FROM 's3://duckdb-blobs/train_services.parquet'
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 10;
