-- Directly query Parquet file in S3
SELECT AS station, count(*) AS num_services
FROM 's3://duckdb-blobs/data/nl-railway/services-2023.parquet'
LIMIT 10;
