// Get the top-3 busiest train stations in May
const db = new duckdb.Database();
db.all(
  `SELECT station, count(*) AS num_services
    FROM train_services
    WHERE monthname(date) = 'May'
    GROUP BY ALL
    ORDER BY num_services DESC
    LIMIT 3;`,
  (err, res) => {
    if (err) {
      throw err;
    } else {
      console.log(res);
    }
  }
);
