// Web Service Integration:
// Create endpoint to generate numbers
import express from "express";
import { DuckDBInstance } from '@duckdb/node-api';
const app = express();
const instance = await DuckDBInstance.create();
const connection = await instance.connect();
app.get("/getnumbers", async (req, res) => {
  const reader = await connection.runAndReadAll(
    "SELECT random() AS num FROM range(10)");
  res.end(JSON.stringify(reader.getRows()));
});

app.listen(8082, () => console.log(
  "Go to: http://localhost:8082/getnumbers"));
