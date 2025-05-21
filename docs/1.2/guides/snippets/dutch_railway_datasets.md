---
layout: docu
title: Dutch Railway Datasets
---

Examples in this documentation often use datasets based on the [Dutch Railway datasets](https://www.rijdendetreinen.nl/en/open-data/).
These high-quality datasets are maintained by the team behind the [Rijden de Treinen _(Are the trains running?)_ application](https://www.rijdendetreinen.nl/en/about).
This page contains download links to our mirrors to the datasets.

## Loading the Datasets

You can load the datasets directly as follows:

```sql
CREATE TABLE services AS
    FROM 'https://blobs.duckdb.org/nl-railway/services-2025-03.csv.gz';
```

```sql
DESCRIBE services;
```

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

## Yearly Data Sets

* [2019](https://blobs.duckdb.org/nl-railway/services-2019.csv.gz) (347 MB)
* [2020](https://blobs.duckdb.org/nl-railway/services-2020.csv.gz) (355 MB)
* [2021](https://blobs.duckdb.org/nl-railway/services-2021.csv.gz) (350 MB)
* [2022](https://blobs.duckdb.org/nl-railway/services-2022.csv.gz) (355 MB)
* [2023](https://blobs.duckdb.org/nl-railway/services-2023.csv.gz) (346 MB)
* [2024](https://blobs.duckdb.org/nl-railway/services-2024.csv.gz) (357 MB)

## Monthly Data Sets

* [2024-01](https://blobs.duckdb.org/nl-railway/services-2024-01.csv.gz) (29 MB)
* [2024-02](https://blobs.duckdb.org/nl-railway/services-2024-02.csv.gz) (28 MB)
* [2024-03](https://blobs.duckdb.org/nl-railway/services-2024-03.csv.gz) (30 MB)
* [2024-04](https://blobs.duckdb.org/nl-railway/services-2024-04.csv.gz) (28 MB)
* [2024-05](https://blobs.duckdb.org/nl-railway/services-2024-05.csv.gz) (30 MB)
* [2024-06](https://blobs.duckdb.org/nl-railway/services-2024-06.csv.gz) (29 MB)
* [2024-07](https://blobs.duckdb.org/nl-railway/services-2024-07.csv.gz) (30 MB)
* [2024-08](https://blobs.duckdb.org/nl-railway/services-2024-08.csv.gz) (29 MB)
* [2024-09](https://blobs.duckdb.org/nl-railway/services-2024-09.csv.gz) (29 MB)
* [2024-10](https://blobs.duckdb.org/nl-railway/services-2024-10.csv.gz) (30 MB)
* [2024-11](https://blobs.duckdb.org/nl-railway/services-2024-11.csv.gz) (29 MB)
* [2024-12](https://blobs.duckdb.org/nl-railway/services-2024-12.csv.gz) (29 MB)
* [2025-01](https://blobs.duckdb.org/nl-railway/services-2025-01.csv.gz) (30 MB)
* [2025-02](https://blobs.duckdb.org/nl-railway/services-2025-02.csv.gz) (28 MB)
* [2025-03](https://blobs.duckdb.org/nl-railway/services-2025-03.csv.gz) (30 MB)
