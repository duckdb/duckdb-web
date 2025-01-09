CREATE OR REPLACE TABLE distances AS
    FROM read_csv('https://blobs.duckdb.org/data/tariff-distances-2022-01.csv', nullstr = 'XXX');

CREATE OR REPLACE TABLE distances AS
    UNPIVOT distances
    ON COLUMNS (* EXCLUDE Station)
    INTO NAME other_station VALUE distance;

CREATE OR REPLACE TABLE distances AS
    SELECT Station AS station1, other_station AS station2, distance
    FROM distances;

COPY distances TO 'distances.parquet'  (FORMAT parquet, COMPRESSION zstd);
