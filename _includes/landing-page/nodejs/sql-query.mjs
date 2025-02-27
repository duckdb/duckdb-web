// Get the top-3 busiest train stations in May
import { DuckDBInstance } from '@duckdb/node-api';
const instance = await DuckDBInstance.create();
const connection = await instance.connect();
const reader = await connection.runAndReadAll(
  `SELECT station_name, count(*) AS num_services
   FROM
   'http://blobs.duckdb.org/train_services.parquet'
   WHERE monthname(date) = 'May'
   GROUP BY ALL
   ORDER BY num_services DESC
   LIMIT 3;`
);
console.table(reader.getRows());
