-- Load CSV file to a table. DuckDB auto-detects
-- the CSV's format, column name and types
CREATE TABLE stations AS
    FROM 's3://duckdb-blobs/stations.csv';
