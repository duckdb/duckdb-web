-- Load CSV file, auto-detecting column name and types
CREATE TABLE services AS
FROM 'https://blobs.duckdb.org/data/railway-2023-02.csv.gz';
