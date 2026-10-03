---
layout: post
title: "Ducks in a Column"
author: "DuckDB Team"
thumb: "/images/blog/thumbs/ducks-in-a-column.svg"
image: "/images/blog/thumbs/ducks-in-a-column.png"
excerpt: "DuckDB is fast because it keeps its ducks in a column. In this post, we walk through DuckDB features that lean on columnar execution: reading files in place, column-level SQL, aggregation shortcuts, window functions, ASOF joins and writing well-organized Parquet. Each one rewards you for touching only the columns you need."
tags: ["using DuckDB"]
---

> **TL;DR:** DuckDB stores and processes data column by column, so a query that touches three columns out of fifty only reads those three. In this post, we show DuckDB features that build on this design: querying files directly, selecting and transforming columns in bulk with `EXCLUDE`, `REPLACE` and `COLUMNS()`, aggregating with `GROUP BY ALL`, `FILTER` and `PIVOT`, looking at neighboring rows with window functions and `ASOF JOIN`, and writing partitioned, sorted Parquet files that are fast to query later.

## Why Columns?

DuckDB is fast because it keeps its ducks in a column. Instead of storing each row as one record, it stores each column on its own, so a query that touches three columns out of fifty only reads those three.

That one design choice explains most of DuckDB's tricks. Columnar storage compresses well, because a column holds values of one type that often repeat. It scans fast, because the engine processes columns in vectors of 2,048 values at a time. And it rewards you for asking only for what you need.

In this post, we walk through DuckDB features that lean on that idea: lining ducks up from files, picking the right ones, counting them, letting them look at their neighbors, and keeping the pond tidy. Every example runs in the DuckDB CLI or from Python with `duckdb.sql(...)`.

```bash
# Get a duck in under a minute
pip install duckdb      # Python
brew install duckdb     # CLI on macOS
```

## Lining Up the Ducks: Querying Files Where They Sit

You don't need to load data before you query it. DuckDB treats a file path as a table and infers column names and types on the way in.

```sql
-- A CSV, sniffed automatically
SELECT * FROM 'ponds.csv' LIMIT 5;

-- A whole folder of Parquet files, with the file name as a column
SELECT filename, count(*) AS ducks
FROM read_parquet('sightings/*.parquet', filename = true)
GROUP BY filename;

-- Remote files over HTTPS or S3 (httpfs autoloads)
SELECT * FROM 's3://wetlands/2026/*.parquet';
```

Parquet is where the column story pays off most. It is columnar on disk too, so DuckDB reads only the columns your query names. It also skips whole row groups whose min/max statistics rule them out.

```sql
-- Reads two columns, skips row groups with no 2026 dates
SELECT species, count(*)
FROM 'sightings/*.parquet'
WHERE seen_at >= DATE '2026-01-01'
GROUP BY species;
```

**Tip: Check the sniffer's work.** When a CSV comes in with odd types, ask DuckDB what it guessed before you fight it.

```sql
DESCRIBE SELECT * FROM 'ponds.csv';
FROM sniff_csv('ponds.csv');

-- Then pin the types you care about
SELECT * FROM read_csv('ponds.csv', types = {'pond_id': 'VARCHAR'});
```

**Tip: Hive partitions become columns.** A path like `year=2026/month=10/` turns into `year` and `month` columns, and filters on them skip folders entirely.

```sql
SELECT count(*)
FROM read_parquet('lake/*/*/*.parquet', hive_partitioning = true)
WHERE year = 2026 AND month = 10;
```

## Picking Your Ducks: Column-Level SQL

DuckDB's [friendly SQL]({% link docs/current/sql/dialect/friendly_sql.md %}) treats columns as things you can select, drop and transform in bulk. On wide tables, this saves both typing and I/O.

**Drop or swap a few ducks with `EXCLUDE` and `REPLACE`.**

```sql
-- Everything except the noisy columns
SELECT * EXCLUDE (raw_json, internal_id) FROM sightings;

-- Everything, but with one column rewritten in place
SELECT * REPLACE (round(weight_g / 1000, 2) AS weight_g) FROM sightings;
```

