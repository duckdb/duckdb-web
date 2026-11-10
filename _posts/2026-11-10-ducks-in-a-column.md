---
layout: post
title: "Ducks in a Column"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/ducks-column.svg"
image: "/images/blog/thumbs/ducks-column.png"
excerpt: "DuckDB is fast among other reasons because it stores data by column, so a query reads only the columns it names. This post covers DuckDB features that take advantage of that design choice: querying files in place, column-level SQL, aggregation shortcuts, window functions, ASOF joins, and writing well-organized Parquet."
tag: using-duckdb
---

## Why Columns?

DuckDB stores each column separately instead of storing each row as one record. A query that touches three columns out of fifty reads only those three.

That design choice explains many of DuckDB’s performance features. Columnar storage [compresses well]({% post_url 2022-10-28-lightweight-compression %}) because a column holds values of one type, and those values often repeat. The engine processes each column in vectors of 2,048 values at a time. And a query that asks for fewer columns does less work.

The examples in this post use a sample dataset of 400 ducks, each marked with a numbered leg band (a ring) and seen at one of four ponds between October 2025 and April 2026. The `sightings` table has five columns: `ring_id`, `pond`, `species`, `weight_g`, and `seen_at`.

```sql
SELECT * FROM sightings LIMIT 3;
```

```text
┌─────────┬───────┬─────────┬──────────┬─────────────────────┐
│ ring_id │ pond  │ species │ weight_g │       seen_at       │
├─────────┼───────┼─────────┼──────────┼─────────────────────┤
│ R0001   │ south │ wigeon  │ 862      │ 2025-11-06 12:18:38 │
│ R0002   │ south │ wigeon  │ 578      │ 2025-12-04 00:12:54 │
│ R0003   │ south │ wigeon  │ 734      │ 2026-01-06 16:50:41 │
└─────────┴───────┴─────────┴──────────┴─────────────────────┘
```

Every example runs in the DuckDB CLI or from Python with `duckdb.sql(...)`.

```bash
pip install duckdb                        # Python
curl https://install.duckdb.org | bash    # CLI
```

## Querying Files in Place

You don’t need to load data before you query it. DuckDB treats a file path as a table and infers column names and types from the file.

```sql
SELECT * FROM 'ponds.csv';
```

```text
┌─────────┬───────┬─────────┐
│ pond_id │ pond  │ area_m2 │
├─────────┼───────┼─────────┤
│ 0007    │ north │ 4200    │
│ 0042    │ south │ 1800    │
│ 0113    │ mill  │ 950     │
│ 0256    │ reed  │ 3100    │
└─────────┴───────┴─────────┘
```

A glob pattern queries a whole folder of Parquet files. With `filename = true`, DuckDB adds the file name as a column:

```sql
SELECT filename, count(*) AS sightings
FROM read_parquet('sightings/*.parquet', filename = true)
GROUP BY ALL
ORDER BY ALL;
```

```text
┌────────────────────────┬───────────┐
│        filename        │ sightings │
├────────────────────────┼───────────┤
│ sightings/2025.parquet │ 184       │
│ sightings/2026.parquet │ 216       │
└────────────────────────┴───────────┘
```

DuckDB can also read remote files over [HTTPS]({% link docs/2.0/core_extensions/httpfs/https.md %}) or [S3]({% link docs/2.0/core_extensions/httpfs/s3api.md %}). The [httpfs extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) loads automatically when you use these paths:

```sql
SELECT * FROM 's3://wetlands/2026/*.parquet';
```

