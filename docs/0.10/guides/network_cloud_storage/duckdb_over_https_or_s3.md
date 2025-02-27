---
layout: docu
title: Attach to a DuckDB Database over HTTPS or S3
---

You can establish a read-only connection to a DuckDB instance via HTTPS or the S3 API.

## Prerequisites

This guide requires the [`httpfs` extension](../../extensions/httpfs), which can be installed using the `INSTALL httpfs` SQL command. This only needs to be run once.

## Attaching to a Database over HTTPS

To connect to a DuckDB database via HTTPS, use the [`ATTACH` statement](../../sql/statements/attach) as follows:

```sql
LOAD httpfs;
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

Then, the database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

## Attaching to a Database over the S3 API

To connect to a DuckDB database via the S3 API, [configure the authentication](s3_import#credentials-and-configuration) for your bucket (if required).
Then, use the [`ATTACH` statement](../../sql/statements/attach) as follows:

```sql
LOAD httpfs;
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

The database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

> Connecting to S3-compatible APIs such as the [Google Cloud Storage (`gs://`)](gcs_import#attaching-to-a-database) is also supported.

## Limitations

* The `httpfs` extension has to be loaded manually, auto-loading is currently not supported.
* Only read-only connections are allowed, writing the database via the HTTPS protocol or the S3 API is not possible.