**Herd ducks by name with `COLUMNS()`.** It takes a regex, a list or a lambda, and applies an expression to every match.

```sql
-- Max of every column whose name starts with temp_
SELECT max(COLUMNS('^temp_')) FROM pond_readings;

-- Null-safe cleanup across all count columns at once
SELECT coalesce(COLUMNS(c -> c LIKE '%_count'), 0) FROM counts;

-- Rename while you go: \1 is the first capture group
SELECT COLUMNS('(.*)_c') AS '\1_celsius' FROM pond_readings;
```

**Start with `FROM`.** You can lead with the table and leave `SELECT` out entirely, which reads nicely in the CLI.

```sql
FROM sightings;                       -- same as SELECT * FROM sightings
FROM sightings SELECT species, pond;  -- FROM-first with columns
```

**Nest ducks in a `STRUCT`.** A struct is a little column of columns. Unpack one with `.*` to get its fields back as top-level columns.

```sql
SELECT {'species': species, 'pond': pond} AS duck FROM sightings;
SELECT duck.* FROM (SELECT {'species': species, 'pond': pond} AS duck FROM sightings);
```

**Tip: Let DuckDB tell you about the columns.** `SUMMARIZE` profiles every column in one pass: type, min, max, approximate distinct count, null percentage and quartiles.

```sql
SUMMARIZE sightings;
SUMMARIZE SELECT * FROM 'sightings/*.parquet';
```

## Counting Ducks: Aggregation without the Boilerplate

Aggregates are where a columnar engine shines: summing one column means streaming one tightly packed array. DuckDB adds syntax so the SQL stays as short as the work.

**`GROUP BY ALL`** groups by every non-aggregated column in the `SELECT` clause, so you never repeat the list.

```sql
SELECT pond, species, count(*) AS ducks, avg(weight_g) AS avg_weight
FROM sightings
GROUP BY ALL
ORDER BY ALL;
```

**`FILTER`** counts several kinds of duck in one pass instead of one query each.

```sql
SELECT
    pond,
    count(*) FILTER (WHERE species = 'mallard')  AS mallards,
    count(*) FILTER (WHERE species = 'teal')     AS teals,
    count(*) FILTER (WHERE weight_g > 1200)      AS heavyweights
FROM sightings
GROUP BY ALL;
```

**`arg_max`** answers "which duck had the biggest X" without a self-join.

```sql
SELECT pond, arg_max(species, weight_g) AS heaviest_species, max(weight_g)
FROM sightings
GROUP BY ALL;
```

**`PIVOT` and `UNPIVOT`** turn rows into columns and back. Turning distinct values into column names is the most literal way to put ducks in a column.

```sql
-- One column per species, one row per pond
PIVOT sightings ON species USING count(*) GROUP BY pond;

-- And back again: every month column becomes rows
UNPIVOT monthly_counts
ON COLUMNS(* EXCLUDE pond)
INTO NAME month VALUE ducks;
```

**Tip: Approximate when exact is expensive.** On billions of rows, `approx_count_distinct` and `approx_quantile` use a fraction of the memory of their exact cousins.

```sql
SELECT approx_count_distinct(ring_id), approx_quantile(weight_g, 0.9)
FROM 'sightings/*.parquet';
```

## Ducks That Know Their Neighbors: Windows and ASOF Joins

A duck in a column can look up and down the line. Window functions compute over neighboring rows without collapsing them.

```sql
SELECT
    pond,
    seen_at,
    ducks,
    ducks - lag(ducks) OVER w                       AS change,
    avg(ducks) OVER (w ROWS 6 PRECEDING)            AS rolling_7
FROM daily_counts
WINDOW w AS (PARTITION BY pond ORDER BY seen_at);
```

**`QUALIFY`** filters on a window result directly, so "latest sighting per duck" needs no subquery.

```sql
SELECT *
FROM sightings
QUALIFY row_number() OVER (PARTITION BY ring_id ORDER BY seen_at DESC) = 1;
```

