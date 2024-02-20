// Get the top-3 busiest train stations in May
const duckdb = require('duckdb');
const db = new duckdb.Database(':memory:');
db.all(
  `SELECT station_name, count(*) AS num_services
    FROM 'http://blobs.duckdb.org/train_services.parquet'
    WHERE monthname(date) = 'May'
    GROUP BY ALL
    ORDER BY num_services DESC
    LIMIT 3;`,
  (err, res) => {
    if (err) {
      console.log("Error", err);
    } else {
      console.table(res);
    }
  }
);
