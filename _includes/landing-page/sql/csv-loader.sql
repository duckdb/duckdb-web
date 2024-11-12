-- Load CSV file, auto-detecting column name and types
CREATE TABLE stations AS
    FROM 's3://duckdb-blobs/stations.csv';