The [Parquet file format]({% link docs/2.0/data/parquet/overview.md %}) also stores data by column. DuckDB reads only the columns your query names. Parquet also stores min and max statistics for each row group, so DuckDB can skip row groups whose statistics rule out a filter ([zonemaps]({% link docs/2.0/guides/performance/indexing.md %}#zonemaps)).

```sql
SELECT species, count(*) AS sightings
FROM 'sightings/*.parquet'
WHERE seen_at >= DATE '2026-01-01'
GROUP BY ALL
ORDER BY ALL;
```

```text
┌─────────┬───────────┐
│ species │ sightings │
├─────────┼───────────┤
│ mallard │ 89        │
│ pintail │ 29        │
│ teal    │ 37        │
│ tufted  │ 29        │
│ wigeon  │ 32        │
└─────────┴───────────┘
```

> Tip **Check the sniffer’s work.** When a CSV loads with unexpected types, ask DuckDB what it guessed. Then pin the types you need.

```sql
DESCRIBE SELECT * FROM 'ponds.csv';
```

```text
┌─────────────┬─────────────┬──────┬──────┬─────────┬───────┐
│ column_name │ column_type │ null │ key  │ default │ extra │
├─────────────┼─────────────┼──────┼──────┼─────────┼───────┤
│ pond_id     │ VARCHAR     │ YES  │ NULL │ NULL    │ NULL  │
│ pond        │ VARCHAR     │ YES  │ NULL │ NULL    │ NULL  │
│ area_m2     │ BIGINT      │ YES  │ NULL │ NULL    │ NULL  │
└─────────────┴─────────────┴──────┴──────┴─────────┴───────┘
```

The sniffer keeps `pond_id` as text, so the leading zeros survive. To override a guess, pass the type explicitly:

```sql
SELECT * FROM read_csv('ponds.csv', types = {'area_m2': 'DOUBLE'});
```

> Tip **Hive partitions become columns.** A path like `year=2026/pond=north/` turns into `year` and `pond` columns, and filters on them skip folders entirely. The next section creates this layout.

```sql
SELECT count(*)
FROM read_parquet('lake/*/*/*.parquet', hive_partitioning = true)
WHERE year = 2026 AND pond = 'north';
```

```text
┌──────────────┐
│ count_star() │
├──────────────┤
│ 58           │
└──────────────┘
```

## Column-Level SQL

DuckDB’s [friendly SQL]({% link docs/2.0/sql/dialect/friendly_sql.md %}) lets you select, exclude, and transform columns in bulk. On wide tables, this saves typing and keeps queries readable.

**Drop columns with `EXCLUDE`, or rewrite them in place with `REPLACE`.**

```sql
SELECT * EXCLUDE (ring_id) FROM sightings LIMIT 3;
```

```text
┌───────┬─────────┬──────────┬─────────────────────┐
│ pond  │ species │ weight_g │       seen_at       │
├───────┼─────────┼──────────┼─────────────────────┤
│ south │ wigeon  │ 862      │ 2025-11-06 12:18:38 │
│ south │ wigeon  │ 578      │ 2025-12-04 00:12:54 │
│ south │ wigeon  │ 734      │ 2026-01-06 16:50:41 │
└───────┴─────────┴──────────┴─────────────────────┘
```

```sql
SELECT * REPLACE (upper(species) AS species) FROM sightings LIMIT 3;
```

```text
┌─────────┬───────┬─────────┬──────────┬─────────────────────┐
│ ring_id │ pond  │ species │ weight_g │       seen_at       │
├─────────┼───────┼─────────┼──────────┼─────────────────────┤
│ R0001   │ south │ WIGEON  │ 862      │ 2025-11-06 12:18:38 │
│ R0002   │ south │ WIGEON  │ 578      │ 2025-12-04 00:12:54 │
│ R0003   │ south │ WIGEON  │ 734      │ 2026-01-06 16:50:41 │
└─────────┴───────┴─────────┴──────────┴─────────────────────┘
```

**Select columns by pattern with `COLUMNS()`.** It takes a regular expression, a list of names, or a lambda, and applies an expression to every matching column. The `pond_readings` table has three temperature columns, so this query returns the highest reading for each:

```sql
SELECT max(COLUMNS('^temp_')) FROM pond_readings;
```

```text
┌────────────────┬─────────────┬────────────────┐
│ temp_morning_c │ temp_noon_c │ temp_evening_c │
├────────────────┼─────────────┼────────────────┤
│ 8.0            │ 13.7        │ 8.3            │
└────────────────┴─────────────┴────────────────┘
```

The same pattern handles missing values. This query replaces each `NULL` with `0` in every column whose name ends in `_count`:

```sql
SELECT coalesce(COLUMNS(lambda c: c LIKE '%_count'), 0)
FROM counts;
```

```text
┌───────────────┬────────────┬──────────────┐
│ mallard_count │ teal_count │ wigeon_count │
├───────────────┼────────────┼──────────────┤
│ 12            │ 0          │ 3            │
│ 0             │ 4          │ 1            │
│ 7             │ 2          │ 0            │
│ 0             │ 0          │ 5            │
└───────────────┴────────────┴──────────────┘
```

You can rename matching columns as you select them. In the replacement, `\1` refers to the first capture group:

```sql
SELECT COLUMNS('temp_(.*)_c') AS '\1_celsius'
FROM pond_readings
LIMIT 3;
```

```text
┌─────────────────┬──────────────┬─────────────────┐
│ morning_celsius │ noon_celsius │ evening_celsius │
├─────────────────┼──────────────┼─────────────────┤
│ 6.3             │ 9.1          │ 8.0             │
│ 6.9             │ 10.7         │ 6.6             │
│ 7.8             │ 8.8          │ 7.9             │
└─────────────────┴──────────────┴─────────────────┘
```

**Start with `FROM`.** You can lead with the table and leave out `SELECT`. `FROM sightings;` alone is the same as `SELECT * FROM sightings;`.

```sql
FROM sightings SELECT species, pond LIMIT 3;
```

```text
┌─────────┬───────┐
│ species │ pond  │
├─────────┼───────┤
│ wigeon  │ south │
│ wigeon  │ south │
│ wigeon  │ south │
└─────────┴───────┘
```

**Pack columns into a `STRUCT`.** A struct is a single column with named fields. Unpack one with `.*` to turn its fields back into top-level columns:

```sql
SELECT sighting.* FROM (
    SELECT {'species': species, 'pond': pond} AS sighting FROM sightings
)
LIMIT 3;
```

```text
┌─────────┬───────┐
│ species │ pond  │
├─────────┼───────┤
│ wigeon  │ south │
│ wigeon  │ south │
│ wigeon  │ south │
└─────────┴───────┘
```

> Tip **Let DuckDB profile the columns.** `SUMMARIZE` returns one row per column, with its type, min, max, approximate distinct count, null percentage, and quartiles.

```sql
SUMMARIZE sightings;
SUMMARIZE SELECT * FROM 'sightings/*.parquet';
```

## Aggregation Shortcuts

Aggregates benefit from columnar storage because summing a column means scanning one column of values. DuckDB adds syntax that keeps the SQL as short as the work.

**[`GROUP BY ALL`]({% link docs/2.0/sql/query_syntax/groupby.md %}#group-by-all) groups by every non-aggregated column in the `SELECT` clause, so you don’t repeat the list.**

```sql
SELECT pond, species, count(*) AS sightings, round(avg(weight_g)) AS avg_weight_g
FROM sightings
GROUP BY ALL
ORDER BY ALL
LIMIT 5;
```

```text
┌──────┬─────────┬───────────┬──────────────┐
│ pond │ species │ sightings │ avg_weight_g │
├──────┼─────────┼───────────┼──────────────┤
│ mill │ mallard │ 46        │ 1110.0       │
│ mill │ pintail │ 11        │ 910.0        │
│ mill │ teal    │ 15        │ 352.0        │
│ mill │ tufted  │ 10        │ 879.0        │
│ mill │ wigeon  │ 14        │ 720.0        │
└──────┴─────────┴───────────┴──────────────┘
```

**`FILTER` counts several categories in one pass,** instead of running one query per category:

```sql
SELECT
    pond,
    count(*) FILTER (WHERE species = 'mallard') AS mallards,
    count(*) FILTER (WHERE species = 'teal')    AS teals,
    count(*) FILTER (WHERE weight_g > 1200)     AS heavyweights
FROM sightings
GROUP BY ALL
ORDER BY ALL;
```

```text
┌───────┬──────────┬───────┬──────────────┐
│ pond  │ mallards │ teals │ heavyweights │
├───────┼──────────┼───────┼──────────────┤
│ mill  │ 46       │ 15    │ 16           │
│ north │ 48       │ 17    │ 12           │
│ reed  │ 26       │ 14    │ 6            │
│ south │ 48       │ 19    │ 16           │
└───────┴──────────┴───────┴──────────────┘
```

**`arg_max` returns the value from the row with the largest value of another column,** so you don’t need a self-join. Here it finds the species of the heaviest bird at each pond:

```sql
SELECT pond,
       arg_max(species, weight_g) AS heaviest_species,
       max(weight_g) AS max_weight_g
FROM sightings
GROUP BY ALL
ORDER BY ALL;
```

```text
┌───────┬──────────────────┬──────────────┐
│ pond  │ heaviest_species │ max_weight_g │
├───────┼──────────────────┼──────────────┤
│ mill  │ mallard          │ 1358         │
│ north │ mallard          │ 1359         │
│ reed  │ mallard          │ 1312         │
│ south │ mallard          │ 1357         │
└───────┴──────────────────┴──────────────┘
```

**`PIVOT` and `UNPIVOT` turn rows into columns and back.** `PIVOT` makes one column per distinct value, here one column per species:

```sql
PIVOT sightings ON species USING count(*) GROUP BY pond ORDER BY pond;
```

```text
┌───────┬─────────┬─────────┬──────┬────────┬────────┐
│ pond  │ mallard │ pintail │ teal │ tufted │ wigeon │
├───────┼─────────┼─────────┼──────┼────────┼────────┤
│ mill  │ 46      │ 11      │ 15   │ 10     │ 14     │
│ north │ 48      │ 19      │ 17   │ 16     │ 17     │
│ reed  │ 26      │ 11      │ 14   │ 13     │ 16     │
│ south │ 48      │ 11      │ 19   │ 14     │ 15     │
└───────┴─────────┴─────────┴──────┴────────┴────────┘
```

`UNPIVOT` goes the other way. The `monthly_counts` table has one column per month, so this query turns those columns back into rows:

```sql
SELECT * FROM (
    UNPIVOT monthly_counts
    ON COLUMNS(* EXCLUDE pond)
    INTO NAME month VALUE sightings
)
WHERE pond = 'north';
```

```text
┌───────┬───────┬───────────┐
│ pond  │ month │ sightings │
├───────┼───────┼───────────┤
│ north │ Apr   │ 6         │
│ north │ Dec   │ 18        │
│ north │ Feb   │ 14        │
│ north │ Jan   │ 21        │
│ north │ Mar   │ 17        │
│ north │ Nov   │ 20        │
│ north │ Oct   │ 21        │
└───────┴───────┴───────────┘
```

> Tip **Approximate when exact is expensive.** On billions of rows, `approx_count_distinct` and `approx_quantile` use a fraction of the memory of their exact counterparts. On this small table, the estimate of 404 distinct rings is close to the exact count of 400.

```sql
SELECT approx_count_distinct(ring_id), approx_quantile(weight_g, 0.9)
FROM sightings;
```

```text
┌────────────────────────────────┬────────────────────────────────┐
│ approx_count_distinct(ring_id) │ approx_quantile(weight_g, 0.9) │
├────────────────────────────────┼────────────────────────────────┤
│ 404                            │ 1236                           │
└────────────────────────────────┴────────────────────────────────┘
```

## Window Functions and ASOF Joins

Window functions compute over neighboring rows without collapsing them. The `daily_counts` table has one row per pond per day, including days with no sightings. This query shows the day-over-day change and a rolling seven-day average:

```sql
SELECT
    pond,
    seen_at,
    ducks,
    ducks - lag(ducks) OVER w                       AS change,
    round(avg(ducks) OVER (w ROWS 6 PRECEDING), 2) AS rolling_7
FROM daily_counts
WINDOW w AS (PARTITION BY pond ORDER BY seen_at)
ORDER BY pond, seen_at
LIMIT 8;
```

```text
┌──────┬────────────┬───────┬────────┬───────────┐
│ pond │  seen_at   │ ducks │ change │ rolling_7 │
├──────┼────────────┼───────┼────────┼───────────┤
│ mill │ 2025-10-01 │ 0     │ NULL   │ 0.0       │
│ mill │ 2025-10-02 │ 0     │ 0      │ 0.0       │
│ mill │ 2025-10-03 │ 0     │ 0      │ 0.0       │
│ mill │ 2025-10-04 │ 1     │ 1      │ 0.25      │
│ mill │ 2025-10-05 │ 0     │ -1     │ 0.2       │
│ mill │ 2025-10-06 │ 0     │ 0      │ 0.17      │
│ mill │ 2025-10-07 │ 0     │ 0      │ 0.14      │
│ mill │ 2025-10-08 │ 2     │ 2      │ 0.43      │
└──────┴────────────┴───────┴────────┴───────────┘
```

**`QUALIFY` filters on a window function directly,** so finding the latest sighting at each pond doesn’t need a subquery:

```sql
SELECT pond, ring_id, species, seen_at
FROM sightings
QUALIFY row_number() OVER (PARTITION BY pond ORDER BY seen_at DESC) = 1
ORDER BY pond;
```

```text
┌───────┬─────────┬─────────┬─────────────────────┐
│ pond  │ ring_id │ species │       seen_at       │
├───────┼─────────┼─────────┼─────────────────────┤
│ mill  │ R0015   │ mallard │ 2026-04-18 18:17:29 │
│ north │ R0077   │ mallard │ 2026-04-14 09:02:03 │
│ reed  │ R0044   │ teal    │ 2026-04-18 21:44:23 │
│ south │ R0045   │ wigeon  │ 2026-04-11 16:29:40 │
└───────┴─────────┴─────────┴─────────────────────┘
```

**[`ASOF JOIN`]({% post_url 2023-09-15-asof-joins-fuzzy-temporal-lookups %}) matches each row to the nearest earlier row in another table.** It’s the right tool when two time series never share exact timestamps, such as sightings and weather readings. The `weather` table has a reading every six hours at each pond. This query attaches the most recent reading to each sighting:

```sql
SELECT s.ring_id, s.seen_at, w.temp_c, w.wind_kmh
FROM sightings s
ASOF JOIN weather w
  ON s.pond = w.pond
 AND s.seen_at >= w.read_at
ORDER BY s.seen_at
LIMIT 5;
```

```text
┌─────────┬─────────────────────┬────────┬──────────┐
│ ring_id │       seen_at       │ temp_c │ wind_kmh │
├─────────┼─────────────────────┼────────┼──────────┤
│ R0096   │ 2025-10-01 03:52:49 │ 10.1   │ 20.0     │
│ R0109   │ 2025-10-01 09:11:24 │ 9.3    │ 33.3     │
│ R0215   │ 2025-10-01 10:59:02 │ 9.2    │ 31.8     │
│ R0315   │ 2025-10-01 20:44:16 │ 10.4   │ 26.4     │
│ R0076   │ 2025-10-01 21:17:05 │ 10.4   │ 26.4     │
└─────────┴─────────────────────┴────────┴──────────┘
```

> Tip **Lists stay in one column.** `list()` gathers a group into a single array value, and list functions work on that array without unnesting it.

```sql
SELECT pond,
       list(ring_id ORDER BY seen_at)[1:3] AS first_three_rings,
       len(list(ring_id))                  AS sightings
FROM sightings
GROUP BY ALL
ORDER BY ALL;
```

```text
┌───────┬───────────────────────┬───────────┐
│ pond  │   first_three_rings   │ sightings │
├───────┼───────────────────────┼───────────┤
│ mill  │ [R0125, R0127, R0122] │ 96        │
│ north │ [R0096, R0160, R0180] │ 117       │
│ reed  │ [R0109, R0323, R0312] │ 80        │
│ south │ [R0215, R0315, R0076] │ 107       │
└───────┴───────────────────────┴───────────┘
```

## Writing Columns Well

How you write data determines how fast later queries can read it. Write Parquet, partition on the columns people filter by, and sort so that similar values sit together.

This query writes the sightings to folders such as `lake/year=2026/pond=north/`, with compressed Parquet files in each:

```sql
COPY (SELECT *, year(seen_at) AS year FROM sightings)
TO 'lake'
(FORMAT parquet, PARTITION_BY (year, pond), COMPRESSION zstd);
```

**Sort before you write.** Compression works best on runs of identical values. Sorting by low-cardinality columns first makes those runs longer, and it makes the min and max statistics tighter, so more row groups can be skipped.

```sql
COPY (SELECT * FROM sightings ORDER BY pond, species, seen_at)
TO 'sightings_sorted.parquet' (FORMAT parquet, ROW_GROUP_SIZE 122_880);
```

**Pick narrow types.** A smaller type takes less space. Use `ENUM` for small fixed sets, `DATE` instead of `TIMESTAMP` when you don’t need the time, and `SMALLINT` when values stay small. Here, `species` has only five possible values, so it becomes an `ENUM`:

```sql
CREATE TYPE species_t AS ENUM ('mallard', 'teal', 'wigeon', 'pintail', 'tufted');
ALTER TABLE sightings ALTER species TYPE species_t;
```

**Check the plan rather than guessing.** `EXPLAIN ANALYZE` shows which columns were read, which filters were pushed into the scan, and where the time went:

```sql
EXPLAIN ANALYZE
SELECT species, count(*) FROM 'lake/**/*.parquet' WHERE pond = 'north' GROUP BY ALL;
```

The part of the output that matters here is the table scan. DuckDB scans 2 of the 8 files, because `pond` is a partition column, and it reads only the `species` column:

```text
Table Scan
  Function: PARQUET_SCAN
  Projections: species
  File Filters: pond = 'north'
  Scanning Files: 2/8
  Total Files Read: 2
```

> Tip **Name your columns, and avoid `SELECT *` in production.** Every column you leave out is one DuckDB never decompresses. On a 60-column table, selecting 4 columns can cut the data read dramatically.

**Query DataFrames in place.** DuckDB queries pandas and Polars DataFrames and Arrow tables directly, and it returns results in the same formats. Converting a result to Polars goes through Arrow, so install `pyarrow` as well.

```python
import duckdb
import polars as pl

sightings = pl.read_parquet("sightings/2026.parquet")
duckdb.sql("SELECT pond, count(*) AS sightings FROM sightings GROUP BY ALL ORDER BY ALL").pl()
```

```text
shape: (4, 2)
┌───────┬───────────┐
│ pond  ┆ sightings │
│ ---   ┆ ---       │
│ str   ┆ i64       │
╞═══════╪═══════════╡
│ mill  ┆ 54        │
│ north ┆ 58        │
│ reed  ┆ 48        │
│ south ┆ 56        │
└───────┴───────────┘
```

## Conclusion

Each feature in this post follows one rule: read only the columns and values your query needs. This table summarizes the tricks:

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

Row stores, such as transactional database systems, keep each record together. That suits lookups of one whole record. Analytical queries usually need the opposite: a few columns across many records. Keep your ducks in a column, and your queries will keep up.
