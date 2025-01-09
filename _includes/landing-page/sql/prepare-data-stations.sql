CREATE OR REPLACE TABLE stations AS
    FROM read_csv('stations-2022-01.csv');

COPY stations TO 'stations.parquet' (FORMAT parquet, COMPRESSION zstd);
