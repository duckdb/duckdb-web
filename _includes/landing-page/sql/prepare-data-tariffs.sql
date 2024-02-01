CREATE OR REPLACE TABLE tariffs AS
    FROM read_csv('distances/tariff-distances-2022-01.csv', header=true, nullstr='XXX');

CREATE OR REPLACE TABLE tariffs AS
    UNPIVOT tariffs
    ON COLUMNS (* EXCLUDE Station)
    INTO NAME OtherStation VALUE Price;

CREATE OR REPLACE TABLE tariffs AS
    SELECT Station AS station1, OtherStation AS station2, Price AS price
    FROM tariffs;

COPY tariffs  TO 'tariffs.parquet'  (FORMAT parquet, COMPRESSION zstd);
