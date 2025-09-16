---
layout: docu
redirect_from: null
title: Dutch Railway Datasets
---

Examples in this documentation often use datasets based on the [Dutch Railway datasets](https://www.rijdendetreinen.nl/en/open-data/).
These high-quality datasets are maintained by the team behind the [Rijden de Treinen _(Are the trains running?)_ application](https://www.rijdendetreinen.nl/en/about).
This page contains download links to our mirrors to the datasets.

> In 2024, we have published a [blog post on the analysis of these datasets]({% post_url 2024-05-31-analyzing-railway-traffic-in-the-netherlands %}).

## Loading the Datasets

You can load the datasets directly as follows:

```sql
CREATE TABLE services AS
    FROM 'https://blobs.duckdb.org/nl-railway/services-2025-03.csv.gz';
```

```sql
DESCRIBE services;
```

<div class="monospace_table"></div>

|         column_name          |       column_type        | null | key  | default | extra |
|------------------------------|--------------------------|------|------|---------|-------|
| Service:RDT-ID               | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Service:Date                 | DATE                     | YES  | NULL | NULL    | NULL  |
| Service:Type                 | VARCHAR                  | YES  | NULL | NULL    | NULL  |
| Service:Company              | VARCHAR                  | YES  | NULL | NULL    | NULL  |
| Service:Train number         | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Service:Completely cancelled | BOOLEAN                  | YES  | NULL | NULL    | NULL  |
| Service:Partly cancelled     | BOOLEAN                  | YES  | NULL | NULL    | NULL  |
| Service:Maximum delay        | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Stop:RDT-ID                  | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Stop:Station code            | VARCHAR                  | YES  | NULL | NULL    | NULL  |
| Stop:Station name            | VARCHAR                  | YES  | NULL | NULL    | NULL  |
| Stop:Arrival time            | TIMESTAMP WITH TIME ZONE | YES  | NULL | NULL    | NULL  |
| Stop:Arrival delay           | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Stop:Arrival cancelled       | BOOLEAN                  | YES  | NULL | NULL    | NULL  |
| Stop:Departure time          | TIMESTAMP WITH TIME ZONE | YES  | NULL | NULL    | NULL  |
| Stop:Departure delay         | BIGINT                   | YES  | NULL | NULL    | NULL  |
| Stop:Departure cancelled     | BOOLEAN                  | YES  | NULL | NULL    | NULL  |

## Datasets

### 80-Month Datasets

* [2019-01 to 2025-08](https://blobs.duckdb.org/nl-railway/railway-services-80-months.zip): 80 months as uncompressed CSVs in a single zip

### Yearly Datasets

The yearly datasets are about 350 MB each.

* [2019](https://blobs.duckdb.org/nl-railway/services-2019.csv.gz)
* [2020](https://blobs.duckdb.org/nl-railway/services-2020.csv.gz)
* [2021](https://blobs.duckdb.org/nl-railway/services-2021.csv.gz)
* [2022](https://blobs.duckdb.org/nl-railway/services-2022.csv.gz)
* [2023](https://blobs.duckdb.org/nl-railway/services-2023.csv.gz)
* [2024](https://blobs.duckdb.org/nl-railway/services-2024.csv.gz)

### Monthly Datasets

The monthly datasets are about 30 MB each.

* [2024-01](https://blobs.duckdb.org/nl-railway/services-2024-01.csv.gz)
* [2024-02](https://blobs.duckdb.org/nl-railway/services-2024-02.csv.gz)
* [2024-03](https://blobs.duckdb.org/nl-railway/services-2024-03.csv.gz)
* [2024-04](https://blobs.duckdb.org/nl-railway/services-2024-04.csv.gz)
* [2024-05](https://blobs.duckdb.org/nl-railway/services-2024-05.csv.gz)
* [2024-06](https://blobs.duckdb.org/nl-railway/services-2024-06.csv.gz)
* [2024-07](https://blobs.duckdb.org/nl-railway/services-2024-07.csv.gz)
* [2024-08](https://blobs.duckdb.org/nl-railway/services-2024-08.csv.gz)
* [2024-09](https://blobs.duckdb.org/nl-railway/services-2024-09.csv.gz)
* [2024-10](https://blobs.duckdb.org/nl-railway/services-2024-10.csv.gz)
* [2024-11](https://blobs.duckdb.org/nl-railway/services-2024-11.csv.gz)
* [2024-12](https://blobs.duckdb.org/nl-railway/services-2024-12.csv.gz)
* [2025-01](https://blobs.duckdb.org/nl-railway/services-2025-01.csv.gz)
* [2025-02](https://blobs.duckdb.org/nl-railway/services-2025-02.csv.gz)
* [2025-03](https://blobs.duckdb.org/nl-railway/services-2025-03.csv.gz)
* [2025-04](https://blobs.duckdb.org/nl-railway/services-2025-04.csv.gz)
* [2025-05](https://blobs.duckdb.org/nl-railway/services-2025-05.csv.gz)
* [2025-06](https://blobs.duckdb.org/nl-railway/services-2025-06.csv.gz)
* [2025-07](https://blobs.duckdb.org/nl-railway/services-2025-07.csv.gz)
* [2025-08](https://blobs.duckdb.org/nl-railway/services-2025-08.csv.gz)
