---
layout: post
title: "DuckDB Tricks – Part 3"
author: "Andra Ionescu, Gabor Szarnyas"
thumb: "/images/blog/thumbs/duckdb-tricks.svg"
image: "/images/blog/thumbs/duckdb-tricks.png"
excerpt: "In this new installment of the DuckDB Tricks series, we present features for convenient handling of tables and performance optimization tips for Parquet and CSV files."
tags: ["using DuckDB"]
---

## Overview

We continue our DuckDB [Tricks]({% post_url 2024-08-19-duckdb-tricks-part-1 %}) [series]({% post_url 2024-10-11-duckdb-tricks-part-2 %}) with a third part,
where we showcase [friendly SQL features]({% link docs/sql/dialect/friendly_sql.md %}) and performance optimizations.

| Operation | SQL instructions |
|-----------|------------------|
| [Excluding columns from a table](#excluding-columns-from-a-table) | `EXCLUDE` or `COLUMNS(…)` and `NOT SIMILAR TO` |
| [Renaming columns with pattern matching](#renaming-columns-with-pattern-matching) | `COLUMNS(…) AS …` |
| [Loading with globbing](#loading-with-globbing) | `FROM '*.csv'` |
| [Reordering Parquet files](#reordering-parquet-files) | `COPY (FROM … ORDER BY …) TO …` |
| [Hive partitioning](#hive-partitioning) | `hive_partitioning = true`  |

## Dataset

We'll use a subset of the [Dutch railway services dataset](https://www.rijdendetreinen.nl/en/open-data/train-archive), which was already featured in a [blog post earlier this year]({% post_url 2024-05-31-analyzing-railway-traffic-in-the-netherlands %}).
This time, we'll use the CSV files between January and October 2024: [`services-2024-01-to-10.tar.zst`](https://blobs.duckdb.org/data/railway/services-2024-01-to-10.tar.zst).

If you would like to follow the examples, you can download and decompress the dataset with the following command:

```bash
curl https://blobs.duckdb.org/data/services-2024-01-to-10.tar.zst \
    | tar -xv --use-compress-program=unzstd
```

## Excluding Columns from a Table

Before creating a table, let's look at the data in the CSV files.
We pick the CSV file for August and inspect it with the [`DESCRIBE` statement]({% link docs/guides/meta/describe.md %}).

```sql
DESCRIBE FROM 'services-2024-08.csv';
```

The result is a table with the column names and the column types.

|         column_name          | column_type | null | key  | default | extra |
|------------------------------|-------------|------|------|---------|-------|
| Service:RDT-ID               | BIGINT      | YES  | NULL | NULL    | NULL  |
| Service:Date                 | DATE        | YES  | NULL | NULL    | NULL  |
| Service:Type                 | VARCHAR     | YES  | NULL | NULL    | NULL  |
| Service:Company              | VARCHAR     | YES  | NULL | NULL    | NULL  |
| Service:Train number         | BIGINT      | YES  | NULL | NULL    | NULL  |
| …                          | …         | …  | …  | …     | …   |

Now, let's use [`SUMMARIZE`]({% link docs/guides/meta/summarize.md %}) to inspect some statistics about the columns.

```sql
SUMMARIZE FROM 'services-2024-08.csv';
```

With `SUMMARIZE`, we get 10 statistics about our data (`min`, `max`, `approx_unique`, etc.).
If we want to remove a few of them the result, we can use the [`EXCLUDE` modifier]({% link docs/sql/expressions/star.md %}#exclude-modifier).
For example, to exclude `min`, `max` and the quantiles `q25`, `q50`, `q75`, we can use issue the following command:

```sql
SELECT * EXCLUDE(min, max, q25, q50, q75) 
FROM (SUMMARIZE FROM 'services-2024-08.csv');
```

Alternatively, we can use the [`COLUMNS`](({% link docs/sql/expressions/star.md %}#columns)) expression with the [`NOT SIMILAR TO` operator]({% link docs/sql/functions/pattern_matching.md %}#similar-to).
This works with a regular expression:

```sql
SELECT COLUMNS(c -> c NOT SIMILAR TO 'min|max|q.*') 
FROM (SUMMARIZE FROM 'services-2024-08.csv');
```

In both cases, the resulting table will contain the 5 remaining statistical columns:

|         column_name          | column_type | approx_unique |         avg         |        std         |  count  | null_percentage |
|------------------------------|-------------|--------------:|---------------------|--------------------|--------:|----------------:|
| Service:RDT-ID               | BIGINT      | 259022        | 14200071.03736433   | 59022.836209662266 | 1846574 | 0.00            |
| Service:Date                 | DATE        | 32            | NULL                | NULL               | 1846574 | 0.00            |
| Service:Type                 | VARCHAR     | 20            | NULL                | NULL               | 1846574 | 0.00            |
| Service:Company              | VARCHAR     | 12            | NULL                | NULL               | 1846574 | 0.00            |
| Service:Train number         | BIGINT      | 17264         | 57781.81688196628   | 186353.76365744913 | 1846574 | 0.00            |
| …                          | …         | …           | …                 | …                | …     | …             |

## Renaming Columns with Pattern Matching

Upon inspecting the columns, we see that their names contain spaces and semicolons (`:`).
These special characters makes writing queries a bit tedious as they necessitate quoting column names with double quotes.
For example, we have to write `"Service:Company"` in the following query:

```sql
SELECT DISTINCT "Service:Company" AS company,
FROM 'services-2024-08.csv'
ORDER BY company;
```

Let's see how we can rename the columns using the `COLUMNS` expression.
To replace the special characters (up to 2), we can write the following query:

```sql
SELECT COLUMNS('(.*?)_*$') AS "\1"
FROM (
    SELECT COLUMNS('(\w*)\W*(\w*)\W*(\w*)') AS "\1_\2_\3"
    FROM 'services-2024-08.csv'
);
```

Add `DESCRIBE` at the beginning of the query and we can see the renamed columns:

|         column_name          | column_type | null | key  | default | extra |
|------------------------------|-------------|------|------|---------|-------|
| Service_RDT_ID               | BIGINT      | YES  | NULL | NULL    | NULL  |
| Service_Date                 | DATE        | YES  | NULL | NULL    | NULL  |
| Service_Type                 | VARCHAR     | YES  | NULL | NULL    | NULL  |
| Service_Company              | VARCHAR     | YES  | NULL | NULL    | NULL  |
| Service_Train_number         | BIGINT      | YES  | NULL | NULL    | NULL  |
| …                          | …         | …  | …  | …     | …   |

Let's break down the query starting with the first `COLUMNS` expression:

```sql
SELECT COLUMNS('(\w*)\W*(\w*)\W*(\w*)') AS "\1_\2_\3"
```

Here, we use regular expression with `(\w*)` groups that capture 0…n word characters (`[0-9A-Za-z_]`).
Meanwhile, the expression `\W*` captures 0…n non-word characters (`[^0-9A-Za-z_]`).
In the alias part we refer to the capture group `i` with `\i` so `"\1_\2_\3"` means that we only keep the word characters and separate their groups with underscores (`_`).
However, because some column names contain words separated by a space, while others don't, after this `SELECT` statement we get column names with a trailing underscore (`_`), 
e.g., `Service_Date_`.
Thus, we need an additional processing step:

```sql
SELECT COLUMNS('(.*?)_*$') AS "\1"
```

Here, we capture the group of characters without the trailing underscore(s) and rename the columns to `\1`, which removes the trailing underscores.

To make writing queries even more convenient, we can rely on the [case-insensitivity of identifiers]({% link docs/sql/dialect/keywords_and_identifiers.md %}#case-sensitivity-of-identifiers) to query the column names in lowercase:

```sql
SELECT DISTINCT service_company
FROM (
    SELECT COLUMNS('(.*?)_*$') AS "\1"
    FROM (
       SELECT COLUMNS('(\w*)\W*(\w*)\W*(\w*)') AS "\1_\2_\3"
       FROM 'services-2024-08.csv'
    )
)
ORDER BY service_company;
```

| Service_Company |
|-----------------|
| Arriva          |
| Blauwnet        |
| Breng           |
| DB              |
| Eu Sleeper      |
| …             |

> The returned column name preserves its original cases even though we used lowercase letters in the query.

## Loading with Globbing

Now that we can simplify the column names, let's ingest all 3 months of data to a table:

```sql
CREATE OR REPLACE TABLE services AS
    SELECT COLUMNS('(.*?)_*$') AS "\1" 
    FROM (
        SELECT COLUMNS('(\w*)\W*(\w*)\W*(\w*)') AS "\1_\2_\3" 
        FROM 'services-2024-*.csv'
    );
```

In the inner `FROM` clause, we use the [`*` glob syntax]({% link docs/sql/functions/pattern_matching.md %}#globbing) to match all files.
DuckDB automatically detects that all files have the same schema and unions them together.
We have now a table with all the data from January to October, amounting to almost 20 million rows.

## Reordering Parquet Files

Suppose we want to analyze the average delay of the [Intercity Direct trains](https://en.wikipedia.org/wiki/Intercity_Direct) operated by the [Nederlandse Spoorwegen (NS)](https://en.wikipedia.org/wiki/Nederlandse_Spoorwegen), measured at the final destination of the train service.
While we can run this analysis directly on the the `.csv` files, the lack of metadata (such as schema and min-max indexes) will limit the performance.
Let's measure this in the CLI client by turning on the [timer]({% link docs/api/cli/dot_commands.md %}):

```plsql
.timer on
```

```sql
SELECT avg("Stop:Arrival delay")
FROM 'services-*.csv'
WHERE "Service:Company" = 'NS'
  AND "Service:Type" = 'Intercity direct'
  AND "Stop:Departure time" IS NULL;
```

This query takes about 1.8 seconds. Now, if we run the same query on `services` table that's already loaded to DuckDB, the query is much faster:

```sql
SELECT avg(Stop_Arrival_delay)
FROM services
WHERE Service_Company = 'NS'
  AND Service_Type = 'Intercity direct'
  AND Stop_Departure_time IS NULL;
```

The run time is about 35 milliseconds.

If we would like to use an external binary file format, we can also export the database to a single Parquet file:

```sql
EXPORT DATABASE 'railway' (FORMAT PARQUET);
```

We can then directly query it as follows:

```sql
SELECT avg(Stop_Arrival_delay)
FROM 'railway/services.parquet'
WHERE Service_Company = 'NS'
  AND Service_Type = 'Intercity direct'
  AND Stop_Departure_time IS NULL;
```

The runtime for this format is about 90 milliseconds – somewhat slower than DuckDB's own file format but about 20× faster than reading the raw CSV files.

If we have a priori knowledge of the fields a query filters on, we can reorder the Parquet file to improve query performance.

```sql
COPY
(FROM 'railway/services.parquet' ORDER BY Service_Company, Service_Type)
TO 'railway/services.parquet';
```

If we run the query again, it's noticeably faster, taking only 35 milliseconds.
This is thanks to [partial reading]({% link docs/data/parquet/overview.md %}#partial-reading), which uses the zonemaps (min-max indexes) to limit the amount of data that has to be scanned.
Reordering the file allows DuckDB to skip more data, leading to faster query times.

## Hive Partitioning

To speed up queries even further, we can use [Hive partitioning]({% link docs/data/partitioning/hive_partitioning.md %}) to create a directory layout on disk that matches the filtering used in the queries.

```sql
COPY services
TO 'services-parquet-hive'
(FORMAT PARQUET, PARTITION_BY (Service_Company, Service_Type));
```

Let's peek into the directory from DuckDB's CLI using the [`.sh` dot command]({% link docs/api/cli/dot_commands.md %}):

```plsql
.sh tree services-parquet-hive
```

```text
services-parquet-hive
├── Service_Company=Arriva
│   ├── Service_Type=Extra%20trein
│   │   └── data_0.parquet
│   ├── Service_Type=Nachttrein
│   │   └── data_0.parquet
│   ├── Service_Type=Snelbus%20ipv%20trein
│   │   └── data_0.parquet
│   ├── Service_Type=Sneltrein
│   │   └── data_0.parquet
│   ├── Service_Type=Stopbus%20ipv%20trein
│   │   └── data_0.parquet
│   ├── Service_Type=Stoptrein
│   │   └── data_0.parquet
│   └── Service_Type=Taxibus%20ipv%20trein
│       └── data_0.parquet
├── Service_Company=Blauwnet
│   ├── Service_Type=Intercity
│   │   └── data_0.parquet
…
```

We can now run the query on the Hive partitioned data set by passing the `hive_partitioning = true` flag:

```sql
SELECT avg(Stop_Arrival_delay)
FROM read_parquet(
         'services-parquet-hive/**/*.parquet',
         hive_partitioning = true
     )
WHERE Service_Company = 'NS'
  AND Service_Type = 'Intercity direct'
  AND Stop_Departure_time IS NULL;
```

This query now takes about 20 milliseconds as DuckDB can use the directory structure to limit the reads even further.
And the neat thing about Hive partitioning is that it even works with CSV files!

```sql
COPY services
TO 'services-csv-hive'
(FORMAT CSV, PARTITION_BY (Service_Company, Service_Type));

SELECT avg(Stop_Arrival_delay)
FROM read_csv('services-csv-hive/**/*.csv', hive_partitioning = true)
WHERE Service_Company = 'NS'
  AND Service_Type = 'Intercity direct'
  AND Stop_Departure_time IS NULL;
```

While the CSV files lack any sort of metadata, DuckDB can rely on the directory structure to limit the scans to the relevant directories,
resulting in execution times around 150 milliseconds, more than 10× faster compared to reading all CSV files.

If all these formats and results got your head spinning, no worries.
We got your covered with this summary table:

| Format                     | Query runtime (ms) |
|----------------------------|-------------------:|
| DuckDB file format         |                 35 |
| CSV (vanilla)              |               1800 |
| CSV (Hive-partitioned)     |                150 |
| Parquet (vanilla)          |                 90 |
| Parquet (reordered)        |                 35 |
| Parquet (Hive-partitioned) |                 20 |

Oh, and we forgot to report the result. The average delay of Intercity Direct trains is 3 minutes!

## Closing Thoughts

That's it for part three of DuckDB tricks. If you have a trick that would like to share, please share it with the DuckDB team on our social media sites, or submit it to the [DuckDB Snippets site](https://duckdbsnippets.com/) (maintained by our friends at MotherDuck).
