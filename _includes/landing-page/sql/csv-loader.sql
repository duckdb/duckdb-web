-- Load CSV file, auto-detecting column name and types
CREATE TABLE services AS
FROM 'https://blobs.duckdb.org/data/nl-railway-2023-week-20.csv.gz';
