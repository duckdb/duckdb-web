---
layout: post
title: "Analyzing Railway Traffic in the Netherlands"
author: Gabor Szarnyas
excerpt: "We use a real-world railway data set to demonstrate some of DuckDB's key features, including querying different file formats, connecting to remote endpoints, and using advanced SQL features."
---

## Introduction

The Netherlands, the birthplace of DuckDB, is a small country with an area of about 42,000&nbsp;km².
It has a [dense railway network](https://en.wikipedia.org/wiki/Rail_transport_in_the_Netherlands), which consists of 3,223 km of tracks and 397 stations.

Information about this network, including its schedule, distances and stations, is available as an [open data set](https://www.rijdendetreinen.nl/en/open-data/).
This high-quality data set is maintained by the team behind the [Rijden de Treinen _(Are the trains running?)_ application](https://www.ijdendetreinen.nl/en/about).

In this post, we'll demonstrate some of DuckDB's analytical features on the Dutch railway network data set.
Unlike most of our other blog posts, this one does introduce a new feature or release: instead, it demonstrates several existing features using a single domain.
Some of the queries explained in this blog post are shown in simplified form on [DuckDB's landing page](/).

## Loading the Data

<!--
    core features used: CSV reader, CTAS, aggregration
    demonstrated friendly features: FROM-first syntax, format pretty-printer
    extensions used: -
-->

For our initial queries, we'll use the 2023 railway schedule.
To get this data set, download the [`services-2023.csv.gz` file](https://blobs.duckdb.org/data/nl-railway/services-2023.csv.gz) (330 MB) and load it to DuckDB.

First, start the [DuckDB command line client](/docs/api/cli/overview) on a persistent database:

```bash
duckdb railway.db
```

Then, load the `services-2023.csv.gz` file into the `services` table.

```sql
CREATE TABLE services AS
    FROM 'services-2023.csv.gz';
```

Despite the seemingly simple query, there is quite a lot going on. Let's deconstruct it:

* First, note that there is no need to explicitly use a [`COPY ... FROM` statement](/docs/sql/statements/copy#copy--from) or to call the [`read_csv()` method](/docs/data/csv/overview#csv-functions):
the CSV reader is invoked because we passed a string in the `FROM` clause, which ends in `.csv.gz`.
DuckDB automatically detects that this is a gzip-compressed CSV file, so it decompresses it and infers its schema from its content using the [CSV sniffer](/docs/data/csv/auto_detection).
The result produced by the CSV reader is treated as a table, which we use in the `FROM` clause.

* Second, the query makes use of DuckDB's [`FROM`-first syntax](/docs/sql/query_syntax/from#from-first-syntax), which allows users to omit the `SELECT *` clause.
The SQL statement `FROM 'services-2023.csv.gz';` is equivalent to `SELECT * FROM 'services-2023.csv.gz';`.

* Third, the query creates a table called `services` and populates it with the result from the CSV reader. This is achieved by using the [`CREATE TABLE ... AS` construct](/docs/sql/statements/create_table#create-table--as-select-ctas).

Using [DuckDB v0.10.3](/docs/installation), loading the data set takes approximately 5&nbsp;seconds on an M2 MacBook Pro. To check the amount of data loaded, we can run the following query which [pretty-prints](/docs/sql/functions/char#print-numbers-with-thousand-separators) the number of rows in the `services` table:

```sql
SELECT format('{:,}', count(*)) AS num_services
FROM services;
```

| num_services |
|-------------:|
| 21,239,393   |

We can see that more than 21&nbsp;million train services ran in the Netherlands in 2023.

## Finding the Busiest Station per Month

<!--
    core features used: GROUP BY ALL
    extensions used: -
-->

Let's ask a simple query first: _What were the busiest railway stations in the Netherlands in the first 6 months of 2023?_

First, let's compute the number of services passing through each station for every month.
To do so, we extract the month from the service's date, then performs a group-by aggregation with a `count(*)`:

```sql
SELECT
    month("Service:Date") AS month,
    "Stop:station name" AS station,
    count(*) AS num_services
FROM services
GROUP BY month, station
LIMIT 5;
```

Note that this query showcases a common redundancy in SQL: we list the names of non-aggregated columns in both the `SELECT` and the `GROUP BY` clauses.
Using DuckDB's [`GROUP BY ALL` feature](/docs/sql/query_syntax/groupby#group-by-all), we can eliminate this.
At the same time, let's also turn this result into an intermediate table called `services_per_month` using the `CREATE TABLE ...  AS` construct:

```sql
CREATE TABLE services_per_month AS
    SELECT
        month("Service:Date") AS month,
        "Stop:station name" AS station,
        count(*) AS num_services
    FROM services
    GROUP BY ALL;
```

To answer the question, we can use the [`arg_max(arg, val)` aggregation function](/docs/sql/aggregates#arg_maxarg-val), which returns a column `arg` in the row with the maximum value `val`.
We filter on the month and return the results:

```sql
SELECT
    month,
    arg_max(station, num_services) AS station,
    max(num_services) AS num_services
FROM services_per_month
WHERE month <= 6
GROUP BY month;
```

| month |      station       | num_services |
|------:|--------------------|-------------:|
| 1     | Utrecht Centraal   | 34760        |
| 2     | Utrecht Centraal   | 32300        |
| 3     | Utrecht Centraal   | 37386        |
| 4     | Amsterdam Centraal | 33426        |
| 5     | Utrecht Centraal   | 35383        |
| 6     | Utrecht Centraal   | 35632        |

Maybe surprisingly, in most months, the busiest railway station is not in Amsterdam but in the country's 4th largest city, [Utrecht](https://en.wikipedia.org/wiki/Utrecht), thanks to its central geographic location.

## Finding the Top-3 Busiest Stations for Each Summer Month

Let's change the question to: _Which are the top-3 busiest stations for each summer month?_
The `arg_max()` function only helps us find the top-1 value but it is not sufficient for finding top-k results.
Luckily, DuckDB has extensive support for SQL features, including [window functions](/docs/sql/window_functions) and we can use the [`rank()` function](/docs/sql/window_functions#rank) to find top-k values:

```sql
SELECT month, month_name, array_agg(station) AS top3_stations
FROM (
    SELECT
        month,
        strftime(make_date(2023, month, 1), '%B') AS month_name,
        rank() OVER
            (PARTITION BY month ORDER BY num_services DESC) AS rank,
        station,
        num_services
    FROM services_per_month
    WHERE month BETWEEN 6 AND 8
)
WHERE rank <= 3
GROUP BY ALL
ORDER BY month;
```

This gives the following result:

| month | month_name |                        top3_stations                         |
|------:|------------|--------------------------------------------------------------|
| 6     | June       | [Utrecht Centraal, Amsterdam Centraal, Schiphol Airport]     |
| 7     | July       | [Utrecht Centraal, Amsterdam Centraal, Schiphol Airport]     |
| 8     | August     | [Utrecht Centraal, Amsterdam Centraal, Amsterdam Sloterdijk] |

We can see that the top-3 spots are shared between four stations: Utrecht Centraal, Amsterdam Centraal, Schiphol Airport, and Amsterdam Sloterdijk.

### Directly Querying Parquet Files through HTTPS or S3

<!--
    core features used: GROUP BY ALL
    extensions used: httpfs, parquet
-->

DuckDB supports directly querying files, including CSV and Parquet, via [the HTTP(S) protocol and the S3 API](/docs/extensions/httpfs).
For example, we can run the following query:

```sql
SELECT "Service:Date", "Stop:station name"
FROM 'https://blobs.duckdb.org/data/services-2023.parquet'
LIMIT 3;
```

It returns the following result:

| Service:Date | Stop:Station name  |
|--------------|--------------------|
| 2023-01-01   | Rotterdam Centraal |
| 2023-01-01   | Delft              |
| 2023-01-01   | Den Haag HS        |

> For querying private S3 buckets, you can use DuckDB's [Secrets Manager](/docs/extensions/httpfs/s3api#configuration-and-authentication) to authenticate.

Using the remote Parquet file, the query for answering [_Which are the top-3 busiest stations for each summer month?_](#finding-the-top-3-busiest-stations-for-each-summer-month) can be run directly on a remote Parquet file without creating any local tables.
To do this, we can define the `services_per_month` table as a [common table expression in the `WITH` clause](/docs/sql/query_syntax/with).
The rest of the query remains the same:

```sql
WITH services_per_month AS (
    SELECT
        month("Service:Date") AS month,
        "Stop:station name" AS station,
        count(*) AS num_services
    FROM 'https://blobs.duckdb.org/data/services-2023.parquet'
    GROUP BY ALL
)
SELECT month, month_name, array_agg(station) AS top3_stations
FROM (
    SELECT
        month,
        strftime(make_date(2023, month, 1), '%B') AS month_name,
        rank() OVER
            (PARTITION BY month ORDER BY num_services DESC) AS rank,
        station,
        num_services
    FROM services_per_month
    WHERE month BETWEEN 6 AND 8
)
WHERE rank <= 3
GROUP BY ALL
ORDER BY month;
```

This query yields the same result as the query above, and completes (depending on the network speed) in about 1–2 seconds.
This speed is possible because DuckDB doesn't need to download the whole Parquet file for evaluating the query:
while the file size is 309&nbsp;MB, it only uses about 20&nbsp;MB of network traffic, approximately 6% of the total file size.
This is thanks to two factors:
Parquet's columnar layout, which allows the reader to only access the required columns,
and
the [zonemaps](/docs/guides/performance/indexing#zonemaps) in Parquet's metadata,
which allow the filter pushdown optimization (e.g., the reader only fetches [row groups](/docs/internals/storage#row-groups) with dates in the summer months).
Both of these optimizations are implemented via [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests),
saving considerable traffic and time when running queries on remote Parquet files.

## Largest Distance between Train Stations in the Netherlands

<!--
    core features used: UNPIVOT, COLUMNS expression
    extensions used: -
-->

Let's answer the following question: _Which two train stations in the Netherlands have the largest distance between them when traveling via rail?_
For this, we'll use two data sets.
The first, [`stations-2022-01.csv`](https://opendata.rijdendetreinen.nl/public/stations/stations-2022-01.csv), contains information on the [railway stations](https://www.rijdendetreinen.nl/en/open-data/stations) (name, country, etc.).

We can simply load and query this data set as follows:

```sql
CREATE TABLE stations AS
    FROM 'https://blobs.duckdb.org/data/stations-2022-01.csv';

SELECT
    id,
    name_short,
    name_long,
    country,
    printf('%.2f', geo_lat) AS latitude,
    printf('%.2f', geo_lng) AS longitude
FROM stations
LIMIT 5;
```

| id  | name_short |       name_long       | country | latitude | longitude |
|----:|------------|-----------------------|---------|----------|-----------|
| 266 | Den Bosch  | 's-Hertogenbosch      | NL      | 51.69    | 5.29      |
| 269 | Dn Bosch O | 's-Hertogenbosch Oost | NL      | 51.70    | 5.32      |
| 227 | 't Harde   | 't Harde              | NL      | 52.41    | 5.89      |
| 8   | Aachen     | Aachen Hbf            | D       | 50.77    | 6.09      |
| 818 | Aachen W   | Aachen West           | D       | 50.78    | 6.07      |

The second data set, [`tariff-distances-2022-01.csv`](https://opendata.rijdendetreinen.nl/public/tariff-distances/tariff-distances-2022-01.csv), contains the [station distances](https://www.rijdendetreinen.nl/en/open-data/station-distances). The distances are defined as the shortest route on the railway network and they are used to calculate the tariffs for tickets.
Let's peek into this file:

```bash
head -n 9 tariff-distances-2022-01.csv | cut -d, -f1-9
```

```csv
Station,AC,AH,AHP,AHPR,AHZ,AKL,AKM,ALM
AC,XXX,82,83,85,90,71,188,32
AH,82,XXX,1,3,8,77,153,98
AHP,83,1,XXX,2,9,78,152,99
AHPR,85,3,2,XXX,11,80,150,101
AHZ,90,8,9,11,XXX,69,161,106
AKL,71,77,78,80,69,XXX,211,96
AKM,188,153,152,150,161,211,XXX,158
ALM,32,98,99,101,106,96,158,XXX
```

We can see that the distances are encoded as a matrix with the diagonal entries set to `XXX`.
As explained in the [data set's description](https://www.rijdendetreinen.nl/en/open-data/station-distances#description), this string implies that the two stations are the same station.
If we just load the values as `XXX`, the CSV reader will assume that all columns have the type `VARCHAR` instead of numeric values.
While this can be cleaned up later, it's a lot easier to avoid this problem altogether.
To do so, we use the `read_csv` function and set the [`nullstr` parameter](/docs/data/csv/overview#parameters) to `XXX`:

```sql
CREATE TABLE distances AS
    FROM read_csv('https://blobs.duckdb.org/data/tariff-distances-2022-01.csv', nullstr = 'XXX');
```

To make the `NULL` values visible in the command line output, we set the [`.nullvalue` dot command](/docs/api/cli/dot_commands) to `NULL`:

```sql
.nullvalue NULL
```

Using the [`DESCRIBE` statement](/docs/guides/meta/describe), we can confirm that DuckDB has inferred by column types correctly as `BIGINT`:

```sql
FROM (DESCRIBE distances)
LIMIT 5;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| Station     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| AC          | BIGINT      | YES  | NULL | NULL    | NULL  |
| AH          | BIGINT      | YES  | NULL | NULL    | NULL  |
| AHP         | BIGINT      | YES  | NULL | NULL    | NULL  |
| AHPR        | BIGINT      | YES  | NULL | NULL    | NULL  |

To show the first 9 columns, we can run the following query with the [`#1`, `#2`, etc. column indexes in the `SELECT` statement](/docs/sql/statements/select):

```sql
SELECT #1, #2, #3, #4, #5, #6, #7, #8, #9
FROM distances
LIMIT 8;
```

| Station |  AC  |  AH  | AHP  | AHPR | AHZ  | AKL  | AKM  | ALM  |
|---------|------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| AC      | NULL | 82   | 83   | 85   | 90   | 71   | 188  | 32   |
| AH      | 82   | NULL | 1    | 3    | 8    | 77   | 153  | 98   |
| AHP     | 83   | 1    | NULL | 2    | 9    | 78   | 152  | 99   |
| AHPR    | 85   | 3    | 2    | NULL | 11   | 80   | 150  | 101  |
| AHZ     | 90   | 8    | 9    | 11   | NULL | 69   | 161  | 106  |
| AKL     | 71   | 77   | 78   | 80   | 69   | NULL | 211  | 96   |
| AKM     | 188  | 153  | 152  | 150  | 161  | 211  | NULL | 158  |
| ALM     | 32   | 98   | 99   | 101  | 106  | 96   | 158  | NULL |

We can see that the data was loaded correctly but the wide table format is a bit unwieldy for further processing:
to query for pairs of stations, we need to turn it into a long table using the [`UNPIVOT`](/docs/sql/statements/unpivot) statement.
Naïvely, we would write something like the following:

```sql
CREATE TABLE distances_long AS
    UNPIVOT distances
    ON AC, AH, AHP, ...
```

We have almost 400 stations, so spelling out their names would be quite tedious.
Fortunately, DuckDB has a trick to help with this:
the [`COLUMNS(*)` expression](/docs/sql/expressions/star#columns-expression) lists all columns
and its optional `EXCLUDE` clause can remove given column names from the list.
Therefore, the expression `COLUMNS(* EXCLUDE station)` lists all column names except `station`, precisely what we need in the `UNPIVOT` command:

```sql
CREATE TABLE distances_long AS
    UNPIVOT distances
    ON COLUMNS (* EXCLUDE station)
    INTO NAME other_station VALUE distance;
```

This results in the following table:

```sql
FROM distances_long
LIMIT 5;
```

| Station | other_station | price |
|---------|---------------|------:|
| AC      | AH            | 82    |
| AC      | AHP           | 83    |
| AC      | AHPR          | 85    |
| AC      | AHZ           | 90    |
| AC      | AKL           | 71    |

Now we can join the `distances_long` table on the `stations` table along both the start and end stations,
then filter to stations which are located in the Netherlands.
We introduce symmetry breaking (`station < other_station`) to ensure that the same pair only occurs once in the output.
Finally, select the top-3 results:

```sql
SELECT
    s1.name_long AS station1,
    s2.name_long AS station2,
    distances_long.distance
FROM distances_long
JOIN stations s1 ON distances_long.station = s1.code
JOIN stations s2 ON distances_long.other_station = s2.code
WHERE s1.country = 'NL'
  AND s2.country = 'NL'
  AND station < other_station
ORDER BY distance DESC
LIMIT 3;
```

The results show that there are pairs of train stations, which are more than 400 km apart via railway.

|     station1     |      station2      | distance |
|------------------|--------------------|---------:|
| Eemshaven        | Vlissingen         | 426      |
| Eemshaven        | Vlissingen Souburg | 425      |
| Bad Nieuweschans | Vlissingen         | 425      |

## Conclusion

In this post, we demonstrated some of DuckDB's key feaures,
including
automatic detection of file formats,
[auto-inferencing the schema of CSV files](/2023/10/27/csv-sniffer),
[several friendly SQL features](/2023/08/23/even-friendlier-sql) (`FROM`-first syntax, `GROUP BY ALL`, `COLUMNS`),
[direct Parquet querying](/2021/06/25/querying-parquet),
[window functions](/2021/10/13/windowing),
[unpivot](/docs/sql/statements/unpivot),
and so on.
The combination of these allow consise formulation of queries using different file formats (CSV, Parquet) and data sources (local, HTTPS, S3).
In the next installment, we'll take a look at
temporal data using [AsOf joins](/2023/09/15/asof-joins-fuzzy-temporal-lookups)
and
geospatial data using the DuckDB [`spatial` extension](/2023/04/28/spatial).
