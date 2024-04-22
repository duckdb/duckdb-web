---
layout: docu
title: Attach to a DuckDB Database over HTTPS or S3
---

You can establish a read-only connection to a DuckDB instance via HTTPS or the S3 API.

## Prerequisites

This guide requires the [`httpfs` extension](../../extensions/httpfs), which can be installed use the `INSTALL` SQL command. This only needs to be run once.

## Connecting via HTTPS

To connect to a DuckDB database via HTTPS, use the [`ATTACH` statement](../../sql/statements/attach) as follows:

```sql
LOAD httpfs;
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db (READONLY);
```

Then, the database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

## Connecting via S3

To connect to a DuckDB database via the S3 API, [configure the authentication](s3_import#credentials-and-configuration) for your bucket, then use the [`ATTACH` statement](../../sql/statements/attach) as follows:

```sql
LOAD httpfs;
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db (READONLY);
```

Then, the database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

## Limitations

* The `httpfs` extension has to be loaded manually.
* Only read-only connections are allowed, writing the database is not possible.
