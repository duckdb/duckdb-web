CREATE TABLE train_services AS FROM 'services-2023.csv.gz';
CREATE TABLE train_services_demo AS
    SELECT
        "Service:RDT-ID" AS service_id,
        "Service:Date" AS date,
        "Service:Type" AS type,
        "Service:Train number" AS train_number,
        "Stop:Station code" AS station_code,
        "Stop:Station name" AS station_name,
        "Stop:Departure time" AS departure_time,
        "Stop:Arrival time" AS arrival_time
    FROM train_services
    WHERE week(date) = 20
    ORDER BY date;

COPY train_services_demo TO 'train_services_demo.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY train_services_demo TO 'train_services_demo.csv.gz';