**`ASOF JOIN`** matches each row to the nearest earlier row in another table. It is the right tool when two time series never share exact timestamps, such as sightings and weather readings.

```sql
SELECT s.ring_id, s.seen_at, w.temp_c, w.wind_kmh
FROM sightings s
ASOF JOIN weather w
  ON s.pond = w.pond
 AND s.seen_at >= w.read_at;
```

**Tip: Lists are ducks in a column, inside a column.** `list()` gathers a group into one array, and list functions work on it without unnesting.

```sql
SELECT pond,
       list(species ORDER BY seen_at)              AS visit_order,
       list_distinct(list(species))                AS species_seen,
       len(list_distinct(list(species)))           AS variety
FROM sightings
GROUP BY ALL;
```

## Keeping the Pond Tidy: Writing Columns Well

How you write data decides how fast the next query reads it. Write Parquet, partition on the columns people filter by, and sort so similar values sit together.

```sql
-- Partitioned, compressed Parquet in one statement
COPY (SELECT * FROM sightings)
TO 'lake'
(FORMAT parquet, PARTITION_BY (year, pond), COMPRESSION zstd);
```

**Sort before you write.** Column compression loves runs of identical values. Sorting by a low-cardinality column first makes those runs long, and makes min/max statistics tight enough to skip row groups.

```sql
COPY (SELECT * FROM sightings ORDER BY pond, species, seen_at)
TO 'sightings_sorted.parquet' (FORMAT parquet, ROW_GROUP_SIZE 122_880);
```

**Pick narrow types.** A smaller type is a smaller column. Use `ENUM` for small fixed sets, `DATE` instead of `TIMESTAMP` when you don't need the time, and `SMALLINT` when counts stay small.

```sql
CREATE TYPE species_t AS ENUM ('mallard', 'teal', 'wigeon', 'pintail');
ALTER TABLE sightings ALTER species TYPE species_t;
```

**Check the plan, not your hunch.** `EXPLAIN ANALYZE` shows which columns were read, which filters were pushed into the scan, and where the time went.

```sql
EXPLAIN ANALYZE
SELECT species, count(*) FROM 'lake/**/*.parquet' WHERE pond = 'north' GROUP BY ALL;
```

**Tip: Name your columns; avoid `SELECT *` in production.** Every column you leave out is a column DuckDB never decompresses. On a 60-column table, asking for 4 can cut I/O by an order of magnitude.

**Tip: Hand ducks to Python without copying.** DuckDB queries pandas and Polars DataFrames and Arrow tables in place, and returns results in the same formats.

```python
import duckdb
import polars as pl

flock = pl.read_parquet("sightings.parquet")
duckdb.sql("SELECT pond, count(*) FROM flock GROUP BY ALL").pl()
```

## Conclusion: Ducks in a Row

Every trick above comes back to one habit: touch as few columns, and as few values in each, as the question needs.

| Trick | What it saves you |
|---|---|
| `FROM 'file.parquet'` | Loading data before querying it |
| `SELECT * EXCLUDE (...)` | Listing 40 columns to drop 2 |
| `COLUMNS('regex')` | Repeating one expression per column |
| `SUMMARIZE` | Writing a profiling query by hand |
| `GROUP BY ALL` | Keeping `SELECT` and `GROUP BY` in sync |
| `count(*) FILTER (WHERE ...)` | One query per category |
| `PIVOT` / `UNPIVOT` | Walls of `CASE` expressions |
| `QUALIFY` | Subqueries around window functions |
| `ASOF JOIN` | Fuzzy time-matching logic |
| `COPY ... PARTITION_BY` | Hand-built folder layouts |
| `ORDER BY` before `COPY` | Poor compression and unskippable row groups |
| `EXPLAIN ANALYZE` | Guessing where the time went |

Row stores line ducks up single file, one whole duck at a time. DuckDB lines them up by feature: all the bills together, all the feet together. Ask for bills, and you only wade through bills.

Keep your ducks in a column, and your queries will keep up.
