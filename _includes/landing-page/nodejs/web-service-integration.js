// Web Service Integration:
// create endpoint to generate numbers
const express = require("express");
const duckdb = require("duckdb");
const app = express();
const db = new duckdb.Database(":memory:");
app.get("/getnumbers", (req, res) => {
  db.all("SELECT random() AS num FROM range(10)", (a, b) => {
    if (a) {
      console.warn(a);
      res.end("Error " + a);
    }
    res.end(JSON.stringify(b));
  });
});

app.listen(8082, () => console.log("Go to: http://localhost:8082/getnumbers"));
