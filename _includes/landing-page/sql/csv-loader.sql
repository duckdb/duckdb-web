-- Load CSV file, auto-detecting column name and types
CREATE TABLE services AS
FROM 'https://blobs.duckdb.org/data/train_services_demo.csv.gz';
