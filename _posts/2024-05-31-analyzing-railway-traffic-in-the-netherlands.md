---
layout: post
title: "Analyzing Railway Traffic in the Netherlands"
author: Gabor Szarnyas
excerpt: "We use real-world railway data to demonstrate some of DuckDB's capabilities, including support for temporal and spatial queries."
---

## Introduction

The Netherlands, the birthplace of DuckDB, is a small country of about 42,000 km2. It has a [dense railway network](https://en.wikipedia.org/wiki/Rail_transport_in_the_Netherlands) that consists of 3,223 km of tracks and 397 stations.

Information about this network, including its schedule, fares and stations, is available as an [open data set](https://www.rijdendetreinen.nl/en/open-data/). This high-quality data set is maintained by the team behind the [Rijden de Treinen _(Are the trains running?)_ application](https://www.ijdendetreinen.nl/en/about).

In this post, we'll demonstrate some of DuckDB's analytical features on the Dutch railway network data set. Unlike most of our other blog posts, this one does introduce a new feature or release: instead, it demonstrates several existing features using a single domain. Some of the queries explained in this blog post are shown in simplified form on [DuckDB's landing page](/).

## Loading the Data

<!--
    core features used: CSV reader
    extensions used: httpfs
-->

For most queries, we'll use the 2023 railway schedule. To get this data set, download the [`services-2023.csv.gz` file](https://blobs.duckdb.org/data/nl-railway/services-2023.csv.gz) (330 MB) and load it to DuckDB as the `services` table:

```bash
duckdb railway.db
```

```sql
CREATE TABLE services AS
    FROM 'services-2023.csv.gz';
```

This query runs the CSV loader, which automatically decompresses the file and infers its schema from its content using the [CSV sniffer](/docs/data/csv/auto_detection).
The query also makes use of DuckDB's [`FROM`-first syntax](/docs/sql/query_syntax/from#from-first-syntax), which allows users to omit the `SELECT *` clause.
Using [DuckDB v0.10.3](/docs/installation), loading the data set from a local disk takes approximately 5 seconds on an M2 MacBook Pro.

To check the amount of data loaded, we can run the following query which [pretty-prints](/docs/sql/functions/char#print-numbers-with-thousand-separators) the number of rows:

```sql
SELECT format('{:,}', count(*)) AS num_services
FROM services;
```

| num_services |
|--------------|
| 21,239,393   |

We can see that more than 21 million train services ran in the Netherlands in 2023.

<!-- DuckDB also allows [loading via the HTTPS protocol](/docs/extensions/httpfs/https). This only requires changing the `FROM` clause:

```sql
CREATE TABLE services AS
    FROM 'https://blobs.duckdb.org/data/nl-railway/services-2023.csv.gz';
``` -->

## Finding the Busiest Stations

<!--
    core features used: GROUP BY ALL
    extensions used: -
-->

Let's ask a simple query first: _What were the top-3 busiest railway stations in the Netherlands in May 2023?_

Answering this query requires a group-by aggregation followed by an order-by and a limit. We use the [`GROUP BY ALL` feature](/docs/sql/query_syntax/groupby#group-by-all) to avoid repeating all non-aggregated column names in both the `SELECT` and the `GROUP BY` clauses.

```sql
SELECT "Stop:station name" AS station, count(*) AS num_services
FROM services
WHERE month("Service:Date") = 5
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 3;
```

|      station       | num_services |
|--------------------|-------------:|
| Utrecht Centraal   | 35383        |
| Amsterdam Centraal | 33725        |
| Schiphol Airport   | 24303        |

Maybe surprisingly, the busiest railway station is not in Amsterdam but in the country's 4th largest city, [Utrecht](https://en.wikipedia.org/wiki/Utrecht), thanks to its central location.

### Directly Querying through S3

<!--
    core features used: GROUP BY ALL
    extensions used: httpfs, parquet
-->

DuckDB supports directly querying files via [the HTTP(S) protocol and the S3 API](/docs/extensions/httpfs).
For example, we can directly run the previous query on a Parquet file stored in an S3 bucket by only changing the `FROM` clause:

```sql
SELECT "Stop:station name" AS station, count(*) AS num_services
FROM 's3://duckdb-blobs/data/nl-railway/services-2023.parquet'
WHERE month("Service:Date") = 5
GROUP BY ALL
ORDER BY num_services DESC
LIMIT 3;
```

Note that DuckDB doesn't need to download the whole file for evaluating the query: it only uses about 13% of the files size as network traffic as it limits the reads to the required columns and filters the rows using [zonemaps](/docs/guides/performance/indexing#zonemaps).

## Temporal Queries



### Window Function

### AsOf Join



## Unpivot

<!--
    core features used: UNPIVOT, COLUMNS expression
    extensions used: -
-->

[Pivot](/docs/sql/statements/pivot) statement

```sql
CREATE OR REPLACE TABLE station AS
    FROM read_csv('stations-2022-01.csv');

CREATE OR REPLACE TABLE tariffs AS
    FROM read_csv('tariff-distances-2022-01.csv', header=true, nullstr='XXX');

CREATE OR REPLACE TABLE tariffs AS
    UNPIVOT tariffs
    ON COLUMNS (* EXCLUDE Station)
    INTO NAME OtherStation VALUE Price;

SELECT s1.name_short, s2.name_short, tariffs.Price
    FROM tariffs
    JOIN station s1 ON s1.country = 'NL' AND tariffs.Station = s1.code
    JOIN station s2 ON s2.country = 'NL' AND tariffs.OtherStation = s2.code
    WHERE Station < OtherStation
    ORDER BY Price DESC
    LIMIT 5;
```

## Weather

<!--
    core features used: as-of joins
    extensions used: httpfs, parquet
-->

## Spatial

<!--
    core features used: ...
    extensions used: spatial
-->

## Conclusion

We demonstrated some of DuckDB's key feaures, including
[automatic detection of CSV files](/2023/10/27/csv-sniffer),
[friendly SQL features](/2023/08/23/even-friendlier-sql),
[direct Parquet querying](/2021/06/25/querying-parquet),
[AsOf joins](/2023/09/15/asof-joins-fuzzy-temporal-lookups),
[window functions](/2021/10/13/windowing),
and the
[spatial extension](/2023/04/28/spatial).
The combination of these allow consise formulation of queries using different file formats (CSV, Parquet), data sources (local, HTTPS, S3), and types (datetime, geospatial).
The performance of DuckDB allows interactive analysis: all queries in the blogpost complete in less than XX seconds.
